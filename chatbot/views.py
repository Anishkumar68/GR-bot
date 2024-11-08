import os
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import spacy

# Import the necessary LangChain components pip install langchain install complete langchain then.
# import help page (https://python.langchain.com/docs/introduction/)
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

from langchain_community.vectorstores import Pinecone

from .text_formating import format_text


# Import Pinecone's 
from pinecone import Pinecone, ServerlessSpec

# Security == Load environment variables 
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


def home(request):
    #No need #  Check if the user's name 
    # user_name = request.session.get("user_name", None)

    # # if user exists
    # if user_name:
    #     initial_prompt = f"Welcome back, {user_name}! How can I assist you with gift recommendations today?"
    # else:
    #     initial_prompt = "Hello! I’m here to help you with gift recommendations. Could you start by telling me your name?"

    # # Pass the initial prompt to the template
    # context = {"initial_prompt": initial_prompt}
    return render(request, "chatbot/chatbot.html")


# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

#Index name pinecone
index_name = "gift-recommendation"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Connect to the created index
index = pc.Index(index_name)

# Initialize LangChain components check langchain documentation
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings.embed_query,
    text_key="text", 
    namespace="chatbot-memory",
)

# Setup ChatGPT model and conversation memory
chat_model = ChatOpenAI(
    model="gpt-4-turbo", openai_api_key=openai_api_key, temperature=0.5
)
conversation_memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True
)

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Prompt template for responses
prompt_template = PromptTemplate(
    input_variables=["user_name", "user_input", "chat_history"],
    template="""
    Your name is Gifty, a friendly and knowledgeable gift recommendation chatbot.
    You are a friendly, knowledgeable assistant specializing in gift recommendations for users in India. Your goal is to help {user_name} with thoughtful, location-specific gift ideas.

    First, check if the user has greeted you in their latest input:
    - If the user greets you (e.g., says "Hello," "Hi," "Hey," etc.), respond with a friendly greeting back and invite them to ask about gift recommendations.

    Next, check if a valid name is already provided in the chat history:
    {chat_history}

    - If the user's name ({user_name}) has already been provided and matches a valid format (e.g., alphabetical characters only), continue with the conversation and provide recommendations based on their input.
    - If the user's name is not in the chat history or does not match a valid name format, politely prompt the user to provide their name.
    - If the user responds with "Hey" or similar informal words instead of their name, gently ask for their name to proceed with personalized gift recommendations.

    User's latest question:
    {user_input}

    Based on this context, provide gift suggestions with the following details:
    - Gift idea and brief description, tailored to the user’s needs and preferences.
    - Price in Indian Rupees (INR), considering a range of budget options if possible.
    - Always provide verified, working product links to trusted Indian e-commerce platforms (such as Amazon.in, Flipkart, etc.) to ensure smooth purchasing.

    Always maintain a friendly and supportive tone, acting like a helpful friend guiding the user through their gift-buying experience. Prioritize user satisfaction, ensuring links are functional and offer a smooth experience. For any unavailable or temporary items, provide alternative suggestions.
    """,
)

# Setup retrieval chain
retrieval_chain = ConversationalRetrievalChain.from_llm(
    llm=chat_model, retriever=vector_store.as_retriever(), memory=conversation_memory
)


def generate_chatbot_response(user_name, user_input):
    # Save context with user input and placeholder response text
    conversation_memory.save_context(
        {"user_input": user_input},
        {
            "assistant_response": f"Responding to {user_name}'s input."
        },  # Placeholder response for context tracking
    )

    # Retrieve chat history and format the prompt
    chat_history = conversation_memory.load_memory_variables({})["chat_history"]
    formatted_prompt = prompt_template.format(
        user_name=user_name, user_input=user_input, chat_history=chat_history
    )

    # Generate response from the model
    response = chat_model.invoke(formatted_prompt)

    # Extract content if response is an AIMessage object
    if isinstance(response, AIMessage):
        response_text = (
            response.content
        ) 
         # Get the text content from the AIMessage object
    elif isinstance(response, dict) and "content" in response:
        response_text = response["content"] 
        # Handle if response is a dictionary
    else:
        response_text = str(
            response
        ).strip()  #

    # Save both user input and actual bot response as plain text to memory
    conversation_memory.save_context(
        {"user_input": user_input}, {"assistant_response": response_text}
    )

    return response_text


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_name = data.get("user_name", "User") 
        # Default name if not provided
        user_input = data.get("message", "")

        # Call the chatbot function to get the response
        # bot_response_test = generate_chatbot_response(user_name, user_input)
        bot_response = format_text(generate_chatbot_response(user_name, user_input))
        # print(bot_response)

        # Return the response as JSON
        return JsonResponse({"message": bot_response})


# NLP function for extracting user details
def extract_user_details(text):
    doc = nlp(text)
    details = {
        "name": None,
        "relationship": None,
        "budget": None,
        "occasion": None,
        "interests": None,
    }
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            details["name"] = ent.text
        elif ent.label_ == "MONEY":
            details["budget"] = ent.text
        elif ent.label_ == "EVENT":
            details["occasion"] = ent.text
        elif ent.label_ in {"ORG", "PRODUCT"}:
            details["interests"] = ent.text
        elif ent.label_ == "NORP":
            details["relationship"] = ent.text
    return {key: value for key, value in details.items() if value is not None}

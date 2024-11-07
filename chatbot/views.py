import os
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import spacy
<<<<<<< HEAD

# Import the necessary LangChain components
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

from langchain_community.vectorstores import Pinecone
=======

# Import the necessary LangChain components
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage

from langchain.chat_models import ChatOpenAI

from langchain.vectorstores import Pinecone
>>>>>>> cc4938fb1fe71b066f850ad2736358243d6a8319

from .text_formating import format_text


# Import Pinecone's updated API
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


def home(request):
    # Check if the user's name is already in the session
    user_name = request.session.get("user_name", None)

    # Set the initial prompt based on whether we know the user's name
    if user_name:
        initial_prompt = f"Welcome back, {user_name}! How can I assist you with gift recommendations today?"
    else:
        initial_prompt = "Hello! I’m here to help you with gift recommendations. Could you start by telling me your name?"

    # Pass the initial prompt to the template
    context = {"initial_prompt": initial_prompt}
    return render(request, "chatbot/chatbot.html", context)


# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

# Define index name and create if it doesn't exist
index_name = "gift-recommendation"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Make sure this matches your embedding model dimension
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Connect to the created index
index = pc.Index(index_name)

# Initialize LangChain components
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings.embed_query,
    text_key="text",  # Specify which metadata key stores text
    namespace="chatbot-memory",
)

# Setup ChatGPT model and conversation memory
chat_model = ChatOpenAI(model="gpt-4-turbo", openai_api_key=openai_api_key)
conversation_memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True
)

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Prompt template for responses
prompt_template = PromptTemplate(
    input_variables=["user_name", "user_input", "chat_history"],
    template="""
    You are a helpful assistant specializing in gift recommendations. The user {user_name} has provided some details.

    Here is the chat history so far:
    {chat_history}

    User's latest question:
    {user_input}

    Based on this context and the user's current question, suggest relevant gift ideas, including:
    - Product name
    - Platform for purchase
    - Direct link to the product if available.
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
        )  # Get the text content from the AIMessage object
    elif isinstance(response, dict) and "content" in response:
        response_text = response["content"]  # Handle if response is a dictionary
    else:
        response_text = str(
            response
        ).strip()  # Fallback for plain strings or unknown objects

    # Save both user input and actual bot response as plain text to memory
    conversation_memory.save_context(
        {"user_input": user_input}, {"assistant_response": response_text}
    )

    return response_text


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_name = data.get("user_name", "User")  # Default name if not provided
        user_input = data.get("message", "")

        # Call the chatbot function to get the response
<<<<<<< HEAD
        # bot_response_test = generate_chatbot_response(user_name, user_input)
        bot_response = format_text(generate_chatbot_response(user_name, user_input))
        # print(bot_response)
=======
        bot_response = format_text(generate_chatbot_response(user_name, user_input))
>>>>>>> cc4938fb1fe71b066f850ad2736358243d6a8319

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

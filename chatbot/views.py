from django.shortcuts import render
import os
import json
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("openai.api_key")


# Home view to render the chatbot HTML page
def home(request):
    return render(request, "chatbot/chatbot.html")  # Renders the chatbot HTML interface


# Chatbot response API to handle POST requests and generate responses
@csrf_exempt
def chatbot_response(request):
    """
    This view function handles POST requests for the chatbot. It receives user input,
    formats it using a LangChain prompt, generates a response via OpenAI, and returns
    the response as JSON.
    """
    if request.method == "POST":
        # Parse user input
        data = json.loads(request.body)
        user_message = data.get("message", "").lower()

        # Initialize the OpenAI chat model
        chat_model = ChatOpenAI(model="gpt-3.5-turbo")

        # Define the prompt template with specific chatbot instructions
        prompt = PromptTemplate(
            input_variables=["user_input"],
            template="You are a helpful gift recommender chatbot. Respond concisely and informatively.\n\nUser: {user_input}\nBot:",
        )

        # Format the prompt with user input
        formatted_prompt = prompt.format(user_input=user_message)
        print(formatted_prompt)

        # Generate response from OpenAI model
        response = chat_model.invoke(formatted_prompt)
        ai_message = response.content.strip()
        print(ai_message)

        # Return JSON response to frontend
        return JsonResponse({"message": ai_message})

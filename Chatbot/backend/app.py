from flask import Flask, request
from llmmodel import LLMModel
from preprocess import create_documents_from_pdfs, create_documents_from_txts
from ragmodel import RAGModel
from qdrant_client import QdrantClient
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

# Load variables 
documents = create_documents_from_txts("utils/blood_pressure_guidelines.txt")
qdrant_api_key = os.getenv('QDRANT_API_KEY')
qdrant_url = os.getenv('QDRANT_URL')
genai_key = os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)
#tuned_model_name = 'tunedModels/blood-pressure-b47p0vvhonqk' 
tuned_model_name = "gemini-pro"   #place holder


# Allow requests from your Firebase app
# CORS(app, resources={r"*": {"origins": ["http://localhost:8080", "https://curtin-health-demo.web.app"]}})
CORS(app, resources={r"*": {"origins": "*"}})

# Create Gemini LLM Model with given API key
llm = LLMModel(
    api_key=genai_key,
    model_name="gemini-pro",
    system_instruction="",
    chat_history=[]
)

# Load reference resource from txt 
documents = create_documents_from_txts("utils/blood_pressure_guidelines.txt")


# Qdrant client for server 
qdrant_client = QdrantClient(           # or QdrantClient(":memory:") if testing locally
            url=qdrant_url,
            api_key=qdrant_api_key,
            timeout=30
        )

# qdrant_client = QdrantClient(":memory:")
# Corresponding RagModel
rag = RAGModel(
    embedding_model_name="BAAI/bge-small-en-v1.5",
    documents=documents,
    qdrantClient=qdrant_client
)


@app.route('/')
def land():
    """
    Home route for the Flask application.

    Returns:
        str: A welcome message for the home route.
    """
    return "Hello app"


@app.route('/api/chat_hist')
def get_hist():
    """
    Outputs chat history of current session with the model

    Returns:
        list: A chat history.
    """
    return llm.chat.history


@app.route('/api/send_msg', methods=["POST"])
def add():
    """
    Handles POST requests to the '/api/send_msg' endpoint.

    This function processes incoming POST requests by passing the request data to the `llm.send_message()` function,
    which generates a response based on the input. The generated response is returned as a JSON-like dictionary.

    Returns:
        dict: A dictionary containing the response text under the key 'response_text'.
    """
    response = ""
    if request.method == 'POST':
        client_message = request.get_data(as_text=True)
        response = llm.send_message_RAG(client_message, rag)

    resp = {
        'response_text': response
    }
    print(resp)
    # For debugging purpose
    # print(response)
    return resp


# Run the app on file execution at host local IP 127.0.0.1
# if __name__ == '__main__':
#     app.run(debug=True)


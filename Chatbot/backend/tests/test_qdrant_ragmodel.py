import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )


from app import app
from llmmodel import LLMModel
from ragmodel import RAGModel
from preprocess import create_documents_from_txts
from qdrant_client import QdrantClient

import unittest
import requests
from unittest.mock import patch, MagicMock
import time
import os
from dotenv import load_dotenv

load_dotenv()
qdrant_api_key = os.getenv('QDRANT_API_KEY')
qdrant_url = os.getenv('QDRANT_URL')
genai_key = os.getenv("GOOGLE_API_KEY")


class QdrantRAGTest(unittest.TestCase):
    ############################### Set up test ################################
    def setUp(self):
        """ Set up the app before testing """
        self.app = app.test_client()
        self.app.testing = True
        self.llmodel = LLMModel(
                            api_key=genai_key,
                            model_name='gemini-pro',
                            system_instruction="",
                            chat_history=[]
                        )

        self.rag = RAGModel(
            embedding_model_name="BAAI/bge-small-en-v1.5",
            documents=create_documents_from_txts("utils/blood_pressure_guidelines.txt"),
            qdrantClient=QdrantClient(":memory:") 
        )

        self.assertEqual(app.debug, False)


    def check_setup(self):
        """Check if the app launch successfully"""
        response = self.app.get("/")
        self.assertEqual(response.data.decode('utf-8'), "Hello app")

    ############################### Testing RAG ################################
    def test_RAG_no_sourced_response(self):
        self.llmodel.chat = self.llmodel.model.start_chat(history=[])
        response = self.llmodel.send_message_RAG("Tell me a joke", self.rag)

        # check default response to a question with no given context source
        self.assertEqual(response, "I cannot find trusted source") 

    def test_RAG_with_source_response(self):
        # prompt and expected answers retrieved from utils/blood_pressure_guidelines.txt
        prompt = "What is blood pressure at hypertension stage 2?"
        diastolic_info = "90 mm Hg or higher"
        systolic_info = "140 mm Hg or higher"

        self.llmodel.chat = self.llmodel.model.start_chat(history=[])
        response = self.llmodel.send_message_RAG(prompt, self.rag)

        print(response)
        

        # check if the answer is as the provided context 
        self.assertTrue(diastolic_info in response and systolic_info in response)
    
if __name__ == '__main__':
    unittest.main()
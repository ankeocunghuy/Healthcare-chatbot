import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )


from app import app
from llmmodel import LLMModel
import unittest
import requests
from unittest.mock import patch, MagicMock
import time
import os
from dotenv import load_dotenv

load_dotenv()

genai_key = os.getenv("GOOGLE_API_KEY")


class GeminiAPITest(unittest.TestCase):
    #########################  Set up #####################################
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

        self.assertEqual(app.debug, False)
        

    def check_setup(self):
        """Check if the app launch successfully"""
        response = self.app.get("/")
        self.assertEqual(response.data.decode('utf-8'), "Hello app")
    
    def check_backend_server(self):
        """ Test connection to backend server """
        # Send POST request to /api/send_msg with "hello" message
        print("Check chatbot response to user hello")
        response = self.app.post('/api/send_msg', data="hello", content_type='text/plain')
    
        self.assertEqual(response.status_code, 200) # Assert the status code is 200

    #########################  Testing API #####################################
    def test_user_query_history_ability(self):
        """ Test chatbot ability to remember previous context """
        self.llmodel.chat = self.llmodel.model.start_chat(history=[]) 
        self.llmodel.send_message("Tom has high blood pressure.")
        response = self.llmodel.send_message("Does Tom have high blood pressure?")
        
        expected_responses = ["yes", "is", "does have", "has"]
        self.assertTrue(any(synonym in response.lower() for synonym in expected_responses))
    
    def test_API_response_time(self):
        ''' Test if API response time is < 3 seconds '''
        start_time = time.time()
        response = self.llmodel.send_message("hello")
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f'Response time: {response_time:.3f} seconds')
        self.assertTrue(response_time <= 3)
    
    @patch('llmmodel.genai.GenerativeModel.start_chat')
    def test_API_mock_response(self, mock_start_chat):
        """ Test API success scenario  """
        # Mock the chat object and simulate an error during send_message
        mock_chat_object = MagicMock()
        mock_chat_object.send_message.return_value.text = "This is a generated response."
        mock_start_chat.return_value = mock_chat_object
        self.llmodel.chat = self.llmodel.model.start_chat(history=[])  # Simulate chat start

        # Send a message and assert the expected response
        response = self.llmodel.send_message("Tell me a story.")
        self.assertEqual(response, "This is a generated response.")
    
    @patch('llmmodel.genai.GenerativeModel.start_chat')  
    def test_API_send_message_error(self, mock_start_chat):
        """ Test API fail scenario  """
        # Create a mock chat object
        mock_chat_object = MagicMock()

        # Generate exception due to API request failed
        mock_chat_object.send_message.side_effect = Exception("API request failed") 
        mock_start_chat.return_value = mock_chat_object

        self.llmodel.chat = self.llmodel.model.start_chat(history=[])  # Simulate chat start
        response = self.llmodel.send_message("Hi")

        # Check if exception is caught, return error message and server still runs
        self.assertEqual(response, "API request failed. Please try again later!")
    
if __name__ == '__main__':
    unittest.main()
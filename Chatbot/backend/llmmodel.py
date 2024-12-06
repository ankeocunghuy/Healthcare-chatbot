import google.generativeai as genai
from ragmodel import RAGModel

class LLMModel:
  """ LLMModel is a class that represents a Large Language Model Google Gemini

    Attributes:
      api_key (str): API key for accessing the model.
      model (GenerativeModel): The pre-trained model itself.
      chat (ChatSession): Chat session of with the model. 
    
    Methods:
      __init__(api_key, model_name, system_instruction, chat_history):
          Initializes the LLMModel with a given API key, model name, 
          system instruction and chat session history (if available).
      
      send_message(message):
          Generates response based on a given message using the loaded language model.

  """

  
  def __init__(self, api_key, model_name, system_instruction, chat_history):
    """ Initializes the LLMModel instance.

        Args:
          api_key (str): API key to access the model
          model_name (str): The name of the pre-trained model to be loaded.
          system_instruction (str): System instruction for the model.
          chat_history (Iterable): Current chat history with the model.
    """
    self.api_key = api_key
    genai.configure(api_key=api_key)
    
    self.model = genai.GenerativeModel(
      model_name=model_name,
    #   system_instruction=system_instruction
    )
    
    self.chat = self.model.start_chat(history=chat_history)


  def send_message(self, message):
      """ Generates text from a given prompt/message using the loaded model.
        
        Args:
            message (str): The input text to generate predictions from.
        
        Returns:
            str: The generated text as output by the model.
       """
      try:
        response = self.chat.send_message(message)
        return response.text
      except Exception as e:
        # Handle exceptions and return a user-friendly message
        return str(e) + ". Please try again later!"


  def send_message_RAG(self, message, ragmodel):
    context = ragmodel.generate_relevant_context(message)

    if not context:
       return "I cannot find trusted source"
    
    augmented_message = f"Given information {context}, answer {message}"
    return self.send_message(augmented_message)

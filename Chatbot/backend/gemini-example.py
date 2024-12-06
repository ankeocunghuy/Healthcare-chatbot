import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=genai_key)
# genai.configure()


# List all available models 
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

# Choose model 
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Chatsession with the model 
while True:
    prompt = input("Ask me anything: ")
    # Exit prompt 
    if (prompt == "exit"):
        break
    
    # Input prompt and get response output from the model
    response = chat.send_message(prompt, stream=True)
    for chunk in response:
        if chunk.text:
          print(chunk.text)


# Execute: source .venv/bin/activate
# python gemini-example.py
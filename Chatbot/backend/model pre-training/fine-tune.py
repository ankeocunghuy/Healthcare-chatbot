# Library imports
import google.generativeai as genai
import pandas as pd
import os
import time
import seaborn as sns

# Configure model
genai.configure(api_key=os.environ["GOOGLE_API_KEY"]) # 'GOOGLE_API_KEY' needs
# to be set as environment variable

# Delete previous fine-tuned models
print("Previous fine-tuned models deleted:")
for model_info in genai.list_tuned_models():
    print(model_info.name)
    genai.delete_tuned_model(model_info.name)

# Fine-tune model
base_model = "models/gemini-1.5-flash-001-tuning"
training_data = pd.read_excel("pre-training data/blood pressure data australia "
                            "prepared.xlsx")
operation = genai.create_tuned_model(
    display_name="blood pressure",
    source_model=base_model,
    epoch_count=5,
    batch_size=4,
    learning_rate=0.001,
    training_data=training_data,
)

# Fine-tuning progress
for status in operation.wait_bar():
    time.sleep(10)
result = operation.result()
print(result)

# Fine-tuning statistics
snapshots = pd.DataFrame(result.tuning_task.snapshots)
sns.lineplot(data=snapshots, x='epoch', y='mean_loss')

# Print fine-tuned models' names
print("Fine-tuned models:")
for model_info in genai.list_tuned_models():
    print(model_info.name)

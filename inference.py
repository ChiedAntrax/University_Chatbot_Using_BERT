from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer
import torch

# Load fine-tuned model and tokenizer
model = DistilBertForQuestionAnswering.from_pretrained('C:\\Users\\tbhry\\OneDrive\\Desktop\\Kia_Upgrade\\fine_tuned_qa_model')
tokenizer = DistilBertTokenizer.from_pretrained('C:\\Users\\tbhry\\OneDrive\\Desktop\\Kia_Upgrade\\fine_tuned_qa_model')

# Example for inference
input_text = "Your input text goes here."
question = "Your question goes here?"

inputs = tokenizer(question, input_text, return_tensors="pt")
start_positions, end_positions = model(**inputs).start_logits.argmax().item(), model(**inputs).end_logits.argmax().item()

# Decode the answer
answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_positions:end_positions+1]))
print("Answer:", answer)

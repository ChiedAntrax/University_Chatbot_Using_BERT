import torch
from torch.utils.data import Dataset
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import pandas as pd
from torch.utils.data import DataLoader
from transformers import Trainer, TrainingArguments
from transformers import default_data_collator
import torch.nn.functional as F


def custom_data_collator(features):
    max_length = max(len(feature['input_ids']) for feature in features)

    # Pad sequences to the maximum length
    for feature in features:
        padding_length = max_length - len(feature['input_ids'])
        feature['input_ids'] = F.pad(feature['input_ids'], (0, padding_length), value=model.config.pad_token_id)
        feature['attention_mask'] = F.pad(feature['attention_mask'], (0, padding_length), value=0)  # Assuming pad token's attention mask is 0

    batch = default_data_collator([{
        'input_ids': feature.get('input_ids', None),
        'attention_mask': feature.get('attention_mask', None),
        'start_positions': feature.get('start_positions', None),
        'end_positions': feature.get('end_positions', None),
    } for feature in features])

    return batch


class CustomQADataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        inputs = {
            'input_ids': row['input_ids'],
            'attention_mask': row['attention_mask'],
            'start_positions': row['start_positions'],
            'end_positions': row['end_positions'],
        }
        return inputs

# Tokenization function
def tokenize_and_convert(row):
    input_text = row['question'] + " " + row['text']
    inputs = tokenizer(input_text, truncation=True, padding=True, max_length=512, return_tensors="pt")

    # Ensure the tokenizer output contains the expected keys
    if 'input_ids' not in inputs or 'attention_mask' not in inputs:
        raise ValueError("Tokenizer output is missing expected keys.")

    return {
        'input_ids': inputs['input_ids'].squeeze(),
        'attention_mask': inputs['attention_mask'].squeeze(),
        'start_positions': row['start_positions'],
        'end_positions': row['end_positions'],
    }

# Initialize tokenizer and model
model_name = "bert-large-uncased"  # or another larger model

model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Read data and create dataset
data = pd.read_csv("processed_university_chatbot_dataset.csv")
dataset = CustomQADataset(data)
dataset.data = dataset.data.apply(tokenize_and_convert, axis=1)

data_eval = pd.read_csv("processed_university_chatbot_dataset.csv")  # Replace with the path to your evaluation dataset
dataset_eval = CustomQADataset(data)
dataset_eval.data = dataset_eval.data.apply(tokenize_and_convert, axis=1)

# Training loop
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=10,
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_steps=50,
    save_steps=0,
    evaluation_strategy="steps",
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    greater_is_better=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=dataset_eval,
    data_collator=custom_data_collator
)

trainer.train()

# Save the model
model.save_pretrained("D:\\Kia_Upgrade\\fine_tuned_qa_model")
tokenizer.save_pretrained("D:\\Kia_Upgrade\\fine_tuned_qa_model")

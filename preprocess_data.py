

import pandas as pd
from transformers import DistilBertTokenizer

def preprocess_csv(csv_file):
    df = pd.read_csv(csv_file)
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased')

    def tokenize_row(row):
        inputs = tokenizer(row['question'] + " " + row['text'], return_tensors='pt', padding=True, truncation=True)
        input_ids = inputs['input_ids'][0]
        attention_mask = inputs['attention_mask'][0]

        return pd.Series({
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'start_positions': row['start_span'],
            'end_positions': row['end_span']
        })

    tokenized_datasets = df.apply(tokenize_row, axis=1)
    processed_data = pd.concat([df, tokenized_datasets], axis=1)

    return processed_data

if __name__ == "__main__":
    processed_data = preprocess_csv('university_chatbot_dataset.csv')

    # Print the column names to check
    print(processed_data.columns)

    processed_data.to_csv('processed_university_chatbot_dataset.csv', index=False)

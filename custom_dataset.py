'''import pandas as pd
from torch.utils.data import Dataset

class CustomQADataset(Dataset):
    def __init__(self, dataframe):
        self.data = dataframe

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
    # Check if the index is within the valid range
        if 0 <= idx < len(self.data):
            row = self.data.iloc[idx]

            # Assuming 'input_ids', 'attention_mask', 'start_positions', and 'end_positions' are column names
            input_ids = row['input_ids']
            attention_mask = row['attention_mask']
            start_positions = row['start_positions']
            end_positions = row['end_positions']

            return {
                'input_ids': input_ids,
                'attention_mask': attention_mask,
                'start_positions': start_positions,
                'end_positions': end_positions,
            }
        else:
            raise IndexError("Index out of bounds")
'''

import pandas as pd
from torch.utils.data import Dataset

class CustomQADataset(Dataset):
    def __init__(self, dataframe, tokenizer):
        self.data = dataframe
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # Check if the index is within the valid range
        if 0 <= idx < len(self.data):
            row = self.data.iloc[idx]

            # Assuming 'sentence', 'start_positions', and 'end_positions' are column names
            sentence = row['sentence']
            start_positions = row['start_positions']
            end_positions = row['end_positions']

            # Tokenize and convert the input sentence
            inputs = self.tokenizer(
                sentence,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            )

            # Assuming 'input_ids' and 'attention_mask' are keys in the tokenizer output
            input_ids = inputs['input_ids']
            attention_mask = inputs['attention_mask']

            return {
                'input_ids': input_ids,
                'attention_mask': attention_mask,
                'start_positions': start_positions,
                'end_positions': end_positions,
            }
        else:
            raise IndexError("Index out of bounds")

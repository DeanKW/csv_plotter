import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import string
import os


def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))


def generate_sample_csv(
    filename='sample.csv',
    num_rows=100,
    columns=None,
    output_dir='samples'
):
    """
    Generate a synthetic CSV file with specified columns and data types.

    Parameters:
        filename (str): Output CSV file name.
        num_rows (int): Number of rows in the dataset.
        columns (list of tuples): Format: [('column_name', 'type'), ...]
                                  Supported types: int, float, str, date, category
        output_dir (str): Directory to save the file.
    """

    if columns is None:
        columns = [
            ('id', 'int'),
            ('value', 'float'),
            ('category', 'category'),
            ('timestamp', 'date'),
            ('label', 'str'),
        ]

    data = {}

    for name, dtype in columns:
        if dtype == 'int':
            data[name] = np.random.randint(0, 1000, size=num_rows)
        elif dtype == 'float':
            data[name] = np.round(np.random.uniform(0.0, 1000.0, size=num_rows), 2)
        elif dtype == 'str':
            data[name] = [random_string(6) for _ in range(num_rows)]
        elif dtype == 'date':
            start = datetime(2020, 1, 1)
            data[name] = [start + timedelta(days=random.randint(0, 1000)) for _ in range(num_rows)]
        elif dtype == 'category':
            categories = ['A', 'B', 'C', 'D']
            data[name] = [random.choice(categories) for _ in range(num_rows)]
        else:
            raise ValueError(f"Unsupported data type: {dtype}")

    df = pd.DataFrame(data)

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"[✓] Sample CSV generated at: {filepath}")


# Example usage
if __name__ == '__main__':
    generate_sample_csv(
        filename='example_data.csv',
        num_rows=200,
        # columns=[
        #     ('user_id', 'int'),
        #     ('purchase_amount', 'float'),
        #     ('signup_date', 'date'),
        #     ('region', 'category'),
        #     ('referrer_code', 'str')
        # ]
        columns=[
            ('img_name', 'str'),
            ('img_path', 'str'),
            ('img_size', 'int'),
            ('img_width', 'int'),
            ('img_height', 'int'),
            ('img_format', 'category'),
            ('img_date', 'date'),
            ('img_label', 'str'),
            ('gt:object_type', 'category'),
            ('gt:angle', 'float'),
            ('classifierA_Score', 'float'),
            ('classifierB_Score', 'float'),
            ('classifierC_Score', 'float'),
            ('classifierD_Score', 'float'),
            ('classifierE_Score', 'float'),
            ('classifierF_Score', 'float'),
            ('classifierG_Score', 'float'),
            ('classifierH_Score', 'float'),
            ('classifierI_Score', 'float'),
            ('classifierJ_Score', 'float')
        ]
    )

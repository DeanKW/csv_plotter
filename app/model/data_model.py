import pandas as pd


class DataModel:
    def __init__(self):
        self.raw_df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.filters = {}

    def load_csv(self, filepath: str):
        """Load a CSV file into the model."""
        self.raw_df = pd.read_csv(filepath)
        self.filtered_df = self.raw_df.copy()
        self.filters.clear()
        print(f"[✓] Loaded CSV with shape: {self.raw_df.shape}")

    def get_columns(self):
        """Return list of columns in the DataFrame."""
        return list(self.raw_df.columns)

    def get_filtered_data(self):
        """Return the filtered DataFrame."""
        return self.filtered_df

    def apply_filters(self, filter_dict: dict):
        """
        Apply column-wise filters to the DataFrame.
        
        Example filter_dict:
        {
            'category': ['A', 'B'],
            'value': (10, 50)  # Numeric range filter
        }
        """
        if self.raw_df.empty:
            print("[!] No data loaded.")
            return

        df = self.raw_df.copy()

        for column, condition in filter_dict.items():
            if isinstance(condition, tuple) and len(condition) == 2:
                # Numeric range filter
                df = df[df[column].between(condition[0], condition[1])]
            elif isinstance(condition, list):
                # Category/multi-value match
                df = df[df[column].isin(condition)]
            else:
                print(f"[!] Unsupported filter format: {column}: {condition}")

        self.filtered_df = df
        self.filters = filter_dict
        print(f"[✓] Applied filters. Resulting shape: {df.shape}")

    def reset_filters(self):
        """Reset filters and use the raw DataFrame."""
        self.filtered_df = self.raw_df.copy()
        self.filters.clear()
        print("[✓] Filters reset.")


if __name__ == "__main__":
    # Example usage
    data_model = DataModel()
    data_model.load_csv("samples/example_data.csv")
    print(data_model.get_columns())
    data_model.apply_filters({'gt:object_type': ['A', 'B'], 'gt:angle': (10, 1000)})
    print(data_model.get_data())
    data_model.reset_filters()
    print(data_model.get_data())
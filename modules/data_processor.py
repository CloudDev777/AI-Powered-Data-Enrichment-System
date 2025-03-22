# modules/data_processor.py
import pandas as pd

class DataProcessor:
    def __init__(self):
        self.data = None
        
    def load_csv(self, file_path):
        """Load data from CSV file"""
        try:
            self.data = pd.read_csv(file_path)
            return True
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return False
    
    def get_query_columns(self):
        """Return column names for query building"""
        if self.data is not None:
            return list(self.data.columns)
        return []
    
    def build_queries(self, query_template, column_name):
        """Build search queries based on template and column"""
        if self.data is None or column_name not in self.data.columns:
            return []
        
        queries = []
        for value in self.data[column_name].dropna().unique():
            query = query_template.replace("{value}", str(value))
            queries.append({"value": value, "query": query})
        return queries
    
    def enrich_data(self, column_name, enriched_data):
        """Add enriched data to the dataframe"""
        if self.data is None:
            return False
        
        for item in enriched_data:
            value = item.get("original_value")
            enriched = item.get("enriched_data", {})
            
            # Create new columns for each enriched field
            for key, val in enriched.items():
                col_name = f"{key}"
                if col_name not in self.data.columns:
                    self.data[col_name] = None
                
                # Update rows matching the value
                self.data.loc[self.data[column_name] == value, col_name] = val
        
        return True
    
    def export_csv(self, output_path):
        """Export enriched data to CSV"""
        if self.data is not None:
            self.data.to_csv(output_path, index=False)
            return True
        return False

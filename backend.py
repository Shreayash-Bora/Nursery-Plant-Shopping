import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

class NurseryPlantFinance:
    def init(self):
        self.df = pd.DataFrame()

    def load_dataset(self, file_path):
        self.df = pd.read_csv(file_path)

    def display_data(self):
        if self.df.empty:
            return "No data loaded."
        data_summary = (f"Head:\n{self.df.head()}\n\n"
                        f"Description:\n{self.df.describe()}\n\n"
                        f"Missing values:\n{self.df.isnull().sum()}")
        return data_summary

    def clean_data(self):
        required_columns = ['Quantity', 'Price', 'DatePurchased']
        if not all(col in self.df.columns for col in required_columns):
            return "Required columns are missing for cleaning"

        self.df['Quantity'] = self.df['Quantity'].fillna(self.df['Quantity'].median())
        self.df['Price'] = self.df['Price'].fillna(self.df['Price'].median())

        return "Data cleaned successfully"

    def exploratory_data_analysis(self, graph_type):
        if not all(col in self.df.columns for col in ['DatePurchased', 'Category', 'PlantName', 'Price']):
            return "Required columns are missing for EDA"

        if not pd.api.types.is_datetime64_any_dtype(self.df['DatePurchased']):
            self.df['DatePurchased'] = pd.to_datetime(self.df['DatePurchased'], errors='coerce')
            self.df.dropna(subset=['DatePurchased'], inplace=True)

        if self.df['DatePurchased'].isnull().all():
            return "All entries in 'DatePurchased' are invalid dates"

        self.df['Month'] = self.df['DatePurchased'].dt.month
        self.df['Day'] = self.df['DatePurchased'].dt.day
        self.df['Year'] = self.df['DatePurchased'].dt.year

        label_encoder = LabelEncoder()
        self.df['Category'] = label_encoder.fit_transform(self.df['Category'])
        self.df['PlantName'] = label_encoder.fit_transform(self.df['PlantName'])

        if graph_type == "Line Graph":
            plt.figure(figsize=(12, 6))
            monthly_sales = self.df.groupby(['Year', 'Month'])['Price'].sum().reset_index()
            sns.lineplot(x='Month', y='Price', hue='Year', data=monthly_sales, marker='o')
            plt.xlabel('Month')
            plt.ylabel('Prices')
            plt.title('Prices Over Time')
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        elif graph_type == "Bar Graph":
            plt.figure(figsize=(12, 6))
            plant_sales = self.df.groupby('PlantName')['Price'].sum().reset_index()
            top_plants = plant_sales.sort_values(by='Price', ascending=False).head(10)
            sns.barplot(x='PlantName', y='Price', data=top_plants, palette='muted')
            plt.xlabel('Plant')
            plt.ylabel('Price')
            plt.title('Top 10 Plants by Price')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    def display_summary(self):
        total_revenue = self.df['Price'].sum()
        total_plants_sold = self.df['Quantity'].sum()
        unique_plants_sold = self.df['PlantName'].nunique()
        summary_message = (f'Total Revenue: {total_revenue:.2f}\n'
                           f'Total Number of Plants Sold: {total_plants_sold}\n'
                           f'Total Unique Plant Types Sold: {unique_plants_sold}')
        return summary_message

    def visualize_data(self, choice):
        if choice == "Price Distribution":
            plt.figure(figsize=(10, 6))
            self.df['Price'].hist(bins=30, alpha=0.7)
            plt.xlabel('Price')
            plt.ylabel('Frequency')
            plt.title('Price Distribution')
            plt.show()

        elif choice == "Quantity Distribution":
            plt.figure(figsize=(10, 6))
            self.df['Quantity'].hist(bins=30, alpha=0.7, color='orange')
            plt.xlabel('Quantity')
            plt.ylabel('Frequency')
            plt.title('Quantity Distribution')
            plt.show()

    def generate_transaction_report(self):
        report = self.df[['Quantity', 'Price', 'DatePurchased', 'Category', 'PlantName']].copy()
        return report.to_string(index=False)

    def generate_profit_gain_report(self):
        if (self.df['Price'] < 0).any() or (self.df['Quantity'] < 0).any():
            return "Negative values detected in Price or Quantity. Please clean the data."

        self.df['Total_cost'] = self.df['Price'] * self.df['Quantity']
        total_revenue = self.df['Price'].sum()
        total_cost = self.df['Total_cost'].sum()
        total_profit = total_cost - total_revenue

        profit_message = (f'Total Revenue: {total_revenue:.2f}\n'
                          f'Total Cost: {total_cost:.2f}\n'
                          f'Total Profit: {total_profit:.2f}')
        return profit_message
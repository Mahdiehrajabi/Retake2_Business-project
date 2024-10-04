import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import os

# Change to the directory to load dataset
new_directory = r'C:\2'  
os.chdir(new_directory)

# Check current working directory
print("Current Working Directory:", os.getcwd())

# Read csv dataset
df = pd.read_csv('amazon.csv')
df.dropna(inplace=True)
def run_code():
    # Clear previous output
    text_output.delete('1.0', tk.END)

    try:

        # Debugging: Print the first few rows of the DataFrame
        print("Loaded DataFrame:")
        print(df.head())  
        
        # Debugging
        print("DataFrame Columns:")
        print(df.columns.tolist())  

        # Check the data types
        print("Data Types:")
        print(df.dtypes)  

        # Check if the expected columns exist
        expected_columns = ['category', 'rating']  
        missing_columns = [col for col in expected_columns if col not in df.columns]
        
        if missing_columns:
            text_output.insert(tk.END, f"Missing columns: {', '.join(missing_columns)}\n")
            return

        # Extract main categories
        df['main_category'] = df['category'].astype(str).str.split('|').str[0]

        # Get top 10 main categories by count
        top_main_categories = df['main_category'].value_counts().nlargest(10)

        # Display the top 10 main categories in the text output
        text_output.insert(tk.END, "Top 10 Main Categories by Count:\n")
        text_output.insert(tk.END, top_main_categories.to_string() + "\n\n")

        # Convert the 'rating' column to numeric
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        # Drop rows with NaN in 'rating' if necessary
        df.dropna(subset=['rating'], inplace=True)

        # Calculate average ratings by main category
        main_category_ratings = df.groupby('main_category')['rating'].mean().sort_values(ascending=False).nlargest(10)

        # Debugging: Print average ratings by main category
        print("Average Ratings by Main Category:")
        print(main_category_ratings)  # Print average ratings for debugging

        # Create a bar chart for average ratings by main category
        fig, ax = plt.subplots(figsize=(8, 5))
        main_category_ratings.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title('Average Rating by Main Category (Top 10)', fontsize=16)
        ax.set_xlabel('Main Category', fontsize=12)
        ax.set_ylabel('Average Rating', fontsize=12)
        ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility

        # Display the bar chart in the GUI
        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=30)

        # Display average ratings in the text output
        text_output.insert(tk.END, "Average Ratings by Main Category:\n")
        for category, rating in main_category_ratings.items():
            text_output.insert(tk.END, f"{category}: {rating:.2f}\n")

    except FileNotFoundError:
        text_output.insert(tk.END, "Error: CSV file not found. Please check the file path.\n")
    except Exception as e:
        text_output.insert(tk.END, f"An error occurred: {e}\n")

# Create the main window
root = tk.Tk()
root.title("Product Analysis")
root.geometry("1100x800")

# Frame for plots
frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Scrollable text output
text_output = scrolledtext.ScrolledText(root, width=70, height=10)
text_output.pack(padx=10, pady=10)

# Button to run the analysis
run_button = ttk.Button(root, text="Run Analysis", command=run_code)
run_button.pack(pady=30)

# Start the Tkinter main loop
root.mainloop()

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import os

# Change to the directory containing the CSV file
new_directory = r'C:\2' 
os.chdir(new_directory)

# Check current working directory
print("Current Working Directory:", os.getcwd())

# Read csv dataset
df = pd.read_csv('amazon.csv')
df.dropna(inplace=True)

def run_code():
    # Clear the output box
    text_output.delete("1.0", tk.END)

    try:
    

        # Convert relevant columns to numeric (Make sure that all are number)
        df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
        df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')
        df.dropna(subset=['discounted_price', 'actual_price'], inplace=True)

        # Define main categories
        df['main_category'] = df['category'].astype(str).str.split('|').str[0]

        # Calculate average prices and counts for main categories
        main_category_counts = df['main_category'].value_counts()[:10]
        avg_discounted_price_by_category = df.groupby('main_category')['discounted_price'].mean().loc[main_category_counts.index]
        avg_actual_price_by_category = df.groupby('main_category')['actual_price'].mean().loc[main_category_counts.index]

        # Combine both averages into a single DataFrame
        comparison_df = pd.DataFrame({
            'Average Discounted Price': avg_discounted_price_by_category,
            'Average Actual Price': avg_actual_price_by_category
        }).reset_index()

        # Set the figure for the bar plot
        fig, ax = plt.subplots(figsize=(12, 6))

        # Set the bar width
        bar_width = 0.25
        x = range(len(comparison_df))

        # Plot bars for average discounted prices
        ax.bar(x, comparison_df['Average Discounted Price'], width=bar_width, label='Average Discounted Price', color='purple')

        # Plot bars for average actual prices
        ax.bar([p + bar_width for p in x], comparison_df['Average Actual Price'], width=bar_width, label='Average Actual Price', color='lightgreen')

        # Set the x-ticks with main category names
        ax.set_xticks([p + bar_width / 2 for p in x])
        ax.set_xticklabels(comparison_df['main_category'], rotation=45, ha='right', fontsize=10)  # Adjust rotation and font size

        # Set titles and labels
        ax.set_title('Comparison of Average Discounted Prices and Actual Prices by Main Category', fontsize=16)
        ax.set_xlabel('Main Category', fontsize=12)
        ax.set_ylabel('Average Price', fontsize=12)
        ax.legend()

        # Display the comparison chart in the GUI
        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=30)

        # Show debug information in the text output
        text_output.insert(tk.END, "Top 10 Main Categories with Average Prices:\n")
        text_output.insert(tk.END, comparison_df.to_string(index=False) + "\n")

    except Exception as e:
        text_output.insert(tk.END, f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Main Category Price Comparison")
root.geometry("800x600")

# Frame for plots
frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Scrolled text for output
text_output = scrolledtext.ScrolledText(root, width=70, height=15)
text_output.pack(padx=10, pady=10)

# Button to run the analysis
run_button = ttk.Button(root, text="Run Price Comparison", command=run_code)
run_button.pack(pady=20)

# Start the main loop
root.mainloop()

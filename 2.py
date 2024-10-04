from subprocess import getoutput
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# Customer behavior according to catogory and rating
# Market trends according to dicounted price and actual price 
# Call .py files
sys.path.append(r'C:\2\customer_behavior') 
sys.path.append(r'C:\2\market_trends') 

# Change to the directory containing the CSV file
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


    # Display data shape and numerical properties
    text_output.insert(tk.END, f" Shape: {df.shape}\n\n")


    #  Diagram of the main categories
    df['main_category'] = df['category'].astype(str).str.split('|').str[0]
    main_category_counts = df['main_category'].value_counts()[:10]

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.barh(range(len(main_category_counts)), main_category_counts.values)
    ax.set_xlabel('Number of Products')
    ax.set_title('Distribution of Products by Main Category (Top 10)')
    ax.set_yticks(range(len(main_category_counts)))
    ax.set_yticklabels(main_category_counts.index)
    ax.tick_params(axis='y', labelsize=4)
    
    # Display the chart 
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Display main category
    text_output.insert(tk.END, "Top 10 main categories:\n")
    top_main_categories = pd.DataFrame({
        'Main Category': main_category_counts.index,
        'Number of Products': main_category_counts.values
    })
    text_output.insert(tk.END, top_main_categories.to_string(index=False) + "\n\n")

    # Dispaly Sub category graph
    df['sub_category'] = df['category'].astype(str).str.split('|').str[-1]
    sub_category_counts = df['sub_category'].value_counts()[:10]

    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ax2.barh(range(len(sub_category_counts)), sub_category_counts.values)
    ax2.set_xlabel('Number of Products')
    ax2.set_title('Distribution of Products by Sub Category (Top 10)')
    ax2.set_yticks(range(len(sub_category_counts)))
    ax2.set_yticklabels(sub_category_counts.index)
    ax2.tick_params(axis='y', labelsize=5)
    
    # Show second graph at same page
    canvas2 = FigureCanvasTkAgg(fig2, master=frame_plot)
    canvas2.draw()
    canvas2.get_tk_widget().pack()
    
    # Show text
    text_output.insert(tk.END, "Top 10 sub categories:\n")
    top_sub_categories = pd.DataFrame({
        'Sub Category': sub_category_counts.index,
        'Number of Products': sub_category_counts.values
    })
    text_output.insert(tk.END, top_sub_categories.to_string(index=False) + "\n")


# Creat a main window
root = tk.Tk()
root.title("Product Analysis")
root.geometry("900x700")

# Fram of window
frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# scroll 
text_output = scrolledtext.ScrolledText(root, width=70, height=10)
text_output.pack(padx=10, pady=10)

# Button for run the code
run_button = ttk.Button(root, text="Run Analysis", command=run_code)
run_button.pack(pady=30)

# Main loop
root.mainloop()


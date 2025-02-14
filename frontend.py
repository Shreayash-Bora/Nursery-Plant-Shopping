import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import sqlite3
from backend import NurseryPlantFinance  # Importing backend
from PIL import Image, ImageTk
import os

# Initialize the finance app
finance_app = NurseryPlantFinance()

# Connect to SQLite3 database
def connect_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Registration", "User registered successfully!")
        conn.close()
        login_frame()
    except sqlite3.IntegrityError:
        messagebox.showerror("Registration Error", "Username already exists.")
    except Exception as e:
        messagebox.showerror("Registration Error", str(e))
    finally:
        conn.close()

def validate_login(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Login Frame
def login_frame():
    global root
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Login")
    root.configure(background="#0096DC")

    # Add Nursery Plant Shopping text
    tk.Label(root, text="Nursery Plant Shopping", font=("Helvetica", 20)).pack(pady=20)

    tk.Label(root, text="Username", bg="yellow").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password", bg="yellow").pack(pady=5)
    password_entry = tk.Entry(root, show='*')
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if validate_login(username, password):
            main_frame()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    tk.Button(root, text="Login", command=login).pack(pady=10)

    # Text and Register button
    tk.Label(root, text="Don't have an account?", bg="yellow").pack(pady=5)
    tk.Button(root, text="Register", command=register_frame).pack(pady=5)

# Registration Frame
def register_frame():
    global root
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Register")
    root.configure(background="light green")

    tk.Label(root, text="Nursery Plant Shopping", font=("Helvetica", 20)).pack(pady=20)

    tk.Label(root, text="Username", bg="yellow").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password", bg="yellow").pack(pady=5)
    password_entry = tk.Entry(root, show='*')
    password_entry.pack(pady=5)

    tk.Label(root, text="Confirm Password", bg="yellow").pack(pady=5)
    confirm_password_entry = tk.Entry(root, show='*')
    confirm_password_entry.pack(pady=5)

    def register():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        if username and password:
            if password == confirm_password:
                register_user(username, password)
            else:
                messagebox.showerror("Registration Error", "Passwords do not match.")
        else:
            messagebox.showerror("Registration Error", "Please enter both username and password.")

    tk.Button(root, text="Register", command=register).pack(pady=10)
    tk.Button(root, text="Back to Login", command=login_frame).pack(pady=5)

# Load dataset function
def load_dataset():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            finance_app.load_dataset(file_path)
            messagebox.showinfo("Info", "Dataset loaded successfully")
            display_data(finance_app.display_data())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset: {str(e)}")

# Display data function
def display_data(data_summary):
    data_window = tk.Toplevel(root)
    data_window.title("Dataset Summary")

    text_area = scrolledtext.ScrolledText(data_window, wrap=tk.WORD, width=100, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.insert(tk.INSERT, data_summary)
    text_area.config(state=tk.DISABLED)

# Clean data function
def clean_data():
    result = finance_app.clean_data()
    messagebox.showinfo("Info", result)

# Exploratory data analysis function with graph type selection
def exploratory_data_analysis():
    eda_window = tk.Toplevel(root)
    eda_window.title("Exploratory Data Analysis")

    options = ["Line Graph", "Bar Graph"]
    selected_option = tk.StringVar()
    selected_option.set(options[0])

    dropdown = ttk.OptionMenu(eda_window, selected_option, *options)
    dropdown.pack(pady=10)

    def perform_eda():
        choice = selected_option.get()
        finance_app.exploratory_data_analysis(choice)

    analyze_button = tk.Button(eda_window, text="Perform Analysis", command=perform_eda)
    analyze_button.pack(pady=10)

# Display summary function
def display_summary():
    summary = finance_app.display_summary()
    messagebox.showinfo("Summary", summary)

# Visualize data function
def visualize_data():
    graph_window = tk.Toplevel(root)
    graph_window.title("Select Graph to Display")

    options = ["Price Distribution", "Quantity Distribution"]
    selected_option = tk.StringVar()
    selected_option.set(options[0])

    dropdown = ttk.OptionMenu(graph_window, selected_option, *options)
    dropdown.pack(pady=10)

    def show_graph():
        choice = selected_option.get()
        finance_app.visualize_data(choice)

    show_button = tk.Button(graph_window, text="Show Graph", command=show_graph)
    show_button.pack(pady=10)

# Generate transaction report function
def generate_transaction_report():
    report_window = tk.Toplevel(root)
    report_window.title("Transaction Report")

    tree = ttk.Treeview(report_window, columns=('Quantity', 'Price', 'DatePurchased', 'Category', 'PlantName'), show='headings')
    tree.heading('Quantity', text='Quantity')
    tree.heading('Price', text='Price')
    tree.heading('DatePurchased', text='Date Purchased')
    tree.heading('Category', text='Category')
    tree.heading('PlantName', text='Plant Name')

    # Adjust the width of columns
    tree.column('Quantity', width=100)
    tree.column('Price', width=100)
    tree.column('DatePurchased', width=150)
    tree.column('Category', width=150)
    tree.column('PlantName', width=150)

    tree.pack(fill=tk.BOTH, expand=True)

    # Insert data into the treeview
    for _, row in finance_app.df.iterrows():
        tree.insert('', 'end', values=(row['Quantity'], row['Price'], row['DatePurchased'], row['Category'], row['PlantName']))

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(report_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Generate profit gain report function
def generate_profit_gain_report():
    report = finance_app.generate_profit_gain_report()
    messagebox.showinfo("Profit Gain Report", report)

# Main frame after login
def main_frame():
    global root
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Nursery Plant Shopping (Finance)")
    root.configure(background="yellow")

    # Add the title label
    title_label = tk.Label(root, text="Nursery Plant Shopping", font=("Helvetica", 24), bg="yellow")
    title_label.pack(pady=20)

    # Add the image using Pillow
    image_path = "plant.png"  # Replace with your image file name
    if os.path.exists(image_path):
        try:
            pil_image = Image.open(image_path)
            
            # Resize the image to make it bigger
            new_size = (400, 300)  # Adjust the size as needed
            pil_image = pil_image.resize(new_size)
            
            logo_image = ImageTk.PhotoImage(pil_image)
            image_label = tk.Label(root, image=logo_image, bg="yellow")
            image_label.image = logo_image  # Keep a reference to avoid garbage collection
            image_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load image: {str(e)}")
    else:
        messagebox.showerror("Image Error", "Image file not found.")

    # Create a frame for the first row of buttons
    button_frame_row1 = tk.Frame(root, bg="yellow")
    button_frame_row1.pack(pady=10)

    # Create a frame for the second row of buttons
    button_frame_row2 = tk.Frame(root, bg="yellow")
    button_frame_row2.pack(pady=10)

    # Row 1 Buttons
    load_button = tk.Button(button_frame_row1, text="Load Data", command=load_dataset, fg="blue")
    load_button.pack(side=tk.LEFT, padx=50 , pady=30)

    clean_button = tk.Button(button_frame_row1, text="Clean Data", command=clean_data, fg="blue")
    clean_button.pack(side=tk.LEFT, padx=50 , pady=30)


    report_button = tk.Button(button_frame_row1, text="Generate Transaction Report", command=generate_transaction_report, fg="blue")
    report_button.pack(side=tk.LEFT, padx=50 , pady=30)

    eda_button = tk.Button(button_frame_row1, text="Exploratory Data Analysis", command=exploratory_data_analysis, fg="blue")
    eda_button.pack(side=tk.LEFT, padx=50 , pady=30)

    # Row 2 Buttons
    summary_button = tk.Button(button_frame_row2, text="Display Summary", command=display_summary, fg="blue")
    summary_button.pack(side=tk.LEFT, padx=50 , pady=30)

    visualize_button = tk.Button(button_frame_row2, text="Visualize Data", command=visualize_data,fg="blue")
    visualize_button.pack(side=tk.LEFT, padx=50 , pady=30)

    profit_button = tk.Button(button_frame_row2, text="Generate Profit Gain Report", command=generate_profit_gain_report, fg="blue")
    profit_button.pack(side=tk.LEFT, padx=50 , pady=30)

# Run the application
root = tk.Tk()
connect_db()
login_frame()
root.mainloop()

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

def center_window(window): # to center window 
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def open_meal_page():
    root.withdraw()  
    meal_page = tk.Toplevel(root)
    meal_page.title("Meal Selection")
    meal_page.configure(bg="#d0f0c0")  
    meal_page.geometry("800x500")
    center_window(meal_page)

    meal_frame = tk.Frame(meal_page, bg="#d0f0c0") 
    meal_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    def add_meal(event=None):  
        query = query_entry.get()
        meal_listbox.insert(tk.END, query)
        query_entry.delete(0, tk.END)

    def delete_meal():
        selected_index = meal_listbox.curselection()
        if len(selected_index) > 0:
            meal_listbox.delete(selected_index)

    query_label = tk.Label(meal_frame, text="Query:", font=("Helvetica", 14), bg="#d0f0c0", fg="black")
    query_label.pack(pady=5)

    query_entry = tk.Entry(meal_frame, font=("Helvetica", 14))
    query_entry.pack(pady=5)

    add_button = tk.Button(meal_frame, text="Add Meal", font=("Helvetica", 14), bg="#9ab973", fg="black", command=add_meal)  
    add_button.pack(pady=10)

    # Bind the "Return" key to enter query 
    query_entry.bind("<Return>", add_meal)

    #frame for meal listbox
    meal_listbox_frame = tk.Frame(meal_frame, bg="#eedc82")  
    meal_listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    #creating the scrollbar 
    scrollbar = tk.Scrollbar(meal_listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #creating the meal listbox 
    meal_listbox = tk.Listbox(meal_listbox_frame, font=("Helvetica", 14), bg="#eedc82", fg="black", selectbackground="#fada5e", selectforeground="black", yscrollcommand=scrollbar.set)
    meal_listbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    #configuring the scrollbar to change the y-view (vertical)
    scrollbar.config(command=meal_listbox.yview)

    #creating the delete button 
    delete_button = tk.Button(meal_frame, text="Delete Meal", font=("Helvetica", 14), bg="#9ab973", fg="black", command=delete_meal)
    delete_button.pack(side=tk.LEFT, pady=10, padx=5)

    def open_optimize_page():
        meal_page.destroy() 
        optimize_page = tk.Toplevel(root)
        optimize_page.title("Optimize Meals")
        optimize_page.configure(bg="#d0f0c0")  
        optimize_page.geometry("800x500")
        center_window(optimize_page)

        #creating the progress label 
        progress_label = tk.Label(optimize_page, text="Optimizing your meals!", font=("Helvetica", 18), bg="#d0f0c0", fg="black")   
        progress_label.pack(pady=10)

        #creating the progress bar 
        progress_bar = ttk.Progressbar(optimize_page, mode='indeterminate')
        progress_bar.pack(pady=10)

        def start_optimization():
            progress_bar.start()

        #creating the start button (for optimization)
        start_button = tk.Button(optimize_page, text="Start Optimization", font=("Helvetica", 14), bg="#9ab973", fg="black", command=start_optimization)  
        start_button.pack(pady=10)

        #creating the cancel button
        cancel_button= tk.Button(optimize_page, text= "Cancel",font=("Helvetica", 14), bg="#9ab973", fg="black", command= open_meal_page)
        cancel_button.pack(pady=10)

    #creating the optimize button in the open_meal_page
    optimize_button = tk.Button(meal_frame, text="Optimize Meals", font=("Helvetica", 14), bg="#9ab973", fg="black", command=open_optimize_page)
    optimize_button.pack(side=tk.LEFT, pady=10, padx=5)

def open_calorie_page():
    root.withdraw()  
    calorie_page = tk.Toplevel(root)
    calorie_page.title("Calorie Limit")
    calorie_page.configure(bg="#d0f0c0")  
    calorie_page.geometry("800x500")
    center_window(calorie_page)

    def calculate_meal_plan():
        calorie_limit = calorie_entry.get()
        #eto yung variable once gagamitin na yung calorie limit for the computation

        calorie_page.destroy()  # Destroy the calorie page before opening the meal page
        open_meal_page()

    #creating calorie entry label
    calorie_label = tk.Label(calorie_page, text="Enter Calorie Limit:", font=("Helvetica", 18), bg="#d0f0c0", fg="black")  
    calorie_label.pack(pady=10)

    #creating the calorie entry field 
    calorie_entry = tk.Entry(calorie_page, font=("Helvetica", 16))
    calorie_entry.pack(pady=5)

    #creating the proceed button
    calculate_button = tk.Button(calorie_page, text="Proceed", font=("Helvetica", 18), bg="#9ab973", fg="black", command=calculate_meal_plan) 
    calculate_button.pack(pady=10)

# main window 
root = tk.Tk()
root.title("SmartPlate")
root.geometry("800x500") #to resize the main window 
center_window(root) #calling the center_window function to center the main window 
root.configure(bg="#d0f0c0")  #setting the background color 

# Set the font
header_font = ("Helvetica", 36, "bold")
slogan_font = ("Helvetica", 24)
button_font = ("Helvetica", 18)

# Create header label
header_label = tk.Label(root, text="SmartPlate", font=header_font, bg="#d0f0c0", fg="black")
header_label.pack(pady=30)

# Create slogan label
slogan_label = tk.Label(root, text="Optimize your meals!", font=slogan_font, bg="#d0f0c0", fg="black")  
slogan_label.pack(pady=15)

# Load and resize the logo image
logo_image = Image.open("D:\SmartPlate GUI\Elements\logo.png")
logo_image = logo_image.resize((200, 200), Image.ANTIALIAS)
logo_photo = ImageTk.PhotoImage(logo_image)

# Create logo label
logo_label = tk.Label(root, image=logo_photo, bg="#d0f0c0")  
logo_label.pack(pady=10)

# Create start button
start_button = tk.Button(root, text="Start", font=button_font, bg="#9ab973", fg="black", command=open_calorie_page)
start_button.pack(pady=15)

# Run the GUI
root.mainloop()

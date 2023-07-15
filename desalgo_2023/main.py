import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import meal_query
import nutritionix
import fractional_knapsack

meals = {}
nutriscores = []
calorie_limit = 0
knapsack_result = []
result_data = []


def center_window(window):  # to center window
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
        result = meal_query.search_meal(query, meals)

        if result is None:
            messagebox.showerror("ERROR", "Please enter a valid meal.")
            return

        meal_treeview.insert("", tk.END, values=(query))
        query_entry.delete(0, tk.END)

    def delete_meal():
        selected_item = meal_treeview.focus()
        meals.pop(meal_treeview.item(selected_item)["values"][0])
        if selected_item:
            meal_treeview.delete(selected_item)

    query_label = tk.Label(
        meal_frame,
        text="Query:",
        font=("Helvetica", 14, "bold"),
        bg="#d0f0c0",
        fg="black",
    )
    query_label.pack(pady=5)

    query_entry = tk.Entry(meal_frame, font=("Helvetica", 14))
    query_entry.pack(pady=5)

    add_button = tk.Button(
        meal_frame,
        text="Add Meal",
        font=("Helvetica", 14),
        bg="#9ab973",
        fg="black",
        command=add_meal,
    )
    add_button.pack(pady=10)

    # Bind the "Return" key to enter query
    query_entry.bind("<Return>", add_meal)

    meal_treeview_frame = tk.Frame(meal_frame, bg="#eedc82")
    meal_treeview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Create scrollbar for y-axis
    scrollbar_y = ttk.Scrollbar(meal_treeview_frame, orient="vertical")
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    # style for the treeview
    style = ttk.Style()
    style.configure("Custom.Treeview", background="#eedc82")

    # Create meal Treeview
    meal_treeview = ttk.Treeview(
        meal_treeview_frame,
        style="Custom.Treeview",
        columns=("meal_name", "nutriscore", "calorie"),
        show="headings",
        yscrollcommand=scrollbar_y.set,
    )
    meal_treeview.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Configure column headers
    meal_treeview.heading("meal_name", text="Meal Name")
    meal_treeview.heading("nutriscore", text="Nutriscore")
    meal_treeview.heading("calorie", text="Calorie")

    # Set column widths
    meal_treeview.column("meal_name", width=200)
    meal_treeview.column("nutriscore", width=100)
    meal_treeview.column("calorie", width=100)

    # configure y scrollbar for treeview
    scrollbar_y.config(command=meal_treeview.yview)

    delete_button = tk.Button(
        meal_frame,
        text="Delete Meal",
        font=("Helvetica", 14),
        bg="#9ab973",
        fg="black",
        command=delete_meal,
    )
    delete_button.pack(side=tk.LEFT, pady=10, padx=5)

    back_button = tk.Button(
        meal_frame,
        text="Back",
        font=("Helvetica", 14),
        bg="#9ab973",
        fg="black",
        command=open_calorie_page,
    )
    back_button.pack(side=tk.RIGHT, pady=10, padx=5)

    def open_optimize_page():

        if meal_treeview.size() == 0:
            messagebox.showerror("Error", "Please add meals to the list.")
            return

        global optimize_page
        meal_page.destroy()
        optimize_page = tk.Toplevel(root)
        optimize_page.title("Optimize Meals")
        optimize_page.configure(bg="#d0f0c0")
        optimize_page.geometry("800x500")
        center_window(optimize_page)

        # creating the progress label
        progress_label = tk.Label(
            optimize_page,
            text="Optimizing your meals!",
            font=("Helvetica", 28, "bold"),
            bg="#d0f0c0",
            fg="black",
        )
        progress_label.pack(pady=50)

        # creating the progress bar
        progress_bar = ttk.Progressbar(optimize_page, mode="indeterminate")
        progress_bar.pack(pady=20)

        def start_optimization():
            global knapsack_result
            progress_bar.start()
            for i in meals.keys():
                meals[i]["nutriscore"] = nutritionix.get_nutriscore(meals[i])

            knapsack_result = fractional_knapsack.calculate(int(calorie_limit), meals)

            # open result page after 3s
            optimize_page.after(3000, open_result_page)

        # creating the start button (for optimization)
        start_button = tk.Button(
            optimize_page,
            text="Start Optimization",
            font=("Helvetica", 18),
            bg="#9ab973",
            fg="black",
            command=start_optimization,
        )
        start_button.pack(pady=10)

        # creating the cancel button
        cancel_button = tk.Button(
            optimize_page,
            text="Cancel",
            font=("Helvetica", 18),
            bg="#9ab973",
            fg="black",
            command=open_meal_page,
        )
        cancel_button.pack(pady=10)

    # creating the optimize button in the open_meal_page
    optimize_button = tk.Button(
        meal_frame,
        text="Optimize Meals",
        font=("Helvetica", 14),
        bg="#9ab973",
        fg="black",
        command=open_optimize_page,
    )
    optimize_button.pack(side=tk.LEFT, pady=10, padx=5)


def open_result_page():
    optimize_page.destroy()
    result_page = tk.Toplevel(root)
    result_page.title("Optimization Result")
    result_page.configure(bg="#d0f0c0")
    result_page.geometry("800x500")
    center_window(result_page)

    # Create the header label
    header_label = tk.Label(
        result_page,
        text="Optimized Meal Selections",
        font=("Helvetica", 18, "bold"),
        bg="#d0f0c0",
        fg="black",
    )
    header_label.pack(pady=10)

    # Create result frame
    result_frame = tk.Frame(result_page, bg="#d0f0c0")
    result_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Create Treeview with custom style
    style = ttk.Style()
    style.configure("Custom.Treeview", background="#eedc82")

    # Create Treeview
    result_table = ttk.Treeview(result_frame, style="Custom.Treeview", height=10)
    result_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure Treeview columns
    result_table["columns"] = (
        "meal_name",
        "quantity",
        "nutriscore",
        "protein",
        "carbohydrates",
        "calorie",
        "sugar",
        "cholesterol",
    )

    # Format column headers
    result_table.heading("meal_name", text="Meal Name")
    result_table.heading("quantity", text="Quantity")
    result_table.heading("nutriscore", text="Nutriscore")
    result_table.heading("protein", text="Protein")
    result_table.heading("carbohydrates", text="Carbohydrates")
    result_table.heading("calorie", text="Calorie")
    result_table.heading("sugar", text="Sugar")
    result_table.heading("cholesterol", text="Cholesterol")

    # Set column widths
    result_table.column("meal_name", width=150)
    result_table.column("quantity", width=100)
    result_table.column("nutriscore", width=100)
    result_table.column("protein", width=100)
    result_table.column("carbohydrates", width=120)
    result_table.column("calorie", width=100)
    result_table.column("sugar", width=100)
    result_table.column("cholesterol", width=120)

    for included_meal in knapsack_result[0]:
        meal = included_meal
        quantity = meals[included_meal]["quantity"]
        nutriscore = nutritionix.nutriscore_conversion(
            meals[included_meal]["nutriscore"]
        )
        protein = meals[included_meal]["protein"]
        carbohydrates = meals[included_meal]["carbohydrates"]
        calorie = meals[included_meal]["calories"]
        sugar = meals[included_meal]["sugar"]
        cholesterol = meals[included_meal]["cholesterol"]

        result_data.append(
            (
                meal,
                quantity,
                nutriscore,
                protein,
                carbohydrates,
                calorie,
                sugar,
                cholesterol,
            )
        )

    # insertion of temporary data into Treeview
    for data in result_data:
        result_table.insert("", tk.END, values=data)

    # Create scrollbar for y-axis
    scrollbar_y = ttk.Scrollbar(
        result_frame, orient="vertical", command=result_table.yview
    )
    scrollbar_y.pack(side=tk.LEFT, fill=tk.Y)

    # Create scrollbar for x-axis
    scrollbar_x = ttk.Scrollbar(
        result_page, orient="horizontal", command=result_table.xview
    )
    scrollbar_x.pack(fill=tk.X)

    # Configure x-axis scrollbar to work with Treeview
    result_table.configure(
        yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set
    )

    # Create a button to go back to the open_meal_page
    def go_back():
        result_page.destroy()
        open_meal_page()

    # Create a label for the note/recommendation section
    note_label = tk.Label(
        result_page,
        text=f"You can reduce {knapsack_result[1]} percent of {knapsack_result[2]} if you want to include it",
        font=("Helvetica", 12),
        bg="#eedc82",
        fg="black",
    )
    note_label.pack(pady=10, padx=20, fill=tk.BOTH)

    do_another_button = tk.Button(
        result_page,
        text="Do another",
        font=("Helvetica", 14),
        bg="#9ab973",
        fg="black",
        command=go_back,
    )
    do_another_button.pack(pady=10)


def open_calorie_page():
    root.withdraw()
    calorie_page = tk.Toplevel(root)
    calorie_page.title("Calorie Limit")
    calorie_page.configure(bg="#d0f0c0")
    calorie_page.geometry("800x500")
    center_window(calorie_page)

    def calculate_meal_plan():
        global calorie_limit
        print(nutriscore_var.get())
        print(carbohydrates_var.get())
        calorie_limit = calorie_entry.get()

        calorie_page.destroy()  # Destroy the calorie page before opening the meal page
        open_meal_page()

    def validate_entry():
        calorie_limit = calorie_entry.get()
        checkbox_selected = (
            nutriscore_var.get()
            or carbohydrates_var.get()
            or protein_var.get()
            or sugar_var.get()
            or cholesterol_var.get()
        )
        if not checkbox_selected:
            messagebox.showerror("Error", "Please select at least one checkbox.")
        elif not calorie_limit.isdigit():
            messagebox.showerror("Error", "Please enter a valid calorie limit.")
        else:
            calculate_meal_plan()

    # creating calorie entry label
    calorie_label = tk.Label(
        calorie_page,
        text="Enter Calorie Limit:",
        font=("Helvetica", 18, "bold"),
        bg="#d0f0c0",
        fg="black",
    )
    calorie_label.pack(pady=10)

    # creating the calorie entry field
    calorie_entry = tk.Entry(calorie_page, font=("Helvetica", 16))
    calorie_entry.pack(pady=5)

    # Adding the label for checkbox options
    options_label = tk.Label(
        calorie_page,
        text="Choose the values you wish to include in the output:",
        font=("Helvetica", 18, "bold"),
        bg="#d0f0c0",
        fg="black",
    )
    options_label.pack(pady=10, anchor="w")

    # Creating the checkbox options
    nutriscore_var = tk.IntVar()
    carbohydrates_var = tk.IntVar()
    protein_var = tk.IntVar()
    sugar_var = tk.IntVar()
    cholesterol_var = tk.IntVar()

    nutriscore_checkbox = tk.Checkbutton(
        calorie_page,
        text="Nutriscore",
        variable=nutriscore_var,
        font=("Helvetica", 12),
        bg="#d0f0c0",
        fg="black",
        anchor="w",
    )
    nutriscore_checkbox.pack(pady=5, anchor="w")

    carbohydrates_checkbox = tk.Checkbutton(
        calorie_page,
        text="Carbohydrates",
        variable=carbohydrates_var,
        font=("Helvetica", 12),
        bg="#d0f0c0",
        fg="black",
        anchor="w",
    )
    carbohydrates_checkbox.pack(pady=5, anchor="w")

    protein_checkbox = tk.Checkbutton(
        calorie_page,
        text="Protein",
        variable=protein_var,
        font=("Helvetica", 12),
        bg="#d0f0c0",
        fg="black",
        anchor="w",
    )
    protein_checkbox.pack(pady=5, anchor="w")

    sugar_checkbox = tk.Checkbutton(
        calorie_page,
        text="Sugar",
        variable=sugar_var,
        font=("Helvetica", 12),
        bg="#d0f0c0",
        fg="black",
        anchor="w",
    )
    sugar_checkbox.pack(pady=5, anchor="w")

    cholesterol_checkbox = tk.Checkbutton(
        calorie_page,
        text="Cholesterol",
        variable=cholesterol_var,
        font=("Helvetica", 12),
        bg="#d0f0c0",
        fg="black",
        anchor="w",
    )
    cholesterol_checkbox.pack(pady=5, anchor="w")

    # creating the proceed button
    calculate_button = tk.Button(
        calorie_page,
        text="Proceed",
        font=(
            "Helvetica",
            18,
        ),
        bg="#9ab973",
        fg="black",
        command=validate_entry,
    )
    calculate_button.pack(pady=10)


def _quit():
    root.quit()
    root.destroy()


# main window
root = tk.Tk()
root.title("SmartPlate")
root.geometry("800x500")  # to resize the main window
center_window(root)  # calling the center_window function to center the main window
root.configure(bg="#d0f0c0")  # setting the background color

# Set the font
header_font = ("Helvetica", 36, "bold")
slogan_font = ("Helvetica", 24)
button_font = ("Helvetica", 18)

# Create header label
header_label = tk.Label(
    root, text="SmartPlate", font=header_font, bg="#d0f0c0", fg="black"
)
header_label.pack(pady=30)

# Create slogan label
slogan_label = tk.Label(
    root, text="Optimize your meals!", font=slogan_font, bg="#d0f0c0", fg="black"
)
slogan_label.pack(pady=15)

# Load and resize the logo image
logo_image = Image.open("assets/logo2.png")
logo_image = logo_image.resize((200, 200), Image.ANTIALIAS)
logo_photo = ImageTk.PhotoImage(logo_image)

# Create logo label
logo_label = tk.Label(root, image=logo_photo, bg="#d0f0c0")
logo_label.pack(pady=10)

# Create start button
start_button = tk.Button(
    root,
    text="Start",
    font=button_font,
    bg="#9ab973",
    fg="black",
    command=open_calorie_page,
)
start_button.pack(pady=15)

root.protocol("WM_DELETE_WINDOW", _quit)

# Run the GUI
root.mainloop()

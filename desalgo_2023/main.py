import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import meal_query
import nutriscore
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


def cancel_optimization():
    global optimize_page
    meals.clear()
    optimize_page.destroy()
    open_meal_page()


def open_meal_page():
    root.withdraw()
    meals.clear()
    meal_page = tk.Toplevel(root)
    meal_page.title("Meal Selection")
    meal_page.configure(bg="#d0f0c0")
    meal_page.geometry("800x500")
    center_window(meal_page)
    guide_page = None

    meal_frame = tk.Frame(meal_page, bg="#d0f0c0")
    meal_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    def back_to_calorie_page():
        meal_page.destroy()
        open_calorie_page()

    def add_meal(event=None):
        query = query_entry.get()
        result = meal_query.search_meal(query, meals)
        meals[query]["nutriscore"] = nutriscore.calculate(meals[query])

        if result is None:
            messagebox.showerror("ERROR", "Please enter a valid meal.")
            return

        meal_treeview.insert(
            "",
            tk.END,
            values=(query, meals[query]["nutriscore"], meals[query]["calories"]),
        )
        query_entry.delete(0, tk.END)

    def delete_meal():
        selected_item = meal_treeview.focus()
        meals.pop(meal_treeview.item(selected_item)["values"][0])
        if selected_item:
            meal_treeview.delete(selected_item)

    def open_nutriscore_guide():
        guide_page = tk.Toplevel(meal_page)
        guide_page.title("Nutriscore Guide")
        guide_page.configure(bg="#d0f0c0")
        guide_page.geometry("600x400")
        center_window(guide_page)

        nutriscore_values = [
            ("A", "Points Solid Food: -15 to 1, Points Beverages: Water", "#9ab973"),
            ("B", "Points Solid Food: 0-2, Points Beverages: <= 1 ", "#c2d99d"),
            ("C", "Points Solid Food: 3-10, Points Beverages: 2-5", "#eedc82"),
            ("D", "Points Solid Food: 11-18, Points Beverages: 6-9", "#f7af72"),
            ("E", "Points Solid Food: 19-40, Points Beverages: 10-40", "#f15f5f"),
        ]

        def create_nutriscore_label(frame, text, tooltip, color):
            label_frame = tk.Frame(frame, bg=color, bd=1, relief="solid")
            label_frame.pack(pady=5, padx=5, fill=tk.X)
            label = tk.Label(label_frame, text=text, font=("Helvetica", 12), bg=color)
            label.pack(side=tk.LEFT, padx=5, pady=5)
            label.bind("<Enter>", lambda event: tooltip_label.config(text=tooltip))
            label.bind("<Leave>", lambda event: tooltip_label.config(text=""))

        for value, tooltip, color in nutriscore_values:
            create_nutriscore_label(guide_page, f"Nutriscore: {value}", tooltip, color)

        tooltip_label = tk.Label(
            guide_page, text="", font=("Helvetica", 12), bg="#d0f0c0"
        )
        tooltip_label.pack(pady=5)

    query_label = tk.Label(
        meal_frame,
        text="Meal Name:",
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

    help_button = tk.Button(
        meal_frame,
        text="Help",
        font=("Helvetica", 14),
        bg="#9ab973",
        fg="black",
        command=open_nutriscore_guide,
    )
    help_button.pack(side=tk.RIGHT, pady=10, padx=5)

    back_button = tk.Button(
        meal_frame,
        text="Back",
        font=("Helvetica", 14),
        bg="#9ab973",
        fg="black",
        command=back_to_calorie_page,
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

            knapsack_result = fractional_knapsack.calculate(
                int(calorie_limit), meals, selected_option_value
            )

            # open result page after 2s
            optimize_page.after(2000, open_result_page)

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
            command=cancel_optimization,
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
        nutriscore_value = nutriscore.nutriscore_conversion(
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
                nutriscore_value,
                protein,
                carbohydrates,
                calorie,
                sugar,
                cholesterol,
            )
        )

    # insertion of data into Treeview
    for data in result_data:
        result_table.insert("", tk.END, values=data)
    result_data.clear()

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
        meals.clear()
        result_data.clear()
        open_meal_page()

    recommendation = ""
    if knapsack_result[2] is None or int(knapsack_result[1]) >= int(
        meals[knapsack_result[2]]["grams"]
    ):
        recommendation = "Happy Eating!"
    else:
        recommendation = f"Tip: You can reduce the weight of {knapsack_result[2]} by {knapsack_result[1]: .2f} grams if you want to include it"
    # Create a label for the note/recommendation section
    note_label = tk.Label(
        result_page,
        text=recommendation,
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
    meals.clear()
    calorie_page = tk.Toplevel(root)
    calorie_page.title("Calorie Limit")
    calorie_page.configure(bg="#d0f0c0")
    calorie_page.geometry("800x500")
    center_window(calorie_page)

    selected_option = tk.StringVar()  # To store the selected radiobutton value

    def calculate_meal_plan():
        global calorie_limit
        global selected_option_value
        calorie_limit = calorie_entry.get()
        selected_option_value = selected_option.get()

        if not calorie_limit.isdigit():
            messagebox.showerror("Error", "Please enter a valid calorie limit.")
        elif not selected_option_value:
            messagebox.showerror("Error", "Please select one option to optimize.")
        else:
            calorie_page.destroy()
            open_meal_page()

    calorie_label = tk.Label(
        calorie_page,
        text="Enter Calorie Limit:",
        font=("Helvetica", 18, "bold"),
        bg="#d0f0c0",
        fg="black",
    )
    calorie_label.pack(pady=10)

    calorie_entry = tk.Entry(calorie_page, font=("Helvetica", 16))
    calorie_entry.pack(pady=5)

    options_label = tk.Label(
        calorie_page,
        text="Choose the values you wish to optimize:",
        font=("Helvetica", 18, "bold"),
        bg="#d0f0c0",
        fg="black",
    )
    options_label.pack(pady=10, anchor="w")

    nutriscore_radiobutton = tk.Radiobutton(
        calorie_page,
        text="Nutriscore",
        variable=selected_option,
        value="nutriscore",
        font=("Helvetica", 12),
        bg="#d0f0c0",
        fg="black",
        anchor="w",
    )
    nutriscore_radiobutton.pack(pady=5, anchor="w")

    sugar_radiobutton = tk.Radiobutton(
        calorie_page,
        text="Sugar",
        variable=selected_option,
        value="sugar",
        font=("Helvetica", 12),
        bg="#d0f0c0",
        fg="black",
        anchor="w",
    )
    sugar_radiobutton.pack(pady=5, anchor="w")

    calculate_button = tk.Button(
        calorie_page,
        text="Proceed",
        font=("Helvetica", 18),
        bg="#9ab973",
        fg="black",
        command=calculate_meal_plan,
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
    root,
    text="Wholesome bites, made smarter!",
    font=slogan_font,
    bg="#d0f0c0",
    fg="black",
)
slogan_label.pack(pady=15)

# Load and resize the logo image
logo_image = Image.open("logo2.png")
logo_image = logo_image.resize((200, 200), Image.ANTIALIAS)
logo_photo = ImageTk.PhotoImage(logo_image)
root.iconbitmap("logo2.ico")

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

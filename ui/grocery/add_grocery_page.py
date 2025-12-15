import customtkinter as ctk # IMPORTS CUSTOMTKINTER
from PIL import Image # IMPORTS PIL FOR SUPPORTING IMAGES
from tkinter import messagebox as mb # IMPORTS MESSAGEBOX
from database.grocery_query import addGrocery, getCategoryForSearch # IMPORTS NECESSARY QUERIES

def open_add_grocery_page(parent, user_id, current_frame=None):

    current_frame.grid_forget() if current_frame else None

    # Grocery Frame
    grocery_frame = ctk.CTkFrame(parent, fg_color="#f0f0f0")
    grocery_frame.grid_columnconfigure(0, weight=1)
    grocery_frame.grid_columnconfigure(1, weight=1)
    grocery_frame.grid_rowconfigure(0, weight=0)
    grocery_frame.grid_rowconfigure(1, weight=1)

    # Banner at the top with title and navigation buttons
    banner = ctk.CTkFrame(grocery_frame, fg_color="#ead729", height=100)
    banner.grid(row=0, column=0, columnspan=2, sticky="nsew")
    banner.grid_columnconfigure(0, weight=2)
    banner.grid_columnconfigure(1, weight=0)

    banner_title = ctk.CTkFrame(banner, fg_color="transparent", height=100)
    banner_title.grid(row=0, column=0, sticky="nsew")

    # Title in the center of the banner
    title = ctk.CTkLabel(
        banner_title,
        text="EatSmart",
        font=("Arial Black", 32),
        text_color="#505ab7",
        fg_color="#ead729"
    )
    title.place(relx=0.5, rely=0.5, anchor="center")

    # Navigation bar on the right side of the banner
    navigation_bar = ctk.CTkFrame(banner, fg_color="transparent", height=40)
    navigation_bar.grid(row=0, column=1, sticky="e")

    btn_kwargs = dict(font=("Arial Black", 16), text_color="white", height=100, width=150, corner_radius=2)

    # Load cart icon for grocery list button
    try:
        cart_image = Image.open("assets/cart_icon.png")
        cart_icon = ctk.CTkImage(light_image=cart_image, size=(50, 40))
        grocerylist = ctk.CTkButton(
            navigation_bar,
            text="Grocery List",
            image=cart_icon,
            compound="top",
            fg_color="#2334d5",
            **btn_kwargs,
            command=parent.show_grocery
        )
    except Exception:
        grocerylist = ctk.CTkButton(
            navigation_bar,
            text="Grocery List",
            fg_color="#2334d5",
            **btn_kwargs,
            command=parent.show_grocery
        )
    grocerylist.grid(row=0, column=0)

    # Load meal icon for meal plan button
    try:
        meal_image = Image.open("assets/meal_icon.png")
        meal_icon = ctk.CTkImage(light_image=meal_image, size=(50, 40))
        mealplan_navbar = ctk.CTkButton(
            navigation_bar,
            text="Meal Plan",
            image=meal_icon,
            compound="top",
            fg_color="#3743b5",
            command=parent.show_mealplan,
            **btn_kwargs
        )
    except Exception:
        mealplan_navbar = ctk.CTkButton(
        navigation_bar,
        text="Meal Plan",
        fg_color="#3743b5",
        command=parent.show_mealplan,
        **btn_kwargs
    )
    mealplan_navbar.grid(row=0, column=1)

    # Load settings icon for settings button
    try:
        settings_image = Image.open("assets/settings_icon.png")
        settings_icon = ctk.CTkImage(light_image=settings_image, size=(50, 40))
        settings_navbar = ctk.CTkButton(
            navigation_bar,
            text="Settings",
            image=settings_icon,
            compound="top",
            fg_color="#505ab7",
            **btn_kwargs,
            command=parent.show_settings
        )
    except Exception:
        settings_navbar = ctk.CTkButton(
            navigation_bar,
            text="Settings",
            fg_color="#505ab7",
            **btn_kwargs,
            command=parent.show_settings
    )
    settings_navbar.grid(row=0, column=2)

    # DISPLAY AREA FRAME
    display_area = ctk.CTkFrame(grocery_frame, fg_color="white")
    display_area.grid(row=1, column=0, columnspan=2, sticky="nsew")
    display_area.grid_columnconfigure(0, weight=1)
    display_area.grid_columnconfigure(0, weight=1)

    # ADD GROCERY LABEL
    add_grocery_label = ctk.CTkLabel(
        display_area,
        text="Add Grocery Item",
        font=("Arial Black", 18),
        fg_color="#ead729",
        text_color="#505ab7",
        width=220,
        height=45,
        corner_radius=12
    )
    add_grocery_label.grid(row=0, column=0, columnspan=2, pady=8)

    # FUNCTION FOR ADDING GROCERY INTO THE DATABASE
    def add_grocery(user_id, category_var, categories):

        import re # IMPORTS RE FOR NECESSARY FORMAT
        KG_CATEGORIES = {"Fruits", "Vegetables", "Meat", "Fisheries"} # SPECIFIED CATEGORIES FOR USING KILOGRAMS (e.g '10kg', '0.5kg')
        PIECE_CATEGORIES = {"Canned Goods", "Pastries", "Condiments", "Dairy"} # SPECIFIC CATEGORIES FOR USING PIECES (e.g '3x', '10x')
        LITER_CATEGORIES = {"Beverages"}

        grocery = grocery_entry.get().strip() # GETS THE GROCERY VALUE
        quantity = quantity_entry.get().strip() # GETS THE QUANTITY VALUE
        date = date_entry.get().strip() # GETS THE DATE VALUE
        category_name = category_var.get() # GETS THE CATEGORY VALUE

        if not grocery or not quantity or category_name == "Enter the Category:" or category_name == "": # CONDITION IF CATEGORY IS NOT FILLED UP
            mb.showerror("Add Grocery Error!", "Please fill all fields correctly!")
            return
        
        if category_name in KG_CATEGORIES: # CONDITION IF CATEGORY IS IN KILOGRAM
            if not re.match(r'^\d+(\.\d+)?kg$', quantity): # CHECKS IF THE QUANTITY IS KILOGRAM UNIT
                mb.showerror(
                    "Quantity Error",
                    "For this category, quantity must be in kilograms (e.g. 1kg, 0.5kg, 2.25kg)."
                )
                return
        
        elif category_name in LITER_CATEGORIES: # CONDITION IF CATEGORY IS IN LITERS
            if not re.match(r'^\d+(\.\d+)?L$', quantity): # CHECKS IF THE QUANTITY IS IN LITERS UNIT
                mb.showerror("Quantity Error", "For this category, quantity must be in liters (e.g. 1l, 0.5l, 2.5l).")
                return
            
        elif category_name in PIECE_CATEGORIES: # CONDITION IF CATEGORY IS IN PIECES
            if not re.match(r'^\d+x$', quantity): # CHECKS IF THE QUANTITY IS IN PIECES UNIT
                mb.showerror("Quantity Error", "For this category, quantity must be in pieces (e.g. 1x, 2x, 5x).")
                return

        else: # CONDITION FOR INVALID SELECTION
            mb.showerror("Category Error", "Invalid category selected")

        category_id = categories[category_name] # GETS THE ID OF THE CATEGORY SELECTED
        addGrocery(user_id, grocery, quantity, category_id, date) # ADDS THE GROCERY ITEM INTO THE GROCERY TABLE

    # GROCERY ENTRY
    grocery_entry = ctk.CTkEntry(
        display_area,
        placeholder_text="Enter the grocery:",
        font=("Arial Black", 14),
        height=60,
        width=370,
        corner_radius=12
    )
    grocery_entry.grid(row=1, column=0, columnspan=2, pady=5)

    # QUANTITY ENTRY
    quantity_entry = ctk.CTkEntry(
        display_area,
        placeholder_text="Enter the quantity:",
        font=("Arial Black", 14),
        height=60,
        width=370,
        corner_radius=12
    )
    quantity_entry.grid(row=2, column=0, columnspan=2, pady=5)

    # DATE ENTRY
    date_entry = ctk.CTkEntry(
        display_area,
        placeholder_text="Enter the Expiration Date (YYYY-MM-DD):",
        font=("Arial Black", 14),
        height=60,
        width=370,
        corner_radius=12
    )
    date_entry.grid(row=3, column=0, columnspan=2, pady=5)

    rows = getCategoryForSearch(user_id) # GETS ALL THE CATEGORIES FROM THE CATEGORY TABLE

    category_map = {name: cid for cid, name in rows} # Creates dictionary from the rows
    category_names = list(category_map.keys())       # Converts dictionary into list

    category_variable = ctk.StringVar() # FOR GETTING THE CATEGORY
    # CATEGORY SELECTOR
    category_field_selector = ctk.CTkOptionMenu(
        display_area,
        values=category_names, variable=category_variable,
        height=60,
        width=370,
        corner_radius=12,
        font=("Arial Black", 14),
        text_color="white",
        fg_color="#505ab7",
        button_color="#505ab7",
        button_hover_color="#3743b5",
        dropdown_font=("Arial Black", 12),
        dropdown_fg_color="#505ab7",
        dropdown_text_color="white",
        dropdown_hover_color="#3743b5"
    )
    category_field_selector.set("Enter the Category:")
    category_field_selector.grid(row=4, column=0, columnspan=2, pady=5)

    # SAVE GROCERY BUTTON
    save_grocery_button = ctk.CTkButton(
        display_area,
        text="Save Grocery Item",
        font=("Arial Black", 20),
        fg_color="#5FCC49",
        text_color="white",
        width=200,
        height=60,
        corner_radius=12,
        hover_color="#97E769",
        command=lambda: add_grocery(user_id, category_variable, category_map) # CALLS THE FUNCTION FOR QUERY
    )
    save_grocery_button.grid(row=5, column=0, columnspan=2, pady=10)

    # CANCEL BUTTON
    cancel_button = ctk.CTkButton(
        display_area,
        text="Cancel",
        font=("Arial Black", 20),
        fg_color="#5F5E5E",
        text_color="white",
        width=200,
        height=60,
        corner_radius=12,
        hover_color="#807E7E",
        command=parent.show_grocery # RETURNS TO GROCERY PAGE
    )
    cancel_button.grid(row=5, column=1, padx=40, pady=10)

    # FOOTER FRAME
    footer_frame = ctk.CTkFrame(display_area, fg_color="white")
    footer_frame.grid(row=6, column=0, columnspan=2, pady=5)
    footer_frame.grid_rowconfigure(0, weight=1)
    footer_frame.grid_rowconfigure(1, weight=1)

    # FOOTER CONTENT
    footer_content = ctk.CTkLabel(
        footer_frame,
        text="EatSmart - Reduce Waste, Eat Wise",
        font=("Arial", 14),
        text_color="#505ab7"
    )
    footer_content.grid(row=0, column=0, columnspan=2, pady=5)

    # FOOTER RESERVED
    footer_label = ctk.CTkLabel(
        footer_frame,
        text="© 2025 EatSmart. All rights reserved.",
        font=("Arial", 10),
        text_color="#888888",
    )
    footer_label.grid(row=1, column=0, columnspan=2, pady=5)


    return grocery_frame


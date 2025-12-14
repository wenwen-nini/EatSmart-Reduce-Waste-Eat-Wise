import customtkinter as ctk     # IMPORT CUSTOMTKINTER
from PIL import Image           # IMPORT PIL FOR SUPPORTING IMAGE
from tkinter import messagebox as mb    # IMPORT MESSAGEBOX
from database.grocery_query import getGroceryAll, getCategoryForSearch   # IMPORTS NECESSARY QUERIES

def open_grocery_page(parent, user_id, current_frame=None):

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
        text="EatSmart\nGrocery List",
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
        )
    except Exception:
        grocerylist = ctk.CTkButton(
            navigation_bar,
            text="Grocery List",
            fg_color="#2334d5",
            **btn_kwargs,
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

    # Frame for display
    display_area = ctk.CTkFrame(grocery_frame, fg_color="#f0f0f0")
    display_area.grid(row=1, column=0, columnspan=2, sticky="nsew")
    display_area.grid_columnconfigure(0, weight=1)
    display_area.grid_rowconfigure(0, weight=0)
    display_area.grid_rowconfigure(1, weight=1)
    display_area.grid_rowconfigure(2, weight=0)
    display_area.grid_rowconfigure(3, weight=0)
    
    # Search Area Frame
    search_frame = ctk.CTkFrame(display_area, fg_color="#f0f0f0", height=100)
    search_frame.grid(row=0, column=0, sticky="nsew")
    search_frame.grid_columnconfigure(0, weight=0)
    search_frame.grid_columnconfigure(1, weight=1)
    search_frame.grid_rowconfigure(0, weight=0)

    # Search Entry
    search_item_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="Search Item:",
        height=40,
        width=250,
        corner_radius=8,
        font=("Arial Black", 16),
        fg_color="transparent",
        border_width=2,
        border_color="#57595a"
    )
    search_item_entry.grid(row=0, column=0, padx=(20,10), pady=20, sticky="w")

    # Main Display Frame
    display_grocery_frame = ctk.CTkScrollableFrame(display_area, fg_color="#505ab7", corner_radius=12)
    display_grocery_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    current_category_id = None # Default (All Categories are present)

    # Function for live searching
    def refresh_grocery_view():
        search_text = search_item_entry.get().strip()
        load_grocery_items(
            parent,
            display_grocery_frame,
            user_id,
            category_id=current_category_id,
            search_text=search_text,
        )
    # Mainly purpose is for live searching
    search_item_entry.bind("<KeyRelease>", lambda _event: refresh_grocery_view())

    rows = getCategoryForSearch(user_id) # Gets the categories' name from category table

    category_map = {name: cid for cid, name in rows}    # Creates dictionary from the rows
    category_names = list(category_map.keys())          # Converts dictionary into list

    # Function for searching by categories
    def on_category_select(choice):
        nonlocal current_category_id
        if choice == "All":
            current_category_id = None
        else:
            current_category_id = category_map.get(choice)
        refresh_grocery_view()

    # Search by Category Selector
    search_field_selector = ctk.CTkOptionMenu(
        search_frame,
        values=["All"] + category_names,
        height=40,
        width=150,
        corner_radius=8,
        font=("Arial Black", 16),
        text_color="white",
        fg_color="#505ab7",
        button_color="#505ab7",
        button_hover_color="#3743b5",
        dropdown_font=("Arial Black", 12),
        dropdown_fg_color="#505ab7",
        dropdown_text_color="white",
        dropdown_hover_color="#3743b5",
        command=on_category_select
    )
    search_field_selector.set("Search By")
    search_field_selector.grid(row=0, column=1, padx=(10,20), pady=20, sticky="w")

    load_grocery_items(parent, display_grocery_frame, user_id) # Calls the function for getting the data from grocery table

    # Add Grocery Button
    add_grocery_button = ctk.CTkButton(
        display_area,
        text="Add Grocery Item",
        font=("Arial Black", 20),
        fg_color="#ead729",
        text_color="#505ab7",
        width=200,
        height=50,
        corner_radius=15,
        hover_color="#e9dd71",
        command=parent.show_add_grocery_page
    )
    add_grocery_button.grid(row=2, column=0, padx=20, pady=(0,20), sticky="w")

    # Footer Frame
    footer_frame = ctk.CTkFrame(display_area, fg_color="#f0f0f0")
    footer_frame.grid(row=3, column=0, columnspan=2, pady=10)
    footer_frame.grid_rowconfigure(0, weight=1)
    footer_frame.grid_rowconfigure(1, weight=1)

    # Footer Content
    footer_content = ctk.CTkLabel(
        footer_frame,
        text="EatSmart - Reduce Waste, Eat Wise",
        font=("Arial", 14),
        text_color="#505ab7"
    )
    footer_content.grid(row=0, column=0, columnspan=2, pady=5)

    # Footer Reserved
    footer_label = ctk.CTkLabel(
        footer_frame,
        text="© 2025 EatSmart. All rights reserved.",
        font=("Arial", 10),
        text_color="#888888",
        fg_color="#f0f0f0"
    )
    footer_label.grid(row=1, column=0, columnspan=2, pady=5)

    return grocery_frame # Returns the frame so this frame could be shown

def load_grocery_items(parent, display_grocery_frame, user_id, category_id=None, search_text=""):
    # Clear previous items
    for widget in display_grocery_frame.winfo_children():
        widget.destroy()

    headers = ["Edit", "Delete", "Item Name", "Quantity", "Category", "Expiry Date", "Days Left"]

    groceries = getGroceryAll(user_id, category_id, search_text) # Gets all data from grocery table

    # Display table headers
    for col, header in enumerate(headers):
        ctk.CTkLabel(
            display_grocery_frame, 
            text=header, 
            font=("Arial Black", 16),
            text_color="white", 
            fg_color="transparent"
        ).grid(row=0, column=col, padx=21, pady=5, sticky="w")

    # Formatting days left based on the number
    def format_days_left(value):
        if value is None:
            return "No date", "white"
        if value < 0:
            return f"Expired {abs(value)}d", "#ff4d4d"
        if value == 0:
            return "Expires today", "#f2c94c"
        if value == 1:
            return "1 day left", "#f2c94c"
        if value <= 3:
            return f"{value} days left", "#f2c94c"
        return f"{value} days left", "white"

    # Display grocery rows
    for row_index, item in enumerate(groceries, start=1): # Loops so that all groceries have their own edit and delete button per row
        ctk.CTkButton(
            display_grocery_frame, 
            text="Edit", 
            font=("Arial Black", 14),
            fg_color="#ead729", 
            text_color="#505ab7", 
            width=75, 
            height=35, 
            corner_radius=8,
            hover_color="#e9dd71", 
            command=lambda i=item: parent.show_edit_grocery_page(i)
        ).grid(row=row_index, column=0, padx=1, pady=3)

        ctk.CTkButton(
            display_grocery_frame, 
            text="Delete", 
            font=("Arial Black", 12),
            fg_color="#ff4d4d", 
            text_color="white", 
            width=75, 
            height=35, 
            corner_radius=8,
            hover_color="#ff1a1a", 
            command=lambda i=item: parent.show_delete_grocery_page(i)
        ).grid(row=row_index, column=1, padx=1, pady=3)

        _, name, quantity, category_name, expiration_date, days_left = item # Unpacks the database row and initialized variables
        for col, value in enumerate((name, quantity, category_name, expiration_date, days_left)): # Loop through each column value
            display_value = value
            text_color = "white"
            if col == 4:  # Days left column
                display_value, text_color = format_days_left(value) # Calls the format function
            
            # Displays the data from the display_value
            ctk.CTkLabel(
                display_grocery_frame, 
                text=str(display_value), 
                font=("Arial Black", 14),
                text_color=text_color, 
                fg_color="#505ab7"
            ).grid(row=row_index, column=col+2, pady=3) # Column starts at 2 because column 0 & column 1 are for edit and delete buttons







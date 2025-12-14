from typing import Any, Dict # IMPORTS TYPE HINTS FOR ANNOTATE VARIABLES 
import customtkinter as ctk # IMPORTS CUSTOMTKINTER
from PIL import Image # IMPORTS PIL FOR SUPPORTING IMAGES
from tkinter import messagebox as mb # IMPORTS MESSAGEBOX
from database.meal_query import addMeal, getIngredients # IMPORTS THE NECESSARY QUERIES

def open_add_meal_page(parent, user_id, current_frame=None):
    current_frame.grid_forget() if current_frame else None

    meal_frame = ctk.CTkFrame(parent, fg_color="#f0f0f0")
    meal_frame.grid_columnconfigure(0, weight=1)
    meal_frame.grid_columnconfigure(1, weight=1)
    meal_frame.grid_rowconfigure(0, weight=0)
    meal_frame.grid_rowconfigure(1, weight=1)

    # Banner at the top with title and navigation buttons
    banner = ctk.CTkFrame(meal_frame, fg_color="#ead729", height=100)
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

    btn_kwargs: Dict[str, Any] = dict(
        font=("Arial Black", 16),
        text_color="white",
        height=100,
        width=150,
        corner_radius=2,
    )

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
    display_area = ctk.CTkFrame(meal_frame, fg_color="white")
    display_area.grid(row=1, column=0, columnspan=2, sticky="nsew")
    display_area.grid_columnconfigure(0, weight=1)
    display_area.grid_columnconfigure(0, weight=1)

    # ADD MEAL LABEL
    add_meal_label = ctk.CTkLabel(
        display_area,
        text="Add Meal",
        font=("Arial Black", 18),
        fg_color="#ead729",
        text_color="#505ab7",
        width=220,
        height=45,
        corner_radius=12
    )
    add_meal_label.grid(row=0, column=0, columnspan=2, pady=8)

    # MEAL ENTRY
    meal_entry = ctk.CTkEntry(
        display_area,
        placeholder_text="Enter the meal: ",
        font=("Arial Black", 14),
        height=60,
        width=370,
        corner_radius=12
    )
    meal_entry.grid(row=1, column=0, columnspan=2, pady=5)

    # DAY SELECTOR
    day_selector = ctk.CTkOptionMenu(
        display_area,
        values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        height=60,
        width=370,
        corner_radius=12,
        font=("Arial Black", 14),
        text_color="white",
        fg_color="#505ab7",
        button_color="#505ab7",
        button_hover_color="#3743b5",
        dropdown_font=("Arial", 12),
        dropdown_fg_color="#505ab7",
        dropdown_text_color="white",
        dropdown_hover_color="#3743b5"
    )
    day_selector.set("Enter which day:")
    day_selector.grid(row=2, column=0, columnspan=2, pady=5)

    # TIME SELECTOR
    time_selector = ctk.CTkOptionMenu(
        display_area,
        values=["Breakfast", "Lunch", "Dinner"],
        height=60,
        width=370,
        corner_radius=12,
        font=("Arial Black", 14),
        text_color="white",
        fg_color="#505ab7",
        button_color="#505ab7",
        button_hover_color="#3743b5",
        dropdown_font=("Arial", 12),
        dropdown_fg_color="#505ab7",
        dropdown_text_color="white",
        dropdown_hover_color="#3743b5"
    )
    time_selector.set("Enter which mealtime:")
    time_selector.grid(row=3, column=0, columnspan=2, pady=5)

    ingredients = getIngredients(user_id) # GETS THE INGREDIENTS (GROCERIES) FROM THE GROCERY TABLE

    # PREPARING THE VALUES FOR INGREDIENT SELECTOR
    if not isinstance(ingredients, (list, tuple)): 
        ingredients = []
    ingredients_map = {}
    ingredient_values = []

    for ing in ingredients:
        groceryID, name, quantity = ing
        display_text = f"{name} (Qty: {quantity})"
        ingredient_values.append(display_text)
        ingredients_map[display_text] = ing

    has_ingredients = bool(ingredient_values) 
    option_values = ingredient_values if has_ingredients else ["No groceries available"] # CHECKS IF THERE'S ATLEAST AN INGREDIENT

    # INGREDIENT SELECTOR
    ingredient_selector = ctk.CTkOptionMenu(
        display_area,
        values=option_values,
        height=60,
        width=370,
        corner_radius=12,
        font=("Arial Black", 14),
        text_color="white",
        fg_color="#505ab7",
        button_color="#505ab7",
        button_hover_color="#3743b5",
        dropdown_font=("Arial", 12),
        dropdown_fg_color="#505ab7",
        dropdown_text_color="white",
        dropdown_hover_color="#3743b5"
    )
    ingredient_selector.set("Ingredient Selector:" if has_ingredients else "No groceries available") # CHECKS IF THERE'S ATLEAST AN INGREDIENT
    if not has_ingredients:
        ingredient_selector.configure(state="disabled") # DISABLED IF THERE'S NO INGREDIENT
    ingredient_selector.grid(row=4, column=0, columnspan=2, pady=5)

    # FOR NONE GROCERY ITEM
    info_row = 5
    if not has_ingredients:
        ctk.CTkLabel(
            display_area,
            text="Add grocery items first if you want to attach ingredients.",
            font=("Arial", 12),
            text_color="#505ab7"
        ).grid(row=info_row, column=0, columnspan=2, pady=(0, 5))

    button_row = info_row + 1 if not has_ingredients else info_row

    # FUNCTION FOR SAVE MEAL
    def save_meal():
        meal_name = meal_entry.get().strip() # GETS THE MEAL ENTRY INPUT
        day_of_week = day_selector.get() # GETS THE DAY INPUT
        mealtime = time_selector.get() # GETS THE MEALTIME INPUT
        ingredient_text = ingredient_selector.get() # GETS THE INGREDIENT INPUT

        # Basic validation
        if not meal_name:   # IF NO MEAL NAME
            mb.showerror("Error", "Please enter a meal name.")
            return
        if day_of_week not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]: # IF NONE OF THE ABOVE IS INPUT
            mb.showerror("Error", "Please select a valid day.")
            return
        if mealtime not in ["Breakfast", "Lunch", "Dinner"]: # IF NONE OF THE ABOVE IS INPUT
            mb.showerror("Error", "Please select a valid mealtime.")
            return

        # PREPARE SELECTED INGREDIENT FOR INSERTION
        selected_ingredients = []
        if ingredient_text and ingredient_text in ingredients_map:
            groceryID, name, quantity = ingredients_map[ingredient_text]
            
            try:
                quantity_needed = int(quantity)  # CONVERTS VARCHAR INTO INT
            except ValueError:
                quantity_needed = 1  # FALLBACK IF CONVERSION FAILS
            
            selected_ingredients.append((groceryID, name, quantity_needed))

        # CALLS THE EXISTING ADD MEAL FUNCTION
        success = addMeal(user_id, meal_name, day_of_week, mealtime, selected_ingredients)
        if success:
            parent.show_mealplan()  # RETURNS TO MEALPLAN PAGE
        else:
            mb.showerror("Error", "Failed to add meal. Check your inputs.") # MESSAGE FOR INPUT VALIDATION

    # SAVE MEAL BUTTON
    save_meal_button = ctk.CTkButton(
        display_area,
        text="Save Meal",
        font=("Arial Black", 20),
        fg_color="#5FCC49",
        text_color="white",
        width=200,
        height=60,
        corner_radius=12,
        hover_color="#97E769",
        command=lambda: save_meal()
    )
    save_meal_button.grid(row=button_row, column=0, padx=(180, 0), pady=10, sticky="w")

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
        command=parent.show_mealplan # RETURNS TO MEALPLAN PAGE
    )
    cancel_button.grid(row=button_row, column=1, padx=(0, 180), pady=10, sticky="e")

    # FOOTER FRAME
    footer_frame = ctk.CTkFrame(display_area, fg_color="white")
    footer_frame.grid(row=button_row + 1, column=0, columnspan=2, pady=5)
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

    return meal_frame
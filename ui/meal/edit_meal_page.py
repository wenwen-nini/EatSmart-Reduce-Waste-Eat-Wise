import customtkinter as ctk # IMPORTS CUSTOMTKINTER
from PIL import Image # IMPORTS PIL FOR SUPPORTING IMAGES
from tkinter import messagebox as mb # IMPORTS MESSAGEBOX
from database.meal_query import getDays, getMealTime, updateMealPlan # IMPORTS NECESSARY QUERIES

def open_edit_meal_page(parent, meals, user_id, current_frame=None):
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
    display_area = ctk.CTkFrame(meal_frame, fg_color="white")
    display_area.grid(row=1, column=0, columnspan=2, sticky="nsew")
    display_area.grid_columnconfigure(0, weight=1)
    display_area.grid_columnconfigure(1, weight=1)
    display_area.grid_rowconfigure(1, weight=1)

    # EDIT MEAL LABEL
    edit_meal_label = ctk.CTkLabel(
        display_area,
        text="Edit Meal Plan",
        font=("Arial Black", 20),
        fg_color="#ead729",
        text_color="#505ab7",
        width=250,
        height=50,
        corner_radius=12
    )
    edit_meal_label.grid(row=0, column=0, columnspan=2, padx=(5,0), pady=20)

    # FUNCTION FOR EDITING MEAL
    def edit_mealplan(user_id, plan_id, meal_id, day, time):
        
        mealName = meal_entry.get().strip() # GETS THE MEAL NAME

        updateMealPlan(user_id, plan_id, meal_id, mealName, day, time) # CALLS THE QUERY FOR UPDATING MEALPLAN ON SPECIFIC DAY AND MEALTIME

    # MEAL DISPLAY FRAME
    meal_display_frame = ctk.CTkFrame(display_area, fg_color="#505ab7", corner_radius=12, height=400, width=300)
    meal_display_frame.grid(row=1, column=0, columnspan=2, sticky="", padx=50, pady=3)
    meal_display_frame.grid_rowconfigure(0, weight=1)
    meal_display_frame.grid_rowconfigure(1, weight=1)
    meal_display_frame.grid_rowconfigure(2, weight=1)
    meal_display_frame.grid_columnconfigure(0, weight=1)

    # MEAL NAME LABEL
    meal_label = ctk.CTkLabel(
        meal_display_frame,
        text=f"Meal Name: {meals[4]}",
        font=("Arial Black", 16),
        fg_color="transparent",
        text_color="#ead729"
    )
    meal_label.grid(row=0, padx=15, pady=10, sticky='w')

    # DAY LABEL
    day_label = ctk.CTkLabel(
        meal_display_frame,
        text=f"Day: {meals[2]}",
        font=("Arial Black", 16),
        fg_color="transparent",
        text_color="#ead729"
    )
    day_label.grid(row=1, padx=15, pady=10, sticky='w')

    # TIME LABEL
    time_label = ctk.CTkLabel(
        meal_display_frame,
        text=f"Time: {meals[3]}",
        font=("Arial Black", 16),
        fg_color="transparent",
        text_color="#ead729",
    )
    time_label.grid(row=2, padx=15, pady=10, sticky='w')

    # MEAL ENTRY
    meal_entry = ctk.CTkEntry(
        display_area,
        placeholder_text="Enter the meal name: ",
        font=("Arial Black", 14),
        height=50,
        width=350,
        corner_radius=12
    )
    meal_entry.grid(row=2, column=0, columnspan=3, padx=20, pady=10)

    # SAVE MEAL BUTTON
    save_meal_button = ctk.CTkButton(
        display_area,
        text="Save Meal Plan",
        font=("Arial Black", 20),
        fg_color="#5FCC49",
        text_color="white",
        width=300,
        height=60,
        corner_radius=12,
        hover_color="#95E769",
        command=lambda: edit_mealplan(user_id, meals[0], meals[1], meals[2], meals[3]) # CALLS THE FUNCTION FOR THE QUERY
    )
    save_meal_button.grid(row=4, column=0, padx=30, pady=30)

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
    cancel_button.grid(row=4, column=1, columnspan=2, padx=(0, 120), pady=30, sticky='e')

    # FOOTER FRAME
    footer_frame = ctk.CTkFrame(display_area, fg_color="white")
    footer_frame.grid(row=5, column=0, columnspan=3)
    footer_frame.grid_rowconfigure(0, weight=1)
    footer_frame.grid_rowconfigure(1, weight=1)

    # FOOTER CONTENT
    footer_content = ctk.CTkLabel(
        footer_frame,
        text="EatSmart - Reduce Waste, Eat Wise",
        font=("Arial", 14),
        text_color="#505ab7"
    )
    footer_content.grid(row=0, column=0, columnspan=3, pady=(0,3))

    # FOOTER RESERVED
    footer_label = ctk.CTkLabel(
        footer_frame,
        text="© 2025 EatSmart. All rights reserved.",
        font=("Arial", 10),
        text_color="#888888",
    )
    footer_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))

    return meal_frame





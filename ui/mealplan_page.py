from typing import Any, Dict        # IMPORTS TYPE HINTS FOR ANNOTATE VARIABLES 
from collections import Counter     # FOR COUNTING MEAL STATUSES

import customtkinter as ctk         # IMPORTS THE CUSTOMTKINTER
from PIL import Image               # IMPORTS PIL FOR SUPPORTING IMAGES
from tkinter import messagebox as mb    # IMPORTS MESSAGE BOX
from database.meal_query import getMealsAll, updateMealStatus   # IMPORTS NECESSARY QUERIES
from database.grocery_query import getGroceryAll                # IMPORTS NECESSARY QUERY

def open_meal_page(parent, user_id, current_frame=None):

    current_frame.grid_forget() if current_frame else None

    # Meal Frame
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
        text="EatSmart\nMeal Plan",
        font=("Arial Black", 32),
        text_color="#505ab7",
        fg_color="#ead729"
    )
    title.place(relx=0.5, rely=0.5, anchor="center")

    # Navigation bar on the right side of the banner
    navigation_bar = ctk.CTkFrame(banner, fg_color="transparent", height=40)
    navigation_bar.grid(row=0, column=1, sticky="e")

    # FOR MINIMAL REDUNDANCY
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
            **btn_kwargs
        )
    except Exception:
        mealplan_navbar = ctk.CTkButton(
        navigation_bar,
        text="Meal Plan",
        fg_color="#3743b5",
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

    # Meal Plan Display Area
    display_area = ctk.CTkFrame(meal_frame, fg_color="transparent")
    display_area.grid(row=1, column=0, columnspan=2, sticky="nsew")
    display_area.grid_columnconfigure(0, weight=1)
    display_area.grid_rowconfigure(0, weight=0)
    display_area.grid_rowconfigure(1, weight=1)
    display_area.grid_rowconfigure(2, weight=0)
    display_area.grid_rowconfigure(3, weight=0)

    # QUERIES
    meals = getMealsAll(user_id)    # Getting all meals from mealplan table
    groceries = getGroceryAll(user_id)  # Getting all groceries from grocery table
    weekly_summary = build_weekly_summary(meals, groceries) # Calls the function for weekly snapshot

    # WEEKLY SNAPSHOT FRAME
    snapshot_frame = ctk.CTkFrame(display_area, fg_color="#f0f0f0", height=120)
    snapshot_frame.grid(row=0, column=0, sticky="nsew")
    snapshot_frame.grid_columnconfigure(0, weight=1)
    snapshot_frame.grid_rowconfigure(0, weight=1)

    # WEEKLY VIEW CARD FRAME
    weekly_view_card = ctk.CTkFrame(
        snapshot_frame,
        fg_color="white",
        corner_radius=12,
        border_width=1,
        border_color="#d5d7da"
    )
    weekly_view_card.grid(row=0, column=0, padx=20, pady=15, sticky="nsew")
    weekly_view_card.grid_columnconfigure(0, weight=1)

    # WEEKLY VIEW CARD LABEL
    ctk.CTkLabel(
        weekly_view_card,
        text="Weekly Snapshot",
        font=("Arial Black", 18),
        text_color="#505ab7"
    ).grid(row=0, column=0, sticky="w", padx=15, pady=(12, 4))

    # INFORMATION LABEL
    ctk.CTkLabel(
        weekly_view_card,
        text=weekly_summary,
        font=("Arial", 14),
        text_color="#1E4D2B",
        justify="left",
        wraplength=600
    ).grid(row=1, column=0, sticky="w", padx=15, pady=(0, 12))

    # MAIN DISPLAY AREA FRAME
    display_meal_frame = ctk.CTkScrollableFrame(display_area, fg_color="#505ab7", corner_radius=12)
    display_meal_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    load_meal_plan(parent, display_meal_frame, meals) # CALLS THE FUNCTION TO LOAD THE MEAL INTO THE DISPLAY AREA

    # ADD MEAL BUTTON
    add_meal_button = ctk.CTkButton(
        display_area,
        text="Add Meal",
        font=("Arial Black", 20),
        fg_color="#ead729",
        text_color="#505ab7",
        width=200,
        height=50,
        corner_radius=15,
        hover_color="#e9dd71",
        command=parent.show_add_meal_page
    )
    add_meal_button.grid(row=2, column=0, padx=20, pady=(0,20), sticky="w")

    # FOOTER FRAME
    footer_frame = ctk.CTkFrame(display_area, fg_color="#f0f0f0")
    footer_frame.grid(row=3, column=0, columnspan=2, pady=10)
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
        text="@ 2025 EatSmart. All rights reserved.",
        font=("Arial", 10),
        text_color="#888888"
    )
    footer_label.grid(row=1, column=0, columnspan=2, pady=5)

    return meal_frame

# VARIABLE FOR STATUS
STATUS_FLOW = ["Pending", "Eaten", "Skipped"]
STATUS_COLORS = {
    "Pending": "#f2c94c",
    "Eaten": "#72e755",
    "Skipped": "#f2994a",
} # DICTIONARY FOR FORMATTING THE BUTTONS

def load_meal_plan(parent, frame, meals): # FUNCTION TO LOAD THE MEALS INTO DISPLAY AREA

    # TABLE HEADERS
    headers = ["Day", "Breakfast", "Lunch", "Dinner"]
    for col, h in enumerate(headers):
        label = ctk.CTkLabel(frame, text=h,
                             font=("Arial Black", 18),
                             text_color="white")
        label.grid(row=0, column=col, pady=10, padx=30)

    # ORDERED DAYS
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                  "Friday", "Saturday", "Sunday"]

    # Convert SQL rows into a dictionary:
    meals_dict: Dict[str, Dict[str, Dict[str, Any] | None]] = {
        day: {"Breakfast": None, "Lunch": None, "Dinner": None} for day in days_order
    }

    # 
    for planID, mealID, day, mealTime, mealName, status in meals: # LOOPING FOR UNPACKING THE ROWS
        status_value = status or "Pending" # IF STATUS HAS VALUE
        meals_dict[day][mealTime] = {
            "meal_name": mealName or "No Meal", # IF MEALNAME HAS VALUE
            "data": (planID, mealID, day, mealTime, mealName, status_value), # MAKES THE DATA INTO TUPLE FOR PASSING VALUES ONTO EDIT PAGE
            "status": status_value, 
        }

    # CREATE THE TABLE ROW
    row_index = 1
    for day in days_order:

        # DAY LABEL
        day_label = ctk.CTkLabel(
            frame,
            text=f"{day}:",
            font=("Arial Black", 18),
            text_color="white"
        )
        day_label.grid(row=row_index, column=0, padx=15, pady=15, sticky="w")

        col_index = 1
        for mealTime in ["Breakfast", "Lunch", "Dinner"]: # MEAL TIME HEADER

            cell = meals_dict[day][mealTime] # CELL'S VALUE IS THE MEAL BASED ON THE DAY (e.g 'Monday') AND MEALTIME (e.g 'Breakfast')
            
            if cell is None: # CONDITION IF THE SPECIFIC DAY AND MEALTIME HAS NO CURRENT MEAL
                meal_name = "No Meal"
                data_tuple = (None, None, day, mealTime, None, "Pending")
                status_text = None
            else: # CONDITION IF THE SPECIFIC DAY AND MEALTIME HAS CURRENT MEAL
                meal_name = cell["meal_name"]
                data_tuple = cell["data"]
                status_text = cell.get("status", "Pending")

            # CREATES THE FRAME FOR EACH MEAL (PURPOSE IS TO DISPLAY THE MEAL, EDIT, AND STATUS IN ONE AREA)
            meal_box = ctk.CTkFrame(frame, fg_color="transparent")
            meal_box.grid(row=row_index, column=col_index, padx=20, pady=5)

            # MEAL LABEL
            label = ctk.CTkLabel(
                meal_box, 
                text=meal_name,
                text_color="white",
                font=("Arial Black", 15)
            )
            label.grid(row=0, column=0, columnspan=2)

            # EDIT BUTTON
            edit_btn = ctk.CTkButton(
                meal_box, text="Edit",
                font=("Arial Black", 12),
                fg_color="#ead729",
                text_color="#505ab7",
                width=70,
                command=lambda d=data_tuple: parent.show_edit_meal_page(d) # CALLS THE OPEN EDIT PAGE FROM main.py
            )
            edit_btn.grid(row=1, column=0, padx=5, pady=(5, 0))

            # STATUS BUTTON
            if data_tuple[0] and status_text: # CONDITION IF A MEAL EXIST THEN IT DISPLAYS STATUS BUTTON IF NOT STATUS BUTTON DOESN'T DISPLAY
                fg = STATUS_COLORS.get(status_text, "#72e755")
                stat_btn = ctk.CTkButton(
                    meal_box,
                    text=status_text,
                    font=("Arial Black", 12),
                    fg_color=fg,
                    text_color="#505ab7",
                    width=70,
                    command=lambda pid=data_tuple[0], status=status_text: handle_status_toggle(parent, pid, status) # CALLS THE TOGGLE STATUS FUNCTION FOR UPDATING MEAL'S STATUS
                )
                stat_btn.grid(row=1, column=1, padx=5, pady=(5, 0))

            col_index += 1

        row_index += 1


def handle_status_toggle(parent, plan_id, current_status): # FUNCTION FOR STATUS BUTTON
    try: # FINDS WHICH MEAL'S STATUS CURRENTLY IS
        current_index = STATUS_FLOW.index(current_status) 
    except ValueError:
        current_index = 0

    next_status = STATUS_FLOW[(current_index + 1) % len(STATUS_FLOW)] # GETS THE NEXT STATUS (e.g if current status is 'pending', then next status is 'eaten')

    if not updateMealStatus(parent.current_user_id, plan_id, next_status): # CONDITION FOR UPDATING THE STATUS FROM THE MEALPLAN TABLE
        mb.showerror("Status Update Failed", "Unable to update meal status. Please try again.")
        return

    parent.show_mealplan() # RELOADS THE ENTIRE PAGE


def build_weekly_summary(meals, groceries): # FUNCTION FOR WEEKLY SNAPSHOT
    total_slots = 21  # 7 days * 3 meals
    occupied_slots = set() # COUNTS HOW MANY SLOTS ARE FILLED
    status_counts = Counter() # COUNTS HOW MANY IS 'PENDING', 'EATEN', OR 'SKIPPED'

    for plan_id, _meal_id, day, meal_time, _meal_name, status in meals: # UNPACKS THE DATA FROM THE MEALPLAN TABLE
        occupied_slots.add((day, meal_time)) # ENSURES THAT DUPLICATE ENTRIES ONLY COUNT ONCE
        if plan_id: # CONDITION FOR COUNTING ONLY IF THERE'S A MEAL
            status_counts[status or "Pending"] += 1

    # FOR COMPUTING TOTALS
    filled_slots = len(occupied_slots)
    pending = status_counts.get("Pending", 0)
    eaten = status_counts.get("Eaten", 0)
    skipped = status_counts.get("Skipped", 0)

    # FOR COMPUTING MISSING MEALS
    missing = max(total_slots - filled_slots, 0)

    total_groceries = len(groceries)    # FOR COMPUTING SUMMARY OF GROCERY
    days_left_values = [item[-1] for item in groceries] # GETS THE DAYS LEFT OF THE GROCERY
    expiring_soon = sum(1 for days_left in days_left_values if days_left is not None and 0 <= days_left <= 2) # COUNTING EXPIRING SOON OF GROCERIES
    expired = sum(1 for days_left in days_left_values if days_left is not None and days_left < 0) # COUNTING CURRENT EXPIRED ITEMS

    # RETURNS THE SUMMARY TEXT
    return (
        f"Meals planned: {filled_slots}/{total_slots} (Pending {pending}, Eaten {eaten}, Skipped {skipped}, Missing {missing})\n"
        f"Groceries tracked: {total_groceries} (Expiring soon {expiring_soon}, Expired {expired})"
    )



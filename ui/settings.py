import customtkinter as ctk # IMPORTS CUSTOMTKINTER
from PIL import Image # IMPORTS PIL FOR SUPPORTING IMAGE
from database.grocery_query import getExpiredGroceryCount, getExpiringSoonGrocery # IMPORTS NECESSARY QUERIES
from database.meal_query import getSuccessfulMealsCount, getMealPlanToday, getTodaysDayAndMealTime
from database.user_query import getUserById, getEmailById

def open_settings_page(parent, user_id, current_frame):

    current_frame.grid_forget() if current_frame else None

    # Settings Frame
    settings_frame = ctk.CTkFrame(parent, fg_color="#f0f0f0")
    settings_frame.grid_columnconfigure(0, weight=1)
    settings_frame.grid_columnconfigure(1, weight=1)
    settings_frame.grid_rowconfigure(0, weight=0)
    settings_frame.grid_rowconfigure(1, weight=1)

    # Banner at the top with title and navigation buttons
    banner = ctk.CTkFrame(settings_frame, fg_color="#ead729", height=100)
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
        )
    except Exception:
        settings_navbar = ctk.CTkButton(
            navigation_bar,
            text="Settings",
            fg_color="#505ab7",
            **btn_kwargs,
    )
    settings_navbar.grid(row=0, column=2)

    your_settings_frame = ctk.CTkFrame(settings_frame, fg_color="#f0f0f0")
    your_settings_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
    your_settings_frame.grid_columnconfigure(0, weight=1)
    your_settings_frame.grid_columnconfigure(1, weight=1)

    # Your Profile Label (centered at top)
    your_profile_label = ctk.CTkLabel(
        your_settings_frame,
        text="Your Profile",
        font=("Arial Black", 22),
        text_color="#505ab7",
        fg_color="#f0f0f0",
        corner_radius=20,
        pady=3,
    )
    your_profile_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 5))

    # Your Profile Frame (left-aligned content)
    your_profile_frame = ctk.CTkFrame(your_settings_frame, fg_color="#f0f0f0")
    your_profile_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nw")
    your_profile_frame.grid_columnconfigure(0, weight=0)

    username = getUserById(user_id)

    # Your Username Label
    your_username_label = ctk.CTkLabel(
        your_profile_frame,
        text=f"{username}",
        font=("Arial Black", 22),
        text_color="#505ab7",
        fg_color="#ead729",
        corner_radius=16,
        width=350,
        padx=10,
        pady=15,
    )
    your_username_label.grid(row=0, column=0, pady=5, sticky="w")

    email = getEmailById(user_id)

    # Your Email Label
    your_email_label = ctk.CTkLabel(
        your_profile_frame,
        text=f"{email}",
        font=("Arial Black", 22),
        text_color="#505ab7",
        fg_color="#ead729",
        corner_radius=16,
        width=350,
        padx=10,
        pady=15,
    )
    your_email_label.grid(row=1, column=0, pady=5, sticky="w")

    # Right Side - Personal Stats (Successful Meal & Expired Food)
    stats_frame = ctk.CTkFrame(your_settings_frame, fg_color="#f0f0f0")
    stats_frame.grid(row=1, column=1, padx=20, pady=10, sticky="ne")
    stats_frame.grid_columnconfigure(0, weight=1)

    # Read successful meals and expired grocery counts
    successful_count = getSuccessfulMealsCount(user_id)
    expired_count = getExpiredGroceryCount(user_id)

    # Meal Successful Label
    successful_label = ctk.CTkLabel(
        stats_frame,
        text=f"Successful Meal Count: {successful_count}",
        font=("Arial Black", 22),
        text_color="#505ab7",
        fg_color="#ead729",
        corner_radius=16,
        padx=10, pady=15, width=350
    )
    successful_label.grid(row=0, column=0, pady=5)

    # Expired Food Label
    expired_label = ctk.CTkLabel(
        stats_frame,
        text=f"Expired Food Count: {expired_count}",
        font=("Arial Black", 22),
        text_color="#505ab7",
        fg_color="#ead729",
        corner_radius=16,
        padx=10, pady=15, width=350
    )
    expired_label.grid(row=1, column=0, pady=5)

    # Your Notification Settings Label
    your_notification_label = ctk.CTkLabel(
        your_settings_frame,
        text="Notification",
        font=("Arial Black", 22),
        text_color="#505ab7",
        fg_color="#f0f0f0",
        corner_radius=20
    )
    your_notification_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=2)

    # Notification Settings Frame
    your_notification_frame = ctk.CTkFrame(your_settings_frame, fg_color="#505ab7", corner_radius=12)
    your_notification_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
    your_notification_frame.grid_columnconfigure(0, weight=1)

    # Reads the expiring soon grocery items
    expiring_soon_groceries = getExpiringSoonGrocery(user_id)
    expiring_text = f"Expiring Soon: {expiring_soon_groceries} item{'s' if expiring_soon_groceries != 1 else ''}"

    # Warning Icon
    warning_icon = None
    try:
        warning_image = Image.open("assets/warning.png")
        warning_icon = ctk.CTkImage(light_image=warning_image, size=(30, 30))
    except Exception:
        warning_icon = None

    # Expiring Soon Text
    expiring_soon_label = ctk.CTkLabel(
        your_notification_frame,
        text=expiring_text,
        image=warning_icon,
        compound="left" if warning_icon else "center",
        padx=5 if warning_icon else 0,
        font=("Arial Black", 16),
        text_color="white",
        fg_color="#505ab7"
    )
    expiring_soon_label.grid(row=0, column=0, padx=15, pady=20, sticky="w")

    # Gets Current Day Meal
    today_info = getTodaysDayAndMealTime() or (None, None)
    today, mealtime = today_info
    if today and mealtime: # Condition if there's a meal in current day and mealtime (e.g a meal from 'Monday' and 'Lunch')
        todays_meal = getMealPlanToday(user_id, today, mealtime) or "No meal scheduled"
    else: # Else if there's no meal from the current day and mealtime then it results to no meal
        todays_meal = "No meal scheduled"

    # Daily Reminder Notification Label with check Icon
    try:
        check_image = Image.open("assets/check_mark.png")
        check_icon = ctk.CTkImage(light_image=check_image, size=(30, 30))
        daily_reminder_label = ctk.CTkLabel(
            your_notification_frame,
            text=f"Daily Reminder: {todays_meal}",
            image=check_icon,
            compound="left",
            padx=5,
            font=("Arial Black", 16),
            text_color="white",
            fg_color="#505ab7"
        )
    except Exception:
        daily_reminder_label = ctk.CTkLabel(
            your_notification_frame,
            text=f"Daily Reminder: {todays_meal}",
            font=("Arial Black", 16),
            text_color="white",
            fg_color="#505ab7"
        )
    daily_reminder_label.grid(row=1, column=0, padx=15, pady=20, sticky="w")

    # Logout Button
    logout_button = ctk.CTkButton(
        your_settings_frame,
        text="Logout",
        font=("Arial Black", 16),
        fg_color="#e03326",
        text_color="#dfe1f0",
        width=10,
        height=40,
        corner_radius=12,
        hover_color="#e05b26",
        command=parent.show_login
    )
    logout_button.grid(row=3, column=1, padx=100, pady=5, sticky="sew")

    # Footer Frame
    footer_frame = ctk.CTkFrame(your_settings_frame, fg_color="transparent")
    footer_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=3)
    footer_frame.grid_columnconfigure(0, weight=1)
    footer_frame.grid_rowconfigure(0, weight=1)
    footer_frame.grid_rowconfigure(1, weight=1)

    # Footer Quote Label
    footer_content = ctk.CTkLabel(
        footer_frame,
        text="EatSmart - Reduce Waste, Eat Wise",
        font=("Arial", 14),
        text_color="#505ab7"
    )
    footer_content.grid(row=0, column=0, pady=5, sticky="ew")

    # Footer Copyright Label
    footer_label = ctk.CTkLabel(
        footer_frame,
        text="© 2025 EatSmart. All rights reserved.",
        font=("Arial", 10),
        text_color="#888888",
        fg_color="#f0f0f0"
    )
    footer_label.grid(row=1, column=0, pady=5, sticky="ew")
    
    return settings_frame
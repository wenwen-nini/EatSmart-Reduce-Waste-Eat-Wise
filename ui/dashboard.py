import customtkinter as ctk
from PIL import Image
from database.grocery_query import getGroceryByUser
from database.user_query import getUserById

def open_dashboard_window(parent, user_id, current_frame=None):
    # Main dashboard frame
    frame = ctk.CTkFrame(parent)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=1)

    # Banner at the top with title and navigation buttons
    banner = ctk.CTkFrame(frame, fg_color="#ead729", height=100)
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

    # Display Area Frame
    display_area = ctk.CTkFrame(frame, fg_color="#f0f0f0")
    display_area.grid(row=1, column=0, columnspan=2, sticky="nsew")
    display_area.grid_columnconfigure(0, weight=1)
    display_area.grid_rowconfigure(0, weight=0) # Welcome message row
    display_area.grid_rowconfigure(1, weight=1) # List view row
    display_area.grid_rowconfigure(2, weight=0) # Quick add buttons row
    display_area.grid_rowconfigure(3, weight=0) # Footer row

    username = getUserById(user_id)

    # Welcome message
    welcome_label = ctk.CTkLabel(
        display_area,
        text=f"Welcome to EatSmart {username if username else 'User'}!",
        font=("Arial Black", 24),
        text_color="#505ab7",
        fg_color="#f0f0f0"
    )
    welcome_label.grid(row=0, column=0, columnspan=2, pady=15)

    # List View Frame
    list_view_frame = ctk.CTkFrame(display_area, fg_color="#505ab7", corner_radius=12)
    list_view_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
    list_view_frame.grid_columnconfigure(0, weight=1)
    list_view_frame.grid_rowconfigure(0, weight=0)
    list_view_frame.grid_rowconfigure(1, weight=1)

    list_view_label = ctk.CTkLabel(
        list_view_frame,
        text="Expiring Soon",
        font=("Arial Black", 20),
        text_color="white",
        fg_color="#505ab7"
    )
    list_view_label.grid(row=0, column=0, pady=10, sticky="ew")

    # List Scrollable Frame
    listbox = ctk.CTkScrollableFrame(list_view_frame, fg_color="#505ab7", border_width=0)
    listbox.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
    listbox.grid_columnconfigure(0, weight=1)

    check_image = Image.open("assets/check_mark.png")
    check_icon = ctk.CTkImage(light_image=check_image, size=(30, 30))

    # Populate grocery items
    groceries = getGroceryByUser(user_id)
    for grocery in groceries:
        item_label = ctk.CTkLabel(
            listbox,
            text=f"{grocery[0]} | {grocery[1]} days left",
            font=("Arial Black", 16),
            image=check_icon,
            compound="left",
            text_color="white",
            fg_color="#505ab7"
            )
        item_label.grid(row=groceries.index(grocery), column=0, padx=10, pady=5, sticky="ew")
    
    # Quick Add Frame
    quick_add_label = ctk.CTkFrame(display_area, fg_color="#f0f0f0")
    quick_add_label.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
    quick_add_label.grid_columnconfigure(0, weight=1)
    quick_add_label.grid_columnconfigure(1, weight=1)
    quick_add_label.grid_rowconfigure(0, weight=0)

    # -----------------
    # QUICK ADD BUTTONS
    # -----------------

    # Quick Add Grocery
    quick_add_grocery = ctk.CTkButton(
        quick_add_label,
        text="Add Grocery Item",
        font=("Arial Black", 16),
        fg_color="#ead729",
        text_color="#505ab7",
        width=200,
        height=50,
        corner_radius=12,
        command=parent.show_add_grocery_page,
        hover_color="#e9dd71"
    )
    quick_add_grocery.grid(row=0, column=0, padx=10, pady=5)

    # Quick Add Meal
    quick_add_meal = ctk.CTkButton(
        quick_add_label,
        text="Add Meal Plan",
        font=("Arial Black", 16),
        fg_color="#ead729",
        text_color="#505ab7",
        width=200,
        height=50,
        corner_radius=12,
        hover_color="#e9dd71",
        command=parent.show_add_meal_page
    )
    quick_add_meal.grid(row=0, column=1, padx=10, pady=5)

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

    # Footer All Rights Reserved
    footer_label = ctk.CTkLabel(
        footer_frame,
        text="© 2025 EatSmart. All rights reserved.",
        font=("Arial", 10),
        text_color="#888888",
        fg_color="#f0f0f0"
    )
    footer_label.grid(row=1, column=0, columnspan=2, pady=5)

    return frame
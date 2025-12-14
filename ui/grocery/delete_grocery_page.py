import customtkinter as ctk # IMPORTS CUSTOMTKINTER
from PIL import Image # IMPORTS PIL FOR SUPPORTING IMAGES
from database.grocery_query import deleteGrocery # IMPORTS NECESSARY QUERY

def open_delete_grocery_page(parent, grocery_data, user_id, current_frame=None):

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

    # DELETE GROCERY LABEL
    delete_grocery_label = ctk.CTkLabel(
        display_area,
        text="Confirm Delete Item",
        font=("Arial Black", 22),
        fg_color="#ead729",
        text_color="#505ab7",
        width=260,
        height=55,
        corner_radius=15
    )
    delete_grocery_label.pack(pady=(30, 10))

    # CONFIRMATION MESSAGE LABEL
    message_confirm_label = ctk.CTkLabel(
        display_area,
        text="Are you sure you want to delete this item?",
        font=("Arial", 18, "bold"),
        text_color="#505ab7",
    )
    message_confirm_label.pack(pady=(10, 20))

    # ITEM DETAILS FRAME
    item_display_frame = ctk.CTkFrame(
        display_area,
        fg_color="#505ab7",
        corner_radius=16,
        width=450,
        height=120
    )
    item_display_frame.pack(pady=10)

    # ITEM DETAILS FRAME CONFIGURATION (GRID)
    item_display_frame.grid_rowconfigure(0, weight=1)
    item_display_frame.grid_rowconfigure(1, weight=1)
    item_display_frame.grid_columnconfigure(0, weight=1)

    # ITEM NAME LABEL
    item_display = ctk.CTkLabel(
        item_display_frame,
        text=f"Item: {grocery_data[1]}",
        font=("Arial Black", 18),
        text_color="#ead729",
        fg_color="transparent"
    )
    item_display.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 0))

    # DATE LABEL
    date_display = ctk.CTkLabel(
        item_display_frame,
        text=f"Expiration: {grocery_data[4]}",
        font=("Arial Black", 18),
        text_color="#ead729",
        fg_color="transparent"
    )
    date_display.grid(row=1, column=0, sticky="w", padx=15, pady=(5, 15))

    # BIG WARNING TEXT
    warning_label = ctk.CTkLabel(
        display_area,
        text="This action cannot be undone.",
        font=("Arial", 16, "bold"),
        text_color="#505ab7",
    )
    warning_label.pack(pady=(20, 30))

    # BUTTON ROW
    btn_row = ctk.CTkFrame(display_area, fg_color="transparent")
    btn_row.pack(pady=10)

    # DELETE BUTTON
    delete_btn = ctk.CTkButton(
        btn_row,
        text="Delete",
        font=("Arial Black", 18),
        fg_color="#d90429",
        hover_color="#b3001f",
        text_color="white",
        width=180,
        height=50,
        corner_radius=12,
        command=lambda: deleteGrocery(user_id, grocery_data[0]) # CALLS THE QUERY FOR DELETING A DATA FROM GROCERY TABLE
    )
    delete_btn.grid(row=0, column=0, padx=20)

    # CANCEL BUTTON
    cancel_btn = ctk.CTkButton(
        btn_row,
        text="Cancel",
        font=("Arial Black", 18),
        fg_color="#6c6c6c",
        hover_color="#555555",
        text_color="white",
        width=180,
        height=50,
        corner_radius=12,
        command=parent.show_grocery # RETURNS TO GROCERY PAGE
    )
    cancel_btn.grid(row=0, column=1, padx=20)

    # FOOTER FRAME
    footer_frame = ctk.CTkFrame(display_area, fg_color="white")
    footer_frame.pack(pady=(3,0))
    footer_frame.grid_rowconfigure(0, weight=1)
    footer_frame.grid_rowconfigure(1, weight=1)

    # FOOTER CONTENT
    footer_content = ctk.CTkLabel(
        footer_frame,
        text="EatSmart - Reduce Waste, Eat Wise",
        font=("Arial", 14),
        text_color="#505ab7"
    )
    footer_content.grid(row=0, column=0, columnspan=2, pady=(0,3))

    # FOOTER RESERVED
    footer_label = ctk.CTkLabel(
        footer_frame,
        text="© 2025 EatSmart. All rights reserved.",
        font=("Arial", 10),
        text_color="#888888",
    )
    footer_label.grid(row=1, column=0, columnspan=2)

    return grocery_frame
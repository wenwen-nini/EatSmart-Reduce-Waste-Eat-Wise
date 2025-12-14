import customtkinter as ctk # IMPORTS CUSTOMTKINTER
from PIL import Image # IMPORTS PIL FOR SUPPORTING IMAGES
from database.user_query import register_user # IMPORTS NECESSARY QUERY

def open_register_window(parent, switch_to_login):

    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    # Register Frame
    register_frame = ctk.CTkFrame(parent)
    register_frame.grid_columnconfigure(0, weight=2)
    register_frame.grid_columnconfigure(1, weight=2)
    register_frame.grid_rowconfigure(0, weight=2)

    ascii_art = Image.open("assets/cart_ascii.png")
    ascii_image = ctk.CTkImage(
        light_image=ascii_art,
        size=(300,300)
    )

    # Left Frame
    left_frame = ctk.CTkFrame(register_frame, fg_color="white")
    left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.grid_columnconfigure(0, weight=1)

    # Cart Image on Background
    ascii_label = ctk.CTkLabel(left_frame, image=ascii_image, text="")
    ascii_label.place(relx=0.50, rely=0.40, anchor="center")

    # Right Frame
    right_frame = ctk.CTkFrame(register_frame, fg_color="white")
    right_frame.grid(row=0, column=1, sticky="nsew")

    # Background Image on Right Frame
    image = Image.open("assets/meal.png")

    bg_image = ctk.CTkImage(
        light_image=image,
        size=(600, 600)
    )
    bg_label = ctk.CTkLabel(right_frame, image=bg_image, text="")
    bg_label.place(relx=0.5, rely=0.5, anchor="center")

    # Banner at the top of Left Frame
    banner = ctk.CTkFrame(left_frame, fg_color="#ead729", height=100)
    banner.grid(row=0, column=0, sticky="nsew")

    # Title in the center of the banner
    title = ctk.CTkLabel(
        banner,
        text="Welcome to\nEatSmart!",
        font=("Arial Black", 32),
        text_color="#505ab7"
    )
    title.place(relx=0.5, rely=0.5, anchor="center")

    # Register Label
    register_label = ctk.CTkLabel(
        left_frame,
        text="Register Window",
        font=("Arial Black", 22),
        fg_color="#ead729",
        corner_radius=20,
        padx=20,
        pady=15,
        text_color="#505ab7"
    )
    register_label.grid(row=1, column=0, pady=(10, 20))

    # Username Entry
    username_entry = ctk.CTkEntry(
        left_frame,
        placeholder_text="Enter your username:",
        font=("Arial Black", 14),
        height=45,
        width=300,
        corner_radius=12
    )
    username_entry.grid(row=2, column=0, pady=5)

    # Email Entry
    email_entry = ctk.CTkEntry(
        left_frame,
        placeholder_text="Enter your email:",
        font=("Arial Black", 14),
        height=45,
        width=300,
        corner_radius=12
    )
    email_entry.grid(row=3, column=0, pady=5)

    # Password Entry
    password_entry = ctk.CTkEntry(
        left_frame,
        placeholder_text="Enter your password:",
        font=("Arial Black", 14),
        show="*",
        height=45,
        width=300,
        corner_radius=12
    )
    password_entry.grid(row=4, column=0, pady=5)

    # Buttons Row Frame
    button_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
    button_frame.grid(row=5, column=0, pady=5)

    # Register Button
    register_btn = ctk.CTkButton(
        button_frame,
        text="Register",
        font=("Arial Black", 16),
        fg_color="#ead729",
        text_color="#505ab7",
        width=140,
        height=40,
        corner_radius=15,
        hover_color="#d4c529",
        command=lambda: register_user(username_entry.get(), password_entry.get(), email_entry.get()) # CALLS FROM THE USER QUERY
    )
    register_btn.grid(row=0, column=0, padx=5)

    # Login Button
    login_btn = ctk.CTkButton(
        button_frame,
        text="Login Here",
        font=("Arial Black", 16),
        fg_color="#ead729",
        text_color="#505ab7",
        width=140,
        height=40,
        corner_radius=15,
        hover_color="#d4c529",
        command = switch_to_login
    )
    login_btn.grid(row=2, column=0, padx=5)

    # Login Note and Button
    note = ctk.CTkLabel(
        button_frame,
        text="Already have an account? Click Login!",
        font=("Arial", 14),
        text_color="#505ab7"
    )
    note.grid(row=1, column=0, pady=(15, 10))

    # Footer
    footer = ctk.CTkLabel(
        left_frame,
        text="EatSmart - Reduce Waste, Eat Wise\n\nSubmitted By: Alwynn Aguho\nBSIT - 2108",
        font=("Arial", 14),
        text_color="#505ab7"
    )
    footer.grid(row=6, column=0, pady=(20, 30))

    return register_frame
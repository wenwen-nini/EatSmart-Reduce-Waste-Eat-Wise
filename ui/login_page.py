import customtkinter as ctk # IMPORTS CUSTOMTKINTER
from PIL import Image # IMPORTS PIL FOR SUPPORTING IMAGE
from tkinter import messagebox as mb # IMPORTS MESSAGEBOX
from database.user_query import login_user # IMPORTS NECESSARY QUERY

def open_login_window(parent, switch_to_register, on_success):

    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    # Login Frame
    login_frame = ctk.CTkFrame(parent)
    login_frame.grid_columnconfigure(0, weight=1)
    login_frame.grid_columnconfigure(1, weight=1)
    login_frame.grid_rowconfigure(0, weight=1)

    # Left Frame
    left_frame = ctk.CTkFrame(login_frame, fg_color="white")
    left_frame.grid(row=0, column=0, sticky="nsew")

    # Background Image on Left Frame
    image = Image.open("assets/cart.png")

    bg_image = ctk.CTkImage(
        light_image=image,
        size=(600,600)
    )
    bg_label = ctk.CTkLabel(left_frame, image=bg_image, text="")
    bg_label.place(relx=0.3, rely=0.5, anchor="center")

    #Cart Image on background
    ascii_art = Image.open("assets/cart_ascii.png")
    ascii_image = ctk.CTkImage(
        light_image=ascii_art,
        size=(300,300)
    )
    # Right Frame
    right_frame = ctk.CTkFrame(login_frame, fg_color="white")
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_columnconfigure(0, weight=1)

    ascii_label = ctk.CTkLabel(right_frame, image=ascii_image, text="")
    ascii_label.place(relx=0.50, rely=0.45, anchor="center")

    # Banner at the top of Right Frame
    banner = ctk.CTkFrame(right_frame, fg_color="#ead729", height=100)
    banner.grid(row=0, column=0, sticky="nsew")

    # Title in the center of the banner
    title = ctk.CTkLabel(
        banner,
        text="Welcome to\nEatSmart!",
        font=("Arial Black", 33.8),
        text_color="#505ab7"
    )
    title.place(relx=0.5, rely=0.5, anchor="center")

    # Login Label
    login_label = ctk.CTkLabel(
        right_frame,
        text="Login Window",
        font=("Arial Black", 22),
        fg_color="#ead729",
        corner_radius=20,
        padx=20,
        pady=10,
        text_color="#505ab7"
    )
    login_label.grid(row=1, column=0, pady=(30, 10))

    # Username Entry
    username_entry = ctk.CTkEntry(
        right_frame,
        placeholder_text="Enter your username:",
        font=("Arial Black", 14),
        height=45,
        width=300,
        corner_radius=12
    )
    username_entry.grid(row=2, column=0, pady=10)

    # Password Entry
    password_entry = ctk.CTkEntry(
        right_frame,
        placeholder_text="Enter your password:",
        font=("Arial Black", 14),
        show="*",
        height=45,
        width=300,
        corner_radius=12
    )
    password_entry.grid(row=3, column=0, pady=10)

    # Buttons Row Frame
    button_frame = ctk.CTkFrame(right_frame, fg_color="white")
    button_frame.grid(row=4, column=0, pady=20)

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
        command = switch_to_register
    )
    register_btn.grid(row=0, column=0, padx=10)

    # Attempt Login Function
    def attempt_login():
        user_id = login_user(username_entry.get(), password_entry.get())
        if user_id:
            # call the success callback (Dashboard)
            try:
                on_success(user_id)
            except Exception:
                pass
        else:
            mb.showerror("Login Failed", "Invalid username or password")

    # Login Button
    login_btn = ctk.CTkButton(
        button_frame,
        text="Login",
        font=("Arial Black", 16),
        fg_color="#ead729",
        text_color="#505ab7",
        width=140,
        height=40,
        corner_radius=15,
        hover_color="#d4c529",
        command=attempt_login
    )
    login_btn.grid(row=0, column=1, padx=10)

    # Register Label
    note = ctk.CTkLabel(
        right_frame,
        text="Don't have an account? Click Register!",
        font=("Arial", 14),
        text_color="#505ab7",  
        fg_color="transparent"
    )
    note.grid(row=5, column=0, pady=(5, 20))

    # Footer
    footer = ctk.CTkLabel(
        right_frame,
        text="EatSmart - Reduce Waste, Eat Wise\n\nSubmitted By: Alwynn Aguho\nBSIT - 2108",
        font=("Arial", 14),
        text_color="#505ab7",
        fg_color="transparent"
    )
    footer.grid(row=6, column=0, pady=(40, 10))

    return login_frame



import customtkinter as ctk
from config.db_config import initialize_tables, create_database
from config.seed_data import seed_initial_data  
from tkinter import messagebox as mb
from ui.login_page import open_login_window
from ui.register_page import open_register_window
from ui.dashboard import open_dashboard_window
from ui.grocery_page import open_grocery_page
from ui.settings import open_settings_page
from ui.mealplan_page import open_meal_page
from ui.grocery.add_grocery_page import open_add_grocery_page
from ui.grocery.edit_grocery_page import open_edit_grocery_page
from ui.grocery.delete_grocery_page import open_delete_grocery_page
from ui.meal.add_meal_page import open_add_meal_page
from ui.meal.edit_meal_page import open_edit_meal_page

class App(ctk.CTk):

    # -----------
    # MAIN WINDOW
    # -----------
    def __init__(self): 
        super().__init__()
        self.geometry("900x600")
        self.title("EatSmart")
        self.resizable(False, False)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.current_frame = None
        self.current_user_id = None
        self.show_login()

    # -----------
    # DASHBOARD
    # -----------
    def show_dashboard(self, user_id):
        self.current_user_id = user_id
        try:
            new_frame = open_dashboard_window(self, user_id=user_id, current_frame=self.current_frame)
        except Exception as e:
            mb.showerror("Dashboard Error", f"Failed to open dashboard:\n{e}")
            return

        if self.current_frame:
            self.current_frame.grid_forget()

        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # ------------
    # GROCERY PAGE
    # ------------
    def show_grocery(self):
        try:
            new_frame = open_grocery_page(self, user_id=self.current_user_id, current_frame=self.current_frame)
        except Exception as e:
            mb.showerror("Grocery Error", f"Failed to open grocery page:\n{e}")
            return

        if self.current_frame:
            self.current_frame.grid_forget()

        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # --------------
    # MEAL PLAN PAGE
    # --------------
    def show_mealplan(self):
        try:
            new_frame = open_meal_page(self, user_id=self.current_user_id, current_frame=self.current_frame)
        except Exception as e:
            mb.showerror("Meal Plan Error", f"Failed to open meal plan page:\n{e}")
            return

        if self.current_frame:
            self.current_frame.grid_forget()

        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # -------------
    # SETTINGS PAGE
    # -------------
    def show_settings(self):
        try:
            new_frame = open_settings_page(self, user_id=self.current_user_id, current_frame=self.current_frame)
        except Exception as e:
            mb.showerror("Settings Error", f"Failed to open settings page:\n{e}")
            return
        if self.current_frame:
            self.current_frame.grid_forget()

        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # -------------
    # LOGIN PAGE
    # -------------
    def show_login(self):
        try:
            new_frame = open_login_window(self, switch_to_register=self.show_register, on_success=self.show_dashboard)
        except Exception as e:
            mb.showerror("UI Error", f"Failed to open login page:\n{e}")
            return

        if self.current_frame:
            self.current_frame.grid_forget()

        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # -------------
    # REGISTER PAGE
    # -------------
    def show_register(self):
        try:
            new_frame = open_register_window(self, switch_to_login=self.show_login)
        except Exception as e:
            mb.showerror("UI Error", f"Failed to open register page:\n{e}")
            return

        if self.current_frame:
            self.current_frame.grid_forget()

        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # ---------------
    # ADD GROCERY PAGE
    # ---------------
    def show_add_grocery_page(self):
        try:
            new_frame = open_add_grocery_page(self, user_id=self.current_user_id, current_frame=self.current_frame)
        except Exception as e:
            mb.showerror("Settings Error", f"Failed to open add grocery page:\n{e}")
            return
        if self.current_frame:
            self.current_frame.grid_forget()
        
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # ---------------
    # EDIT GROCERY PAGE
    # ---------------
    def show_edit_grocery_page(self, grocery_data):
        try:
            new_frame=open_edit_grocery_page(self, grocery_data, user_id=self.current_user_id, current_frame=self.current_frame)
        except Exception as e:
            mb.showerror("Settings Error", f"Failed to open edit grocery page:\n{e}")
            return
        if self.current_frame:
            self.current_frame.grid_forget()
        
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # ---------------
    # DELETE GROCERY PAGE
    # ---------------
    def show_delete_grocery_page(self, grocery_data):
        try:
            new_frame=open_delete_grocery_page(self, grocery_data, user_id=self.current_user_id, current_frame=self.current_frame)
        except Exception as e:
            mb.showerror("Settings Error", f"Failed to open edit grocery page:\n{e}")
            return
        if self.current_frame:
            self.current_frame.grid_forget()
        
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # ---------------
    # ADD MEAL PAGE
    # ---------------
    def show_add_meal_page(self):
        try:
            new_frame=open_add_meal_page(self, user_id=self.current_user_id, current_frame=self.current_frame)
        except Exception as e:
            mb.showerror("Settings Error", f"Failed to open edit grocery page:\n{e}")
            return
        if self.current_frame:
            self.current_frame.grid_forget()
        
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    # ---------------
    # EDIT MEAL PAGE
    # ---------------
    def show_edit_meal_page(self, meal_data):
        try:
            new_frame= open_edit_meal_page(self, meal_data, user_id=self.current_user_id, current_frame=self.current_frame)
        except Exception as e:
            mb.showerror("Settings Error", f"Failed to open edit meal page:\n{e}")
            return
        if self.current_frame:
            self.current_frame.grid_forget()
        
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    # STARTING THE SYSTEM
if __name__ == "__main__":
    create_database() # CREATES THE INITIALIZED DATABASE
    initialize_tables() # CREATES THE INITIALIZED TABLES OF DB
    seed_initial_data() # SAMPLE DATAS FOR DATABASE
    App().mainloop()
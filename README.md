# EatSmart

A meal planning and grocery management application designed to help reduce food waste and eat wisely.

## Features

### Meal Planning
- **Weekly Meal Plan View**: Plan your meals across 7 days with 3 meals per day (Breakfast, Lunch, Dinner)
- **Status Tracking**: Track meal status as Pending, Eaten, or Skipped
- **Weekly Snapshot**: Quick overview showing filled meal slots, meal status breakdown, and missing meals
- **Add/Edit Meals**: Create new meals and attach grocery ingredients
- **Meal Ingredients**: Link meals to groceries you already have

### Grocery Management
- **Add Grocery Items**: Track items with quantity, category, and expiration date
- **Search & Filter**: Search items by name or filter by category
- **Days Left Indicator**: Automatically calculated expiration countdown that updates daily
- **Color-Coded Status**: Visual indicators for items expiring soon, expired, or safe
  - Yellow: Expires today or within 3 days
  - Red: Already expired
  - White: Safe to consume
- **Category Organization**: Organize groceries by predefined categories (Canned Goods, Fruits, Vegetables, Meat, Dairy, Fisheries, Pastries, Beverages, Condiments)

### Dashboard
- **Quick Stats**: View successful meal count and expired food count
- **Expiring Soon Alerts**: Notifications for items expiring within 1 day
- **Daily Reminder**: See today's scheduled meal for your current time
- **Quick Actions**: Fast access to add grocery items or meal plans

### Settings
- **Profile Management**: View your username and email
- **Personal Stats**: Track successful meals eaten and expired food count
- **Notifications**: See expiring soon groceries and today's meal reminders

## System Requirements

- Python 3.7+
- MySQL Server
- CustomTkinter for UI
- MySQL Connector for Python
- Pillow for image handling

## Installation

1. **Clone or download the project**

2. **Install Python dependencies**:
   ```bash
   pip install customtkinter pillow mysql-connector-python
   ```

3. **Install MySQL in your windows**:

4. **Set up MySQL Database**:
   - Ensure MySQL Server is running on localhost with default port 3306
   - Update credentials in `config/db_config.py` if needed:
     ```python
     def get_db():
         return mysql.connector.connect(
             host="localhost",
             user="root",
             password="password", # Password depends on your mysql password
             database="eatsmart_db"
         )
     ```

5. **Run the application**:
   ```bash
   python main.py
   ```

The database tables will be created automatically on first run, and seed data (admin user with sample meals and groceries) will be inserted.

## Default Login

For testing purposes, the app comes with a default admin account:
- **Username**: `admin`
- **Password**: `admin123`

## Project Structure

```
EatSmart/
├── main.py                    # Application entry point
├── assets/                    # Icons and images
│   ├── cart_icon.png
│   ├── meal_icon.png
│   ├── settings_icon.png
│   ├── warning.png
│   └── check_mark.png
├── config/
│   ├── db_config.py          # Database connection configuration
│   └── seed_data.py          # Initial data seeding
├── database/
│   ├── grocery_query.py      # Grocery CRUD operations
│   ├── meal_query.py         # Meal plan CRUD operations
│   └── user_query.py         # User authentication
├── ui/
│   ├── dashboard.py          # Dashboard page
│   ├── grocery_page.py       # Grocery list page
│   ├── mealplan_page.py      # Meal plan page
│   ├── settings.py           # Settings/profile page
│   ├── login_page.py         # Login page
│   ├── register_page.py      # Registration page
│   ├── meal/
│   │   ├── add_meal_page.py
│   │   └── edit_meal_page.py
│   └── grocery/
│       ├── add_grocery_page.py
│       ├── edit_grocery_page.py
│       └── delete_grocery_page.py
└── components/
    ├── custom_widgets.py     # Reusable UI components
    ├── navbar.py             # Navigation bar component
    └── theme_toggle.py       # Theme utilities
```

## Database Schema

### Tables
- **users**: User accounts and authentication
- **grocery**: Grocery items with expiration tracking
- **category**: Grocery categories
- **meal**: Meal definitions
- **mealPlan**: Weekly meal schedule with status tracking
- **meal_ingredients**: Links meals to groceries

## Key Workflows

### Adding a Meal
1. Go to Meal Plan page
2. Click "Add Meal"
3. Enter meal name
4. Select day and meal time
5. Optionally select ingredients from your groceries
6. Click "Save Meal"

### Managing Groceries
1. Go to Grocery List page
2. Use search bar to find items
3. Filter by category with the dropdown
4. Edit expiration dates or delete items as needed
5. The "Days Left" column updates automatically

### Tracking Meal Status
1. In the Meal Plan page, click the status button on any meal
2. Status cycles through: Pending → Eaten → Skipped → Pending
3. Status is saved to the database immediately
4. Successful meal count updates in Settings/Dashboard

## Troubleshooting

### Database Connection Issues
- Ensure MySQL Server is running
- Verify host, user, and password in `config/db_config.py`
- Check that port 3306 is not blocked

### Missing Images
- Ensure all PNG files are in the `assets/` folder
- The app gracefully falls back to text-only buttons if images are missing

### No Groceries in Add Meal
- Add grocery items first in the Grocery List page
- The ingredient selector is disabled if no groceries exist

## Future Enhancements

- Multi-user account support improvements
- Recipe suggestions based on available ingredients
- Shopping list generation from meal plans
- Nutritional information tracking
- Export meal plans and shopping lists

## License

This project is part of the EatSmart initiative to reduce food waste and promote conscious eating.

---

**EatSmart - Reduce Waste, Eat Wise**

from config.db_config import get_db

def seed_initial_data():
    db = get_db()
    # Use buffered cursor so each SELECT result is fully read even if we mix reads/writes
    cursor = db.cursor(buffered=True)

    # -----------------------------
    # 1. CATEGORIES
    # -----------------------------
    categories = ["Canned Goods", "Fruits", "Vegetables", "Meat", "Dairy",
                  "Fisheries", "Pastries", "Beverages", "Condiments"]
    
    for cat in categories:
        cursor.execute("SELECT categoryID FROM category WHERE categoryName=%s", (cat,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO category (categoryName) VALUES (%s)
            """, (cat,))
    
    # -----------------------------
    # 2. ADMIN USER
    # -----------------------------
    cursor.execute("SELECT userID FROM users WHERE username='admin'")
    admin_row = cursor.fetchone()

    if not admin_row:
        cursor.execute("""
            INSERT INTO users (username, password, email)
            VALUES (%s, %s, %s)
        """, ('admin', 'admin123', 'admin@example.com'))

        cursor.execute("SELECT userID FROM users WHERE username='admin'")
        admin_row = cursor.fetchone()

    admin_id = int(admin_row[0])

    # -----------------------------
    # 3. GROCERY ITEMS
    # -----------------------------
    grocery_items = [
        ('San Marino Tuna', '3x', 'Canned Goods', '2025-12-05'),
        ('Gala Apples', '2kg', 'Fruits', '2025-12-20'),
        ('Broccoli', '1kg', 'Vegetables', '2025-11-30'),
        ('Fresh Milk', '2x', 'Dairy', '2025-12-25'),
        ('Chicken Breast', '1kg', 'Meat', '2025-12-19'),
    ]

    for name, quantity, category, expiration_date in grocery_items:

        # get categoryID
        cursor.execute("SELECT categoryID FROM category WHERE categoryName=%s", (category,))
        category_id = cursor.fetchone()[0]

        # check grocery item
        cursor.execute("""
            SELECT groceryID FROM grocery
            WHERE userID=%s AND name=%s
        """, (admin_id, name))

        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO grocery(userID, categoryID, name, quantity, expirationDate)
                VALUES (%s, %s, %s, %s, %s)
            """, (admin_id, category_id, name, quantity, expiration_date))

    # -----------------------------
    # 4. MEALS
    # -----------------------------
    meals = ["Chicken Salad", "Tuna Pasta", "Apple Yogurt Bowl"]

    for meal in meals:
        cursor.execute("""
            SELECT mealID FROM meal WHERE userID=%s AND mealName=%s
        """, (admin_id, meal))

        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO meal (userID, mealName)
                VALUES (%s, %s)
            """, (admin_id, meal))

    # rebuild meal dictionary
    cursor.execute("SELECT mealID, mealName FROM meal WHERE userID=%s", (admin_id,))
    meal_dict = {name: mid for (mid, name) in cursor.fetchall()}

    def get_or_create_meal_id(meal_name):
        existing_id = meal_dict.get(meal_name)
        if existing_id:
            return existing_id

        cursor.execute(
            "SELECT mealID FROM meal WHERE userID=%s AND mealName=%s",
            (admin_id, meal_name)
        )
        row = cursor.fetchone()
        if row:
            meal_dict[meal_name] = row[0]
            return row[0]

        cursor.execute(
            """
                INSERT INTO meal (userID, mealName)
                VALUES (%s, %s)
            """,
            (admin_id, meal_name)
        )
        new_id = cursor.lastrowid
        if not new_id:
            cursor.execute(
                "SELECT mealID FROM meal WHERE userID=%s AND mealName=%s",
                (admin_id, meal_name)
            )
            fallback_row = cursor.fetchone()
            new_id = fallback_row[0] if fallback_row else None
        meal_dict[meal_name] = new_id
        return new_id

    # -----------------------------
    # 5. MEAL INGREDIENTS
    # -----------------------------
    ingredients = [
        ("Chicken Salad", "Chicken Breast", 1),
        ("Chicken Salad", "Broccoli", 1),
        ("Tuna Pasta", "San Marino Tuna", 1),
        ("Apple Yogurt Bowl", "Gala Apples", 2),
        ("Apple Yogurt Bowl", "Fresh Milk", 1),
    ]

    for meal_name, grocery_name, qty in ingredients:
        meal_id = get_or_create_meal_id(meal_name)
        if not meal_id:
            continue

        cursor.execute("""
            SELECT groceryID FROM grocery
            WHERE userID=%s AND name=%s
        """, (admin_id, grocery_name))
        grocery_row = cursor.fetchone()
        if not grocery_row:
            # skip if the related grocery was removed by the user
            continue
        grocery_id = grocery_row[0]

        # check if ingredient exists
        cursor.execute("""
            SELECT ingredientID FROM meal_ingredients
            WHERE mealID=%s AND ingredientName=%s
        """, (meal_id, grocery_name))

        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO meal_ingredients (mealID, groceryID, ingredientName, quantityNeeded)
                VALUES (%s, %s, %s, %s)
            """, (meal_id, grocery_id, grocery_name, qty))

    # -----------------------------
    # 6. MEAL PLAN
    # -----------------------------
    meal_plan_samples = [
        ("Monday", "Breakfast",  "Chicken Salad"),
        ("Monday", "Lunch",      "Tuna Pasta"),
        ("Monday", "Dinner",     "Apple Yogurt Bowl"),

        ("Tuesday", "Breakfast", "Apple Yogurt Bowl"),
        ("Tuesday", "Lunch",     "Chicken Salad"),
        ("Tuesday", "Dinner",    "Tuna Pasta"),

        ("Wednesday", "Breakfast", "Tuna Pasta"),
        ("Wednesday", "Lunch",     "Apple Yogurt Bowl"),
        ("Wednesday", "Dinner",    "Chicken Salad"),

        ("Thursday", "Breakfast",  "Chicken Salad"),
        ("Thursday", "Lunch",      "Tuna Pasta"),
        ("Thursday", "Dinner",     "Apple Yogurt Bowl"),

        ("Friday", "Breakfast",    "Apple Yogurt Bowl"),
        ("Friday", "Lunch",        "Chicken Salad"),
        ("Friday", "Dinner",       "Tuna Pasta"),

        ("Saturday", "Breakfast",  "Tuna Pasta"),
        ("Saturday", "Lunch",      "Apple Yogurt Bowl"),
        ("Saturday", "Dinner",     "Chicken Salad"),

        ("Sunday", "Breakfast",    "Chicken Salad"),
        ("Sunday", "Lunch",        "Tuna Pasta"),
        ("Sunday", "Dinner",       "Apple Yogurt Bowl"),
    ]

    for day, time, meal_name in meal_plan_samples:
        cursor.execute("""
            SELECT planID FROM mealPlan
            WHERE userID=%s AND dayOfWeek=%s AND mealTime=%s
        """, (admin_id, day, time))
        plan_exists = cursor.fetchone()

        meal_id = get_or_create_meal_id(meal_name)

        if not plan_exists and meal_id:
            cursor.execute("""
                INSERT INTO mealPlan (userID, mealID, dayOfWeek, mealTime)
                VALUES (%s, %s, %s, %s)
            """, (admin_id, meal_id, day, time))

    # -----------------------------
    db.commit()
    cursor.close()
    db.close()
    print("Seed data inserted successfully without duplicates!")

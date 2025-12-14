from config.db_config import get_db
from tkinter import messagebox as mb
import re

def getMealsByUser(user_id):
    #Get meals by user ID // For Dashboard display
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT mp.dayOFWeek, mp.mealTime, m.mealName 
            FROM mealplan mp
            JOIN meal m ON mp.mealID = m.mealID
            WHERE mp.userID = %s
            ORDER BY FIELD(mp.dayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
            FIELD(mp.mealTime, 'Breakfast', 'Lunch', 'Dinner')
    """, (user_id,))
    except Exception as e:
        print(f"Error retrieving meals: {e}")
        return []
    meals = cursor.fetchall()
    cursor.close()
    db.close()
    return meals

def getMealsAll(user_id):
    # Get all meals by user ID // For Meal Plan display
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT mp.planID, mp.mealID, mp.dayOfWeek, mp.mealTime, m.mealName, mp.status
            FROM mealplan mp
            JOIN meal m ON mp.mealID = m.mealID
            WHERE mp.userID = %s
            ORDER BY FIELD(mp.dayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
            FIELD(mp.mealTime, 'Breakfast', 'Lunch', 'Dinner')
        """, (user_id,))
        meals = cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving meals: {e}")
        return []
    finally:
        cursor.close()
        db.close()
    return meals

def getDays():
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT COLUMN_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'mealplan'
                AND COLUMN_NAME = 'dayOfWeek'
        """)
        column_type = cursor.fetchone()[0]
        enum_day_list = re.findall(r"'(.*?)'", column_type)
        return enum_day_list
    except Exception as e:
        print(f"Error retrieving dayOfWeek: {e}")
        return []
    
def getMealTime():
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT COLUMN_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'mealplan'
                AND COLUMN_NAME = 'mealTime'
        """)
        column_type = cursor.fetchone()[0]
        enum_time_list = re.findall(r"'(.*?)'", column_type)
        return enum_time_list
    except Exception as e:
        print(f"Error retrieving dayOfWeek: {e}")
        return None
    
def getIngredients(user_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT groceryID, name, quantity 
            FROM grocery
            WHERE userID = %s
        """, (user_id,))
        result = cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving ingredients: {e}")
        return 0
    cursor.close()
    db.close()
    return result

def addMeal(user_id, meal_name, dayOfWeek, mealTime, selected_ingredients):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # 1. Insert the meal
        cursor.execute(
            "INSERT INTO meal (userID, mealName) VALUES (%s, %s)",
            (user_id, meal_name)
        )
        meal_id = cursor.lastrowid
        
        # 2. Insert into meal plan
        cursor.execute(
            "INSERT INTO mealPlan (userID, mealID, dayOfWeek, mealTime) VALUES (%s, %s, %s, %s)",
            (user_id, meal_id, dayOfWeek, mealTime)
        )
        
        # 3. Insert each selected ingredient into meal_ingredients
        for grocery_id, ingredient_name, quantity_needed in selected_ingredients:
            cursor.execute(
                """INSERT INTO meal_ingredients (mealID, groceryID, ingredientName, quantityNeeded) 
                   VALUES (%s, %s, %s, %s)""",
                (meal_id, grocery_id, ingredient_name, quantity_needed)
            )
        mb.showinfo("Successfull Meal Added", f"Your {meal_name} has been successfully added.")
        db.commit()
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(f"Error adding meal: {e}")
        return False
    
def updateMealPlan(user_id, plan_id, meal_id, mealName, dayOfWeek, mealTime):
    #Update meal plan by user ID
    db = get_db()
    cursor = db.cursor()
    
    try:
        if dayOfWeek not in getDays():
            mb.showerror("Invalid Day", f"{dayOfWeek} is not a valid day.")
            return False

        if mealTime not in getMealTime():
            mb.showerror("Invalid Meal Time", f"{mealTime} is not a valid mealtime.")
            return False
        
        cursor.execute("SELECT mealName FROM meal WHERE mealID = %s AND userID = %s", (meal_id, user_id))
        current_meal_name = cursor.fetchone()[0]

        if current_meal_name != mealName:
            # Create a new meal in meal table
            cursor.execute(
                "INSERT INTO meal (userID, mealName) VALUES (%s, %s)",
                (user_id, mealName)
            )
            new_meal_id = cursor.lastrowid
        else:
            # No change in meal name, keep existing mealID
            new_meal_id = meal_id

        cursor.execute("UPDATE mealplan SET mealID = %s WHERE userID = %s AND planID = %s AND dayOfWeek = %s AND mealTime = %s", (new_meal_id, user_id, plan_id, dayOfWeek, mealTime))
        mb.showinfo("Successfully Updated Meal Plan", f"Your {mealName} has been successfully added")

    except Exception as e:
        print(f"Error updating meal plan: {e}")
        return False
    db.commit()
    cursor.close()
    db.close()
    return True
    
def viewMeal(user_id):
    #View meals by user ID
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT m.dayOfWeek, m.mealTime, me.mealName
            FROM mealplan m
            JOIN meal me ON m.mealID = me.mealID
            WHERE m.userID = %s
            ORDER BY FIELD(m.dayOfWeek, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
            FIELD(m.mealTime, 'Breakfast', 'Lunch', 'Dinner')
    """, (user_id,))
    except Exception as e:
        print(f"Error retrieving meals: {e}")
        return []
    meals = cursor.fetchall()
    cursor.close()
    db.close()
    return meals

def getSuccessfulMealsCount(user_id):
    #Get count of successful meals (Eaten) for user ID
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM mealPlan 
            WHERE userID = %s AND status = 'Eaten'
        """, (user_id,))
        result = cursor.fetchone()
    except Exception as e:
        print(f"Error retrieving successful meals count: {e}")
        return 0
    cursor.close()
    db.close()
    return result[0] if result else 0  

def updateMealStatus(user_id, plan_id, new_status):
    db = None
    cursor = None
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
                UPDATE mealPlan
                SET status = %s
                WHERE userID = %s AND planID = %s
            """,
            (new_status, user_id, plan_id)
        )
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating meal status: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def getMealPlanToday(user_id, day_of_week, mealtime):
    #Get meal plan for today by user ID, day of week, and mealtime
    db = get_db()
    cursor = db.cursor()

    today = day_of_week.title()
    timeToday = mealtime.title()

    try:
        cursor.execute("""
            SELECT m.mealName 
            FROM mealPlan mp
            JOIN meal m ON mp.mealID = m.mealID
            WHERE mp.userID = %s AND mp.dayOfWeek = %s AND mp.mealTime = %s
        """, (user_id, today, timeToday))
        result = cursor.fetchone()
    except Exception as e:
        print(f"Error retrieving today's meal plan: {e}")
        return None
    cursor.close()
    db.close()
    if not result:
        return None
    meal_name, = result
    return meal_name

def getTodaysDayAndMealTime():
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT DAYNAME(CURDATE()), CASE WHEN HOUR(NOW()) < 12 THEN 'Breakfast' WHEN HOUR(NOW()) < 17 THEN 'Lunch' ELSE 'Dinner' END")
        result = cursor.fetchone()
    except Exception as e:
        print(f"Error retrieving today's day and meal time: {e}")
        return None
    cursor.close()
    db.close()
    return result if result else (None, None)

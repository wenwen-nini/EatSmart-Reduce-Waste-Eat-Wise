from config.db_config import get_db
from tkinter import messagebox as mb

def getGroceryByUser(user_id):
    #Get groceries by user ID // For Dashboard display
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT name, DATEDIFF(expirationDate, CURDATE()) AS days_left FROM grocery WHERE userID = %s ORDER BY expirationDate ASC", (user_id,))
    groceries = cursor.fetchall()
    cursor.close()
    db.close()
    return groceries

def getGroceryAll(user_id, category_id=None, search_text=""):
    #Get all groceries by user ID // For Grocery List display
    try:
        db = get_db()
        cursor = db.cursor()

        query = """
                 SELECT g.groceryID, g.name, g.quantity, c.categoryName, g.expirationDate, 
                     DATEDIFF(g.expirationDate, CURDATE()) AS days_left
            FROM grocery g
            LEFT JOIN category c ON g.categoryID = c.categoryID
            WHERE g.userID = %s
        """
        params = [user_id]

        if category_id:
            query += " AND g.categoryID = %s"
            params.append(category_id)

        if search_text:
            query += " AND g.name LIKE %s"
            params.append(f"%{search_text}%")

        query += " ORDER BY g.expirationDate ASC"

        cursor.execute(query, params)
        groceries = cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving groceries: {e}")
        return []

    cursor.close()
    db.close()
    return groceries

def addGrocery(user_id, name, quantity, category_id, expiration_date):
    #Add grocery item
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO grocery (userID, name, quantity, categoryID, expirationDate) VALUES (%s, %s, %s, %s, %s)",
            (user_id, name, quantity, category_id, expiration_date) 
        )
        mb.showinfo("Successfully Added Grocery Item", f"Your {name} has been successfully added.")
        db.commit()
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(f"Error adding grocery: {e}")
        return False
    
def updateGrocery(user_id, grocery_id, name, quantity, category_id, expiration_date):
    #Update grocery item
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE grocery SET name = %s, quantity = %s, categoryID = %s, expirationDate = %s WHERE groceryID = %s AND userID = %s",
            (name, quantity, category_id, expiration_date, grocery_id, user_id)
        )
        mb.showinfo("Successfully Updated Grocery Item", f"Your {name} has been succesfully added")
    except Exception as e:
        print(f"Error updating grocery: {e}")
        return False
    db.commit()
    cursor.close()
    db.close()
    return True

def deleteGrocery(user_id, grocery_id):
    #Delete grocery item
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM grocery WHERE groceryID = %s and userID = %s",
            (grocery_id, user_id)
        )
        mb.showinfo("Successfully Deleted Grocery Item", f"The item has been successfully deleted!")
    except Exception as e:
        print(f"Error deleting grocery: {e}")
        return False
    db.commit()
    cursor.close()
    db.close()
    return True

def getExpiredGroceryCount(user_id):
    #Get count of expired groceries for user
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT COUNT(*) 
            FROM grocery
            WHERE userID = %s AND expirationDate < CURDATE()
        """, (user_id,))
        result = cursor.fetchone()
        expired_count = result[0] if result else 0
    except Exception as e:
        print(f"Error retrieving expired grocery count: {e}")
        return 0
    cursor.close()
    db.close()
    return expired_count

def getExpiringSoonGrocery(user_id):
    #Get count of groceries expiring within 1 day for user
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT COUNT(*) 
            FROM grocery
            WHERE userID = %s 
            AND expirationDate >= CURDATE()
            AND expirationDate <= DATE_ADD(CURDATE(), INTERVAL 1 DAY)
        """, (user_id,))
        result = cursor.fetchone()
        expiring_soon_count = result[0] if result else 0
    except Exception as e:
        print(f"Error retrieving expiring soon grocery count: {e}")
        return 0
    cursor.close()
    db.close()
    return expiring_soon_count

def getCategoryForSearch(user_id):
    #Get the category's id and name by user
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT categoryID, categoryName FROM category ORDER BY categoryName")
        rows = cursor.fetchall()
    except Exception as e:
        print(f"Error retrieving categories: {e}")
        return None
    cursor.close()
    db.close()
    return rows
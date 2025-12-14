import mysql.connector # IMPORTS FOR CONNECTING MYSQL TO PYTHON

# Gets the database
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="eatsmart_db"
    )

# Creates the database if not exist
def create_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS eatsmart_db")
        conn.commit()
        cursor.close()
        conn.close()
        print("Database checked/created successfully!")
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")

current_user_id = 1

# Initializing the tables if not exist
def initialize_tables():

    try:
        db = get_db()
        cursor = db.cursor()

        # USERS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                userID INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE
            )
        """)

        # CATEGORY
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                categoryID INT AUTO_INCREMENT PRIMARY KEY,
                categoryName VARCHAR(100) NOT NULL UNIQUE
            )
        """)

        # GROCERY
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grocery (
                groceryID INT AUTO_INCREMENT PRIMARY KEY,
                userID INT,
                categoryID INT NULL,
                name VARCHAR(100) NOT NULL,
                quantity VARCHAR(50) NOT NULL DEFAULT 1,
                expirationDate DATE NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('Fresh', 'Expired') DEFAULT 'Fresh',
                FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE,
                FOREIGN KEY (categoryID) REFERENCES category(categoryID) ON DELETE SET NULL
            )
        """)

        # MEAL
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meal (
                mealID INT AUTO_INCREMENT PRIMARY KEY,
                userID INT,
                mealName VARCHAR(200) NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE
            )
        """)

        # MEAL PLAN
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mealPlan (
                planID INT AUTO_INCREMENT PRIMARY KEY,
                userID INT,
                mealID INT,
                dayOfWeek ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
                mealTime ENUM('Breakfast', 'Lunch', 'Dinner') NOT NULL,
                status ENUM('Pending', 'Eaten', 'Skipped') DEFAULT 'Pending',
                FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE,
                FOREIGN KEY (mealID) REFERENCES meal(mealID) ON DELETE CASCADE
            )
        """)

        # MEAL INGREDIENTS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meal_ingredients (
                ingredientID INT AUTO_INCREMENT PRIMARY KEY,
                mealID INT NOT NULL,
                groceryID INT NULL,
                ingredientName VARCHAR(200),
                quantityNeeded INT DEFAULT 1,
                FOREIGN KEY (mealID) REFERENCES meal(mealID) ON DELETE CASCADE,
                FOREIGN KEY (groceryID) REFERENCES grocery(groceryID) ON DELETE SET NULL
            )
        """)

        db.commit()
        cursor.close()
        db.close()
        print("Tables checked/added successfully!")
    except:
        print("Database not found! Please take time to read the readme.md File!")
        return

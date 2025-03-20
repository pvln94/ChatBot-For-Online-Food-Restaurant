# Author: Dhaval Patel. Codebasics YouTube Channel

import mysql.connector

global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Narasimha@123",
    database="pandeyji_eatery"
)

# Function to call the MySQL stored procedure and insert an order item
def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Committing the changes
        cnx.commit()
        cursor.close()

        print("Order item inserted successfully!")
        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")
        cnx.rollback()
        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        cnx.rollback()
        return -1

# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    try:
        cursor = cnx.cursor()
        insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, status))
        cnx.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting order tracking: {err}")
        cnx.rollback()

# Function to get the total order price
def get_total_order_price(order_id):
    try:
        cursor = cnx.cursor()
        query = "SELECT get_total_order_price(%s)"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"Error fetching total order price: {err}")
        return None

# Function to get the next available order_id
def get_next_order_id():
    try:
        cursor = cnx.cursor()
        query = "SELECT COALESCE(MAX(order_id), 0) + 1 FROM orders"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error fetching next order ID: {err}")
        return None

# Function to fetch the order status from the order_tracking table
def get_order_status(order_id):
    try:
        cursor = cnx.cursor()
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"Error fetching order status: {err}")
        return None

if __name__ == "__main__":
    print(get_next_order_id())

import sqlite3


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)


def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def create_product(connection, product: tuple):
    sql = '''INSERT INTO products 
    (product_title, price, quantity)
    VALUES (?, ?, ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, product)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def update_product_price(connection, product_id, new_price):
    sql = '''UPDATE products SET price = ? WHERE id = ? '''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (new_price, product_id))
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def update_product_quantity(connection, product_id, new_quantity):
    sql = '''UPDATE products SET quantity = ? WHERE id = ? '''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (new_quantity, product_id))
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def delete_product(connection, product_id):
    sql = '''DELETE FROM products WHERE id = ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (product_id,))
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def select_all_products(connection):
    sql = '''SELECT * FROM products'''
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for r in rows:
        print(r)


def search_product_by_title(connection, search_product):
    sql = '''SELECT * FROM products WHERE product_title LIKE ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, ('%' + search_product + '%',))
        rows = cursor.fetchall()
        if rows:
            print("Matching Products:")
            for row in rows:
                print(row)
        else:
            print("No matching products found.")
    except sqlite3.Error as e:
        print(e)


def select_product_by_quantity_and_price(connection, price, quantity):
    sql = '''SELECT * FROM products WHERE price < ? AND quantity > ?'''
    cursor = connection.cursor()
    cursor.execute(sql, (price, quantity,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)


connection = create_connection("phones.db")

sql_create_products_table = '''
CREATE TABLE IF NOT EXISTS products ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    product_title VARCHAR(200) NOT NULL,
    price DOUBLE(10, 2) NOT NULL DEFAULT 0.0,
    quantity INTEGER NOT NULL DEFAULT 0
);
'''


def print_products(connection):
    print('All Products:')
    select_all_products(connection)


def add_products(connection):
    products = [('Iphone XS', 50, 10), ('Iphone XR', 70, 4), ('Iphone SE', 30, 7), ('Iphone X', 60, 6),
                ('Iphone 11', 80, 12), ('Iphone 12', 90, 53), ('Iphone 13', 100, 34), ('Iphone 13 Pro', 120, 56),
                ('Iphone 13 Pro Max', 150, 60), ('Iphone 14', 160, 70), ('Iphone 14 Pro', 170, 80),
                ('Iphone 14 Pro Max', 200, 86),
                ('Iphone 15', 230, 90), ('Iphone 15 Pro', 250, 100), ('Iphone 15 Pro Max', 300, 120)]
    for product in products:
        create_product(connection, product)


if connection:
    print("Connection with DB was successful")
    create_table(connection, sql_create_products_table)
    select_all_products(connection)
    add_products(connection)
    update_product_quantity(connection, 5, 20)
    update_product_price(connection, 4, 900)
    delete_product(connection, 2)
    select_product_by_quantity_and_price(connection, 100, 5)
    search_product_by_title(connection, 'Pro Max')
    print_products(connection)
    connection.close()

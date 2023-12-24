import sqlite3

from datetime import datetime

db = sqlite3.connect('dostavka.db')
kavrak = db.cursor()

# Создание таблицы пользователя
kavrak.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name TEXT, phone_number TEXT, address TEXT, '
               'reg_date DATETIME);')

# Создание таблицы продуктов
kavrak.execute('CREATE TABLE IF NOT EXISTS products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT,'
               ' pr_name TEXT, pr_price REAL, pr_quantity INTEGER, pr_des TEXT, pr_photo TEXT, reg_date DATETIME);')

# Создание таблицы для корзины пользователя
kavrak.execute('CREATE TABLE IF NOT EXISTS user_cart (user_id INTEGER, user_product TEXT, quantity INTEGER,'
               'total_for_price REAL);')


# Регистрация пользователя
def register_user(tg_id, name, phone_number, address):
    with sqlite3.connect('dostavka.db') as db:
        kavrak = db.cursor()

# Добавляем пользователя в базу данных
    kavrak.execute('INSERT INTO users (tg_id, name, phone_number, address, reg_date) VALUES '
                   '(?, ?, ?, ?, ?);', (tg_id, name, phone_number, address, datetime.now()))

    db.commit()


# Проверяем пользователя есть ли такой id в нашей базе данных
def check_user(user_id):
    with sqlite3.connect('dostavka.db') as db:
        kavrak = db.cursor()

    checker = kavrak.execute('SELECT tg_id FROM users WHERE tg_id=?;', (user_id,))

    if checker.fetchone():
        return True
    else:
        return False


# Добавления продукта в таблицу products
def add_product(pr_name, pr_price, pr_quantity, pr_des, pr_photo):
    with sqlite3.connect('dostavka.db') as db:
        kavrak = db.cursor()

    kavrak.execute('INSERT INTO products (pr_name, pr_price, pr_quantity, pr_des, pr_photo, reg_date) VALUES '
                   '(?, ?, ?, ?, ?, ?);', (pr_name, pr_price, pr_quantity, pr_des, pr_photo, datetime.now()))

    db.commit()


# Получаем все продукты из базы только его (name, id)
def get_pr_name_id():
    with sqlite3.connect('dostavka.db') as db:
        kavrak = db.cursor()

    products = kavrak.execute('SELECT pr_id, pr_name, pr_quantity FROM products;').fetchall()

    sorted_products = [(i[1], i[0]) for i in products if i[2] > 0]

    return sorted_products


def get_pr_id():
    with sqlite3.connect('dostavka.db') as db:
        kavrak = db.cursor()

    products = kavrak.execute('SELECT pr_id, pr_quantity FROM products;').fetchall()
    sorted_products = [(i[0]) for i in products if i[1] > 0]

    return sorted_products


# Получить информацию про определенный продукт через его pr_id
def get_product_id(pr_id):
    with sqlite3.connect('dostavka.db') as db:
        kavrak = db.cursor()

    product_id = kavrak.execute('SELECT * FROM products WHERE pr_id=?;', (pr_id,)).fetchone()[2]
    db.close()
    return product_id


# Добавления продуктов в корзину
def add_product_to_cart(user_id, user_product, quantity):
    with sqlite3.connect('dostavka.db') as db:
        kavrak = db.cursor()

    product_price = get_product_id(user_product)
    print(product_price)

    kavrak.execute('INSERT INTO user_cart(user_id, user_product, quantity, total_for_price)'
                   'VALUES (?, ?, ?, ?);', (user_id, user_product, quantity, quantity * product_price))

    db.commit()


# Удаление продуктов из корзины
def delete_product_from_cart(user_id):
    with sqlite3.connect('dostavka.db') as db:
        kavrak = db.cursor()

    # Удалить продукт из корзины через pr_id(продукт айди)
    kavrak.execute('DELETE FROM user_cart WHERE user_id=?;', (user_id,))



def get_exact_user_cart(user_id):

    connection = sqlite3.connect('dostavka.db')

    sql = connection.cursor()

    user_cart = sql.execute('SELECT products.pr_name, user_cart.quantity, user_cart.total_for_price '
                            'FROM products INNER JOIN user_cart ON products.pr_id=user_cart.user_product '
                            'WHERE user_cart.user_id=?;',
                            (user_id,)).fetchall()
    print(user_cart)

    return user_cart

# Получить номер телефона и имя пользователя
def get_user_number_name(user_id):

    connection = sqlite3.connect('dostavka.db')

    sql = connection.cursor()

    exact_user = sql.execute('SELECT name, phone_number FROM users WHERE tg_id=?;', (user_id,))

    return exact_user.fetchone()




# функция для обновления адреса пользователя

def update_user_address(user_id, address):
    db = sqlite3.connect('dostavka.db')
    kavrak = db.cursor()
    kavrak.execute('UPDATE users SET address=? WHERE tg_id=?;', (address, user_id))
    db.commit()
    db.close()



# Функция поиска товара по имени

def get_product_by_name(product_name):
    connection = None
    try:
        connection = sqlite3.connect('database.db')
        kavrak = connection.cursor()
        kavrak.execute("SELECT * FROM products WHERE pr_name=?", (product_name,))
        return kavrak.fetchone()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()



# Удаление продуктов по имени
def delete_product(pr_name):
    connection = None
    try:
        connection = sqlite3.connect('dostavka.db')
        kavrak = connection.cursor()

        # Удалить продукт по имени
        kavrak.execute('DELETE FROM products WHERE pr_name=?;', (pr_name,))
        print('Товввра удален')
        # Сохранить изменения
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

def get_user_location(user_id):
    with sqlite3.connect('dostavka.db') as db:
        kavrak = db.cursor()

    location = kavrak.execute('SELECT address FROM users WHERE tg_id=?;', (user_id,)).fetchone()

    return location[0] if location else None


def get_product_by_id(pr_id):
    with sqlite3.connect('dostavka.db') as db:
        kavrak = db.cursor()

    product_info = kavrak.execute('SELECT * FROM products WHERE pr_id=?;', (pr_id,)).fetchone()
    db.close()
    return product_info

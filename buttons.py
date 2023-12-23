from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# Кнопки со всеми продуктами(основное меню)
def main_menu_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Заказать товар🛍"))
    markup.add(types.KeyboardButton("Поддержка❓"))
    return markup

def main_menu(get_pr_name_id):
    # Создаем пространство для кнопок
    buttons = InlineKeyboardMarkup(row_width=2)

    # Создаем кнопки (несгорамые)
    order = InlineKeyboardButton(text='Оформить заказ', callback_data='order')
    cart = InlineKeyboardButton(text='Корзина🛒', callback_data='cart')

    buttons.row(order)
    buttons.row(cart)
    return buttons

def products(get_pr_name_id):
    # Генерация кнопок с товарами(базы данных)
    all_products = [InlineKeyboardButton(text=f'{i[0]}', callback_data=i[1]) for i in get_pr_name_id]
    print(all_products)

    #Обединить наши кнопки с пространством
    buttons = InlineKeyboardMarkup()
    buttons.add(*all_products)

    return buttons

# Кнопки для выбора кол-во
def choose_product_count(plus_or_minus='', current_amount=1):
    # Создаем пространство для кнопок
    buttons = InlineKeyboardMarkup(row_width=3)

    # Несгораемые кнопки
    back = InlineKeyboardButton(text='Назад', callback_data='back')
    plus = InlineKeyboardButton(text='+', callback_data='plus')
    minus = InlineKeyboardButton(text='-', callback_data='minus')
    count = InlineKeyboardButton(text=str(current_amount), callback_data=str(current_amount))
    cart = InlineKeyboardButton(text='Добавить в корзину', callback_data='to_cart')

    #Отслеживать плюс или минус
    if plus_or_minus == 'plus':
        new_amount = int(current_amount) + 1
        print(f' plus{new_amount}')

        count = InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
        print(f" vixod {count}")

    elif plus_or_minus == 'minus':
        if int(current_amount) > 1:
            new_amount = int(current_amount) - 1
            print(f' minus{new_amount}')

            count = InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
            print(f" vixod {count}")

    # Обединить кнопки с пространством
    buttons.add(minus, count, plus)
    buttons.row(cart)
    buttons.row(back)

    return buttons

# кнопки что бы подтвердить заказ
def get_accept():
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton('Подтвердить')
    no = KeyboardButton('Отменить')

    buttons.add(yes, no)

    return buttons

# Кнопка для перехода в корзину
def get_cart():
    buttons = InlineKeyboardMarkup(row_width=1)

    clear_cart = InlineKeyboardButton(text='Очистить корзину', callback_data='clear_cart')
    order = InlineKeyboardButton(text='Оформить заказ', callback_data='order')
    back = InlineKeyboardButton(text='Назад', callback_data='back')

    buttons.add(clear_cart, order, back)

    return buttons



def number_buttons():
    # Создать пространство для кнопок
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    num_button = types.KeyboardButton('Поделиться контактом', request_contact=True)

    buttons.add(num_button)

    return buttons


def geo_buttons():
    # Создать пространство для кнопок
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    g_button = types.KeyboardButton('Поделиться локацией', request_location=True)

    buttons.add(g_button)

    return buttons

# кнопки для подтверждения заказа
def get_accept_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton('Подтвердить')
    no = KeyboardButton('Отменить')

    kb.add(yes, no)

    return kb
# Подтверждение в группе
def accept_or_cancel():
    kb = InlineKeyboardMarkup(row_width=2)
    accept_button = InlineKeyboardButton('Принять заказ', callback_data='accept_order')
    cancel_button = InlineKeyboardButton('Отменить заказ', callback_data='cancel_order')
    kb.add(accept_button, cancel_button)
    return kb
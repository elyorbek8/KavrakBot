import telebot
import buttons
import database
from telebot import types
from database import get_exact_user_cart, get_user_number_name
import requests

GOOGLE_MAPS_API_KEY = 'AIzaSyD7WKNnIQITdsoZNp28W5mDXkOCXslnmNo'

bot = telebot.TeleBot('6733360508:AAGzdnGvr8nUJoC8T6TkJ2dan9idjzd8nEs')


users = {}



#database.delete_product('SANTA')
database.add_product('SANTA', 250.000, 1000, 'САНТА САНТА ТЕБЯ ПОЗДРАВИТ САНТА', 'media/SANTA.jpg')
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    checker = database.check_user(user_id)

    if checker:
        products = database.get_pr_name_id()
        bot.send_message(user_id, 'Привет', reply_markup=buttons.main_menu_buttons())
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu(products))
    elif not checker:
        bot.send_message(user_id, 'Привет, отправьте свое имя')
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    username = message.text
    bot.send_message(user_id, 'Отправьте свою локацию', reply_markup=buttons.geo_buttons())
    bot.register_next_step_handler(message, handle_location, username)


# Обработчик локации при регистрации
def handle_location(message, username):
    user_id = message.from_user.id
    if message.location:
        lat = message.location.latitude
        long = message.location.longitude

        # Запрос к Google Places API для получения названия места по координатам
        place_name = get_place_name_from_coordinates(lat, long)

        # Добавление адреса пользователя в базу данных
        database.update_user_address(user_id, place_name)

        bot.send_message(user_id, f'Ваша локация: {place_name} \nОтправьте свой номер телефона', reply_markup=buttons.number_buttons())
        bot.register_next_step_handler(message, get_number, username)
    else:
        bot.send_message(user_id, 'Отправьте вашу локацию', reply_markup=buttons.geo_buttons())
        bot.register_next_step_handler(message, handle_location, username)

def get_place_name_from_coordinates(latitude, longitude):
    # Формирование запроса к Google Places API для получения названия места по координатам
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GOOGLE_MAPS_API_KEY}'
    response = requests.get(url)
    data = response.json()

    # Проверяем, есть ли результаты и название места
    if 'results' in data and data['results']:
        place_name = data['results'][0]['formatted_address']
        return place_name
    else:
        return 'Unknown Place'

def get_number(message, name):
    user_id = message.from_user.id

    if message.contact:
        # сохраняем контакт
        phone_number = message.contact.phone_number


        # Сохраняем его в базе
        database.register_user(user_id, name, phone_number, 'Not yet')
        bot.send_message(user_id, f'Вы успешно зарегистрировались {name}',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu_buttons())

    # если пользователь не отправил контакт
    elif not message.contact:
        bot.send_message(user_id, 'Отправьте контакт с помощью кнопки', reply_markup=buttons.number_buttons())

        # Обратно на этап получения номера
        bot.register_next_step_handler(message, get_number, name)

# Заказать товар
@bot.message_handler(func=lambda message: message.text == "Заказать товар🛍")
def show_pr(message):
    user_id = message.from_user.id
    checker = database.check_user(user_id)

    if checker:
        products = database.get_pr_name_id()
        bot.send_message(user_id, 'Выберите товар', reply_markup=buttons.products(products))
    elif not checker:
        bot.send_message(user_id, 'Вы не зарегистрированы, отправьте свое имя')
        bot.register_next_step_handler(message, get_name)


# Функция для обработки кнопки Поддержка❓
@bot.message_handler(func=lambda message: message.text == "Поддержка❓")
def show_support(message):
    user_id = message.from_user.id
    checker = database.check_user(user_id)

    if checker:
        bot.send_message(message.chat.id, f"Поддержка: @Elyorbek_2708")
    elif not checker:
        bot.send_message(user_id, 'Вы не зарегистрированы, отправьте свое имя')
        bot.register_next_step_handler(message, get_name)



# Обработчик команды "Корзина"
# Обработчик команды "Корзина"
@bot.message_handler(func=lambda message: message.text == "Корзина🛒")
def handle_cart(message):
    user_id = message.from_user.id
    checker = database.check_user(user_id)

    if checker:
        user_cart = get_exact_user_cart(user_id)
        if user_cart:
            cart_text = "Ваша корзина:\n"
            for item in user_cart:
                cart_text += f"{item[0]} - {item[1]} шт. - {item[2]} сум.\n"

            user_info = get_user_number_name(user_id)
            user_name = user_info[0] if user_info else "Уважаемый клиент"
            cart_text += f"\nИтого к оплате: {sum([item[2] for item in user_cart])} сум.\n"
            cart_text += f"\n{user_name}, Оформите заказ, чтобы продолжить."

            bot.send_message(user_id, cart_text, reply_markup=buttons.get_cart())
        else:
            bot.send_message(user_id, "Ваша корзина пуста. Закажите товар, чтобы добавить его в корзину.")
    elif not checker:
        bot.send_message(user_id, 'Вы не зарегистрированы, отправьте свое имя')
        bot.register_next_step_handler(message, get_name)

# Обработчик выбора количества
@bot.callback_query_handler(lambda call: call.data in ['plus', 'minus', 'to_cart', 'back'])
def get_user_product_count(call):
    # Сохраним айди пользователя
    user_id = call.message.chat.id

    # Если пользователь нажал на +
    if call.data == 'plus':
        print(users)
        actual_count = users[user_id]['pr_count']
        print(actual_count)
        print(call)
        users[user_id]['pr_count'] += 1
        # Меняем значение кнопки
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count('plus', actual_count))

    # Если пользователь нажал на -
    elif call.data == 'minus':
        print(users)
        actual_count = users[user_id]['pr_count']
        print(actual_count)
        print(call)
        users[user_id]['pr_count'] -= 1
        # Меняем значение кнопки
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count('minus', actual_count))

    # back
    # Если пользователь нажал 'назад'
    elif call.data == 'back':
        # Получаем меню
        products = database.get_pr_name_id()
        # меняем на меню
        bot.edit_message_text('Выберите пункт меню',
                              user_id,
                              call.message.message_id,
                              reply_markup=buttons.main_menu(products))

    # Если нажал Добавить в корзину
    elif call.data == 'to_cart':
        # Получаем данные
        product_count = users[user_id]['pr_count']
        user_product = users[user_id]['pr_name']
        print(users)
        # Добавляем в базу(корзина пользователя)
        database.add_product_to_cart(user_id, user_product, product_count)

        # Получаем обратно меню
        products = database.get_pr_name_id()
        # меняем на меню
        bot.edit_message_text('Продукт добавлен в корзину\nЧто-нибудь еще?',
                              user_id,
                              call.message.message_id,
                              reply_markup=buttons.main_menu(products))



@bot.callback_query_handler(lambda call: call.data in ['order', 'cart', 'clear_cart'])
def main_menu_handle(call):
    user_id = call.message.chat.id
    message_id = call.message.message_id
    products = database.get_pr_name_id()
    # Если нажал на кнопку: Оформить заказ
    if call.data == 'order':
        # Удалим сообщение с верхними кнопками
        bot.delete_message(user_id, message_id)
        user_cart = database.get_exact_user_cart(user_id)

        # формируем сообщение со всеми данными
        full_text = 'Ваш заказ:\n\n'
        user_info = database.get_user_number_name(user_id)
        print(user_info)
        full_text += f'Имя: {user_info[0]}\nНомер телефона: {user_info[1]}\n\n'
        total_amount = 0

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]

        # Итог и Адрес
        full_text += f'\nИтог: {total_amount}'

        bot.send_message(user_id, full_text, reply_markup=buttons.get_accept_kb())
        # Переход на этап подтверждение
        bot.register_next_step_handler(call.message, get_accept,  full_text)

    # Если нажал на кнопку "Корзина"
    elif call.data == 'cart':
        # получим корзину пользователя
        user_cart = database.get_exact_user_cart(user_id)

        # формируем сообщение со всеми данными
        full_text = 'Ваша корзина:\n\n'
        total_amount = 0

        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]

        # Итог
        full_text += f'\nИтог: {total_amount}'

        # отправляем ответ пользователю
        bot.edit_message_text(full_text,
                              user_id,
                              message_id,
                              reply_markup=buttons.get_cart())

    # Если нажал на очистить корзину
    elif call.data == 'clear_cart':
        # вызов функции очистки корзины
        database.delete_product_from_cart(user_id)

        # отправим ответ
        bot.edit_message_text('Ваша корзина очищена',
                              user_id,
                              message_id,
                              reply_markup=buttons.main_menu(database.get_pr_name_id()))




# Функции подтвердить отменить заказ

@bot.callback_query_handler(lambda call: call.data in ['accept_order', 'cancel_order'])
def handle_order_actions(call):
    user_id = call.message.chat.id


    if call.data == 'accept_order':
        # Отправить пользователю сообщение о том, что заказ принят
        bot.send_message(user_id, 'Заказ принят. Оператор свяжется с вами в ближайшее.', reply_markup=types.ReplyKeyboardRemove())


    elif call.data == 'cancel_order':
        bot.send_message(user_id, 'Заказ отменен : Товар закончился')



# функция сохранения статуса заказа
def get_accept(message, full_text):
    user_id = message.from_user.id
    message_id = message.message_id
    user_answer = message.text

    # Получение локации пользователя
    user_location = database.get_user_location(user_id)

    # получим все продукты из базы для кнопок
    products = database.get_pr_name_id()

    # Если пользователь нажал "подтвердить"
    if user_answer == 'Подтвердить':
        GROUP_CHAT_ID = -1002088545962
        # очистить корзину пользователя
        database.delete_product_from_cart(user_id)
        # Отправить сообщение в группу с информацией о заказе и локацией пользователя
        order_message = f"ОФОРМЛЕН ЗАКАЗ\n{full_text}\nЛокация: {user_location}"
        bot.send_message(GROUP_CHAT_ID, order_message, reply_markup=buttons.accept_or_cancel())

        # отправим ответ
        bot.send_message(user_id, 'Заказ оформлен', reply_markup=types.ReplyKeyboardRemove())

    elif user_answer == 'Отменить':
        # отправим ответ
        bot.send_message(user_id, 'Заказ отменен', reply_markup=types.ReplyKeyboardRemove())

    # Обратно в меню
    bot.send_message(user_id, 'Выберите пункт меню', reply_markup=buttons.main_menu_buttons())




        # Обработчик выбора товара
@bot.callback_query_handler(lambda call: int(call.data) in database.get_pr_id())
def get_user_product(call):
    # Сохраним айди пользователя
    user_id = call.message.chat.id

    # Сохраним продукт во временный словарь
    # call.data - значение нажатой кнопки(инлайн)
    users[user_id] = {'pr_name': call.data, 'pr_count': 1}

    # Получаем информацию о продукте по его id
    product_info = database.get_product_by_id(call.data)
    product_name = product_info[1]
    product_description = product_info[4]
    product_price = product_info[2]

    # Отправляем фото и информацию о продукте
    photo_path = product_info[5]
    photo = open(photo_path, 'rb')
    bot.send_photo(user_id, photo, caption=f'{product_name}\n{product_description}\nЦена: {product_price}00Cум.',
                   reply_markup=buttons.choose_product_count())



bot.infinity_polling()

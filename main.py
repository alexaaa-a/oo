import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage=StateMemoryStorage()

bot=telebot.TeleBot("6334680461:AAG4YVUcBBwhlDzhm9Q9DEP7Ia43KWZ5ltw",
                    state_storage=state_storage, parse_mode="Markdown")

class PollState(StatesGroup):
    name=State()
    age=State()
    v=State()

class HelpState(StatesGroup):
    wait_text=State()

text_poll="опрос"
text_button_1="Нажмите, если хотите узнать чем я обычно занимаюсь."
text_button_2="Нажмите, если хотите кратко узнать обо мне."
text_button_3="Нажмите, если хотите больше узнать обо мне."

menu_keyboard=telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_3
    )
)

@bot.message_handler(state="*", commands='start')
def start_ex(message):
    bot.send_message(
        message.chat.id,
        "Привет, что будем делать?",
        reply_markup=menu_keyboard
    )

@bot.message_handler(func=lambda message: text_poll==message.text)
def first(message):
    bot.send_message(message.chat.id, "Супер, *Ваше* _имя_?")
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)

@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name']=message.text
    bot.send_message(message.chat.id, "Супер, Ваш возраст?")
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)

@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age']=message.text
    bot.send_message(message.chat.id, "Круто, а Вы хотите подкачаться?")
    bot.set_state(message.from_user.id, PollState.v, message.chat.id)

@bot.message_handler(state=PollState.v)
def v(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['v']=message.text
    bot.send_message(message.chat.id, "Если да, то предлагаю вам [этот сайт](https://builderbody.ru/?ysclid=lnuicqsdo0681821571). Если нет, то можете пропустить")
    bot.set_state(message.from_user.id, message.chat.id)

@bot.message_handler(func=lambda message: text_button_1==message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Я люблю заниматься программированием и лыжными гонками", reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_button_2==message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Меня зовут Александр. Мне 16 лет. Я занимаюсь программированием(прошёл курс по Python от ТГУ). Занимаюсь лыжными гонками и имею 1 спортивный разряд по ним, а также дополнительно занимаюсь в спортзале", reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_button_3==message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Чтобы узнавать о моей жизни больше, подписывайтесь на [мой тг-канал](https://t.me/shurik297)", reply_markup=menu_keyboard)

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
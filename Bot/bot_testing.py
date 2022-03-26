import telebot
from telebot import types

from KEYS import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)


# Bot's logic

# BOT INTRO on Greeting

# STEP 0: Get Underlying from the user

# OPTION 1
# Summary Functionality
# C or P / C & P Highest Daily Volume
# C vs P Parity in % (Daily Volume)
# C or P / C & P / Expiration Date Highest OI
#  
# 


# OPTION 2
# Plotting Functionality

# {} <- Chosen by user

# 1 => Volatility Smile ATM
# {C or P} / {C vs. Put} * 
# Period {3M / 6M / 1Y / 1Y6M / 2Y / Max}

# 2 => Metrics
# P / C / P vs.C
# {Strike Range}
# {Specific DOE} OR {3M / 6M / 1Y / 1Y6M / 2Y / Max}
# Metric {Nominal Price / OI / Vol / IV / delta / gamma / vega / theta / rho}


# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	bot.send_message(message.chat.id ,text = "Assalam Aleykum!")


# Handles all text messages that match the regular expression
@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):
	pass

# Handles all messages for which the lambda returns True
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
	pass

# Which could also be defined as:
def test_message(message):
	return message.document.mime_type == 'text/plain'

@bot.message_handler(func=test_message, content_types=['document'])
def handle_text_doc(message):
	pass

# Handlers can be stacked to create a function which will be called if either message_handler is eligible
# This handler will be called if the message starts with '/hello' OR is some emoji
@bot.message_handler(commands=['hello'])
@bot.message_handler(func=lambda msg: msg.text.encode("utf-8") == SOME_FANCY_EMOJI)
def send_something(message):
    pass



# Custom Response Keyboard Layouts

# markup = types.ReplyKeyboardMarkup()
# itembtna = types.KeyboardButton('')
# itembtnv = types.KeyboardButton('v')
# itembtnc = types.KeyboardButton('c')
# itembtnd = types.KeyboardButton('d')
# itembtne = types.KeyboardButton('e')
# markup.row(itembtna, itembtnv)
# markup.row(itembtnc, itembtnd, itembtne)
# # tb.send_message(chat_id, "Choose one letter:", reply_markup=markup)


# Infinite polling (Does not quit on errors)
bot.infinity_polling()
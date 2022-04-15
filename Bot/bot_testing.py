# Bot server / Python + API library


from email import message
import telebot
from telebot import types

from KEYS import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)


# Bot's logic

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['menu', 'help'])
def handle_start_help(message):
	bot.send_message(message.chat.id ,text = "Assalam Aleykum!")


# "Menu" -> Plotting / Statistics

# Menu defined
markup = types.ReplyKeyboardMarkup()
itembtna = types.KeyboardButton('Plotting')
itembtnv = types.KeyboardButton('Statistics')
itembtnc = types.KeyboardButton('Cancel')
markup.row(itembtna, itembtnv)
markup.row(itembtnc)



@bot.message_handler(commands=['start'])
def handle_menu_call(message):
	reply = bot.send_message(message.chat.id, "What would you like to see?:", reply_markup = markup)
	bot.register_next_step_handler(reply, markup_handler)

# Prompt user to enter the ticker symbol	
def getUnderlying(message):
	bot.send_message(message.chat.id, "Enter the Ticker Symol preceded by #:")

def plottingHandler(message):
	getUnderlying(message)

def statsHandler(message):
	getUnderlying(message)

def markup_handler(message):

	if(message.text == 'Plotting'):
		plottingHandler(message)

	elif (message.text == 'Statistics'):
		plottingHandler(message)



# PLOTTING -> Get Underlying

# -> Data (ATM) / DOE (1 curve)

# -> Data (Strike Range) ()


# Receive a ticker
@bot.message_handler(func = lambda msg: '#' == msg.text[0])
def getTicker(message):
	bot.send_message(message.chat.id, 'KOK!')




# STATISTICS -> Get Underlying
# Most Traded table
# Put/call parity
# 



# "About" -> Bot's Intro



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



# Infinite polling (Does not quit on errors)
bot.infinity_polling()
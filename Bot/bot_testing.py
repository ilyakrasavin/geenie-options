
import telebot
from telebot import types

from KEYS import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)


# STORE THE PROGRAM STATE on EXECUTION:

# Plotting Mode (0 - uninitialized / 1 - DOExATM / 2 - DOExStrikeRange / 4 - Statistics)

class SessionState:

	def __init__(self):
		self.sessionTicker = ""
		self.requestMode = 0
		self.isComplete = False

		# Common Attributes:
		self.o_type = ""
		self.doe_type = ""
		self.doe_args = ""
		self.metric = ""

		# Specific Attributes
		self.atm_px = 0
		self.strike_range = (0, 0)


	def verify(self):
		if(self.sessionTicker != ""):
			print("KOKKUSIKI")
		

	def reset(self):
		self.__init__()



session = SessionState()
session.__init__()



# Bot's logic

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['menu', 'help'])
def handle_start_help(message):
	bot.send_message(message.chat.id ,text = "Assalam Aleykum!")


# "Menu" -> Plotting / Statistics

# Main Menu buttons
markup = types.ReplyKeyboardMarkup()
itembtna = types.KeyboardButton('Plotting')
itembtnv = types.KeyboardButton('Statistics')
itembtnc = types.KeyboardButton('Cancel')
markup.row(itembtna, itembtnv)
markup.row(itembtnc)

# Plotting Menu Step 1:

plot_markup1 = types.ReplyKeyboardMarkup()
plotmenu_btn1 = types.KeyboardButton("DOE x ATM")
plotmenu_btn2 = types.KeyboardButton("DOE x Strike Range")
plotmenu_btn3 = types.KeyboardButton("Cancel")
plot_markup1.row(plotmenu_btn1)
plot_markup1.row(plotmenu_btn2)
plot_markup1.row(plotmenu_btn3)


# Plotting DOE Mode setting markup
plot_doe_markup = types.ReplyKeyboardMarkup()
doe_button1 = types.KeyboardButton("Exact")
doe_button2 = types.KeyboardButton("Range")
doe_button3 = types.KeyboardButton("Quarterly")
doe_button4 = types.KeyboardButton("Weekly")
doe_button5 = types.KeyboardButton("Cancel")
plot_doe_markup.row(doe_button1, doe_button2)
plot_doe_markup.row(doe_button3, doe_button4)
plot_doe_markup.row(doe_button5)


# Plotting DOE Metric setting Markup
plot_metrics_markup = types.ReplyKeyboardMarkup()
metric_button1 = types.KeyboardButton("Spot Px")
metric_button2 = types.KeyboardButton("OI")
metric_button3 = types.KeyboardButton("Volume")
metric_button4 = types.KeyboardButton("IV")
metric_button5 = types.KeyboardButton("Greeks")
metric_button6 = types.KeyboardButton("Cancel")

plot_metrics_markup.row(metric_button1, metric_button2)
plot_metrics_markup.row(metric_button3, metric_button4)
plot_metrics_markup.row(metric_button5)
plot_metrics_markup.row(metric_button6)


# Contract Type markup
contractType_markup = types.ReplyKeyboardMarkup()
typeButton1 = types.KeyboardButton("Call")
typeButton2 = types.KeyboardButton("Put")
typeButton3 = types.KeyboardButton("Call & Put")
typeButton4 = types.KeyboardButton("Cancel")

contractType_markup.row(typeButton1, typeButton2)
contractType_markup.row(typeButton3)
contractType_markup.row(typeButton4)


@bot.message_handler(commands=['start'])
def handle_menu_call(message):
	reply = bot.send_message(message.chat.id, "Please choose an option:", reply_markup = markup)
	bot.register_next_step_handler(reply, mainMenu_handler)

def getUnderlying(message):
	bot.send_message(message.chat.id, "Enter the Ticker Symol preceded by #:")


def plottingHandler(message):
	getUnderlying(message)

def statsHandler(message):
	getUnderlying(message)


def mainMenu_handler(message):

	if(message.text == 'Plotting'):
		session.requestMode = 1
		plottingHandler(message)

	elif (message.text == 'Statistics'):
		session.requestMode = 2
		statsHandler(message)

	elif (message.text == 'Cancel'):
		session.reset()
		bot.send_message(message.chat.id, "Aborted")


# Store the data in the session class
def plotMenu_contractTypeHandler(message):
	if(message.text == "Call"):
		session.o_type = "C"
		plotMenu_handler(message)

	elif(message.text == "Put"):
		session.o_type = "P"
		plotMenu_handler(message)

	elif(message.text == "Call & Put"):
		session.o_type = "B"
		plotMenu_handler(message)

	elif(message.text == "Cancel"):
		session.reset()
		bot.send_message(message.chat.id, "Aborted")
		

# Collect input from Plotting Menu
def plotMenu_handler(message):
	reply = bot.send_message(message.chat.id, "Select Plotting Mode", reply_markup = plot_markup1)
	bot.register_next_step_handler(reply, plotMenu_DOEHandler)


def plotMenu_lvl2_handler(message):
	reply = bot.send_message(message.chat.id, "Select DOE", reply_markup = contractType_markup)
	bot.register_next_step_handler(reply, plotMenu_DOEArgHandler)


def plotMenu_DOEHandler(message):
	if(message.text == "DOE x ATM"):
		session.requestMode = 1
		plotMenu_lvl2_handler(message)

	elif(message.text == "DOE x Strike Range"):
		session.requestMode = 2
		plotMenu_lvl2_handler(message)

	elif(message.text == "Cancel"):
		session.reset()
		bot.send_message(message.chat.id, "Aborted")


def plotMenu_DOEArgHandler(message):
	if(message.text == "Exact"):
		session.doe_type = "Exact"
		exactDOEhandler(message)

	elif(message.text == "Range"):
		session.doe_type = "Range"
		rangeDOEhandler(message)

	elif(message.text == "Quarterly"):
		session.doe_type = "Quarterly"
		otherDOEhandler(message)

	elif(message.text == "Weekly"):
		session.doe_type = "Weekly"
		otherDOEhandler(message)

	elif(message.text == "Cancel"):
		session.reset()
		bot.send_message(message.chat.id, "Aborted")


def exactDOEhandler(message):
	bot.send_message(message.chat.id, "Provide Exact DOE in YY-MM-DD format")

def rangeDOEhandler(message):
	yield

def otherDOEhandler(message):
	yield 


@bot.message_handler(func = lambda msg: msg.text[2] == '-' and session.isComplete == False)
def getExactDOE(message):
	assert(session.doe_type == "Exact")
	session.doe_args = message.text
	plotMenu_MetricHandler(message)



def plotMenu_MetricHandler(message):
	reply = bot.send_message(message.chat.id, "Plot:", reply_markup = plot_metrics_markup)
	bot.register_next_step_handler(reply, result_handler)	


def plotMenu_StrikeRangeHandler(message):
	yield


def result_handler(message):
	yield


# Receive a ticker when uninitialized
@bot.message_handler(func = lambda msg: '#' == msg.text[0] and session.sessionTicker == "")
def getTicker(message):
	bot.send_message(message.chat.id, 'KOK!')

	# Initialize the session state	
	session.sessionTicker = message.text[1:]

	reply = bot.send_message(message.chat.id, "Select Contract Type:", reply_markup = contractType_markup)
	bot.register_next_step_handler(reply, plotMenu_contractTypeHandler)





# STATISTICS -> Get Underlying
# Most Traded table
# Put/call parity


# "About" -> Bot's Intro



# # Handles all text messages that match the regular expression
# @bot.message_handler(regexp="SOME_REGEXP")
# def handle_message(message):
# 	pass



# # Handles all messages for which the lambda returns True
# @bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
# def handle_text_doc(message):
# 	pass

# # Which could also be defined as:
# def test_message(message):
# 	return message.document.mime_type == 'text/plain'

# @bot.message_handler(func=test_message, content_types=['document'])
# def handle_text_doc(message):
# 	pass


# # Handlers can be stacked to create a function which will be called if either message_handler is eligible
# # This handler will be called if the message starts with '/hello' OR is some emoji
# @bot.message_handler(commands=['hello'])
# @bot.message_handler(func=lambda msg: msg.text.encode("utf-8") == SOME_FANCY_EMOJI)
# def send_something(message):
#     pass



# Infinite polling (Does not quit on errors)
bot.infinity_polling()

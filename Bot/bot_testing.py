# Telegram Bot API

import telebot
from telebot import types

# Keyboard Markup Layouts
from markup import * 

from KEYS import API_TOKEN



# STORE THE PROGRAM STATE on EXECUTION:

# Plotting Mode (0 - uninitialized / 1 - DOExATM / 2 - DOExStrikeRange / 3 - Statistics)

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

		tickerCond = self.sessionTicker != 0
		reqCond = self.requestMode != 0
		typeCond = self.o_type != ""
		doe_tCond = self.doe_type != ""
		doe_aCond = self.doe_args != ""
		metCond = self.metric != ""

		atmCond = self.atm_px != 0
		strRangeCond = self.strike_range != (0, 0)

		if(self.requestMode == 1 and tickerCond and reqCond and typeCond
								and doe_tCond and doe_aCond and metCond
								and atmCond and (not strRangeCond)):
			self.isComplete = True
			return True

		elif(self.requestMode == 2 and tickerCond and reqCond and typeCond
								and doe_tCond and doe_aCond and metCond
								and (not atmCond) and strRangeCond):

			self.isComplete = True
			return True

		elif(self.requestMode == 3):
			return False

		else:
			return False


	def reset(self):
		self.__init__()



# Initialize the bot and Session State
bot = telebot.TeleBot(API_TOKEN)

session = SessionState()
session.__init__()




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
	reply = bot.send_message(message.chat.id, "Select DOE", reply_markup = plot_doe_markup)
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
	reply = bot.send_message(message.chat.id, "Please choose the range:", reply_markup = doe_range_markup)
	bot.register_next_step_handler(reply, range2next)

def otherDOEhandler(message):
	plotMenu_MetricHandler(message)


@bot.message_handler(func = lambda msg: msg.text[2] == '-' and session.isComplete == False)
def getExactDOE(message):
	assert(session.doe_type == "Exact")
	session.doe_args = message.text
	plotMenu_MetricHandler(message)


def plotMenu_MetricHandler(message):
	reply = bot.send_message(message.chat.id, "Plot:", reply_markup = plot_metrics_markup)
	bot.register_next_step_handler(reply, result_handler)


def range2next(message):
	if(message.text == "Cancel"):
		bot.send_message(message.chat.id, "Aborted")
		session.reset()
	else:
		session.doe_args = message.text
		plotMenu_MetricHandler(message)
	

def plotMenu_StrikeRangeHandler(message):
	yield


def result_handler(message):

	if(message.text == "Cancel"):
		session.reset()

	elif(message.text == "Greeks"):
		greekHandler(message)

	else:
		session.metric = message.text
		# session.verify()
		bot.send_message(message.chat.id, "Your plot is being produced:")


# Receive a ticker when uninitialized
@bot.message_handler(func = lambda msg: '#' == msg.text[0] and session.sessionTicker == "")
def getTicker(message):
	bot.send_message(message.chat.id, 'KOK!')

	# Initialize the session state	
	session.sessionTicker = message.text[1:]

	reply = bot.send_message(message.chat.id, "Select Contract Type:", reply_markup = contractType_markup)
	bot.register_next_step_handler(reply, plotMenu_contractTypeHandler)



def greekHandler(message):
	reply = bot.send_message(message.chat.id, "Choose the Greek:", reply_markup = greekMarkup)
	bot.register_next_step_handler(reply, greek2final)


def greek2final(message):

	if(message.text == "Cancel"):
		bot.send_message(message.chat.id, "Aborted")

	else:
		session.metric = message.text
		bot.send_message(message.chat.id, "Your plot is being produced:", reply_markup = None)


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

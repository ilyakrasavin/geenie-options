import telebot
from telebot import types

from base64 import decode
from datetime import datetime
import matplotlib.pyplot as plt

import subprocess
import sys

# User-Defined Libraries / Paths
from markup import * 
from KEYS import API_TOKEN

sys.path.insert(0, '../Requests')
from request_automatic import getStrikesDOEs


# Stores the Session State

class SessionState:

	def __init__(self):
		self.sessionTicker = ""
		self.requestMode = 0

		# Common Attributes:
		self.o_type = ""
		self.doe_type = ""
		self.doe_args = ""
		self.metric = ""

		# Specific Attributes
		self.atm_px = 0
		self.strike_range = {}

		self.strikes_all = []
		self.expirations_all = []

		self.chat_id = ""

	def verify(self):

		# tickerCond = self.sessionTicker != 0
		# reqCond = self.requestMode != 0
		# typeCond = self.o_type != ""
		# doe_tCond = self.doe_type != ""
		# doe_aCond = self.doe_args != ""
		# metCond = self.metric != ""

		# atmCond = self.atm_px != 0
		

		if(self.requestMode == 1):
			self.isComplete = True
			return (True, 1)

		elif(self.requestMode == 2):
			self.isComplete = True
			return (True, 2)


		# if(self.requestMode == 1 and tickerCond and reqCond and typeCond
		# 						and doe_tCond and doe_aCond and metCond
		# 						and atmCond and (not (self.strike_range['lower'] != self.strike_range['upper']))):
		# 	self.isComplete = True
		# 	return (True, 1)

		# elif(self.requestMode == 2 and tickerCond and reqCond and typeCond
		# 						and doe_tCond and doe_aCond and metCond
		# 						and (not atmCond) and (self.strike_range['lower'] != self.strike_range['upper'])):

		# 	self.isComplete = True
		# 	return (True, 2)


		elif(self.requestMode == 3):
			return (False, 3)

		else:
			return (False, -1)


	def makeRequest(self):
		
		_, mode = self.verify()

		if mode == 1:
			proc = subprocess.run(['python3', '../Pricing/plotting.py', session.sessionTicker, str(1), session.o_type, session.doe_type, session.doe_args, session.metric, str(session.atm_px)], capture_output=True)
			print(proc.stdout.decode('utf-8'))
			hangleImage(self.chat_id, proc.stdout.decode('utf-8')[:-1])

		if mode == 2:
			proc = subprocess.run(['python3', '../Pricing/plotting.py', session.sessionTicker, str(2), session.o_type, session.doe_type, session.doe_args, session.metric, str(session.strike_range['lower']), str(session.strike_range['upper'])], capture_output = True)
			print(proc.stdout.decode('utf-8'))
			hangleImage(self.chat_id, proc.stdout.decode('utf-8')[:-1])


	def reset(self):
		self.__init__()



# Initialize the bot and Session State
bot = telebot.TeleBot(API_TOKEN)

session = SessionState()
session.__init__()


@bot.message_handler(commands=['start'])
def main_menu(message):
	reply = bot.send_message(message.chat.id, "Please choose a mode to proceed!", reply_markup = markup)
	session.chat_id = message.chat.id
	bot.register_next_step_handler(reply, mainMenu_handler)

def plottingHandler(message):
	getUnderlying(message)

def statModeHandler(message):
	bot.send_message(message.chat.id, "Sorry, this feature is still in development!")
	# TODO: Proceed to Underlying 
	session.reset()
	

def mainMenu_handler(message):

	if(message.text == 'Plotting'):
		session.requestMode = 1
		plottingHandler(message)

	elif (message.text == 'Statistics (In Dev.)'):
		session.requestMode = 2
		statModeHandler(message)

	elif (message.text == 'Cancel'):
		session.reset()
		bot.send_message(message.chat.id, "Aborted. Use /start to make another request!")


def getUnderlying(message):
	bot.send_message(message.chat.id, "Enter the Ticker Symol preceded by #:")


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
		# plotMenu_handler(message)
		bot.send_message(message.chat.id, "Sorry. This feature is still in development.")
		session.reset()

	elif(message.text == "Cancel"):
		session.reset()
		bot.send_message(message.chat.id, "Aborted")
		

# Collect input from Plotting Menu
def plotMenu_handler(message):

	# Make requests for DOEs, Strikes and ATM px.
	populateSessionData()

	# Populate the Strike Range Keyboard:
	for each in session.strikes_all:
		# buttons[each] = types.KeyboardButton(each)
		strikeRange.row(types.KeyboardButton(each))

	reply = bot.send_message(message.chat.id, "Select Plotting Mode", reply_markup = plotModeMarkup)
	bot.register_next_step_handler(reply, resolveModeMenu)



def resolveModeMenu(message):
	if(message.text == "DOE x ATM"):
		session.requestMode = 1
		resolveDoeMode(message)

	elif(message.text == "DOE x Strike Range"):
		session.requestMode = 2
		resolveStrikeLower(message)

	elif(message.text == "Cancel"):
		session.reset()
		bot.send_message(message.chat.id, "Aborted")


# RESOLVE DOE RELATED OPTIONS
#####################################################################
def resolveDoeMode(message):
	reply = bot.send_message(message.chat.id, "Select DOE Mode:", reply_markup = doeModeMarkup)
	bot.register_next_step_handler(reply, resolveDoeArgs)


def resolveDoeArgs(message):
	if(message.text == "Exact"):
		session.doe_type = "exact"
		exactDOEhandler(message)

	elif(message.text == "Range"):
		session.doe_type = "range"
		rangeDOEhandler(message)

	elif(message.text == "Quarterly"):
		session.doe_type = "quarterly"
		otherDOEhandler(message)

	elif(message.text == "Weekly"):
		session.doe_type = "weekly"
		otherDOEhandler(message)

	elif(message.text == "Cancel"):
		session.reset()
		bot.send_message(message.chat.id, "Aborted")


def exactDOEhandler(message):
	bot.send_message(message.chat.id, "Provide Exact DOE in YY-MM-DD format")

	doeListMarkup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

	all_expirations = session.expirations_all

	for each in all_expirations:
		# doeButtons[each] = types.KeyboardButton(each)
		doeListMarkup.row(types.KeyboardButton(each))

	reply = bot.send_message(message.chat.id, "Please Select DOE:", reply_markup = doeListMarkup)
	# assert(session.doe_type == "exact")
	# session.doe_args = message.text

	bot.register_next_step_handler(reply, exactDoe2Metric)


def exactDoe2Metric(message):
	assert(session.doe_type == "exact")
	session.doe_args = message.text
	metricHandler(message)



def rangeDOEhandler(message):
	reply = bot.send_message(message.chat.id, "Please choose the range:", reply_markup = doeRangeMarkup)
	bot.register_next_step_handler(reply, range2metric)


def range2metric(message):
	if(message.text == "Cancel"):
		bot.send_message(message.chat.id, "Aborted")
		session.reset()
	else:
		session.doe_args = message.text
		metricHandler(message)
	

def otherDOEhandler(message):
	metricHandler(message)


def metricHandler(message):
	reply = bot.send_message(message.chat.id, "Plot:", reply_markup = metricModeMarkup)
	bot.register_next_step_handler(reply, resolveResult)



def greekHandler(message):
	reply = bot.send_message(message.chat.id, "Choose the Greek:", reply_markup = greekMarkup)
	bot.register_next_step_handler(reply, greek2final)


def greek2final(message):

	if(message.text == "Cancel"):
		bot.send_message(message.chat.id, "Aborted")

	else:
		session.metric = message.text.lower()
		bot.send_message(message.chat.id, "Your plot is being produced:")
		session.makeRequest()
		session.reset()


#####################################################################



# RESOLVE STRIKE RANGES
#####################################################################
def resolveStrikeLower(message):
	reply = bot.send_message(message.chat.id, "Please select the LOWER Strike Price:", reply_markup = strikeRange)
	bot.register_next_step_handler(reply, lowerStrikeHandler)

def lowerStrikeHandler(message):
	session.strike_range['lower'] = float(message.text)
	upperStrike(message)

def upperStrike(message):
	reply = bot.send_message(message.chat.id, "Please select the UPPER Strike Price:", reply_markup = strikeRange)
	bot.register_next_step_handler(reply, upperStrikeHandler)

def upperStrikeHandler(message):
	session.strike_range['upper'] = float(message.text)
	resolveDoeMode(message)
#####################################################################



def resolveResult(message):

	if(message.text == "Cancel"):
		session.reset()

	elif(message.text == "Greeks"):
		greekHandler(message)

	else:

		if message.text == 'Last Px.':
			session.metric = 'lastPrice'
		elif message.text == 'Volume':
			session.metric = 'volume'
		elif message.text == 'OI':
			session.metric = 'openInterest'
		elif message.text == 'IV':
			session.metric = 'impliedVolatility'
		
		bot.send_message(message.chat.id, "Your plot is being produced:")

		session.makeRequest()
		session.reset()



def populateSessionData():

	strikes, does, atm = getStrikesDOEs(session.sessionTicker, session.o_type)

	session.strikes_all = strikes
	session.expirations_all = does
	session.atm_px = atm



# Receive a ticker if uninitialized
@bot.message_handler(func = lambda msg: '#' == msg.text[0] and session.sessionTicker == "")
def getTicker(message):

	session.sessionTicker = message.text[1:]

	reply = bot.send_message(message.chat.id, "Select Contract Type:", reply_markup = contractType_markup)
	bot.register_next_step_handler(reply, plotMenu_contractTypeHandler)



# @bot.message_handler(commands=['ipo'])
def hangleImage(id, filename):
	filepath = '../../Images/' + filename
	# bot.send_document(id, document=open(filepath, 'rb'))
	bot.send_photo(id, photo=open(filepath, 'rb'))



# STATISTICS -> Get Underlying
# Most Traded table
# Put/call parity


# "About" Command -> Bot's Intro


# Infinite polling (Does not quit on errors)
bot.infinity_polling()
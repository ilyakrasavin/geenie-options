# Telegram Bot API

from base64 import decode
from datetime import datetime
import subprocess
import telebot
from telebot import types

import sys

from markup import * 
from KEYS import API_TOKEN


import matplotlib.pyplot as plt


sys.path.insert(0, '../Requests')
from request_automatic import getStrikesDOEs

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
		
		validation, mode = self.verify()

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

strikeRangeTuple = (0, 0)
rangeCollection = False



strikeRange = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = {}


@bot.message_handler(commands=['start'])
def handle_menu_call(message):
	reply = bot.send_message(message.chat.id, "Please choose an option:", reply_markup = markup)
	session.chat_id = message.chat.id
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

	elif (message.text == 'Statistics (In Dev.)'):
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



def plotMenu_strikeRHandler(message):
	reply = bot.send_message(message.chat.id, "Please select the LOWER Strike Price:", reply_markup = strikeRange)
	bot.register_next_step_handler(reply, bottomStrikeHandler)


def bottomStrikeHandler(message):
	session.strike_range['lower'] = float(message.text)
	upperStrike(message)

def upperStrike(message):
	reply = bot.send_message(message.chat.id, "Please select the UPPER Strike Price:", reply_markup = strikeRange)
	bot.register_next_step_handler(reply, upperStrikeHandler)


def upperStrikeHandler(message):
	session.strike_range['upper'] = float(message.text)
	plotMenu_lvl2_handler(message)


def plotMenu_DOEHandler(message):
	if(message.text == "DOE x ATM"):
		session.requestMode = 1
		plotMenu_lvl2_handler(message)

	elif(message.text == "DOE x Strike Range"):
		session.requestMode = 2
		plotMenu_strikeRHandler(message)

	elif(message.text == "Cancel"):
		session.reset()
		bot.send_message(message.chat.id, "Aborted")




def plotMenu_DOEArgHandler(message):
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


# ADD KEYBOARD W/ EXPIRATION DATES
def exactDOEhandler(message):
	bot.send_message(message.chat.id, "Provide Exact DOE in YY-MM-DD format")

	doeList = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	doeButtons = {}

	all_expirations = expirationsData()

	for each in all_expirations:
		# doeButtons[each] = types.KeyboardButton(each)
		doeList.row(types.KeyboardButton(each))

	reply = bot.send_message(message.chat.id, "Please Select DOE:", reply_markup = doeList)
	# assert(session.doe_type == "exact")
	# session.doe_args = message.text

	bot.register_next_step_handler(reply, exactDoe2Metric)


def exactDoe2Metric(message):
	assert(session.doe_type == "exact")
	session.doe_args = message.text
	plotMenu_MetricHandler(message)


def rangeDOEhandler(message):
	reply = bot.send_message(message.chat.id, "Please choose the range:", reply_markup = doe_range_markup)
	bot.register_next_step_handler(reply, range2next)

def otherDOEhandler(message):
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
	



def plotMenu_StrikeRangeHandler1(message):
	bot.send_message(message.chat.id, message.text)


def result_handler(message):

	if(message.text == "Cancel"):
		session.reset()

	elif(message.text == "Greeks"):
		greekHandler(message)

	else:
		session.metric = message.text
		bot.send_message(message.chat.id, "Your plot is being produced:")
		filepath = session.makeRequest()
		session.reset()


def strikes_expirations():

	strikes, does = getStrikesDOEs(session.sessionTicker)

	session.strikes_all = strikes
	session.expirations_all = does


# Receive a ticker when uninitialized
@bot.message_handler(func = lambda msg: '#' == msg.text[0] and session.sessionTicker == "")
def getTicker(message):

	# Initialize the session state	
	session.sessionTicker = message.text[1:]

	strikes_expirations()

	for each in session.strikes_all:
		buttons[each] = types.KeyboardButton(each)
		strikeRange.row(buttons[each])

	reply = bot.send_message(message.chat.id, "Select Contract Type:", reply_markup = contractType_markup)

	bot.register_next_step_handler(reply, plotMenu_contractTypeHandler)



def greekHandler(message):
	reply = bot.send_message(message.chat.id, "Choose the Greek:", reply_markup = greekMarkup)
	bot.register_next_step_handler(reply, greek2final)


def greek2final(message):

	if(message.text == "Cancel"):
		bot.send_message(message.chat.id, "Aborted")

	else:
		session.metric = message.text.lower()
		session.makeRequest()
		session.reset()
		bot.send_message(message.chat.id, "Your plot is being produced:")



# @bot.message_handler(commands=['ipo'])
def hangleImage(id, filename):
	bot.send_photo(id, photo=open('../../Images/' + filename, 'rb'))



# STATISTICS -> Get Underlying
# Most Traded table
# Put/call parity


# "About" -> Bot's Intro


# Infinite polling (Does not quit on errors)
bot.infinity_polling()
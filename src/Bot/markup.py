
# Keyboard and Button Layouts

import telebot
from telebot import types

# Main Menu buttons
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
itembtna = types.KeyboardButton('Plotting')
itembtnv = types.KeyboardButton('Statistics (In Dev.)')
itembtnc = types.KeyboardButton('Cancel')
markup.row(itembtna, itembtnv)
markup.row(itembtnc)

# Plotting Menu Step 1:
plotModeMarkup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
plotMode_btn1 = types.KeyboardButton("DOE x ATM")
plotMode_btn2 = types.KeyboardButton("DOE x Strike Range")
plotMode_btn3 = types.KeyboardButton("Cancel")
plotModeMarkup.row(plotMode_btn1)
plotModeMarkup.row(plotMode_btn2)
plotModeMarkup.row(plotMode_btn3)


# Plotting DOE Mode setting markup
doeModeMarkup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
doe_mode1 = types.KeyboardButton("Exact")
doe_mode2 = types.KeyboardButton("Range")
doe_mode3 = types.KeyboardButton("Quarterly")
doe_mode4 = types.KeyboardButton("Weekly")
doe_mode5 = types.KeyboardButton("Cancel")
doeModeMarkup.row(doe_mode1, doe_mode2)
doeModeMarkup.row(doe_mode3, doe_mode4)
doeModeMarkup.row(doe_mode5)


# Plotting DOE Metric setting Markup
metricModeMarkup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
metric_button1 = types.KeyboardButton("Last Px.")
metric_button2 = types.KeyboardButton("OI")
metric_button3 = types.KeyboardButton("Volume")
metric_button4 = types.KeyboardButton("IV")
metric_button5 = types.KeyboardButton("Greeks")
metric_button6 = types.KeyboardButton("Cancel")

metricModeMarkup.row(metric_button1, metric_button2)
metricModeMarkup.row(metric_button3, metric_button4)
metricModeMarkup.row(metric_button5)
metricModeMarkup.row(metric_button6)


# Contract Type markup
contractType_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
typeButton1 = types.KeyboardButton("Call")
typeButton2 = types.KeyboardButton("Put")
typeButton3 = types.KeyboardButton("Call & Put")
typeButton4 = types.KeyboardButton("Cancel")

contractType_markup.row(typeButton1, typeButton2)
contractType_markup.row(typeButton3)
contractType_markup.row(typeButton4)


doeRangeMarkup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
range1 = types.KeyboardButton("30D")
range2 = types.KeyboardButton("60D")
range3 = types.KeyboardButton("90D")
range4 = types.KeyboardButton("180D")
range5 = types.KeyboardButton("1Y")
range6 = types.KeyboardButton("1Y6M")
range7 = types.KeyboardButton("2Y")
range8 = types.KeyboardButton("MAX")
range9 = types.KeyboardButton("Cancel")

doeRangeMarkup.row(range1, range2, range3, range4)
doeRangeMarkup.row(range5, range6, range7, range8)
doeRangeMarkup.row(range9)



greekMarkup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
greek1 = types.KeyboardButton("Delta")
greek2 = types.KeyboardButton("Gamma")
greek3 = types.KeyboardButton("Vega")
greek4 = types.KeyboardButton("Theta")
greek5 = types.KeyboardButton("Rho")
greek6 = types.KeyboardButton("Cancel")

greekMarkup.row(greek1)
greekMarkup.row(greek2)
greekMarkup.row(greek3)
greekMarkup.row(greek4)
greekMarkup.row(greek5)
greekMarkup.row(greek6)



strikeRange = types.ReplyKeyboardMarkup(one_time_keyboard=True)

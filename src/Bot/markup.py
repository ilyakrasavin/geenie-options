
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
plot_markup1 = types.ReplyKeyboardMarkup(one_time_keyboard=True)
plotmenu_btn1 = types.KeyboardButton("DOE x ATM")
plotmenu_btn2 = types.KeyboardButton("DOE x Strike Range")
plotmenu_btn3 = types.KeyboardButton("Cancel")
plot_markup1.row(plotmenu_btn1)
plot_markup1.row(plotmenu_btn2)
plot_markup1.row(plotmenu_btn3)


# Plotting DOE Mode setting markup
plot_doe_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
doe_button1 = types.KeyboardButton("Exact")
doe_button2 = types.KeyboardButton("Range")
doe_button3 = types.KeyboardButton("Quarterly")
doe_button4 = types.KeyboardButton("Weekly")
doe_button5 = types.KeyboardButton("Cancel")
plot_doe_markup.row(doe_button1, doe_button2)
plot_doe_markup.row(doe_button3, doe_button4)
plot_doe_markup.row(doe_button5)


# Plotting DOE Metric setting Markup
plot_metrics_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
metric_button1 = types.KeyboardButton("lastPrice")
metric_button2 = types.KeyboardButton("openInterest")
metric_button3 = types.KeyboardButton("volume")
metric_button4 = types.KeyboardButton("impliedVolatility")
metric_button5 = types.KeyboardButton("Greeks")
metric_button6 = types.KeyboardButton("Cancel")

plot_metrics_markup.row(metric_button1, metric_button2)
plot_metrics_markup.row(metric_button3, metric_button4)
plot_metrics_markup.row(metric_button5)
plot_metrics_markup.row(metric_button6)


# Contract Type markup
contractType_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
typeButton1 = types.KeyboardButton("Call")
typeButton2 = types.KeyboardButton("Put")
typeButton3 = types.KeyboardButton("Call & Put")
typeButton4 = types.KeyboardButton("Cancel")

contractType_markup.row(typeButton1, typeButton2)
contractType_markup.row(typeButton3)
contractType_markup.row(typeButton4)


doe_range_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
range1 = types.KeyboardButton("30D")
range2 = types.KeyboardButton("60D")
range3 = types.KeyboardButton("90D")
range4 = types.KeyboardButton("180D")
range5 = types.KeyboardButton("1Y")
range6 = types.KeyboardButton("1Y6M")
range7 = types.KeyboardButton("2Y")
range8 = types.KeyboardButton("MAX")
range9 = types.KeyboardButton("Cancel")

doe_range_markup.row(range1, range2, range3, range4)
doe_range_markup.row(range5, range6, range7, range8)
doe_range_markup.row(range9)



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



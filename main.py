#!/usr/bin/env python3

import time

import telebot
from telebot import types, apihelper

import config


bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message_handler(message):
	cid = message.chat.id
	uid = message.from_user.id
	text = 'Главное меню'  # TODO: текущее состояние счета
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
	for x in config.main_markup:
		markup.row(*x)
	return bot.send_message(cid, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text_handler(message):
	cid = message.chat.id
	uid = message.from_user.id

	# Вернуться в главное меню
	if message.text == '↩️ Назад':
		text = 'Главное меню'  # TODO: текущее состояние счета
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for x in config.main_markup:
			markup.row(*x)
		return bot.send_message(cid, text, reply_markup=markup)

	# Обработать главное меню
	if message.text == 'Добавить операцию':
		text = 'Выберите тип операции'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for x in config.operations_markup:
			markup.row(*x)
		markup.row('↩️ Назад')
		return bot.send_message(cid, text, reply_markup=markup)
	elif message.text == 'Счет и портфель' or message.text == '⤴️ Назад':
		text = 'TODO'  # TODO: информация о портфеле
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for x in config.schet_markup:
			markup.row(*x)
		markup.row('↩️ Назад')
		return bot.send_message(cid, text, reply_markup=markup)

	# Обработать меню Счет и Портфель
	if message.text == 'Посмотреть историю операций':
		text = 'Информация за текущий месяц'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for x in config.history_markup:
			markup.row(*x)
		markup.row('⤴️ Назад')
		return bot.send_message(cid, text, reply_markup=markup)


def main():
	if config.DEBUG:
		apihelper.proxy = {'https': 'socks5h://114.4.132.43:443'}
		bot.polling()
	else:
		while True:
			try:
				bot.polling(none_stop=True, interval=0)
			except Exception as e:
				print(e)
				time.sleep(30)
				continue


if __name__ == '__main__':
	main()

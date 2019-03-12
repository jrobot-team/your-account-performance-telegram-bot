#!/usr/bin/env python3

import time

import telebot
from telebot import types, apihelper

import util
import config


bot = telebot.TeleBot(config.BOT_TOKEN)

READY_TO_ADD_AMOUNT = {}
READY_TO_MINUS_ACCOUNT = {}

READY_TO_TAX = {}
READY_TO_COMISSION = {}
READY_TO_COUPON_INCOME = {}
READY_TO_DIVIDENDS = {}


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

	# Обработать отмену операции
	if message.text == '❌ Отмена':
		if uid in READY_TO_ADD_AMOUNT:
			del READY_TO_ADD_AMOUNT[uid]
		if uid in READY_TO_MINUS_ACCOUNT:
			del READY_TO_MINUS_ACCOUNT[uid]
		
		if uid in READY_TO_TAX:
			del READY_TO_TAX[uid]
		if uid in READY_TO_COMISSION:
			del READY_TO_COMISSION[uid]
		if uid in READY_TO_COUPON_INCOME:
			del READY_TO_COUPON_INCOME[uid]
		if uid in READY_TO_DIVIDENDS:
			del READY_TO_DIVIDENDS[uid]
		text = 'Операция отменена'
		bot.send_message(cid, text)
		text = 'Выберите тип операции'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for x in config.operations_markup:
			markup.row(*x)
		markup.row('↩️ Назад')
		return bot.send_message(cid, text, reply_markup=markup)

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
		text = 'Счет и портфель'  # TODO: информация о портфеле
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

	# Обработать операции
	if message.text == 'Пополнить счет':
		READY_TO_ADD_AMOUNT[uid] = {}
		text = 'Введите сумму пополнения'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		markup.row('❌ Отмена')
		return bot.send_message(cid, text, reply_markup=markup)
	elif message.text == 'Вывести средства':
		READY_TO_MINUS_ACCOUNT[uid] = {}
		text = 'Введите сумму, которую хотите вывести'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		markup.row('❌ Отмена')
		return bot.send_message(cid, text, reply_markup=markup)
	elif message.text == 'Купить акции':
		pass
	elif message.text == 'Продать акции':
		pass
	elif message.text == 'Купить облигации':
		pass
	elif message.text == 'Продать облигации':
		pass
	elif message.text == 'Заплатить налог':
		READY_TO_TAX[uid] = {}
		text = 'Введите стоимость налога'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		markup.row('❌ Отмена')
		return bot.send_message(cid, text, reply_markup=markup)
	elif message.text == 'Заплатить комиссию':
		READY_TO_COMISSION[uid] = {}
		text = 'Введите стоимость комиссии'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		markup.row('❌ Отмена')
		return bot.send_message(cid, text, reply_markup=markup)
	if message.text == 'Получить купонный доход':
		READY_TO_COUPON_INCOME[uid] = {}
		text = 'Введите идентификатор облигации, по которой получен доход'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		markup.row('❌ Отмена')
		return bot.send_message(cid, text, reply_markup=markup)
	if message.text == 'Получить дивиденды':
		READY_TO_DIVIDENDS[uid] = {}
		text = 'Введите идентификатор пакета акций, по которому получены дивиденды'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		markup.row('❌ Отмена')
		return bot.send_message(cid, text, reply_markup=markup)

	# Обработать состояние операций
	if uid in READY_TO_ADD_AMOUNT:
		if 'amount' not in READY_TO_ADD_AMOUNT[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_ADD_AMOUNT[uid]['amount'] = int(message.text)
			text = 'Введите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_ADD_AMOUNT[uid]:
			READY_TO_ADD_AMOUNT[uid]['broker'] = message.text
			util.DataBase.add_new_amount(
				uid, int(time.time()), 
				READY_TO_ADD_AMOUNT[uid]['amount'], 
				READY_TO_ADD_AMOUNT[uid]['broker'])
			print(READY_TO_ADD_AMOUNT[uid])
			del READY_TO_ADD_AMOUNT[uid]
			text = 'Вы успешно пополнили счет'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
			for x in config.operations_markup:
				markup.row(*x)
			markup.row('↩️ Назад')
			return bot.send_message(cid, text, reply_markup=markup)
	
	# Обработать состояние вывода средств
	if uid in READY_TO_MINUS_ACCOUNT:
		if 'amount' not in READY_TO_MINUS_ACCOUNT[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_MINUS_ACCOUNT[uid]['amount'] = message.text
			print(READY_TO_MINUS_ACCOUNT[uid])
			util.DataBase.add_minus_amount(
				uid, int(time.time()), 
				READY_TO_MINUS_ACCOUNT[uid]['amount'])
			del READY_TO_MINUS_ACCOUNT[uid]
			text = 'Вы успешно вывели средства'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
			for x in config.operations_markup:
				markup.row(*x)
			markup.row('↩️ Назад')
			return bot.send_message(cid, text, reply_markup=markup)
	
	# Обработать сотояние удержания налога
	if uid in READY_TO_TAX:
		if 'amount' not in READY_TO_TAX[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_TAX[uid]['amount'] = int(message.text)
			text = 'Введите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_TAX[uid]:
			READY_TO_TAX[uid]['broker'] = message.text
			util.DataBase.add_new_tax(
				uid, int(time.time()), 
				READY_TO_TAX[uid]['amount'], 
				READY_TO_TAX[uid]['broker'])
			print(READY_TO_TAX[uid])
			del READY_TO_TAX[uid]
			text = 'Вы успешно оплатили налог'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
			for x in config.operations_markup:
				markup.row(*x)
			markup.row('↩️ Назад')
			return bot.send_message(cid, text, reply_markup=markup)
	
	# Обработать сотояние удержания комиссии
	if uid in READY_TO_COMISSION:
		if 'amount' not in READY_TO_COMISSION[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_COMISSION[uid]['amount'] = int(message.text)
			text = 'Введите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_COMISSION[uid]:
			READY_TO_COMISSION[uid]['broker'] = message.text
			util.DataBase.add_new_commission(
				uid, int(time.time()), 
				READY_TO_COMISSION[uid]['amount'], 
				READY_TO_COMISSION[uid]['broker'])
			print(READY_TO_COMISSION[uid])
			del READY_TO_COMISSION[uid]
			text = 'Вы успешно оплатили комиссию'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
			for x in config.operations_markup:
				markup.row(*x)
			markup.row('↩️ Назад')
			return bot.send_message(cid, text, reply_markup=markup)

	# Обработать сотояние добавления купонного дохода
	if uid in READY_TO_COUPON_INCOME:
		if 'bond' not in READY_TO_COUPON_INCOME[uid]:
			READY_TO_COUPON_INCOME[uid]['bond'] = message.text
			text = 'Введите стоимость дохода'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_COUPON_INCOME[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_COUPON_INCOME[uid]['amount'] = int(message.text)
			text = 'Введите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_COUPON_INCOME[uid]:
			READY_TO_COUPON_INCOME[uid]['broker'] = message.text
			util.DataBase.add_new_coupon_income(
				uid, int(time.time()), 
				READY_TO_COUPON_INCOME[uid]['bond'],
				READY_TO_COUPON_INCOME[uid]['amount'], 
				READY_TO_COUPON_INCOME[uid]['broker'])
			print(READY_TO_COUPON_INCOME[uid])
			del READY_TO_COUPON_INCOME[uid]
			text = 'Вы успешно добавили купонный доход'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
			for x in config.operations_markup:
				markup.row(*x)
			markup.row('↩️ Назад')
			return bot.send_message(cid, text, reply_markup=markup)
		
	# Обработать сотояние добавления купонного дохода
	if uid in READY_TO_DIVIDENDS:
		if 'dividend' not in READY_TO_DIVIDENDS[uid]:
			READY_TO_DIVIDENDS[uid]['dividend'] = message.text
			text = 'Введите стоимость дохода'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_DIVIDENDS[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_DIVIDENDS[uid]['amount'] = int(message.text)
			text = 'Введите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_DIVIDENDS[uid]:
			READY_TO_DIVIDENDS[uid]['broker'] = message.text
			util.DataBase.add_new_dividend(
				uid, int(time.time()), 
				READY_TO_DIVIDENDS[uid]['dividend'],
				READY_TO_DIVIDENDS[uid]['amount'], 
				READY_TO_DIVIDENDS[uid]['broker'])
			print(READY_TO_DIVIDENDS[uid])
			del READY_TO_DIVIDENDS[uid]
			text = 'Вы успешно добавили дивиденд'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
			for x in config.operations_markup:
				markup.row(*x)
			markup.row('↩️ Назад')
			return bot.send_message(cid, text, reply_markup=markup)


def main():
	util.DataBase.deploy_database()

	if config.DEBUG:
		apihelper.proxy = {'https': 'socks5h://35.185.64.205:1080'}
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

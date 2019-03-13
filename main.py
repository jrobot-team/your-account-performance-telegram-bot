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
		text = 'Главное меню'  # TODO: текущее состояние счета
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for x in config.main_markup:
			markup.row(*x)
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
		keyboard = types.InlineKeyboardMarkup()
		for x in config.operations_markup:
			keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
		# keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='back'))
		return bot.send_message(cid, text, reply_markup=keyboard)
	elif message.text == 'Счет и портфель' or message.text == '⤴️ Назад':
		text = 'Счет и портфель'  # TODO: информация о портфеле
		keyboard = types.InlineKeyboardMarkup()
		for x in config.schet_markup:
			keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
		# keyboard.add(types.InlineKeyboardButton(text='↩️ Назад', callback_data='back'))
		return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать состояние операций
	if uid in READY_TO_ADD_AMOUNT:
		if 'amount' not in READY_TO_ADD_AMOUNT[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_ADD_AMOUNT[uid]['amount'] = int(message.text)
			text = 'Выберите брокера'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.brokers:
				keyboard.add(types.InlineKeyboardButton(text=config.brokers[x], callback_data=x))
			return bot.send_message(cid, text, reply_markup=keyboard)
		if 'broker' not in READY_TO_ADD_AMOUNT[uid]:
			text = 'Выберите одного из брокеров из списка'
			return bot.send_message(cid, text)
	
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
			return bot.send_message(cid, text)
	
	# Обработать сотояние удержания налога
	if uid in READY_TO_TAX:
		if 'amount' not in READY_TO_TAX[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_TAX[uid]['amount'] = int(message.text)
			text = 'Выберите брокера'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.brokers:
				keyboard.add(types.InlineKeyboardButton(text=config.brokers[x], callback_data=x))
			return bot.send_message(cid, text, reply_markup=keyboard)
		if 'broker' not in READY_TO_TAX[uid]:
			text = 'Выберите одного из брокеров из списка'
			return bot.send_message(cid, text)
	
	# Обработать сотояние удержания комиссии
	if uid in READY_TO_COMISSION:
		if 'amount' not in READY_TO_COMISSION[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_COMISSION[uid]['amount'] = int(message.text)
			text = 'Выберите брокера'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.brokers:
				keyboard.add(types.InlineKeyboardButton(text=config.brokers[x], callback_data=x))
			return bot.send_message(cid, text, reply_markup=keyboard)
		if 'broker' not in READY_TO_COMISSION[uid]:
			text = 'Выберите одного из брокеров из списка'
			return bot.send_message(cid, text)

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
			text = 'Выберите брокера'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.brokers:
				keyboard.add(types.InlineKeyboardButton(text=config.brokers[x], callback_data=x))
			return bot.send_message(cid, text, reply_markup=keyboard)
		if 'broker' not in READY_TO_COUPON_INCOME[uid]:
			text = 'Выберите одного из брокеров из списка'
			return bot.send_message(cid, text)
		
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
			text = 'Выберите брокера'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.brokers:
				keyboard.add(types.InlineKeyboardButton(text=config.brokers[x], callback_data=x))
			return bot.send_message(cid, text, reply_markup=keyboard)
		if 'broker' not in READY_TO_DIVIDENDS[uid]:
			text = 'Выберите одного из брокеров из списка'
			return bot.send_message(cid, text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	uid = call.from_user.id
	cid = call.message.chat.id

	print(call.data)

	try:
		bot.answer_callback_query(call.id, 'Выполнено')
	except Exception as e:
		print(e)

	if call.data == 'history':
		text = 'Информация за текущий месяц'
		keyboard = types.InlineKeyboardMarkup()
		for x in config.history_markup:
			keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
		bot.delete_message(cid, call.message.message_id)
		return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать операции
	if call.data == 'add_amount':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_ADD_AMOUNT[uid] = {}
		text = 'Введите сумму пополнения'
		return bot.send_message(cid, text)
	elif call.data == 'minus_amount':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_MINUS_ACCOUNT[uid] = {}
		text = 'Введите сумму, которую хотите вывести'
		return bot.send_message(cid, text)
	elif call.data == 'add_aczii':
		pass
	elif call.data == 'delete_aczii':
		pass
	elif call.data == 'add_oblig':
		pass
	elif call.data == 'delete_oblig':
		pass
	elif call.data == 'pay_nalog':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_TAX[uid] = {}
		text = 'Введите стоимость налога'
		return bot.send_message(cid, text)
	elif call.data == 'pay_comission':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_COMISSION[uid] = {}
		text = 'Введите стоимость комиссии'
		return bot.send_message(cid, text)
	if call.data == 'get_cupon':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_COUPON_INCOME[uid] = {}
		text = 'Введите идентификатор облигации, по которой получен доход'
		return bot.send_message(cid, text)
	if call.data == 'get_dividends':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_DIVIDENDS[uid] = {}
		text = 'Введите идентификатор пакета акций, по которому получены дивиденды'
		return bot.send_message(cid, text)

	# Обработать состояние операций
	if uid in READY_TO_ADD_AMOUNT:
		if 'broker' not in READY_TO_ADD_AMOUNT[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_ADD_AMOUNT[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_new_amount(
				uid, int(time.time()), 
				READY_TO_ADD_AMOUNT[uid]['amount'], 
				READY_TO_ADD_AMOUNT[uid]['broker'])
			print(READY_TO_ADD_AMOUNT[uid])
			del READY_TO_ADD_AMOUNT[uid]
			text = 'Вы успешно пополнили счет'
			return bot.send_message(cid, text)

	# Обработать сотояние удержания налога
	if uid in READY_TO_TAX:
		if 'broker' not in READY_TO_TAX[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_TAX[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_new_tax(
				uid, int(time.time()), 
				READY_TO_TAX[uid]['amount'], 
				READY_TO_TAX[uid]['broker'])
			print(READY_TO_TAX[uid])
			del READY_TO_TAX[uid]
			text = 'Вы успешно оплатили налог'
			return bot.send_message(cid, text)

	# Обработать сотояние удержания комиссии
	if uid in READY_TO_COMISSION:
		if 'broker' not in READY_TO_COMISSION[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_COMISSION[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_new_commission(
				uid, int(time.time()), 
				READY_TO_COMISSION[uid]['amount'], 
				READY_TO_COMISSION[uid]['broker'])
			print(READY_TO_COMISSION[uid])
			del READY_TO_COMISSION[uid]
			text = 'Вы успешно оплатили комиссию'
			return bot.send_message(cid, text)
	
	# Обработать сотояние добавления купонного дохода
	if uid in READY_TO_COUPON_INCOME:
		if 'broker' not in READY_TO_COUPON_INCOME[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_COUPON_INCOME[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_new_coupon_income(
				uid, int(time.time()), 
				READY_TO_COUPON_INCOME[uid]['bond'],
				READY_TO_COUPON_INCOME[uid]['amount'], 
				READY_TO_COUPON_INCOME[uid]['broker'])
			print(READY_TO_COUPON_INCOME[uid])
			del READY_TO_COUPON_INCOME[uid]
			text = 'Вы успешно добавили купонный доход'
			return bot.send_message(cid, text)
	
	# Обработать сотояние добавления купонного дохода
	if uid in READY_TO_DIVIDENDS:
		if 'broker' not in READY_TO_DIVIDENDS[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_DIVIDENDS[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_new_dividend(
				uid, int(time.time()), 
				READY_TO_DIVIDENDS[uid]['dividend'],
				READY_TO_DIVIDENDS[uid]['amount'], 
				READY_TO_DIVIDENDS[uid]['broker'])
			print(READY_TO_DIVIDENDS[uid])
			del READY_TO_DIVIDENDS[uid]
			text = 'Вы успешно добавили дивиденд'
			bot.send_message(cid, text)
			return bot.send_message(cid, text)


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

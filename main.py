#!/usr/bin/env python3

import time
import datetime
import threading
import dateutil.relativedelta

import schedule
import telebot
from telebot import types, apihelper

import util
import config


bot = telebot.TeleBot(config.BOT_TOKEN)

READY_TO_ADD_AMOUNT = {}
READY_TO_MINUS_ACCOUNT = {}
READY_TO_buystock = {}
READY_TO_salestock = {}
READY_TO_buybond = {}
READY_TO_salebond = {}
READY_TO_TAX = {}
READY_TO_COMISSION = {}
READY_TO_couponincome = {}
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
		if uid in READY_TO_couponincome:
			del READY_TO_couponincome[uid]
		if uid in READY_TO_DIVIDENDS:
			del READY_TO_DIVIDENDS[uid]
		text = 'Операция отменена'
		bot.send_message(cid, text)
		text = 'Главное меню'  # TODO: текущее состояние счета
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for x in config.main_markup:
			markup.row(*x)
		return bot.send_message(cid, text, reply_markup=markup)

	# Обработать команду для удаления операции
	if message.text.startswith('/del'):
		arr = message.text.split('_')
		if len(arr) < 3:
			text = 'Неверный тип команды'
			return bot.send_message(cid, text)
		operation = util.DataBase.get_operation(arr[1], uid, arr[2])
		if not operation:
			text = 'Вы не можете удалить операцию'
			return bot.send_message(cid, text)
		
		table_name = ''
		if arr[1] == 'accountamount':
			table_name = 'Пополнение счета'
		elif arr[1] == 'accountminusamount':
			table_name = 'Вывод средств'
		elif arr[1] == 'buystock':
			table_name = 'Покупка акций'
		elif arr[1] == 'salestock':
			table_name = 'Продажа акций'
		elif arr[1] == 'buybond':
			table_name = 'Покупка облигаций'
		elif arr[1] == 'salebond':
			table_name = 'Продажа облигаций'
		elif arr[1] == 'taxes':
			table_name = 'Оплата налога'
		elif arr[1] == 'comissions':
			table_name = 'Оплата комиссии'
		elif arr[1] == 'couponincome':
			table_name = 'Получение купонного дохода'
		elif arr[1] == 'dividends':
			table_name = 'Получение дивидендов'

		text = 'Дата: {!s}\n'.format(operation['input_date'])
		if arr[1] == 'accountamount':
			text += 'Сумма: {!s}\nБрокер: {!s}'.format(operation['amount'], operation['broker'])
		if arr[1] == 'accountminusamount':
			text += 'Сумма: {!s}\nБрокер: {!s}'.format(operation['amount'], operation['broker'])
		if arr[1] == 'buystock':
			text += 'Тикер: {!s}\nКол-во: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
				operation['ticker'], operation['count'], operation['price'], operation['broker'])
		if arr[1] == 'salestock':
			text += 'Тикер: {!s}\nКол-во: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
				operation['ticker'], operation['count'], operation['price'], operation['broker'])
		if arr[1] == 'buybond':
			text += 'Тикер: {!s}\nКол-во: {!s}\nНКД: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
				operation['ticker'], operation['count'], operation['nkd'], operation['price'], operation['broker'])
		if arr[1] == 'salebond':
			text += 'Тикер: {!s}\nКол-во: {!s}\nНКД: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
				operation['ticker'], operation['count'], operation['nkd'], operation['price'], operation['broker'])
		if arr[1] == 'taxes':
			text += 'Сумма: {!s}\nБрокер: {!s}'.format(operation['amount'], operation['broker'])
		if arr[1] == 'comissions':
			text += 'Сумма: {!s}\nБрокер: {!s}'.format(operation['amount'], operation['broker'])
		if arr[1] == 'couponincome':
			text += 'Тикер: {!s}\nСумма: {!s}\nБрокер: {!s}'.format(
				operation['bond'], operation['amount'], operation['broker'])
		if arr[1] == 'dividends':
			text += 'Тикер: {!s}\nСумма: {!s}\nБрокер: {!s}'.format(
				operation['dividend'], operation['amount'], operation['broker'])

		text = 'Вы хотите удалить операцию "{!s}"?\n{!s}'.format(table_name, text)
		keyboard = types.InlineKeyboardMarkup()
		cb = 'delop-{!s}-{!s}'.format(arr[1], arr[2])
		keyboard.add(types.InlineKeyboardButton(text='Удалить', callback_data=cb))
		keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data='cancelldelete'))
		return bot.send_message(cid, text, reply_markup=keyboard)

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
		return bot.send_message(cid, text, reply_markup=keyboard)
	elif message.text == 'Счет и портфель' or message.text == '⤴️ Назад':
		text = 'Счет и портфель'  # TODO: информация о портфеле
		keyboard = types.InlineKeyboardMarkup()
		for x in config.schet_markup:
			keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
		return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать состояние добавления средств
	if uid in READY_TO_ADD_AMOUNT:
		if 'input_date' not in READY_TO_ADD_AMOUNT[uid]:
			READY_TO_ADD_AMOUNT[uid]['input_date'] = message.text
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_ADD_AMOUNT[uid]:
			READY_TO_ADD_AMOUNT[uid]['broker'] = message.text
			text = 'Укажите сумму'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_ADD_AMOUNT[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_ADD_AMOUNT[uid]['amount'] = int(message.text)
			util.DataBase.add_new_amount(
				uid, int(time.time()),
				READY_TO_ADD_AMOUNT[uid]['input_date'],
				READY_TO_ADD_AMOUNT[uid]['amount'], 
				READY_TO_ADD_AMOUNT[uid]['broker'])
			print(READY_TO_ADD_AMOUNT[uid])
			del READY_TO_ADD_AMOUNT[uid]
			text = 'Вы успешно пополнили счет'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)
	
	# Обработать состояние вывода средств
	if uid in READY_TO_MINUS_ACCOUNT:
		if 'input_date' not in READY_TO_MINUS_ACCOUNT[uid]:
			READY_TO_MINUS_ACCOUNT[uid]['input_date'] = message.text
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_MINUS_ACCOUNT[uid]:
			READY_TO_MINUS_ACCOUNT[uid]['broker'] = message.text
			text = 'Укажите сумму'
			return bot.send_message(cid, text)
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
				READY_TO_MINUS_ACCOUNT[uid]['input_date'],
				READY_TO_MINUS_ACCOUNT[uid]['amount'],
				READY_TO_MINUS_ACCOUNT[uid]['broker'])
			del READY_TO_MINUS_ACCOUNT[uid]
			text = 'Вы успешно вывели средства'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать покупку акции
	if uid in READY_TO_buystock:
		if 'input_date' not in READY_TO_buystock[uid]:
			READY_TO_buystock[uid]['input_date'] = message.text
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_buystock[uid]:
			READY_TO_buystock[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'ticker' not in READY_TO_buystock[uid]:
			'''
			TODO
			api_price = util.Moex.get_stock_price(message.text)
			if not api_price:
				text = 'Такого тикера не существует'
				return bot.send_message(cid, text)
			READY_TO_buystock[uid]['api_price'] = api_price
			'''
			READY_TO_buystock[uid]['api_price'] = 0

			READY_TO_buystock[uid]['ticker'] = message.text
			text = 'Напишите количество акций для покупки'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_buystock[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_buystock[uid]['count'] = int(message.text)
			text = 'Введите цену акции'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_buystock[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_buystock[uid]['price'] = int(message.text)
			util.DataBase.add_buystock(
				uid, int(time.time()),
				READY_TO_buystock[uid]['input_date'],
				READY_TO_buystock[uid]['ticker'],
				READY_TO_buystock[uid]['count'],
				READY_TO_buystock[uid]['broker'],
				READY_TO_buystock[uid]['price'],
				READY_TO_buystock[uid]['api_price'])
			print(READY_TO_buystock[uid])
			del READY_TO_buystock[uid]
			text = 'Вы успешно купили акцию'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать продажу акции
	if uid in READY_TO_salestock:
		if 'input_date' not in READY_TO_salestock[uid]:
			READY_TO_salestock[uid]['input_date'] = message.text
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_salestock[uid]:
			READY_TO_salestock[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'ticker' not in READY_TO_salestock[uid]:
			READY_TO_salestock[uid]['ticker'] = message.text
			text = 'Напишите количество акций для продажи'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_salestock[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_salestock[uid]['count'] = int(message.text)
			text = 'Введите цену акции'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_salestock[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_salestock[uid]['price'] = int(message.text)
			util.DataBase.add_salestock(
				uid, int(time.time()),
				READY_TO_salestock[uid]['input_date'],
				READY_TO_salestock[uid]['ticker'],
				READY_TO_salestock[uid]['count'],
				READY_TO_salestock[uid]['broker'],
				READY_TO_salestock[uid]['price'])
			print(READY_TO_salestock[uid])
			del READY_TO_salestock[uid]
			text = 'Вы успешно продали акцию'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать покупку облигации
	if uid in READY_TO_buybond:
		if 'input_date' not in READY_TO_buybond[uid]:
			READY_TO_buybond[uid]['input_date'] = message.text
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_buybond[uid]:
			READY_TO_buybond[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'ticker' not in READY_TO_buybond[uid]:
			'''
			TODO
			api_price = util.Moex.get_bond_price(message.text)
			if not api_price:
				text = 'Такого тикера не существует'
				return bot.send_message(cid, text)
			READY_TO_buybond[uid]['api_price'] = api_price
			'''
			READY_TO_buybond[uid]['api_price'] = 0
			READY_TO_buybond[uid]['ticker'] = message.text
			text = 'Введите количество облигаций для покупки'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_buybond[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_buybond[uid]['count'] = int(message.text)
			text = 'Введите цену облигации'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_buybond[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_buybond[uid]['price'] = int(message.text)
			text = 'Введите НКД'
			return bot.send_message(cid, text)
		if 'nkd' not in READY_TO_buybond[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_buybond[uid]['nkd'] = int(message.text)
			util.DataBase.add_buybond(
				uid, int(time.time()), 
				READY_TO_buybond[uid]['input_date'],
				READY_TO_buybond[uid]['ticker'], 
				READY_TO_buybond[uid]['count'],
				READY_TO_buybond[uid]['nkd'],
				READY_TO_buybond[uid]['price'],
				READY_TO_buybond[uid]['broker'],
				READY_TO_buybond[uid]['api_price'])
			print(READY_TO_buybond[uid])
			del READY_TO_buybond[uid]
			text = 'Вы успешно купили облигации'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)
	
	# Обработать продажу облигации
	if uid in READY_TO_salebond:
		if 'input_date' not in READY_TO_salebond[uid]:
			READY_TO_salebond[uid]['input_date'] = message.text
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_salebond[uid]:
			READY_TO_salebond[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'ticker' not in READY_TO_salebond[uid]:
			READY_TO_salebond[uid]['ticker'] = message.text
			text = 'Введите количество облигаций'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_salebond[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_salebond[uid]['count'] = message.text
			text = 'Введите стоимость облигации'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_salebond[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_salebond[uid]['price'] = message.text
			text = 'Введите НКД'
			return bot.send_message(cid, text)
		if 'nkd' not in READY_TO_salebond[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_salebond[uid]['nkd'] = message.text
			util.DataBase.add_salebond(
				uid, int(time.time()), 
				READY_TO_salebond[uid]['input_date'],
				READY_TO_salebond[uid]['ticker'], 
				READY_TO_salebond[uid]['count'],
				READY_TO_salebond[uid]['broker'],
				READY_TO_salebond[uid]['nkd'],
				READY_TO_salebond[uid]['price'])
			print(READY_TO_salebond[uid])
			del READY_TO_salebond[uid]
			text = 'Вы успешно продали облигации'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать сотояние удержания налога
	if uid in READY_TO_TAX:
		if 'input_date' not in READY_TO_TAX[uid]:
			READY_TO_TAX[uid]['input_date'] = message.text
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_TAX[uid]:
			READY_TO_TAX[uid]['broker'] = message.text
			text = 'Введите стоимость налога'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_TAX[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_TAX[uid]['amount'] = int(message.text)
			util.DataBase.add_new_tax(
				uid, int(time.time()), 
				READY_TO_TAX[uid]['input_date'],
				READY_TO_TAX[uid]['amount'], 
				READY_TO_TAX[uid]['broker'])
			print(READY_TO_TAX[uid])
			del READY_TO_TAX[uid]
			text = 'Вы успешно оплатили налог'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)
	
	# Обработать сотояние удержания комиссии
	if uid in READY_TO_COMISSION:
		if 'input_date' not in READY_TO_COMISSION[uid]:
			READY_TO_COMISSION[uid]['input_date'] = message.text
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_COMISSION[uid]:
			READY_TO_COMISSION[uid]['broker'] = message.text
			text = 'Введите стоимость комиссии'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_COMISSION[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_COMISSION[uid]['amount'] = int(message.text)
			util.DataBase.add_new_commission(
				uid, int(time.time()), 
				READY_TO_COMISSION[uid]['input_date'],
				READY_TO_COMISSION[uid]['amount'], 
				READY_TO_COMISSION[uid]['broker'])
			print(READY_TO_COMISSION[uid])
			del READY_TO_COMISSION[uid]
			text = 'Вы успешно оплатили комиссию'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать сотояние добавления купонного дохода
	if uid in READY_TO_couponincome:
		if 'input_date' not in READY_TO_couponincome[uid]:
			READY_TO_couponincome[uid]['input_date'] = message.text
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_couponincome[uid]:
			READY_TO_couponincome[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'bond' not in READY_TO_couponincome[uid]:
			READY_TO_couponincome[uid]['bond'] = message.text
			text = 'Введите стоимость дохода'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_couponincome[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_couponincome[uid]['amount'] = int(message.text)
			util.DataBase.add_new_couponincome(
				uid, int(time.time()), 
				READY_TO_couponincome[uid]['input_date'],
				READY_TO_couponincome[uid]['bond'],
				READY_TO_couponincome[uid]['amount'], 
				READY_TO_couponincome[uid]['broker'])
			print(READY_TO_couponincome[uid])
			del READY_TO_couponincome[uid]
			text = 'Вы успешно добавили купонный доход'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать сотояние добавления купонного дохода
	if uid in READY_TO_DIVIDENDS:
		if 'input_date' not in READY_TO_DIVIDENDS[uid]:
			READY_TO_DIVIDENDS[uid]['input_date'] = message.text
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_DIVIDENDS[uid]:
			READY_TO_DIVIDENDS[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
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
			util.DataBase.add_new_dividend(
				uid, int(time.time()), 
				READY_TO_DIVIDENDS[uid]['input_date'],
				READY_TO_DIVIDENDS[uid]['dividend'],
				READY_TO_DIVIDENDS[uid]['amount'], 
				READY_TO_DIVIDENDS[uid]['broker'])
			print(READY_TO_DIVIDENDS[uid])
			del READY_TO_DIVIDENDS[uid]
			text = 'Вы успешно добавили дивиденд'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	uid = call.from_user.id
	cid = call.message.chat.id

	print(call.data)

	try:
		bot.answer_callback_query(call.id, 'Выполнено')
	except Exception as e:
		print(e)

	# Обработать истории операций
	if call.data.startswith('history'):
		time_data = call.data.split('_')
		# Операции за текущий месяц
		if len(time_data) == 2:
			start_timestamp = datetime.datetime.now()
			d2 = start_timestamp - dateutil.relativedelta.relativedelta(months=1)
			end_timestamp = int(d2.timestamp())
		# Операции за прошлый месяц
		elif time_data[2] == 'lastmonth':
			d = datetime.datetime.now()
			start_timestamp = d - dateutil.relativedelta.relativedelta(months=1)
			d2 = start_timestamp - dateutil.relativedelta.relativedelta(months=1)
			start_timestamp = int(start_timestamp.timestamp())
			end_timestamp = int(d2.timestamp())
		# Операции за 3 месяца
		elif time_data[2] == 'threemonths':
			start_timestamp = datetime.datetime.now()
			d2 = start_timestamp - dateutil.relativedelta.relativedelta(months=3)
			end_timestamp = int(d2.timestamp())
		# Операции за все время
		elif time_data[2] == 'allmonths':
			start_timestamp = datetime.datetime.now()
			end_timestamp = 0

		if time_data[1] == 'papers':
			available_tables = ['buystock', 'salestock', 'buybond', 'salebond']
		elif time_data[1] == 'money':
			available_tables = [
				'accountamount', 'accountminusamount', 
				'taxes', 'comissions', 
				'couponincome', 'dividends'
			]

		operations = util.get_history(uid, start_timestamp, end_timestamp)
		print(operations)

		if len(operations) == 0:
			text = 'Вы ещё не совершили ни одной операции за это время'
			bot.edit_message_text(text, cid, call.message.message_id)

		text = ''
		for x in operations:
			if x['table'] not in available_tables:
				continue
			# _date = datetime.datetime.utcfromtimestamp(int(x['date'])).strftime('%Y.%m.%d     %H:%M:%S')
			text += 'Операция: {!s}\nДата: {!s}\n'.format(x['title'], x['input_date'])

			if x['table'] == 'accountamount':
				text += 'Сумма: {!s}\nБрокер: {!s}'.format(x['amount'], x['broker'])
			if x['table'] == 'accountminusamount':
				text += 'Сумма: {!s}\nБрокер: {!s}'.format(x['amount'], x['broker'])
			if x['table'] == 'buystock':
				text += 'Тикер: {!s}\nКол-во: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
					x['ticker'], x['count'], x['price'], x['broker'])
			if x['table'] == 'salestock':
				text += 'Тикер: {!s}\nКол-во: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
					x['ticker'], x['count'], x['price'], x['broker'])
			if x['table'] == 'buybond':
				text += 'Тикер: {!s}\nКол-во: {!s}\nНКД: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
					x['ticker'], x['count'], x['nkd'], x['price'], x['broker'])
			if x['table'] == 'salebond':
				text += 'Тикер: {!s}\nКол-во: {!s}\nНКД: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
					x['ticker'], x['count'], x['nkd'], x['price'], x['broker'])
			if x['table'] == 'taxes':
				text += 'Сумма: {!s}\nБрокер: {!s}'.format(x['amount'], x['broker'])
			if x['table'] == 'comissions':
				text += 'Сумма: {!s}\nБрокер: {!s}'.format(x['amount'], x['broker'])
			if x['table'] == 'couponincome':
				text += 'Тикер: {!s}\nСумма: {!s}\nБрокер: {!s}'.format(
					x['bond'], x['amount'], x['broker'])
			if x['table'] == 'dividends':
				text += 'Тикер: {!s}\nСумма: {!s}\nБрокер: {!s}'.format(
					x['dividend'], x['amount'], x['broker'])
			text += '\nЧто бы удалить операцию, нажмите на ссылку /del_{!s}_{!s}\n\n'.format(x['table'], x['id'])
			
			if len(text) > 3500:
				bot.send_message(cid, text)
				text = ''

		if len(text) > 0:
			bot.send_message(cid, text)

		if time_data[1] == 'papers':
			mk = config.papers_history_markup
			text = 'Вы можете посмотреть операции c ценными бумагами за другой промежуток времени'
		if time_data[1] == 'money':
			mk = config.money_history_markup
			text = 'Вы можете посмотреть операции c деньгами за другой промежуток времени'
		keyboard = types.InlineKeyboardMarkup()
		for x in mk:
			keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
		return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать удаление операций
	if call.data.startswith('delop'):
		arr = call.data.split('-')
		util.DataBase.delete_operation(arr[1], uid, arr[2])		
		text = 'Операция успешно удалена'
		bot.edit_message_text(text, cid, call.message.message_id)
		text = 'Вы можете посмотреть операции'
		keyboard = types.InlineKeyboardMarkup()
		for x in config.schet_markup:
			keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
		return bot.send_message(cid, text, reply_markup=keyboard)
	
	if call.data == 'cancelldelete':
		text = 'Удаление отменено'
		return bot.edit_message_text(text, cid, call.message.message_id)

	# Обработать кнопки выбора операции
	if call.data == 'add_amount':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_ADD_AMOUNT[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'minus_amount':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_MINUS_ACCOUNT[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'add_aczii':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_buystock[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'delete_aczii':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_salestock[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'add_oblig':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_buybond[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'delete_oblig':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_salebond[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'pay_nalog':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_TAX[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'pay_comission':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_COMISSION[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГ'
		return bot.send_message(cid, text)
	if call.data == 'get_cupon':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_couponincome[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГ'
		return bot.send_message(cid, text)
	if call.data == 'get_dividends':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_DIVIDENDS[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГ'
		return bot.send_message(cid, text)

	'''
	# Обработать состояние добавления средств
	if uid in READY_TO_ADD_AMOUNT:
		if 'broker' not in READY_TO_ADD_AMOUNT[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_ADD_AMOUNT[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_new_amount(
				uid, int(time.time()),
				READY_TO_ADD_AMOUNT[uid]['input_date'],
				READY_TO_ADD_AMOUNT[uid]['amount'], 
				READY_TO_ADD_AMOUNT[uid]['broker'])
			print(READY_TO_ADD_AMOUNT[uid])
			del READY_TO_ADD_AMOUNT[uid]
			text = 'Вы успешно пополнили счет'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)
	
	# Обработать вывод средств
	if uid in READY_TO_MINUS_ACCOUNT:
		if 'broker' not in READY_TO_MINUS_ACCOUNT[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_MINUS_ACCOUNT[uid]['broker'] = config.brokers[call.data]
			print(READY_TO_MINUS_ACCOUNT[uid])
			util.DataBase.add_minus_amount(
				uid, int(time.time()), 
				READY_TO_MINUS_ACCOUNT[uid]['input_date'],
				READY_TO_MINUS_ACCOUNT[uid]['amount'],
				READY_TO_MINUS_ACCOUNT[uid]['broker'])
			del READY_TO_MINUS_ACCOUNT[uid]
			text = 'Вы успешно вывели средства'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать покупку акции
	if uid in READY_TO_buystock:
		if 'broker' not in READY_TO_buystock[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_buystock[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_buystock(
				uid, int(time.time()),
				READY_TO_buystock[uid]['input_date'],
				READY_TO_buystock[uid]['ticker'],
				READY_TO_buystock[uid]['count'],
				READY_TO_buystock[uid]['broker'],
				READY_TO_buystock[uid]['price'],
				READY_TO_buystock[uid]['api_price'])
			print(READY_TO_buystock[uid])
			del READY_TO_buystock[uid]
			text = 'Вы успешно купили акцию'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать продажу акции
	if uid in READY_TO_salestock:
		if 'broker' not in READY_TO_salestock[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_salestock[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_salestock(
				uid, int(time.time()),
				READY_TO_salestock[uid]['input_date'],
				READY_TO_salestock[uid]['ticker'],
				READY_TO_salestock[uid]['count'],
				READY_TO_salestock[uid]['broker'],
				READY_TO_salestock[uid]['price'])
			print(READY_TO_salestock[uid])
			del READY_TO_salestock[uid]
			text = 'Вы успешно продали акцию'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать покупку облигации
	if uid in READY_TO_buybond:
		if 'broker' not in READY_TO_buybond[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_buybond[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_buybond(
				uid, int(time.time()), 
				READY_TO_buybond[uid]['input_date'],
				READY_TO_buybond[uid]['ticker'], 
				READY_TO_buybond[uid]['count'],
				READY_TO_buybond[uid]['nkd'],
				READY_TO_buybond[uid]['price'],
				READY_TO_buybond[uid]['broker'],
				READY_TO_buybond[uid]['api_price'])
			print(READY_TO_buybond[uid])
			del READY_TO_buybond[uid]
			text = 'Вы успешно купили облигации'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать продажу облигации
	if uid in READY_TO_salebond:
		if 'broker' not in READY_TO_salebond[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_salebond[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_salebond(
				uid, int(time.time()), 
				READY_TO_salebond[uid]['input_date'],
				READY_TO_salebond[uid]['ticker'], 
				READY_TO_salebond[uid]['count'],
				READY_TO_salebond[uid]['broker'],
				READY_TO_salebond[uid]['nkd'],
				READY_TO_salebond[uid]['price'])
			print(READY_TO_salebond[uid])
			del READY_TO_salebond[uid]
			text = 'Вы успешно продали облигации'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать сотояние удержания налога
	if uid in READY_TO_TAX:
		if 'broker' not in READY_TO_TAX[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_TAX[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_new_tax(
				uid, int(time.time()), 
				READY_TO_TAX[uid]['input_date'],
				READY_TO_TAX[uid]['amount'], 
				READY_TO_TAX[uid]['broker'])
			print(READY_TO_TAX[uid])
			del READY_TO_TAX[uid]
			text = 'Вы успешно оплатили налог'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать сотояние удержания комиссии
	if uid in READY_TO_COMISSION:
		if 'broker' not in READY_TO_COMISSION[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_COMISSION[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_new_commission(
				uid, int(time.time()), 
				READY_TO_COMISSION[uid]['input_date'],
				READY_TO_COMISSION[uid]['amount'], 
				READY_TO_COMISSION[uid]['broker'])
			print(READY_TO_COMISSION[uid])
			del READY_TO_COMISSION[uid]
			text = 'Вы успешно оплатили комиссию'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать сотояние добавления купонного дохода
	if uid in READY_TO_couponincome:
		if 'broker' not in READY_TO_couponincome[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_couponincome[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_new_couponincome(
				uid, int(time.time()), 
				READY_TO_couponincome[uid]['input_date'],
				READY_TO_couponincome[uid]['bond'],
				READY_TO_couponincome[uid]['amount'], 
				READY_TO_couponincome[uid]['broker'])
			print(READY_TO_couponincome[uid])
			del READY_TO_couponincome[uid]
			text = 'Вы успешно добавили купонный доход'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать сотояние добавления купонного дохода
	if uid in READY_TO_DIVIDENDS:
		if 'broker' not in READY_TO_DIVIDENDS[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_DIVIDENDS[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_new_dividend(
				uid, int(time.time()), 
				READY_TO_DIVIDENDS[uid]['input_date'],
				READY_TO_DIVIDENDS[uid]['dividend'],
				READY_TO_DIVIDENDS[uid]['amount'], 
				READY_TO_DIVIDENDS[uid]['broker'])
			print(READY_TO_DIVIDENDS[uid])
			del READY_TO_DIVIDENDS[uid]
			text = 'Вы успешно добавили дивиденд'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)
	'''


def monitor():
	"""
	Обновлять данные с биржи раз в сутки
	"""
	schedule.every().day.at('00:00').do(util.update_moex)
	while True:
		schedule.run_pending()
		time.sleep(1)


def main():
	util.DataBase.deploy_database()
	th1 = threading.Thread(target=monitor)
	th1.start()
	if config.DEBUG:
		apihelper.proxy = {'https': 'socks5h://13.95.197.15:1080'}
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

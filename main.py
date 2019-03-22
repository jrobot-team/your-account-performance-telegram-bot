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
	text = 'Главное меню'
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
	for x in config.main_markup:
		markup.row(*x)
	return bot.send_message(cid, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text_handler(message):
	cid = message.chat.id
	uid = message.from_user.id

	'''
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
		text = 'Действие отменено'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for x in config.main_markup:
			markup.row(*x)
		return bot.send_message(cid, text, reply_markup=markup)
	'''

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
			table_name = 'Удержание налога'
		elif arr[1] == 'comissions':
			table_name = 'Удержание комиссии'
		elif arr[1] == 'couponincome':
			table_name = 'Зачисление купонного дохода'
		elif arr[1] == 'dividends':
			table_name = 'Зачисление дивидендов'

		_date = datetime.datetime.utcfromtimestamp(int(operation['input_date'])).strftime('%d.%m.%Y')
		text = 'Дата: {!s}\n'.format(_date)
		if arr[1] == 'accountamount':
			text += 'Сумма: {!s}\nБрокер: {!s}'.format(operation['amount'], operation['broker'])
		if arr[1] == 'accountminusamount':
			text += 'Сумма: {!s}\nБрокер: {!s}'.format(operation['amount'], operation['broker'])
		if arr[1] == 'buystock':
			text += 'Тикер: {!s}\nКоличество: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
				operation['ticker'], operation['count'], operation['price'], operation['broker'])
		if arr[1] == 'salestock':
			text += 'Тикер: {!s}\nКоличество: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
				operation['ticker'], operation['count'], operation['price'], operation['broker'])
		if arr[1] == 'buybond':
			text += 'Тикер: {!s}\nКоличество: {!s}\nНКД: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
				operation['ticker'], operation['count'], operation['nkd'], operation['price'], operation['broker'])
		if arr[1] == 'salebond':
			text += 'Тикер: {!s}\nКоличество: {!s}\nНКД: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
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

	'''
	# Вернуться в главное меню
	if message.text == '↩️ Назад':
		text = 'Главное меню'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for x in config.main_markup:
			markup.row(*x)
		return bot.send_message(cid, text, reply_markup=markup)
	'''

	# Обработать главное меню
	if message.text == 'Добавить операцию':
		text = 'Выберите тип операции'
		keyboard = types.InlineKeyboardMarkup()
		for x in config.operations_markup:
			keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
		return bot.send_message(cid, text, reply_markup=keyboard)
	elif message.text == 'Портфель':
		account = util.get_account_state(uid)
		portfolio_amount = util.get_portfolio_amount(uid)
		text = 'На брокерских счетах {!s} ₽, в т.ч. денежных средств {!s} ₽. Накопленная прибыль/убыток {!s} ₽'.format(
			int(account['amount']), int(account['money_amount']), portfolio_amount)
		bot.send_message(cid, text)
		text = 'Обработка данных...'
		msg = bot.send_message(cid, text)
		text = ''
		portfolio = util.get_portfolio(uid)
		for x in portfolio['stocks']:
			text += '*{!s}*\nВ портфеле {!s} шт.\nСред. цена {!s} ₽\n'.format(
				x['ticker'], x['count'], int(x['average_price']))
			text += 'Цена закрытия: {!s} ₽\nСтоимость {!s} ₽\nПрибыль/убыток {!s} ₽\n\n'.format(
				int(x['close_price']), int(x['current_price']), int(x['price_difference']))
		for x in portfolio['bonds']:
			text += '*{!s}*\nВ портфеле {!s} шт.\nСред. цена {!s} ₽\n'.format(
				x['ticker'], x['count'], int(x['average_price']))
			text += 'Цена закрытия: {!s} ₽\nСтоимость {!s} ₽\nПрибыль/убыток {!s} ₽\n\n'.format(
				int(x['close_price']), int(x['current_price']), int(x['price_difference']))
		if len(text) == 0:
			text = 'Вы ещё не совершали ни одной операции'
		keyboard = types.InlineKeyboardMarkup()
		for x in config.schet_markup:
			keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
		return bot.edit_message_text(text, chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=keyboard, parse_mode='MARKDOWN')

	# Обработать состояние добавления средств
	if uid in READY_TO_ADD_AMOUNT:
		if 'input_date' not in READY_TO_ADD_AMOUNT[uid]:
			timestamp = util.get_timestamp(message.text)
			if not timestamp:
				text = 'Неверный формат даты.\nФормат: ДД.ММ.ГГГГ'
				return bot.send_message(cid, text)
			READY_TO_ADD_AMOUNT[uid]['input_date'] = timestamp
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_ADD_AMOUNT[uid]:
			READY_TO_ADD_AMOUNT[uid]['broker'] = message.text
			text = 'Укажите сумму'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_ADD_AMOUNT[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_ADD_AMOUNT[uid]['amount'] = message.text
			util.DataBase.add_new_amount(
				uid, int(time.time()),
				READY_TO_ADD_AMOUNT[uid]['input_date'],
				READY_TO_ADD_AMOUNT[uid]['amount'],
				READY_TO_ADD_AMOUNT[uid]['broker'])
			print(READY_TO_ADD_AMOUNT[uid])
			del READY_TO_ADD_AMOUNT[uid]
			text = 'Операция успешно добавлена'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)
	
	# Обработать состояние вывода средств
	if uid in READY_TO_MINUS_ACCOUNT:
		if 'input_date' not in READY_TO_MINUS_ACCOUNT[uid]:
			timestamp = util.get_timestamp(message.text)
			if not timestamp:
				text = 'Неверный формат даты.\nФормат: ДД.ММ.ГГГГ'
				return bot.send_message(cid, text)
			READY_TO_MINUS_ACCOUNT[uid]['input_date'] = timestamp
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_MINUS_ACCOUNT[uid]:
			READY_TO_MINUS_ACCOUNT[uid]['broker'] = message.text
			text = 'Укажите сумму'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_MINUS_ACCOUNT[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_MINUS_ACCOUNT[uid]['amount'] = message.text
			print(READY_TO_MINUS_ACCOUNT[uid])
			util.DataBase.add_minus_amount(
				uid, int(time.time()), 
				READY_TO_MINUS_ACCOUNT[uid]['input_date'],
				READY_TO_MINUS_ACCOUNT[uid]['amount'],
				READY_TO_MINUS_ACCOUNT[uid]['broker'])
			del READY_TO_MINUS_ACCOUNT[uid]
			text = 'Операция успешно добавлена'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать покупку акции
	if uid in READY_TO_buystock:
		if 'input_date' not in READY_TO_buystock[uid]:
			timestamp = util.get_timestamp(message.text)
			if not timestamp:
				text = 'Неверный формат даты.\nФормат: ДД.ММ.ГГГГ'
				return bot.send_message(cid, text)
			READY_TO_buystock[uid]['input_date'] = timestamp
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_buystock[uid]:
			READY_TO_buystock[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'ticker' not in READY_TO_buystock[uid]:
			api_price = util.Moex.get_stock_price(message.text)
			if not api_price:
				text = 'Такого тикера не существует'
				return bot.send_message(cid, text)
			READY_TO_buystock[uid]['api_price'] = api_price
			READY_TO_buystock[uid]['ticker'] = message.text.upper()
			text = 'Укажите количество акций'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_buystock[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_buystock[uid]['count'] = int(message.text)
			text = 'Укажите цену акции'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_buystock[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_buystock[uid]['price'] = message.text
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
			text = 'Операция успешно добавлена'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать продажу акции
	if uid in READY_TO_salestock:
		if 'input_date' not in READY_TO_salestock[uid]:
			timestamp = util.get_timestamp(message.text)
			if not timestamp:
				text = 'Неверный формат даты.\nФормат: ДД.ММ.ГГГГ'
				return bot.send_message(cid, text)
			READY_TO_salestock[uid]['input_date'] = timestamp
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_salestock[uid]:
			READY_TO_salestock[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'ticker' not in READY_TO_salestock[uid]:
			READY_TO_salestock[uid]['ticker'] = message.text.upper()
			text = 'Укажите количество акций'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_salestock[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_salestock[uid]['count'] = int(message.text)
			text = 'Укажите цену акции'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_salestock[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_salestock[uid]['price'] = message.text
			util.DataBase.add_salestock(
				uid, int(time.time()),
				READY_TO_salestock[uid]['input_date'],
				READY_TO_salestock[uid]['ticker'],
				READY_TO_salestock[uid]['count'],
				READY_TO_salestock[uid]['broker'],
				READY_TO_salestock[uid]['price'])
			print(READY_TO_salestock[uid])
			del READY_TO_salestock[uid]
			text = 'Операция успешно добавлена'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать покупку облигации
	if uid in READY_TO_buybond:
		if 'input_date' not in READY_TO_buybond[uid]:
			timestamp = util.get_timestamp(message.text)
			if not timestamp:
				text = 'Неверный формат даты.\nФормат: ДД.ММ.ГГГГ'
				return bot.send_message(cid, text)
			READY_TO_buybond[uid]['input_date'] = timestamp
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_buybond[uid]:
			READY_TO_buybond[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'ticker' not in READY_TO_buybond[uid]:
			data = util.Moex.get_bond_data(message.text)
			if not data:
				text = 'Такого тикера не существует'
				return bot.send_message(cid, text)
			READY_TO_buybond[uid]['api_price'] = data['price']
			READY_TO_buybond[uid]['api_nkd'] = data['nkd']
			READY_TO_buybond[uid]['api_FACEVALUE'] = data['FACEVALUE']
			READY_TO_buybond[uid]['api_ACCINT'] = data['ACCINT']
			READY_TO_buybond[uid]['ticker'] = message.text.upper()
			text = 'Укажите количество облигаций'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_buybond[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_buybond[uid]['count'] = int(message.text)
			text = 'Укажите цену облигации'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_buybond[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_buybond[uid]['price'] = message.text
			text = 'Укажите НКД'
			return bot.send_message(cid, text)
		if 'nkd' not in READY_TO_buybond[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_buybond[uid]['nkd'] = message.text
			util.DataBase.add_buybond(
				uid, int(time.time()), 
				READY_TO_buybond[uid]['input_date'],
				READY_TO_buybond[uid]['ticker'], 
				READY_TO_buybond[uid]['count'],
				READY_TO_buybond[uid]['nkd'],
				READY_TO_buybond[uid]['price'],
				READY_TO_buybond[uid]['broker'],
				READY_TO_buybond[uid]['api_price'],
				READY_TO_buybond[uid]['api_nkd'],
				READY_TO_buybond[uid]['api_FACEVALUE'],
				READY_TO_buybond[uid]['api_ACCINT'])
			print(READY_TO_buybond[uid])
			del READY_TO_buybond[uid]
			text = 'Операция успешно добавлена'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)
	
	# Обработать продажу облигации
	if uid in READY_TO_salebond:
		if 'input_date' not in READY_TO_salebond[uid]:
			timestamp = util.get_timestamp(message.text)
			if not timestamp:
				text = 'Неверный формат даты.\nФормат: ДД.ММ.ГГГГ'
				return bot.send_message(cid, text)
			READY_TO_salebond[uid]['input_date'] = timestamp
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_salebond[uid]:
			READY_TO_salebond[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'ticker' not in READY_TO_salebond[uid]:
			READY_TO_salebond[uid]['ticker'] = message.text.upper()
			text = 'Укажите количество облигаций'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_salebond[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_salebond[uid]['count'] = message.text
			text = 'Укажите цену облигации'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_salebond[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_salebond[uid]['price'] = message.text
			text = 'Укажите НКД'
			return bot.send_message(cid, text)
		if 'nkd' not in READY_TO_salebond[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
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
			text = 'Операция успешно добавлена'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать сотояние удержания налога
	if uid in READY_TO_TAX:
		if 'input_date' not in READY_TO_TAX[uid]:
			timestamp = util.get_timestamp(message.text)
			if not timestamp:
				text = 'Неверный формат даты.\nФормат: ДД.ММ.ГГГГ'
				return bot.send_message(cid, text)
			READY_TO_TAX[uid]['input_date'] = timestamp
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_TAX[uid]:
			READY_TO_TAX[uid]['broker'] = message.text
			text = 'Укажите сумму'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_TAX[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_TAX[uid]['amount'] = message.text
			util.DataBase.add_new_tax(
				uid, int(time.time()), 
				READY_TO_TAX[uid]['input_date'],
				READY_TO_TAX[uid]['amount'], 
				READY_TO_TAX[uid]['broker'])
			print(READY_TO_TAX[uid])
			del READY_TO_TAX[uid]
			text = 'Операция успешно добавлена'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)
	
	# Обработать сотояние удержания комиссии
	if uid in READY_TO_COMISSION:
		if 'input_date' not in READY_TO_COMISSION[uid]:
			timestamp = util.get_timestamp(message.text)
			if not timestamp:
				text = 'Неверный формат даты.\nФормат: ДД.ММ.ГГГГ'
				return bot.send_message(cid, text)
			READY_TO_COMISSION[uid]['input_date'] = timestamp
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_COMISSION[uid]:
			READY_TO_COMISSION[uid]['broker'] = message.text
			text = 'Укажите сумму'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_COMISSION[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_COMISSION[uid]['amount'] = message.text
			util.DataBase.add_new_commission(
				uid, int(time.time()), 
				READY_TO_COMISSION[uid]['input_date'],
				READY_TO_COMISSION[uid]['amount'], 
				READY_TO_COMISSION[uid]['broker'])
			print(READY_TO_COMISSION[uid])
			del READY_TO_COMISSION[uid]
			text = 'Операция успешно добавлена'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать сотояние добавления купонного дохода
	if uid in READY_TO_couponincome:
		if 'input_date' not in READY_TO_couponincome[uid]:
			timestamp = util.get_timestamp(message.text)
			if not timestamp:
				text = 'Неверный формат даты.\nФормат: ДД.ММ.ГГГГ'
				return bot.send_message(cid, text)
			READY_TO_couponincome[uid]['input_date'] = timestamp
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_couponincome[uid]:
			READY_TO_couponincome[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'bond' not in READY_TO_couponincome[uid]:
			READY_TO_couponincome[uid]['bond'] = message.text
			text = 'Укажите сумму'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_couponincome[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_couponincome[uid]['amount'] = message.text
			util.DataBase.add_new_couponincome(
				uid, int(time.time()), 
				READY_TO_couponincome[uid]['input_date'],
				READY_TO_couponincome[uid]['bond'],
				READY_TO_couponincome[uid]['amount'], 
				READY_TO_couponincome[uid]['broker'])
			print(READY_TO_couponincome[uid])
			del READY_TO_couponincome[uid]
			text = 'Операция успешно добавлена'
			bot.send_message(cid, text)
			text = 'Выберите тип операции'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.operations_markup:
				keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
			return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать сотояние добавления купонного дохода
	if uid in READY_TO_DIVIDENDS:
		if 'input_date' not in READY_TO_DIVIDENDS[uid]:
			timestamp = util.get_timestamp(message.text)
			if not timestamp:
				text = 'Неверный формат даты.\nФормат: ДД.ММ.ГГГГ'
				return bot.send_message(cid, text)
			READY_TO_DIVIDENDS[uid]['input_date'] = timestamp
			text = 'Укажите брокера'
			return bot.send_message(cid, text)
		if 'broker' not in READY_TO_DIVIDENDS[uid]:
			READY_TO_DIVIDENDS[uid]['broker'] = message.text
			text = 'Укажите тикер'
			return bot.send_message(cid, text)
		if 'dividend' not in READY_TO_DIVIDENDS[uid]:
			READY_TO_DIVIDENDS[uid]['dividend'] = message.text
			text = 'Укажите сумму'
			return bot.send_message(cid, text)
		if 'amount' not in READY_TO_DIVIDENDS[uid]:
			message.text = message.text.replace(',', '.')
			try:
				float(message.text)
			except Exception as e:
				text = 'Введите целое число!'
				return bot.send_message(cid, text)
			READY_TO_DIVIDENDS[uid]['amount'] = message.text
			util.DataBase.add_new_dividend(
				uid, int(time.time()), 
				READY_TO_DIVIDENDS[uid]['input_date'],
				READY_TO_DIVIDENDS[uid]['dividend'],
				READY_TO_DIVIDENDS[uid]['amount'], 
				READY_TO_DIVIDENDS[uid]['broker'])
			print(READY_TO_DIVIDENDS[uid])
			del READY_TO_DIVIDENDS[uid]
			text = 'Операция успешно добавлена'
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
			start_timestamp = int(start_timestamp.timestamp())
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
			start_timestamp = int(start_timestamp.timestamp())
			end_timestamp = int(d2.timestamp())
		# Операции за все время
		elif time_data[2] == 'allmonths':
			start_timestamp = 32510505600
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
			_date = datetime.datetime.utcfromtimestamp(int(x['input_date'])).strftime('%d.%m.%Y')
			text += 'Операция: {!s}\nДата: {!s}\n'.format(x['title'], _date)

			if x['table'] == 'accountamount':
				text += 'Сумма: {!s}\nБрокер: {!s}'.format(x['amount'], x['broker'])
			if x['table'] == 'accountminusamount':
				text += 'Сумма: {!s}\nБрокер: {!s}'.format(x['amount'], x['broker'])
			if x['table'] == 'buystock':
				text += 'Тикер: {!s}\nКоличество: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
					x['ticker'], x['count'], x['price'], x['broker'])
			if x['table'] == 'salestock':
				text += 'Тикер: {!s}\nКоличество: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
					x['ticker'], x['count'], x['price'], x['broker'])
			if x['table'] == 'buybond':
				text += 'Тикер: {!s}\nКоличество: {!s}\nНКД: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
					x['ticker'], x['count'], x['nkd'], x['price'], x['broker'])
			if x['table'] == 'salebond':
				text += 'Тикер: {!s}\nКоличество: {!s}\nНКД: {!s}\nЦена: {!s}\nБрокер: {!s}'.format(
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
			text += '\nДля удаления операции нажмите на ссылку /del_{!s}_{!s}\n\n'.format(x['table'], x['id'])
			
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
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'minus_amount':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_MINUS_ACCOUNT[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'add_aczii':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_buystock[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'delete_aczii':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_salestock[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'add_oblig':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_buybond[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'delete_oblig':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_salebond[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'pay_nalog':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_TAX[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГГ'
		return bot.send_message(cid, text)
	elif call.data == 'pay_comission':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_COMISSION[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГГ'
		return bot.send_message(cid, text)
	if call.data == 'get_cupon':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_couponincome[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГГ'
		return bot.send_message(cid, text)
	if call.data == 'get_dividends':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_DIVIDENDS[uid] = {}
		text = 'Введите дату операции\nФормат: ДД.ММ.ГГГГ'
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
		# apihelper.proxy = {'https': 'socks5h://TV360_4_217166737:rkO8KhVov4x93EKs@0x5c.private.ss5.ch:1080'}
		apihelper.proxy = {'https': 'socks5h://111.223.75.178:8888'}
		bot.polling(none_stop=True, interval=0)
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

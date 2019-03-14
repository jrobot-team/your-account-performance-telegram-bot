#!/usr/bin/env python3

import time
import datetime
import dateutil.relativedelta

import telebot
from telebot import types, apihelper

import util
import config


bot = telebot.TeleBot(config.BOT_TOKEN)

READY_TO_ADD_AMOUNT = {}
READY_TO_MINUS_ACCOUNT = {}
READY_TO_BUY_STOCK = {}
READY_TO_SALE_STOCK = {}
READY_TO_BUY_BOND = {}
READY_TO_SALE_BOND = {}
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

	# Обработать состояние добавления средств
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
	
	# Обработать покупку акции
	if uid in READY_TO_BUY_STOCK:
		if 'ticker' not in READY_TO_BUY_STOCK[uid]:
			# TODO: сделать выборку цены акции
			READY_TO_BUY_STOCK[uid]['api_price'] = 0
			READY_TO_BUY_STOCK[uid]['ticker'] = message.text
			text = 'Напишите количество акций для покупки'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_BUY_STOCK[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_BUY_STOCK[uid]['count'] = int(message.text)
			text = 'Выберите брокера'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.brokers:
				keyboard.add(types.InlineKeyboardButton(text=config.brokers[x], callback_data=x))
			return bot.send_message(cid, text, reply_markup=keyboard)
		if 'broker' not in READY_TO_BUY_STOCK[uid]:
			text = 'Выберите одного из брокеров из списка'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_BUY_STOCK[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_BUY_STOCK[uid]['price'] = int(message.text)
			util.DataBase.add_buy_stock(
				uid, int(time.time()),
				READY_TO_BUY_STOCK[uid]['ticker'],
				READY_TO_BUY_STOCK[uid]['count'],
				READY_TO_BUY_STOCK[uid]['broker'],
				READY_TO_BUY_STOCK[uid]['price'],
				READY_TO_BUY_STOCK[uid]['api_price'])
			print(READY_TO_BUY_STOCK[uid])
			del READY_TO_BUY_STOCK[uid]
			text = 'Вы успешно купили акцию'
			return bot.send_message(cid, text)

	# Обработать продажу акции
	if uid in READY_TO_SALE_STOCK:
		if 'ticker' not in READY_TO_SALE_STOCK[uid]:
			READY_TO_SALE_STOCK[uid]['ticker'] = message.text
			text = 'Напишите количество акций для продажи'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_SALE_STOCK[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_SALE_STOCK[uid]['count'] = int(message.text)
			text = 'Выберите брокера'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.brokers:
				keyboard.add(types.InlineKeyboardButton(text=config.brokers[x], callback_data=x))
			return bot.send_message(cid, text, reply_markup=keyboard)
		if 'broker' not in READY_TO_SALE_STOCK[uid]:
			text = 'Выберите одного из брокеров из списка'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_SALE_STOCK[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_SALE_STOCK[uid]['price'] = int(message.text)
			util.DataBase.add_sale_stock(
				uid, int(time.time()),
				READY_TO_SALE_STOCK[uid]['ticker'],
				READY_TO_SALE_STOCK[uid]['count'],
				READY_TO_SALE_STOCK[uid]['broker'],
				READY_TO_SALE_STOCK[uid]['price'])
			print(READY_TO_SALE_STOCK[uid])
			del READY_TO_SALE_STOCK[uid]
			text = 'Вы успешно продали акцию'
			return bot.send_message(cid, text)
	
	# Обработать покупку облигации
	if uid in READY_TO_BUY_BOND:
		if 'ticker' not in READY_TO_BUY_BOND[uid]:
			# TODO: сделать выборку цены акции
			READY_TO_BUY_BOND[uid]['api_price'] = 0
			READY_TO_BUY_BOND[uid]['ticker'] = message.text
			text = 'Введите количество облигаций для покупки'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_BUY_BOND[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_BUY_BOND[uid]['count'] = int(message.text)
			text = 'Введите цену облигации'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_BUY_BOND[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_BUY_BOND[uid]['price'] = int(message.text)
			text = 'Введите НКД'
			return bot.send_message(cid, text)
		if 'nkd' not in READY_TO_BUY_BOND[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_BUY_BOND[uid]['nkd'] = int(message.text)
			util.DataBase.add_buy_bond(
				uid, int(time.time()), 
				READY_TO_BUY_BOND[uid]['ticker'], 
				READY_TO_BUY_BOND[uid]['count'],
				READY_TO_BUY_BOND[uid]['nkd'],
				READY_TO_BUY_BOND[uid]['price'])
			print(READY_TO_BUY_BOND[uid])
			del READY_TO_BUY_BOND[uid]
			text = 'Вы успешно купили облигации'
			return bot.send_message(cid, text)
	
	# Обработать продажу облигации
	if uid in READY_TO_SALE_BOND:
		if 'name' not in READY_TO_SALE_BOND[uid]:
			READY_TO_SALE_BOND[uid]['name'] = message.text
			text = 'Введите тикер облигации для покупки'
			return bot.send_message(cid, text)
		if 'ticker' not in READY_TO_SALE_BOND[uid]:
			READY_TO_SALE_BOND[uid]['ticker'] = message.text
			text = 'Введите количество облигаций'
			return bot.send_message(cid, text)
		if 'count' not in READY_TO_SALE_BOND[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_SALE_BOND[uid]['count'] = message.text
			text = 'Введите стоимость облигации'
			return bot.send_message(cid, text)
		if 'price' not in READY_TO_SALE_BOND[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_SALE_BOND[uid]['price'] = message.text
			text = 'Введите НКД'
			return bot.send_message(cid, text)
		if 'nkd' not in READY_TO_SALE_BOND[uid]:
			try:
				int(message.text)
			except Exception as e:
				text = 'Введите число!'
				return bot.send_message(cid, text)
			READY_TO_SALE_BOND[uid]['nkd'] = message.text
			text = 'Выберите брокера'
			keyboard = types.InlineKeyboardMarkup()
			for x in config.brokers:
				keyboard.add(types.InlineKeyboardButton(text=config.brokers[x], callback_data=x))
			return bot.send_message(cid, text, reply_markup=keyboard)
		if 'broker' not in READY_TO_SALE_BOND[uid]:
			text = 'Выберите одного из брокеров из списка'
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
		bot.answer_callback_query(call.id, '✅ Выполнено')
	except Exception as e:
		print(e)

	# Обработать истории операций
	if call.data.startswith('history'):
		time_data = call.data.split('_')
		# Операции за текущий месяц
		if len(time_data) == 1:
			start_timestamp = datetime.datetime.now()
			d2 = start_timestamp - dateutil.relativedelta.relativedelta(months=1)
			end_timestamp = int(d2.timestamp())
		# Операции за прошлый месяц
		elif time_data[1] == 'lastmonth':
			d = datetime.datetime.now()
			start_timestamp = d - dateutil.relativedelta.relativedelta(months=1)
			d2 = start_timestamp - dateutil.relativedelta.relativedelta(months=1)
			start_timestamp = int(start_timestamp.timestamp())
			end_timestamp = int(d2.timestamp())
		# Операции за 3 месяца
		elif time_data[1] == 'threemonths':
			start_timestamp = datetime.datetime.now()
			d2 = start_timestamp - dateutil.relativedelta.relativedelta(months=3)
			end_timestamp = int(d2.timestamp())
		# Операции за все время
		elif time_data[1] == 'allmonths':
			start_timestamp = datetime.datetime.now()
			end_timestamp = 0
	
		operations = util.get_history(uid, start_timestamp, end_timestamp)
		print(operations)

		if len(operations) == 0:
			text = 'Вы ещё не совершили ни одной операции за это время'
			bot.edit_message_text(text, cid, call.message.message_id)

		for x in operations:
			_date = datetime.datetime.utcfromtimestamp(int(x['date'])).strftime('%Y.%m.%d  %H:%M:%S')
			text = 'Операция: {!s}\nДата: {!s}\n'.format(x['title'], _date)

			if x['table'] == 'account_amount':
				text += 'Сумма: {!s}\nБрокер: {!s}'.format(x['amount'], x['broker'])
			if x['table'] == 'account_minus_amount':
				text += 'Сумма: {!s}'.format(x['amount'])
			if x['table'] == 'buy_stock':
				text += 'Тикер: {!s}\nКол-во: {!s}\nБрокер: {!s}\nЦена: {!s}'.format(
					x['ticker'], x['count'], x['broker'], x['price'])
			if x['table'] == 'sale_stock':
				text += 'Тикер: {!s}\nКол-во: {!s}\nБрокер: {!s}\nЦена: {!s}'.format(
					x['ticker'], x['count'], x['broker'], x['price'])
			if x['table'] == 'buy_bond':
				text += 'Тикер: {!s}\nКол-во: {!s}\nНКД: {!s}\nЦена: {!s}'.format(
					x['ticker'], x['count'], x['nkd'], x['price'])
			if x['table'] == 'sale_bond':
				text += 'Номер: {!s}\nТикер: {!s}\nКол-во: {!s}\nБрокер: {!s}\nНКД: {!s}\nЦена: {!s}'.format(
					x['name'], x['ticker'], x['count'], x['nkd'], x['nkd'], x['price'])
			if x['table'] == 'taxes':
				text += 'Сумма: {!s}\nБрокер: {!s}'.format(x['amount'], x['broker'])
			if x['table'] == 'comissions':
				text += 'Сумма: {!s}\nБрокер: {!s}'.format(x['amount'], x['broker'])
			if x['table'] == 'coupon_income':
				text += 'Идентификатор облигации: {!s}\nСумма: {!s}\nБрокер: {!s}'.format(
					x['bond'], x['amount'], x['broker'])
			if x['table'] == 'dividends':
				text += 'Идентификатор акции: {!s}\nСумма: {!s}\nБрокер: {!s}'.format(
					x['dividend'], x['amount'], x['broker'])

			keyboard = types.InlineKeyboardMarkup()
			cb = 'delop-{!s}-{!s}'.format(x['table'], x['id'])
			keyboard.add(types.InlineKeyboardButton(text='⛔ Удалить', callback_data=cb))
			bot.send_message(cid, text, reply_markup=keyboard)

		text = 'Вы можете посмотреть операции за другой промежуток времени'
		keyboard = types.InlineKeyboardMarkup()
		for x in config.history_markup:
			keyboard.add(types.InlineKeyboardButton(text=x[0]['text'], callback_data=x[0]['callback']))
		return bot.send_message(cid, text, reply_markup=keyboard)

	# Обработать удаление операций
	if call.data.startswith('delop'):
		arr = call.data.split('-')
		print(arr)
		util.DataBase.delete_operation(arr[1], uid, arr[2])		
		text = 'Операция успешно удалена'
		return bot.edit_message_text(text, cid, call.message.message_id)

	# Обработать кнопки выбора операции
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
		bot.delete_message(cid, call.message.message_id)
		READY_TO_BUY_STOCK[uid] = {}
		text = 'Введите тикер акции для покупки'
		return bot.send_message(cid, text)
	elif call.data == 'delete_aczii':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_SALE_STOCK[uid] = {}
		text = 'Введите тикер акции для продажи'
		return bot.send_message(cid, text)
	elif call.data == 'add_oblig':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_BUY_BOND[uid] = {}
		text = 'Введите тикер облигации для покупки'
		return bot.send_message(cid, text)
	elif call.data == 'delete_oblig':
		bot.delete_message(cid, call.message.message_id)
		READY_TO_SALE_BOND[uid] = {}
		text = 'Введите имя облигации для продажи'
		return bot.send_message(cid, text)
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

	# Обработать состояние добавления средств
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
	
	# Обработать покупку акции
	if uid in READY_TO_BUY_STOCK:
		if 'broker' not in READY_TO_BUY_STOCK[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_BUY_STOCK[uid]['broker'] = config.brokers[call.data]
			text = 'Введите цену акции'
			return bot.send_message(cid, text)
	
	# Обработать продажу акции
	if uid in READY_TO_SALE_STOCK:
		if 'broker' not in READY_TO_SALE_STOCK[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_SALE_STOCK[uid]['broker'] = config.brokers[call.data]
			text = 'Введите цену акции'
			return bot.send_message(cid, text)
	
	# Обработать продажу облигации
	if uid in READY_TO_SALE_BOND:
		if 'broker' not in READY_TO_SALE_BOND[uid]:
			bot.delete_message(cid, call.message.message_id)
			READY_TO_SALE_BOND[uid]['broker'] = config.brokers[call.data]
			util.DataBase.add_sale_bond(
				uid, int(time.time()), 
				READY_TO_SALE_BOND[uid]['name'], 
				READY_TO_SALE_BOND[uid]['ticker'], 
				READY_TO_SALE_BOND[uid]['count'],
				READY_TO_SALE_BOND[uid]['broker'],
				READY_TO_SALE_BOND[uid]['nkd'],
				READY_TO_SALE_BOND[uid]['price'])
			print(READY_TO_SALE_BOND[uid])
			del READY_TO_SALE_BOND[uid]
			text = 'Вы успешно продали облигации'
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

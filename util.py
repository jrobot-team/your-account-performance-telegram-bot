import time
import datetime
from operator import itemgetter

import requests
import pymysql.cursors

import config


class DataBase:
	"""
	DataBase Class
	"""

	@staticmethod
	def deploy_database():
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = '''
				CREATE TABLE IF NOT EXISTS `accountamount` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`input_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`amount` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `accountminusamount` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`input_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`amount` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `buystock` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`input_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`ticker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`count` int(11) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`price` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`api_price` varchar(255) COLLATE utf8_general_ci NOT NULL,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `salestock` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`input_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`ticker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`count` int(11) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`price` varchar(255) COLLATE utf8_general_ci NOT NULL,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `buybond` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`input_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`ticker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`count` int(11) COLLATE utf8_general_ci NOT NULL,
					`nkd` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci,
					`price` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`api_price` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`api_nkd` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`api_FACEVALUE` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`api_ACCINT` varchar(255) COLLATE utf8_general_ci NOT NULL,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `salebond` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`input_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`ticker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`count` int(11) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci,
					`nkd` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`price` varchar(255) COLLATE utf8_general_ci NOT NULL,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `taxes` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`input_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`amount` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `comissions` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`input_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`amount` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `couponincome` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`input_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`bond` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`amount` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `dividends` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`input_date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`dividend` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`amount` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_new_amount(uid, date, input_date, amount, broker):
		"""
		Пополнить счет
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'INSERT INTO `accountamount` (`uid`, `date`, `input_date`, `amount`, `broker`) VALUES (%s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, input_date, amount, broker))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_minus_amount(uid, date, input_date, amount, broker):
		"""
		Вывод средств
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'INSERT INTO `accountminusamount` (`uid`, `date`, `input_date`, `amount`, `broker`) VALUES (%s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, input_date, amount, broker))
			connection.commit()
		finally:
			connection.close()
	
	@staticmethod
	def add_buystock(uid, date, input_date, ticker, count, broker, price, api_price=0):
		"""
		Покупка акций
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'INSERT INTO `buystock` (`uid`, `date`, `input_date`, `ticker`, `count`, `broker`, `price`, `api_price`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, input_date, ticker, count, broker, price, api_price))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_salestock(uid, date, input_date, ticker, count, broker, price):
		"""
		Продажа акций
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'INSERT INTO `salestock` (`uid`, `date`, `input_date`, `ticker`, `count`, `broker`, `price`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, input_date, ticker, count, broker, price))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_buybond(uid, date, input_date, ticker, count, nkd, price, broker, api_price, api_nkd, api_FACEVALUE, api_ACCINT):
		"""
		Покупка облигаций
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'INSERT INTO `buybond` (`uid`, `date`, `input_date` ,`ticker`, `count`, `nkd`, `price`, `broker`, `api_price`, `api_nkd`, `api_FACEVALUE`, `api_ACCINT`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, input_date, ticker, count, nkd, price, broker, api_price, api_nkd, api_FACEVALUE, api_ACCINT))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_salebond(uid, date, input_date, ticker, count, broker, nkd, price):
		"""
		Продажа облигации
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'INSERT INTO `salebond` (`uid`, `date`, `input_date`, `ticker`, `count`, `broker`, `nkd`, `price`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, input_date, ticker, count, broker, nkd, price))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_new_tax(uid, date, input_date, amount, broker):
		"""
		Налог
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'INSERT INTO `taxes` (`uid`, `date`, `input_date`, `amount`, `broker`) VALUES (%s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, input_date, amount, broker))
			connection.commit()
		finally:
			connection.close()
	
	@staticmethod
	def add_new_commission(uid, date, input_date, amount, broker):
		"""
		Комиссия
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'INSERT INTO `comissions` (`uid`, `date`, `input_date`, `amount`, `broker`) VALUES (%s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, input_date, amount, broker))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_new_couponincome(uid, date, input_date, bond, amount, broker):
		"""
		Купонный доход
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'INSERT INTO `couponincome` (`uid`, `date`, `input_date`, `bond`, `amount`, `broker`) VALUES (%s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, input_date, bond, amount, broker))
			connection.commit()
		finally:
			connection.close()
	
	@staticmethod
	def add_new_dividend(uid, date, input_date, dividend, amount, broker):
		"""
		Зачисление дивидендов
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'INSERT INTO `dividends` (`uid`, `date`, `input_date`, `dividend`, `amount`, `broker`) VALUES (%s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, input_date, dividend, amount, broker))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def delete_operation(table, uid, id):
		"""
		Удалить операцию
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'DELETE FROM {!s} WHERE uid=%s AND id=%s' .format(table)
				cursor.execute(sql, (uid, id))
			connection.commit()
		finally:
			connection.close()
	
	@staticmethod
	def get_operation(table, uid, id):
		"""
		Получить операцию
		"""
		connection = pymysql.connect(
			host=config.db_host,
			user=config.db_user,
			password=config.db_password,
			db=config.db_database,
			charset=config.db_charset,
			cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				sql = 'SELECT * FROM {!s} WHERE uid=%s AND id=%s' .format(table)
				cursor.execute(sql, (uid, id))
				res = cursor.fetchone()
				return res
			connection.commit()
		except:
			return None
		finally:
			connection.close()
		return None


def get_history(uid, start_timestamp, end_timestamp):
	"""
	Получить историю операций в виде сообщений
	"""
	connection = pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)
	try:
		operations = []
		with connection.cursor() as cursor:

			sql = 'SELECT * FROM accountamount WHERE uid=%s AND input_date < %s AND input_date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Пополнение счета'
				operations[-1]['table'] = 'accountamount'
			
			sql = 'SELECT * FROM accountminusamount WHERE uid=%s AND input_date < %s AND input_date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Вывод средств'
				operations[-1]['table'] = 'accountminusamount'
			
			sql = 'SELECT * FROM buystock WHERE uid=%s AND input_date < %s AND input_date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Покупка акций'
				operations[-1]['table'] = 'buystock'
			
			sql = 'SELECT * FROM salestock WHERE uid=%s AND input_date < %s AND input_date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Продажа акций'
				operations[-1]['table'] = 'salestock'
			
			sql = 'SELECT * FROM buybond WHERE uid=%s AND input_date < %s AND input_date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Покупка облигаций'
				operations[-1]['table'] = 'buybond'
			
			sql = 'SELECT * FROM salebond WHERE uid=%s AND input_date < %s AND input_date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Продажа облигаций'
				operations[-1]['table'] = 'salebond'
			
			sql = 'SELECT * FROM taxes WHERE uid=%s AND input_date < %s AND input_date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Удержание налога'
				operations[-1]['table'] = 'taxes'
			
			sql = 'SELECT * FROM comissions WHERE uid=%s AND input_date < %s AND input_date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Удержание комиссии'
				operations[-1]['table'] = 'comissions'
			
			sql = 'SELECT * FROM couponincome WHERE uid=%s AND input_date < %s AND input_date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Зачисление купонного дохода'
				operations[-1]['table'] = 'couponincome'
			
			sql = 'SELECT * FROM dividends WHERE uid=%s AND input_date < %s AND input_date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Зачисление дивидендов'
				operations[-1]['table'] = 'dividends'

		connection.commit()
		return sorted(operations, key=itemgetter('input_date'), reverse=False)
	finally:
		connection.close()


class Moex:
	"""
	API биржи Moex
	"""

	@staticmethod
	def get_stock_price(tiker):
		"""
		Получить стоимость акции
		"""
		try:
			current_date = datetime.datetime.now().strftime('%Y-%m-%d')
			last_day = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
			res = requests.get('http://iss.moex.com/iss/securities.json?q={!s}'.format(tiker))
			board = ''
			for x in res.json()['securities']['data']:
				if x[1] == tiker:
					board = x[-1]
					break
			if len(board) == 0:
				return None
			# board = res.json()['securities']['data'][0][-1]
			url = 'http://iss.moex.com/iss/history/engines/stock/markets/shares/boards/{!s}/securities/{!s}.json?from={!s}&till={!s}'.format(
				board, tiker, last_day, current_date
			)
			print(url)
			res = requests.get(url)
			price = res.json()['history']['data'][-1][9]
			return float('{0: >#016.2f}'.format(float(price)).strip())
		except Exception as e:
			print(e)
			return None

	@staticmethod
	def get_bond_price(code):
		"""
		DEPRECATED!
		Получить стоимость облигации
		"""
		try:
			current_date = datetime.datetime.now().strftime('%Y-%m-%d')
			last_day = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
			res = requests.get('http://iss.moex.com/iss/securities.json?q={!s}'.format(code))
			board = res.json()['securities']['data'][0][-1]
			url = 'http://iss.moex.com/iss/history/engines/stock/markets/bonds/boards/{!s}/securities/{!s}.json?from={!s}&till={!s}'.format(
				board, code, last_day, current_date
			)
			res = requests.get(url)
			print(url)
			price = res.json()['history']['data'][-1][9]
			return float('{0: >#016.2f}'.format(float(price)).strip())
		except Exception as e:
			print(e)
			return None

	@staticmethod
	def get_bond_nkd(code):
		"""
		DEPRECATED!
		Получить стоимость облигации
		"""
		try:
			current_date = datetime.datetime.now().strftime('%Y-%m-%d')
			last_day = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
			res = requests.get('http://iss.moex.com/iss/securities.json?q={!s}'.format(code))
			board = res.json()['securities']['data'][0][-1]
			url = 'http://iss.moex.com/iss/history/engines/stock/markets/bonds/boards/{!s}/securities/{!s}.json?from={!s}&till={!s}'.format(
				board, code, last_day, current_date
			)
			res = requests.get(url)
			print(url)
			nkd = res.json()['history']['data'][-1][27]
			return float('{0: >#016.2f}'.format(float(nkd)).strip())
		except Exception as e:
			print(e)
			return None

	@staticmethod
	def get_bond_data(code):
		"""
		Получить стоимость облигации
		"""
		try:
			current_date = datetime.datetime.now().strftime('%Y-%m-%d')
			last_day = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
			res = requests.get('http://iss.moex.com/iss/securities.json?q={!s}'.format(code))
			board = res.json()['securities']['data'][0][-1]
			url = 'http://iss.moex.com/iss/history/engines/stock/markets/bonds/boards/{!s}/securities/{!s}.json?from={!s}&till={!s}'.format(
				board, code, last_day, current_date
			)
			res = requests.get(url)
			print(url)

			price = res.json()['history']['data'][-1][9]
			nkd = res.json()['history']['data'][-1][27]
			FACEVALUE = res.json()['history']['data'][-1][30]
			ACCINT = res.json()['history']['data'][-1][10]

			price = float('{0: >#016.2f}'.format(float(price)).strip())
			nkd = float('{0: >#016.2f}'.format(float(nkd)).strip())
			FACEVALUE = float('{0: >#016.2f}'.format(float(FACEVALUE)).strip())
			ACCINT = float('{0: >#016.2f}'.format(float(ACCINT)).strip())

			return {
				'price': price,
				'nkd': nkd,
				'FACEVALUE': FACEVALUE,
				'ACCINT': ACCINT,
			}
		except Exception as e:
			print(e)
			return None


def update_moex():
	"""
	Обновить стоимости акций и облигаций
	"""
	connection = pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)
	try:
		with connection.cursor() as cursor:
			# Обработать акции
			sql = 'SELECT * FROM buystock'
			cursor.execute(sql)
			res = cursor.fetchall()
			print(res)
			for stock in res:
				new_api_price = Moex.get_stock_price(stock['ticker'])
				sql = 'UPDATE buystock SET api_price=%s WHERE id=%s'
				cursor.execute(sql, (new_api_price, stock['id']))
			# Обработать облигации
			sql = 'SELECT * FROM buybond'
			cursor.execute(sql)
			res = cursor.fetchall()
			print(res)
			for bond in res:
				data = Moex.get_bond_data(bond['ticker'])
				sql = 'UPDATE buybond SET api_price=%s, api_nkd=%s, api_FACEVALUE=%s, api_ACCINT=%s WHERE id=%s'
				cursor.execute(sql, (data['price'], data['nkd'], data['FACEVALUE'], data['ACCINT'], bond['id']))
		connection.commit()
	finally:
		connection.close()
	return None


def get_timestamp(str_date):
	"""
	Получить timestamp из строка 

	:param: str_date - строка формата ДД.ММ.ГГГГ
	:return: timestamp (int) если строка валидная или None
	"""
	date_arr = str_date.split('.')
	if not len(date_arr) == 3:
		return None
	try:
		dt = datetime.datetime(int(date_arr[2]), int(date_arr[1]), int(date_arr[0])) 
		# Добавить +3 часа, что бы сойтись с мировым временем
		dt += datetime.timedelta(hours=3)
	except:
		return None
	try:
		unixtime = int(time.mktime(dt.timetuple()))
	except:
		return None
	return unixtime


def get_portfolio(uid):
	"""
	Получить информацию о портфеле пользователя
	"""
	connection = pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)
	try:
		result = {
			'stocks': [],
			'bonds': [],
		}
		with connection.cursor() as cursor:
			# Получить все купленные тикеры акций
			sql = 'SELECT DISTINCT ticker FROM buystock WHERE uid=%s'
			cursor.execute(sql, (uid,))
			tickers_buy = cursor.fetchall()
			sql = 'SELECT DISTINCT ticker FROM salestock WHERE uid=%s'
			cursor.execute(sql, (uid,))
			tickers_sale = cursor.fetchall()
			print(tickers_buy, tickers_sale)
			tickers = []
			for x in tickers_buy:
				if x['ticker'] not in tickers:
					tickers.append(x['ticker'])
			for x in tickers_sale:
				if x['ticker'] not in tickers:
					tickers.append(x['ticker'])
			print(tickers)
			for ticker in tickers:
				# ticker = x['ticker']
				sql = 'SELECT * FROM buystock WHERE uid=%s AND ticker=%s'
				cursor.execute(sql, (uid, ticker))
				res1 = cursor.fetchall()
				buy_count = 0
				for x in res1:
					buy_count += x['count']
				sql = 'SELECT * FROM salestock WHERE uid=%s AND ticker=%s'
				cursor.execute(sql, (uid, ticker))
				res2 = cursor.fetchall()
				sale_count = 0
				for x in res2:
					sale_count += x['count']
				print(buy_count, sale_count)
				# Количество акций по тикеру
				count = buy_count - sale_count
				print(count)
				if count == 0:
					continue

				amount = 0
				for x in res1:
					amount += float(x['price']) * int(x['count'])
				for x in res2:
					amount -= float(x['price']) * int(x['count'])
				# Сумма всех цен операций покупки
				print(amount)
				# Средняя стоимость
				average_price = amount / count
				print(average_price)

				# Текущая стоимость
				if len(res1) == 0:
					api_price = Moex.get_stock_price(ticker)
				else:
					api_price = res1[0]['api_price']
				current_price = float(api_price) * count
				print(current_price)
				# Разница стоимости
				price_difference = current_price - average_price * count
				print(price_difference)
				print('\n')
				result['stocks'].append({
					'ticker': ticker,
					'count': count,
					'average_price': float('{0: >#016.2f}'.format(float(average_price))),
					'close_price': float('{0: >#016.2f}'.format(float(api_price))),
					'current_price': float('{0: >#016.2f}'.format(float(current_price))),
					'price_difference': float('{0: >#016.2f}'.format(float(price_difference))),
				})

			# Получить все купленные тикеры облигаций
			sql = 'SELECT DISTINCT ticker FROM buybond WHERE uid=%s'
			cursor.execute(sql, (uid,))
			tickers_buy = cursor.fetchall()
			sql = 'SELECT DISTINCT ticker FROM salebond WHERE uid=%s'
			cursor.execute(sql, (uid,))
			tickers_sale = cursor.fetchall()
			print(tickers_buy, tickers_sale)
			tickers = []
			for x in tickers_buy:
				if x['ticker'] not in tickers:
					tickers.append(x['ticker'])
			for x in tickers_sale:
				if x['ticker'] not in tickers:
					tickers.append(x['ticker'])
			print(tickers)
			for ticker in tickers:
				# ticker = x['ticker']
				sql = 'SELECT * FROM buybond WHERE uid=%s AND ticker=%s'
				cursor.execute(sql, (uid, ticker))
				res1 = cursor.fetchall()
				buy_count = 0
				for x in res1:
					buy_count += x['count']
				sql = 'SELECT * FROM salebond WHERE uid=%s AND ticker=%s'
				cursor.execute(sql, (uid, ticker))
				res2 = cursor.fetchall()
				sale_count = 0
				for x in res2:
					sale_count += x['count']
				print(buy_count, sale_count)
				# Количество облигаций по тикеру
				count = buy_count - sale_count
				print(count)
				if count == 0:
					continue

				amount = 0
				for x in res1:
					amount += (float(x['price']) + float(x['nkd'])) * int(x['count'])
				for x in res2:
					amount -= (float(x['price']) + float(x['nkd'])) * int(x['count'])
				# Сумма всех цен операций покупки
				print(amount)
				# Средняя стоимость
				average_price = amount / count
				print(average_price)

				# Текущая стоимость
				if len(res1) == 0:
					data = Moex.get_bond_data(ticker)
					api_price = data['price']
					api_nkd = data['nkd']
					api_FACEVALUE = data['FACEVALUE']
					api_ACCINT = data['ACCINT']
				else:
					api_price = res1[0]['api_price']
					api_nkd = res1[0]['api_nkd']
					api_FACEVALUE = res1[0]['api_FACEVALUE']
					api_ACCINT = res1[0]['api_ACCINT']
				# current_price = (float(api_price) + float(api_nkd)) * count
				current_price = (float(api_price) * float(api_FACEVALUE) / 100 + float(api_ACCINT)) * count
				print(current_price)
				# Разница стоимости
				price_difference = current_price - average_price * count
				# price_difference = (average_price - current_price) * count
				print(price_difference)
				print('\n')
				result['bonds'].append({
					'ticker': ticker,
					'count': count,
					'average_price': float('{0: >#016.2f}'.format(float(average_price))),
					'close_price': float('{0: >#016.2f}'.format(float(api_price))),
					'current_price': float('{0: >#016.2f}'.format(float(current_price))),
					'price_difference': float('{0: >#016.2f}'.format(float(price_difference))),
				})
		connection.commit()
		return result
	finally:
		connection.close()


def get_portfolio_amount(uid):
	"""
	Получить накопленную прибыль/убыток
	"""
	data = get_portfolio(uid)
	print(data)
	amount = 0
	for x in data['stocks']:
		amount += x['price_difference']
	for x in data['bonds']:
		amount += x['price_difference']
	return int(amount)


def get_account_state(uid):
	"""
	Получить состояние счета пользователя
	"""
	connection = pymysql.connect(
		host=config.db_host,
		user=config.db_user,
		password=config.db_password,
		db=config.db_database,
		charset=config.db_charset,
		cursorclass=pymysql.cursors.DictCursor)
	try:
		broker_amount = 0
		money_amount = 0
		amount = 0
		with connection.cursor() as cursor:
			# Высчитать пополнение счета
			sql = 'SELECT * FROM accountamount WHERE uid=%s'
			cursor.execute(sql, (uid,))
			res = cursor.fetchall()
			for x in res:
				amount += float(x['amount'])
				money_amount += float(x['amount'])
			# Высчитать вывод средств
			sql = 'SELECT * FROM accountminusamount WHERE uid=%s'
			cursor.execute(sql, (uid,))
			res = cursor.fetchall()
			for x in res:
				amount -= float(x['amount'])
				money_amount -= float(x['amount'])
			# Высчитать покупку акций
			sql = 'SELECT * FROM buystock WHERE uid=%s'
			cursor.execute(sql, (uid,))
			res = cursor.fetchall()
			for x in res:
				amount -= float(x['price']) * int(x['count'])
				broker_amount += float(x['price']) * int(x['count'])
			# Высчитать продажу акций
			sql = 'SELECT * FROM salestock WHERE uid=%s'
			cursor.execute(sql, (uid,))
			res = cursor.fetchall()
			for x in res:
				amount += float(x['price']) * int(x['count'])
				broker_amount -= float(x['price']) * int(x['count'])
			# Высчитать покупку облигаций
			sql = 'SELECT * FROM buybond WHERE uid=%s'
			cursor.execute(sql, (uid,))
			res = cursor.fetchall()
			for x in res:
				amount -= float(x['price']) * int(x['count'])
				amount -= float(x['nkd'])
				broker_amount += float(x['price']) * int(x['count'])
				broker_amount += float(x['nkd'])
			# Высчитать продажу облигаций
			sql = 'SELECT * FROM salebond WHERE uid=%s'
			cursor.execute(sql, (uid,))
			res = cursor.fetchall()
			for x in res:
				amount += float(x['price']) * int(x['count']) 
				amount += float(x['nkd'])
				broker_amount -= float(x['price']) * int(x['count'])
				broker_amount -= float(x['nkd'])
			# Высчитать удержание налога
			sql = 'SELECT * FROM taxes WHERE uid=%s'
			cursor.execute(sql, (uid,))
			res = cursor.fetchall()
			for x in res:
				amount -= float(x['amount'])
				money_amount -= float(x['amount'])
			# Высчитать удержание комиссии
			sql = 'SELECT * FROM comissions WHERE uid=%s'
			cursor.execute(sql, (uid,))
			res = cursor.fetchall()
			for x in res:
				amount -= float(x['amount'])
				money_amount -= float(x['amount'])
			# Высчитать зачисление купонного дохода
			sql = 'SELECT * FROM couponincome WHERE uid=%s'
			cursor.execute(sql, (uid,))
			res = cursor.fetchall()
			for x in res:
				amount += float(x['amount'])
				money_amount += float(x['amount'])
			# Высчитать стоимость дивидедов
			sql = 'SELECT * FROM dividends WHERE uid=%s'
			cursor.execute(sql, (uid,))
			res = cursor.fetchall()
			for x in res:
				amount += float(x['amount'])
				money_amount += float(x['amount'])
		connection.commit()
		broker_amount += get_portfolio_amount(uid)
		return {
			'amount': amount,
			'money_amount': money_amount,
			'broker_amount': broker_amount,
		}
	finally:
		connection.close()


# print(get_account_state(217166737))
# print(get_portfolio(217166737))
# print(get_timestamp('21.03.3000'))
# print(Moex.get_stock_price('SBER'))
# print(Moex.get_bond_data('SU26210RMFS3'))
# print(get_portfolio_amount(217166737))
# update_moex()

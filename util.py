import datetime
from operator import itemgetter

import pandas as pd
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
					`amount` int(11) COLLATE utf8_general_ci NOT NULL,
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
					`amount` int(11) COLLATE utf8_general_ci NOT NULL,
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
					`ticker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`count` int(11) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`price` int(11) COLLATE utf8_general_ci NOT NULL,
					`api_price` int(11),
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
					`ticker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`count` int(11) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`price` int(11),
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
					`ticker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`count` int(11) COLLATE utf8_general_ci NOT NULL,
					`nkd` int(11) NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci,
					`price` int(11) NOT NULL,
					`api_price` int(11),
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
					`ticker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`count` int(11) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(255) COLLATE utf8_general_ci,
					`nkd` int(11) NOT NULL,
					`price` int(11) NOT NULL,
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
					`amount` int(11) COLLATE utf8_general_ci NOT NULL,
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
					`amount` int(11) COLLATE utf8_general_ci NOT NULL,
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
					`bond` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`amount` int(11) COLLATE utf8_general_ci NOT NULL,
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
					`dividend` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`amount` int(11) COLLATE utf8_general_ci NOT NULL,
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
	def add_new_amount(uid, date, amount, broker):
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
				sql = 'INSERT INTO `accountamount` (`uid`, `date`, `amount`, `broker`) VALUES (%s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, amount, broker))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_minus_amount(uid, date, amount, broker):
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
				sql = 'INSERT INTO `accountminusamount` (`uid`, `date`, `amount`, `broker`) VALUES (%s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, amount, broker))
			connection.commit()
		finally:
			connection.close()
	
	@staticmethod
	def add_buystock(uid, date, ticker, count, broker, price, api_price=0):
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
				sql = 'INSERT INTO `buystock` (`uid`, `date`, `ticker`, `count`, `broker`, `price`, `api_price`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, ticker, count, broker, price, api_price))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_salestock(uid, date, ticker, count, broker, price):
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
				sql = 'INSERT INTO `salestock` (`uid`, `date`, `ticker`, `count`, `broker`, `price`) VALUES (%s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, ticker, count, broker, price))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_buybond(uid, date, ticker, count, nkd, price, broker, api_price=0):
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
				sql = 'INSERT INTO `buybond` (`uid`, `date`, `ticker`, `count`, `nkd`, `price`, `broker`, `api_price`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, ticker, count, nkd, price, broker, api_price))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_salebond(uid, date, ticker, count, broker, nkd, price):
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
				sql = 'INSERT INTO `salebond` (`uid`, `date`, `ticker`, `count`, `broker`, `nkd`, `price`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, ticker, count, broker, nkd, price))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_new_tax(uid, date, amount, broker):
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
				sql = 'INSERT INTO `taxes` (`uid`, `date`, `amount`, `broker`) VALUES (%s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, amount, broker))
			connection.commit()
		finally:
			connection.close()
	
	@staticmethod
	def add_new_commission(uid, date, amount, broker):
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
				sql = 'INSERT INTO `comissions` (`uid`, `date`, `amount`, `broker`) VALUES (%s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, amount, broker))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_new_couponincome(uid, date, bond, amount, broker):
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
				sql = 'INSERT INTO `couponincome` (`uid`, `date`, `bond`, `amount`, `broker`) VALUES (%s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, bond, amount, broker))
			connection.commit()
		finally:
			connection.close()
	
	@staticmethod
	def add_new_dividend(uid, date, dividend, amount, broker):
		"""
		Получение дивидендов
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
				sql = 'INSERT INTO `dividends` (`uid`, `date`, `dividend`, `amount`, `broker`) VALUES (%s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, dividend, amount, broker))
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

			sql = 'SELECT * FROM accountamount WHERE uid=%s AND date < %s AND date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Пополнение счета'
				operations[-1]['table'] = 'accountamount'
			
			sql = 'SELECT * FROM accountminusamount WHERE uid=%s AND date < %s AND date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Вывод средств'
				operations[-1]['table'] = 'accountminusamount'
			
			sql = 'SELECT * FROM buystock WHERE uid=%s AND date < %s AND date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Покупка акций'
				operations[-1]['table'] = 'buystock'
			
			sql = 'SELECT * FROM salestock WHERE uid=%s AND date < %s AND date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Продажа акций'
				operations[-1]['table'] = 'salestock'
			
			sql = 'SELECT * FROM buybond WHERE uid=%s AND date < %s AND date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Покупка облигаций'
				operations[-1]['table'] = 'buybond'
			
			sql = 'SELECT * FROM salebond WHERE uid=%s AND date < %s AND date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Продажа облигаций'
				operations[-1]['table'] = 'salebond'
			
			sql = 'SELECT * FROM taxes WHERE uid=%s AND date < %s AND date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Оплата налога'
				operations[-1]['table'] = 'taxes'
			
			sql = 'SELECT * FROM comissions WHERE uid=%s AND date < %s AND date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Оплата комиссии'
				operations[-1]['table'] = 'comissions'
			
			sql = 'SELECT * FROM couponincome WHERE uid=%s AND date < %s AND date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Получение купонного дохода'
				operations[-1]['table'] = 'couponincome'
			
			sql = 'SELECT * FROM dividends WHERE uid=%s AND date < %s AND date > %s'
			cursor.execute(sql, (uid, start_timestamp, end_timestamp))
			res = cursor.fetchall()
			for x in res:
				operations.append(x)
				operations[-1]['title'] = 'Получение дивидендов'
				operations[-1]['table'] = 'dividends'

		connection.commit()
		return sorted(operations, key=itemgetter('date'), reverse=False)
	finally:
		connection.close()

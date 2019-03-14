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
				CREATE TABLE IF NOT EXISTS `account_amount` (
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
				CREATE TABLE IF NOT EXISTS `account_minus_amount` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`amount` int(11) COLLATE utf8_general_ci NOT NULL,
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `buy_stock` (
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
				CREATE TABLE IF NOT EXISTS `sale_stock` (
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
				CREATE TABLE IF NOT EXISTS `buy_bond` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`ticker` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`count` int(11) COLLATE utf8_general_ci NOT NULL,
					`nkd` int(11) NOT NULL,
					`price` int(11) NOT NULL,
					`api_price` int(11),
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
				AUTO_INCREMENT=1;
				'''
				cursor.execute(sql)
				sql = '''
				CREATE TABLE IF NOT EXISTS `sale_bond` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`name` varchar(255) COLLATE utf8_general_ci NOT NULL,
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
				CREATE TABLE IF NOT EXISTS `coupon_income` (
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
				sql = 'INSERT INTO `account_amount` (`uid`, `date`, `amount`, `broker`) VALUES (%s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, amount, broker))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_minus_amount(uid, date, amount):
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
				sql = 'INSERT INTO `account_minus_amount` (`uid`, `date`, `amount`) VALUES (%s, %s, %s)'
				cursor.execute(sql, (uid, date, amount))
			connection.commit()
		finally:
			connection.close()
	
	@staticmethod
	def add_buy_stock(uid, date, ticker, count, broker, price, api_price=0):
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
				sql = 'INSERT INTO `buy_stock` (`uid`, `date`, `ticker`, `count`, `broker`, `price`, `api_price`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, ticker, count, broker, price, api_price))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_sale_stock(uid, date, ticker, count, broker, price):
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
				sql = 'INSERT INTO `sale_stock` (`uid`, `date`, `ticker`, `count`, `broker`, `price`) VALUES (%s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, ticker, count, broker, price))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_buy_bond(uid, date, ticker, count, nkd, price, api_price=0):
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
				sql = 'INSERT INTO `buy_bond` (`uid`, `date`, `ticker`, `count`, `nkd`, `price`, `api_price`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, ticker, count, nkd, price, api_price))
			connection.commit()
		finally:
			connection.close()

	@staticmethod
	def add_sale_bond(uid, date, name, ticker, count, broker, nkd, price):
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
				sql = 'INSERT INTO `sale_bond` (`uid`, `date`, `name`, `ticker`, `count`, `broker`, `nkd`, `price`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, name, ticker, count, broker, nkd, price))
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
	def add_new_coupon_income(uid, date, bond, amount, broker):
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
				sql = 'INSERT INTO `coupon_income` (`uid`, `date`, `bond`, `amount`, `broker`) VALUES (%s, %s, %s, %s, %s)'
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

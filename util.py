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
					`broker` varchar(11) COLLATE utf8_general_ci,
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
				CREATE TABLE IF NOT EXISTS `taxes` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`uid` int(11) COLLATE utf8_general_ci NOT NULL,
					`date` varchar(255) COLLATE utf8_general_ci NOT NULL,
					`amount` int(11) COLLATE utf8_general_ci NOT NULL,
					`broker` varchar(11) COLLATE utf8_general_ci,
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
					`broker` varchar(11) COLLATE utf8_general_ci,
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
				sql = 'INSERT INTO `comissions` (`uid`, `date`, `amount`, `broker`) VALUES (%s, %s, %s, %s)'
				cursor.execute(sql, (uid, date, amount, broker))
			connection.commit()
		finally:
			connection.close()

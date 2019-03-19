BOT_TOKEN = '613026738:AAFk1_rW2Uab7Kg7h1zhKW6GVBxB-zBc_FA'
DEBUG = False

# MySql auth data
# CREATE DATABASE `account_performance` CHARACTER SET utf8 COLLATE utf8_general_ci;
db_host = 'localhost'
db_user='root'
db_password='123456'
db_database='account_performance'
db_charset = 'utf8'

main_markup = [
	['Добавить операцию'],
	['Портфель'],
]

operations_markup = [
	[{'text': 'Пополнение счета', 'callback': 'add_amount'}],
	[{'text': 'Вывод средств', 'callback': 'minus_amount'}],
	[{'text': 'Покупка акций', 'callback': 'add_aczii'}],
	[{'text': 'Продажа акций', 'callback': 'delete_aczii'}],
	[{'text': 'Покупка облигаций', 'callback': 'add_oblig'}],
	[{'text': 'Продажа облигаций', 'callback': 'delete_oblig'}],
	[{'text': 'Удержание налога', 'callback': 'pay_nalog'}],
	[{'text': 'Удержание комиссии', 'callback': 'pay_comission'}],
	[{'text': 'Зачисление купонного дохода', 'callback': 'get_cupon'}],
	[{'text': 'Зачисление дивидендов', 'callback': 'get_dividends'}],
]

'''
brokers = {
	'0': 'БКС',
	'1': 'Тинькофф',
	'2': 'Сбербанк',
}
'''

schet_markup = [
	[{'text': 'История операций с ценными бумагами', 'callback': 'history_papers'}],
	[{'text': 'История операций с деньгами', 'callback': 'history_money'}],
]

papers_history_markup = [
	[{'text': 'За предыдущий месяц', 'callback': 'history_papers_lastmonth'}],
	[{'text': 'За три месяца', 'callback': 'history_papers_threemonths'}],
	[{'text': 'Все', 'callback': 'history_papers_allmonths'}],
]

money_history_markup = [
	[{'text': 'За предыдущий месяц', 'callback': 'history_money_lastmonth'}],
	[{'text': 'За три месяца', 'callback': 'history_money_threemonths'}],
	[{'text': 'Все', 'callback': 'history_money_allmonths'}],
]

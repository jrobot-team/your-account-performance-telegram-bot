BOT_TOKEN = '857078060:AAG5zcSuFPh6-XSd1SVTQ45r-tLVqOGEUx0'
DEBUG = False
PROXY = {'https': 'socks5h://vielfrass:vielfrass@vielfrassx.tk:8000'}

# MySql auth data
# CREATE DATABASE `account_performance` CHARACTER SET utf8 COLLATE utf8_general_ci;
db_host = 'localhost'
db_user='root'
db_password='123456'
db_database='account_performance'
db_charset = 'utf8'

operations_markup = [
	[{'text': 'Пополнение счета', 'callback': 'add_amount'}, {'text': 'Вывод средств', 'callback': 'minus_amount'}],
	[{'text': 'Покупка акций', 'callback': 'add_aczii'}, {'text': 'Продажа акций', 'callback': 'delete_aczii'}],
	[{'text': 'Покупка облигаций', 'callback': 'add_oblig'}, {'text': 'Продажа облигаций', 'callback': 'delete_oblig'}],
	[{'text': 'Налог', 'callback': 'pay_nalog'}, {'text': 'Комиссия', 'callback': 'pay_comission'}],
	[{'text': 'Купонный доход', 'callback': 'get_cupon'}, {'text': 'Дивиденды', 'callback': 'get_dividends'}],
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

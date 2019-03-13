BOT_TOKEN = '613026738:AAFk1_rW2Uab7Kg7h1zhKW6GVBxB-zBc_FA'
DEBUG = True

# MySql auth data
# CREATE DATABASE `account_performance` CHARACTER SET utf8 COLLATE utf8_general_ci;
db_host = 'localhost'
db_user='root'
db_password='123456'
db_database='account_performance'
db_charset = 'utf8'

main_markup = [
	['Добавить операцию'],
	['Счет и портфель'],
]

operations_markup = [
	[{'text': 'Пополнить счет', 'callback': 'add_amount'}],
	[{'text': 'Вывести средства', 'callback': 'minus_amount'}],
	[{'text': 'Купить акции', 'callback': 'add_aczii'}],
	[{'text': 'Продать акции', 'callback': 'delete_aczii'}],
	[{'text': 'Купить облигации', 'callback': 'add_oblig'}],
	[{'text': 'Продать облигации', 'callback': 'delete_oblig'}],
	[{'text': 'Заплатить налог', 'callback': 'pay_nalog'}],
	[{'text': 'Заплатить комиссию', 'callback': 'pay_comission'}],
	[{'text': 'Получить купонный доход', 'callback': 'get_cupon'}],
	[{'text': 'Получить дивиденды', 'callback': 'get_dividends'}],
]

brokers = {
	'0': 'БКС',
	'1': 'Тинькофф',
	'2': 'Сбербанк',
}

schet_markup = [
	[{'text': 'Посмотреть историю операций', 'callback': 'history'}],
]

history_markup = [
	[{'text': 'За предыдущий месяц', 'callback': 'last_month'}],
	[{'text': 'За три месяца', 'callback': 'three_months'}],
	[{'text': 'Все', 'callback': 'all_months'}],
]

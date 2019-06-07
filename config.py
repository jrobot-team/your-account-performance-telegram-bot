BOT_TOKEN = '842528423:AAEazSuFCdmnC8maAA3bW8X_G1Jh_w1_WpM'
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

schet_markup = [
	[{'text': 'История операций', 'callback': 'history_papers'}],
]

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
'''

history_markup = [
	[{'text': 'За предыдущий месяц', 'callback': 'history_money_lastmonth'}],
	[{'text': 'За три месяца', 'callback': 'history_money_threemonths'}],
	[{'text': 'Все', 'callback': 'history_money_allmonths'}],
	[{'text': 'Экспорт', 'callback': 'export_history'}],
	[{'text': 'Импорт', 'callback': 'import_history'}],
]

spravka = '''
Чат-бот позволяет учитывать операции с ETF, акциями и облигациями, находящимися в обращении на ММВБ, а также уже погашенными выпусками облигаций.

Тикер ценной бумаги: например, LKOH или SU26210RMFS3.

Цена закрытия рассчитывается по итогам торгового дня, обновляется в нашей базе в 20.00 ежедневно и используется для расчета стоимости остатков ценных бумаг.

Выбывшие ценные бумаги учитываются по стоимости первых по времени приобретений (ФИФО метод).

При добавлении операций с облигациями необходимо разделять “чистую” цену и накопленный купонный доход (НКД), при этом облигации отражаются в портфеле по стоимости приобретения с учётом НКД,то есть по “грязной” цене.

Под прибылью или убытком по бумаге понимается потенциальная прибыль или убыток в случае реализации всего пакета по цене закрытия.

При импорте операций из пользовательского файла .xlsx происходит их добавление к базе чат-бота. Для успешного импорта операций необходимо строго следовать формату файла .xlsx, генерируемого при экспорте, и точно указывать названия операций. Возможны следующие типы операций: “Пополнение счета”, “Комиссия”, “Покупка акций”, “Вывод средств”, “Покупка облигаций”, “Продажа акций”, “Продажа облигаций”, “Купонный доход”, “Дивиденды”. Импортирование возможно прервать нажатием “Отмена”.
'''

contacts = '''
Мы рады видеть ваши замечания и предложения по адресу:
YourPortfolioPerformance@gmail.com
'''

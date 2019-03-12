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
    ['Пополнить счет'],
    ['Вывести средства'],
    ['Купить акции'],
    ['Продать акции'],
    ['Купить облигации'],
    ['Продать облигации'],
    ['Заплатить налог'],
    ['Заплатить комиссию'],
    ['Получить купонный доход'],    
    ['Получить дивиденды'],
]

schet_markup = [
    ['Посмотреть историю операций'],
]

history_markup = [
    ['За предыдущий месяц'],
    ['За три месяца'],
    ['Все'],
]

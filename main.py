'''
* Создать БД
    * Описать её структуру
        * Оформить создание БД в модуль (ИДЕЯ)
    + Заполнить БД тестовыми данными
* Реализовать вывод списка тем в древовидной ф-ме
* Реализовать выбор тем на 3х уровнях
* Реализовать вывод существующей темы
* Реализовать создание новой темы на любом уровне
* Реализовать ввод и сохранения темы
* Реализовать меню
* Реализовать проверку уникальности ключа
+ Реализовать логику очистки экрана
* Сформировать модель БД
* Вынести модель в файл моделей

% Решить вопрос о переходе к реально БД, 
и вывод проекта на новй уровень
% Попытка перейти на mysql (ОТМЕНА)
https://ilso.ru/sqlite-vs-mysql/

Как это должно в итоге выглядеть:
	Вывод списка из первого уровня
		1. Выйти
		2. Добавить тему
		3. Редактировать тему
		4. Развернуть тему
			Вывод второго уровня
				1. назад
				2. Добавить тему
				3. Редактировать тему
				4. Развернуть тему
					Вывод третьего уровня
						1. Назад
						2. Добавить тему
						3. Редактировать тему
						4. Развернуть тему
							Вывести значение
							1. Дополнить
							2. Редактирвать
							3. Выход
		
'''

import sqlite3
import unittest
import os
import flask
from flask import Flask
from peewee import *
from datetime import date


db = SqliteDatabase('work.db')
nameDB = 'db'
nameTabInDB = 'mydb'
dbdict = {}
conn = None
cursor = None
online = False




# class TestSS(unittest.TestCase):

#     def test_1(self):
#         self.assertEqual(ins('1', '5'), '1000000')



# # Определяем базовую модель о которой будут наследоваться остальные
# class BaseModel(Model):
#     class Meta:
#         database = conn  # соединение с базой, из шаблона выше

# # Определяем модель исполнителя
# class Artist(BaseModel):
#     artist_id = AutoField(column_name='ArtistId')
#     name = TextField(column_name='Name', null=True)

#     class Meta:
#         table_name = 'Artist'







class level1(Model):
    alias = CharField()
    key = CharField()
    description = CharField()
    is_active = BooleanField()

    class Meta:
        database = db  # модель будет использовать базу данных 'people.db'


class level2(Model):
    owner = ForeignKeyField(level1, related_name='pets')
    alias = CharField()
    key = CharField()
    description = CharField()
    is_active = BooleanField()

    class Meta:
        database = db  # модель будет использовать базу данных 'people.db'


class level3(Model):
    owner = ForeignKeyField(level2, related_name='pets')
    alias = CharField()
    key = CharField()
    description = CharField()
    is_active = BooleanField()

    class Meta:
        database = db  # модель будет использовать базу данных 'people.db'







'''
Открывается БД в глобальных переменных
Все считывается в глобальный словарь dbdict
'''
def init():
    global conn, cursor, dbdict

    level1.create_table()
    level2.create_table()
    level3.create_table()

    print("Добро пожаловать в программу!")

    conn = sqlite3.connect(nameDB) # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    sql = "SELECT * FROM mydb"
    cursor.execute(sql)
    dblist = cursor.fetchall()

    i = 0
    for item in dblist:
        dbdict[str(i)] = {
            'key': item[0],
            'value': item[1],
            'alias': item[2]
        }
        i += 1


# Ввод
def inp(numb, text):
    #  Пока пользователь не сделает того, чего мы хотим
    while(True):
        try:
            var = int(input(text))

            count = 1

            while count != numb+1:
                if var == count:
                    print("\n")
                    return var
                count += 1

            print("\tОШИБКА: Такого варианта нет\n")

        except ValueError:          
            print("\tОШИБКА: Вы ввели недопустимое значение... \n")
    pass


'''
Вставка в БД
todo:
    * параллельно вставить в словарь
    * обновить параметры
    * Не вставлять value, если уровень < 3
    * Понимать количество уровней
'''
def ins(k, v):
    global conn, cursor

    sql = "SELECT * FROM " + nameTabInDB + " WHERE key = " + k
    cursor.execute(sql)

    exists = cursor.fetchall()

    # print("sql = ", sql)
    # print("cursor.fetchall() = ", exists)

    if not exists:
        print("OK, it-s new")
        cursor.execute(""" INSERT INTO """ + nameTabInDB + """
                      VALUES """ + value + """ """)
        conn.commit()              	
    else:
         print("NO, it-s already in use.")


'''
Выводит список из словаря на экран
todo:
    * Вывод по уровням
    * Собственное меню
        * Развернуть уровень на подуровни
            * Разбить строку на 3 части по уровням
            * Выявлять если уровень меньше
        * Вернуться на уровень
        * Прочитать тему
        * редактировать тему


Уровни:
    1. Тема (1 уровень)
    1.1. Подтема (2 уровень)
    1.1.1. Часть > значение (3 уровень)
'''
def dbout():
    global dbdict

    cl1 = 0

    for lvl in level1.select():
    	print(lvl.key, ".", lvl.alias)
    	cl1 += 1


    txt = '''
    Действия:
    0. Вернуться
    х. Развернуть тему под номером х (введите число)
    Выбор: '''

    while True:
        try:
            var = str(input(txt))
            if var == str(0):
            	break

            # count = 0

            print("var = ", var, ", ct1 = ", cl1)
            print("level1.get(level1.key ==  var) - ", level1.get(level1.key ==  var))

            try:
                if level1.get(level1.key ==  var) and int(var) < int(cl1):
                    print("OK")
                else:
                    print("\tОШИБКА: Такого варианта нет\n")
            except ValueError:
            	print("\tОШИБКА: Такого варианта нет\n")



            # while count != cl1:
            #     print("cl1 = ", cl1, ", var = ", var, ", count = ", count)
            #     if str(var) == str(count):
            #         print("найден!")
            #         break
            #     count += 1

            # print("\tОШИБКА: Такого варианта нет\n")

        except ValueError:          
            print("\tОШИБКА: Вы ввели недопустимое значение... \n")
        

def dbcreate():
	pass
    

'''
Основное меню
'''
def main():
    global nameDB, nameTabInDB, conn, cursor

    os.system('clear')
    txt = """\nГлавное меню:
    1. Вывести список
    2. Внести изменения
    3. Выход
    Выбор: """

    while True:
        var = inp(3, txt)
        os.system('clear')

        if var == 1:
            dbout()
            continue

        elif var == 2:
            editor()
            continue

        elif var == 3:
            break


        pass
    
    os.system('clear')
    print("\n\n\tДо свидания!\n\n")

    

''' NO
Реализация редактирования текста 
todo:
    * Установить уровень
        * Проверить корректность
        * Проверить принадлежность
    * Установить алиас
    * Установить значение
'''
def editor():

    alias = input("Введите название темы: ")
    key1 = input("Введите ")
    pass




if __name__ == '__main__':
    init()
    main()
    conn.close()


'''
sql = """
            CREATE TABLE db
            (key text, value text)
      """

dict = {
    'ключь' = [значение]
}


    # # Создание таблицы
    # cursor.execute("""CREATE TABLE mydb
    #               (key text, value text)
    #            """)

    # value = "('1', '2')"
    # # Вставляем данные в таблицу
    # cursor.execute(""" INSERT INTO """ + nameTabInDB + """
    #               VALUES """ + value + """ """)
    # # Сохраняем изменения
    # conn.commit()

    # # Удаление по ключу
    # sql = "DELETE FROM " + nameTabInDB + " WHERE key = 'key'"
    # cursor.execute(sql)
    # conn.commit()


    # ins('2S', '5')

    # sql = "SELECT * FROM mydb"
    # cursor.execute(sql)
    # print(cursor.fetchall()) # or use fetchone()


Структура БД:

Код			Алиас					Значения
1.1.3		Название темы			Сама тема

'''
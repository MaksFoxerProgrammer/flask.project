# Импортируем библиотеку, соответствующую типу нашей базы данных 
# В данном случае импортируем все ее содержимое, чтобы при обращении не писать каждый раз имя библиотеки, как мы делали в первой статье
from peewee import *
from model import *


Artist.create_table()

artists_data = [{'name': 'Первый2'}, {'name': 'Второй2'}]
Artist.insert_many(artists_data).execute()


def add_category(name):
    row = Artist(
        name=name.lower().strip(),
    )
    row.save()
 
add_category('Books2')


artists = Artist.get(artist_id = 1)
print(artists.name)
# input()
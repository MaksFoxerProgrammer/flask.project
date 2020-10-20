from peewee import *

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
conn = SqliteDatabase('TEST')
print("Подключение: OK")

# Определяем базовую модель о которой будут наследоваться остальные
class BaseModel(Model):    
    class Meta:
        database = conn  # соединение с базой, из шаблона выше

# Определяем модель исполнителя
class Artist(BaseModel):
    artist_id = AutoField(column_name='ArtistId')
    name = TextField(column_name='Name', null=True)

    class Meta:
        table_name = 'Artist'
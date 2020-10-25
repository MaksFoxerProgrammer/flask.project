from peewee import *

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
conn = SqliteDatabase('work.db')
# print("Подключение: OK")

# Определяем базовую модель о которой будут наследоваться остальные
class BaseModel(Model):    
    class Meta:
        database = conn  # соединение с базой, из шаблона выше



# Определяем модель исполнителя
class Level1(BaseModel):
    alias = TextField(column_name='alias')
    key = TextField(column_name='key', null=True)
    description = TextField(column_name='description')
    is_active = BooleanField(column_name='is_active', null=True)

    class Meta:
        table_name = 'Level1'


class Level2(BaseModel):
    alias = TextField(column_name='alias')
    key = TextField(column_name='Name', null=True)
    description = TextField(column_name='description')
    is_active = BooleanField(column_name='is_active', null=True)
    owner_id = ForeignKeyField(Level1, related_name='Level2', on_delete='cascade', on_update='cascade')

    class Meta:
        table_name = 'Level2'


class Level3(BaseModel):
    alias = TextField(column_name='alias')
    key = TextField(column_name='Name', null=True)
    description = TextField(column_name='description')
    is_active = BooleanField(column_name='is_active', null=True)
    owner_id = ForeignKeyField(Level2, related_name='Level3', on_delete='cascade', on_update='cascade')

    class Meta:
        table_name = 'Level3'


Level1.create_table()
Level2.create_table()
Level3.create_table()

print(" * ConnectToDb........OK")
import sqlite3
from models import *
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort # Для вывода 404 ошибки (?)

'''
Глобальный объект request для доступа к входящим данным запроса, которые будут подаваться через форму HTML.
Функция url_for() для генерирования URL-адресов.
Функция flash() для появления сообщения при обработке запроса.
Функция redirect() для перенаправления клиента в другое расположение.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wef.kh4on93842t98n43289y3n4t08923y490t82y3495n832y4985y'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    post = Level1.get(id=post_id)
    if post is None:
        abort(404)
    return post


def c2in1(ownid):
    # Достать все записи второго уровня в данной категории
    # В цикле найти их число
    lvl2 = Level2.select(owner_id=ownid)

    pass


# @app.route('/')
# def index():
#     posts = Level1.select()
#     return render_template('index.html', posts=posts)


@app.route('/')
def index():
    level1 = Level1.select()
    level2 = Level2.select()
    level3 = Level3.select()
    return render_template('index.html',level1=level1,level2=level2,level3=level3,Level1=Level1, Level2=Level2, Level3=Level3)


@app.route('/menu')
def menu():
    level1 = Level1.select()
    level2 = Level2.select()
    level3 = Level3.select()
    return render_template('menu.html',level1=level1,level2=level2,level3=level3,Level1=Level1, Level2=Level2, Level3=Level3)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        alias = request.form['alias']
        description = request.form['description']

        if not alias:
            flash('Title is required!')
        else:
            id = Level1.create(alias=alias, description=description)

            data = Level1(id=id)
            k = id
            print(k)
            data.key = k
            data.save()

            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/create2', methods=('GET', 'POST'))
def create2(id):
    if request.method == 'POST':
        alias = request.form['alias']
        description = request.form['description']

        if not alias:
            flash('Title is required!')
        else:

            key = str(id) + "." + str(c2in1(id))

            id = Level2.create(alias=alias, description=description, owner_id=id, key=key)
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/create3', methods=('GET', 'POST'))
def create3(id):
    if request.method == 'POST':
        alias = request.form['alias']
        description = request.form['description']
        if not alias:
            flash('Title is required!')
        else:
            Level3.create(alias=alias, description=description,owner_id=id)
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        alias = request.form['alias']
        description = request.form['description']

        if not alias:
            flash('alias is required!')
        else:
            # conn = get_db_connection()
            # conn.execute('UPDATE posts SET title = ?, content = ?'
                        #  ' WHERE id = ?',
                        #  (title, content, id))
            # conn.commit()
            # conn.close()
            data = Level1(id=id)
            data.alias = alias
            data.description = description
            data.save()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    # conn = get_db_connection()
    # conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    # conn.commit()
    # conn.close()
    # deli = Level1.get(id=id)

    flash('"{}" was successfully deleted!'.format(post.alias))
    post.delete_instance()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

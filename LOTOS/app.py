from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# КЛЮЧ ДЛЯ СЕССИИ
app.secret_key = 'lotos_secret_key_2026'

# ДАННЫЕ АДМИНИСТРАТОРА
ADMIN_LOGIN = 'admin'
ADMIN_PASSWORD = 'lotos123'


# ПОДКЛЮЧЕНИЕ БАЗЫ ДАННЫХ
def get_database():
    connection = sqlite3.connect('database.db')
    return connection


# СОЗДАНИЕ БАЗЫ ДАННЫХ
def create_database():
    connection = get_database()

    connection.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            service TEXT,
            master TEXT,
            date TEXT,
            time TEXT,
            comment TEXT
        )
    ''')

    connection.commit()
    connection.close()


# ГЛАВНАЯ
@app.route('/')
def home():
    return render_template('index.html')


# УСЛУГИ
@app.route('/services')
def services():
    return render_template('services.html')


# МАСТЕРА
@app.route('/team')
def team():
    return render_template('team.html')


# ГАЛЕРЕЯ
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


# О САЛОНЕ
@app.route('/about')
def about():
    return render_template('about.html')


# КОНТАКТЫ
@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


# ОНЛАЙН-ЗАПИСЬ
@app.route('/booking', methods=['GET', 'POST'])
def booking():

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        service = request.form['service']
        master = request.form['master']
        date = request.form['date']
        time = request.form['time']
        comment = request.form['comment']

        connection = get_database()

        connection.execute('''
            INSERT INTO bookings
            (name, phone, service, master, date, time, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, service, master, date, time, comment))

        connection.commit()
        connection.close()

        return render_template('booking.html', success=True)

    return render_template('booking.html', success=False)


# ВХОД АДМИНИСТРАТОРА
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_LOGIN and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')

        return render_template('login.html', error='Неверный логин или пароль')

    return render_template('login.html')


# АДМИНИСТРАТИВНАЯ ПАНЕЛЬ
@app.route('/admin')
def admin():

    if not session.get('admin'):
        return redirect('/login')

    connection = get_database()

    bookings = connection.execute('''
        SELECT * FROM bookings ORDER BY id DESC
    ''').fetchall()

    connection.close()

    return render_template('admin.html', bookings=bookings)


# УДАЛЕНИЕ ЗАЯВКИ
@app.route('/delete_booking/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):

    if not session.get('admin'):
        return redirect('/login')

    connection = get_database()

    connection.execute(
        'DELETE FROM bookings WHERE id = ?',
        (booking_id,)
    )

    connection.commit()
    connection.close()

    return redirect('/admin')


# ВЫХОД
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')


if __name__ == '__main__':
    create_database()
    app.run(debug=True)

from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash,generate_password_hash

app = Flask (__name__)

#koneksi Database
app.secret_key = "projectakhir"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'toko'
mysql = MySQL(app)

# Halaman Admin
@app.route('/')
def index():
    if 'loggedin' in session:
        return render_template('index.html')
    flash('Hallo Selamat Datang Admin Silahkan Lengkapi Data Anda')
    return redirect(url_for('loginadmin'))




# daftar Admin
@app.route('/registrasi/', methods=('GET','POST'))
def registrasi():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        telepon = request.form['telepon']
        # cek username / email
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin WHERE username=%s OR email=%s',(username,email,))
        akun = cursor.fetchone()
        if akun is None:
            cursor.execute('INSERT INTO admin VALUES (NULL,%s,%s,%s,%s)',(username,telepon,email,generate_password_hash(password)))
            mysql.connection.commit()
            flash('Daftar Telah Berhasil,Silahkan untuk Login')
        else :
            flash('Username atau email sudah ada')

    return render_template('registrasi.html')

# loginadmin
@app.route('/loginadmin', methods=('GET','POST'))
def loginadmin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # cek username 
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin WHERE email=%s',(email,))
        akun = cursor.fetchone()
        if akun is None :
            flash('Login gagal, Silahkan cek username anda!!!')
        elif not check_password_hash(akun[4],password):
            flash('Login gagal, silahkan cek password anda!!!')
        else :
            session['loggedin'] = True
            session['username'] = akun[1]
            session['telepon'] = akun[2]
            return redirect (url_for('index'))
    return render_template('loginadmin.html')

# logoutAdmin
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username', None)
    session.pop('telepon', None)
    return redirect(url_for('loginadmin'))


if __name__ == '__main__':
    app.run(debug=True)
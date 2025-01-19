from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime
from DB_Operations import get_db_connection




app = Flask(__name__)
app.secret_key = 'your_secret_key' 

USERNAME = "husain"
PASSWORD = "123"
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Username atau password salah!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Berhasil logout.', 'success')
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET'])
def admin():
    if not session.get('logged_in'):
        flash('Harap login terlebih dahulu!', 'warning')
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM berita ORDER BY tanggal DESC')
        berita_list = cursor.fetchall()
        cursor.execute('SELECT * FROM penyakit ORDER BY id DESC')
        penyakit_list = cursor.fetchall()
        cursor.execute('SELECT * FROM chat_publik ORDER BY tanggal DESC')
        chat_list = cursor.fetchall()
        cursor.execute('SELECT * FROM langganan ORDER BY tanggal DESC;')
        pelanggan_list = cursor.fetchall()
        app.logger.info("Berita: %s", berita_list)
        app.logger.info("Penyakit: %s", penyakit_list)
        app.logger.info("Chat: %s", chat_list)
        app.logger.info("Pelanggan: %s", pelanggan_list)

    except Exception as e:
        app.logger.error("Error saat mengambil data admin: %s", e)
        flash(f'Terjadi kesalahan: {e}', 'danger')
        berita_list = []
        penyakit_list = []
        chat_list = []
        pelanggan_list = []
    finally:
        cursor.close()
        conn.close()
    return render_template(
        'admin.html',
        berita_list=berita_list,
        penyakit_list=penyakit_list,
        chat_list=chat_list,
        pelanggan_list=pelanggan_list
    )

@app.route('/')
def beranda():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM berita ORDER BY tanggal DESC LIMIT 4') 
    berita_terbaru = cursor.fetchall()
    cursor.close()
    conn.close()
    print(berita_terbaru)
    return render_template('beranda.html', berita_terbaru=berita_terbaru)

@app.route('/informasi_penyakit')
def informasi_penyakit():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM penyakit')
    penyakit_list = cursor.fetchall()
    cursor.close()
    conn.close()
    print(penyakit_list)
    return render_template('informasi_penyakit.html', diseases=penyakit_list)

@app.route('/tambah_penyakit', methods=['GET', 'POST'])
def tambah_penyakit():
    if request.method == 'POST':
        nama_penyakit = request.form['nama_penyakit']
        gejala_awal = request.form['gejala_awal']
        cara_penanganan = request.form['penanganan']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO penyakit (nama_penyakit, gejala_awal, cara_penanganan) VALUES (%s, %s, %s)', (nama_penyakit, gejala_awal, cara_penanganan))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin'))
    return render_template('tambah_penyakit.html')

@app.route('/edit_penyakit/<int:penyakit_id>', methods=['GET', 'POST'])
def edit_penyakit(penyakit_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        nama_penyakit = request.form['nama_penyakit']
        gejala_awal = request.form['gejala_awal']
        cara_penanganan = request.form['penanganan']
        cursor.execute("""
            UPDATE penyakit SET nama_penyakit = %s, gejala_awal = %s, cara_penanganan = %s
            WHERE id = %s
        """, (nama_penyakit, gejala_awal, cara_penanganan, penyakit_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin'))
    cursor.execute('SELECT * FROM penyakit WHERE id = %s', (penyakit_id,))
    penyakit = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_penyakit.html', penyakit=penyakit)

@app.route('/hapus_penyakit/<int:penyakit_id>', methods=['GET'])
def hapus_penyakit(penyakit_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM penyakit WHERE id = %s", (penyakit_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('admin'))  

@app.route('/berita/<int:berita_id>')
def berita_detail(berita_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM berita WHERE id = %s', (berita_id,)) 
    berita = cursor.fetchone()
    cursor.close()
    conn.close()
    if berita:
        return render_template('berita_detail.html', berita=berita)
    else:
        return "Berita tidak ditemukan", 404

@app.route('/berita-terkini')
def berita_terkini():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM berita ORDER BY tanggal DESC')  
    berita_terkini = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('berita_terkini.html', berita_terbaru=berita_terkini)

@app.route('/tambah_berita', methods=['GET', 'POST'])
def tambah_berita():
    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        penjelasan = request.form['penjelasan']
        dampak = request.form['dampak']
        solusi = request.form['solusi']
        langkah_pemerintah = request.form['langkah_pemerintah']
        penutup = request.form['penutup']
        tanggal = datetime.strptime(request.form['tanggal'], "%Y-%m-%dT%H:%M")
        db = get_db_connection()  
        cursor = db.cursor()
        query = """
        INSERT INTO berita (judul, isi, penjelasan, dampak, solusi, langkah_pemerintah, penutup, tanggal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (judul, isi, penjelasan, dampak, solusi, langkah_pemerintah, penutup, tanggal)
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('admin'))  
    return render_template('tambah_berita.html')

@app.route('/edit_berita/<int:berita_id>', methods=['GET', 'POST'])
def edit_berita(berita_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:

        app.logger.info(f"Mengambil data untuk ID: {berita_id}")

        cursor.execute('SELECT * FROM berita WHERE id = %s', (berita_id,))
        berita = cursor.fetchone()

        app.logger.info(f"Data berita: {berita}")
        
        if not berita:
            flash('Berita tidak ditemukan.', 'danger')
            return redirect(url_for('admin'))
    
        if request.method == 'POST':
            judul = request.form.get('judul')
            isi = request.form.get('isi')
            penjelasan = request.form.get('penjelasan')
            dampak = request.form.get('dampak')
            solusi = request.form.get('solusi')
            langkah_pemerintah = request.form.get('langkah_pemerintah')
            penutup = request.form.get('penutup')
            tanggal = request.form.get('tanggal')

            cursor.execute(
                '''
                UPDATE berita
                SET judul = %s, isi = %s, penjelasan = %s, dampak = %s, solusi = %s, langkah_pemerintah = %s, penutup = %s, tanggal = %s
                WHERE id = %s
                ''',
                (judul, isi, penjelasan, dampak, solusi, langkah_pemerintah, penutup, tanggal, berita_id)
            )
            conn.commit()
            flash('Berita berhasil diperbarui.', 'success')
            return redirect(url_for('admin'))
    except Exception as e:
        app.logger.error(f"Error: {e}")
        flash(f'Terjadi kesalahan: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return render_template('edit_berita.html', berita=berita)



@app.route('/hapus_berita/<int:berita_id>', methods=['GET'])
def hapus_berita(berita_id):
    conn = get_db_connection()  
    cursor = conn.cursor()
    cursor.execute("DELETE FROM berita WHERE id = %s", (berita_id,))
    conn.commit()
    cursor.close()
    conn.close()  
    return redirect(url_for('admin'))  

@app.route('/chat_publik', methods=['GET', 'POST'])
def chat_publik():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        pesan = request.form.get('pesan').strip()
        if not email or not pesan:
            error_message = "Email dan pesan tidak boleh kosong."
            return render_template('chat_publik.html', error=error_message)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO chat_publik (email, pesan, tanggal) VALUES (%s, %s, %s)',
                (email, pesan, datetime.now())
            )
            conn.commit()
        except mysql.connector.Error as e:
            return render_template('chat_publik.html', error=f"Terjadi kesalahan: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return redirect(url_for('chat_publik'))
    order = request.args.get('order', 'newest')  
    order_by = 'DESC' if order == 'newest' else 'ASC'
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM chat_publik ORDER BY tanggal {order_by}')
        chats = cursor.fetchall()
    except mysql.connector.Error as e:
        return render_template('chat_publik.html', error=f"Terjadi kesalahan: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return render_template('chat_publik.html', chats=chats, order=order)

@app.route('/tambah_chat', methods=['POST'])
def tambah_chat():
    if not session.get('logged_in'):
        flash('Harap login terlebih dahulu!', 'warning')
        return redirect(url_for('login'))
    email = request.form.get('email', 'Admin@gmail.com') 
    pesan = request.form.get('chat_message')
    if pesan:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO chat_publik (email, pesan, tanggal) VALUES (%s, %s, NOW())',
            (email, pesan)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Pesan berhasil dikirim!', 'success')
    else:
        flash('Pesan tidak boleh kosong.', 'danger')
    return redirect(url_for('admin'))

@app.route('/hapus_chat/<int:chat_id>', methods=['GET'])
def hapus_chat(chat_id):
    if not session.get('logged_in'):
        flash('Harap login terlebih dahulu!', 'warning')
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chat_publik WHERE id = %s', (chat_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Pesan berhasil dihapus.', 'success')
    return redirect(url_for('admin'))

@app.route('/berlangganan', methods=['GET', 'POST'])
def berlangganan():
    if request.method == 'POST':
        try:
            nama = request.form['nama']
            email = request.form['email']
            if not nama or not email:
                return render_template('berlangganan.html', error="Nama dan email harus diisi.")
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM langganan WHERE email = %s', (email,))
            existing_subscription = cursor.fetchone()
            if existing_subscription:
                cursor.close()
                conn.close()
                return render_template('berlangganan.html', error="Email sudah terdaftar.")
            cursor.execute('INSERT INTO langganan (nama, email) VALUES (%s, %s)', (nama, email))
            conn.commit()  
            cursor.close()
            conn.close()
            return render_template('berlangganan.html', success=True, nama=nama, email=email)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('berlangganan.html', error="Terjadi kesalahan.")
    return render_template('berlangganan.html')

@app.route('/akhiri_langganan/<int:pelanggan_id>', methods=['GET'])
def akhiri_langganan(pelanggan_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM langganan WHERE id = %s', (pelanggan_id,))
        pelanggan = cursor.fetchone()
        if not pelanggan:
            cursor.close()
            conn.close()
            flash('Pelanggan tidak ditemukan.', 'danger')
            return redirect(url_for('admin'))
        cursor.execute('DELETE FROM langganan WHERE id = %s', (pelanggan_id,))
        conn.commit()
        flash('Langganan pelanggan berhasil diakhiri.', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Terjadi kesalahan saat menghapus pelanggan: {e}', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('admin'))

@app.route('/tentang_kami')
def tentang_kami():
    return render_template('tentang_kami.html')

@app.route('/portofolio')
def portofolio():
    return render_template('portofolio.html')

if __name__ == '__main__':
    app.run(debug=True)
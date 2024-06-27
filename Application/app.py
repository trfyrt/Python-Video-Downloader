from flask import Flask, render_template, request, redirect, url_for, flash
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Mendapatkan path absolut untuk direktori downloads
downloads_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/downloads')

@app.route('/index')
def index():
    # Memeriksa apakah direktori downloads ada dan mendapatkan daftar file
    files = os.listdir(downloads_dir) if os.path.exists(downloads_dir) else []
    return render_template('index.html', files=files)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        # Membuat direktori downloads jika belum ada
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        
        # Mengunduh video menggunakan yt_dlp
        with yt_dlp.YoutubeDL({}) as ydl:
            # Mendapatkan informasi video tanpa mengunduh (download=False)
            info_dict = ydl.extract_info(url, download=False)
            # Menyimpan judul video
            video_title = info_dict.get('title', 'video')
            
            # Opsi untuk pengunduhan
            ydl_opts = {
                'outtmpl': os.path.join(downloads_dir, '%(title)s.%(ext)s'),  
                # Menggunakan judul sebagai nama file, %(title)s akan diganti dengan judul video
                'no_overwrites': False,  # Memungkinkan penggantian file yang sudah ada
                'ignoreerrors': True,    # Mengabaikan error jika terjadi masalah saat mengunduh
            }
            
            # Melakukan pengunduhan video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            flash('Download Berhasil!')
        
    except Exception as e:
        print(f'Error: {e}')  # Mencetak error ke konsol untuk debugging
        flash(f'Error: {str(e)}')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

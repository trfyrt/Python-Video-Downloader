from flask import Flask, render_template, request, redirect, url_for, flash
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

#mendapatkan path absolut untuk direktori downloads
downloads_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/downloads')

@app.route('/index')
def index():
    #memeriksa apakah direktori downloads ada dan mendapatkan daftar file
    files = os.listdir(downloads_dir) if os.path.exists(downloads_dir) else []
    return render_template('index.html', files=files)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    ydl_opts = {
        'outtmpl': os.path.join(downloads_dir, '%(uploader)s.%(ext)s'),  #Menggunakan username Twitter sebagai nama file
    }
    try:
        #membuat direktori downloads jika belum ada
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        
        #menggunakan yt-dlp untuk mengunduh video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #mendapatkan informasi video tanpa mengunduh (download=False)
            info_dict = ydl.extract_info(url, download=False)
            #menyiapkan nama file berdasarkan informasi video
            video_title = ydl.prepare_filename(info_dict)
            print(f'Downloading to: {video_title}')  # Output untuk debugging
            #mengunduh video
            ydl.download([url])
        flash('Download Successful!')
    except Exception as e:
        print(f'Error: {e}')  #mencetak kesalahan ke konsol untuk debugging
        flash(f'Error: {str(e)}')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

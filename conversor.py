from flask import Flask, request, send_file, render_template
import os
import yt_dlp

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_video_to_audio():
    video_url = request.form['url']
    if not video_url.startswith('https://www.youtube.com' and 'https://youtu.be'):
        return 'URL inválida. Por favor, insira um link do YouTube.'

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        title = info_dict.get('title', None)

    audio_file = f'downloads/{title}.mp3'
    if os.path.exists(audio_file):
        return send_file(audio_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
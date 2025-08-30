from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    quality = request.form["quality"]

    file_id = str(uuid.uuid4())
    output_path = f"{file_id}.%(ext)s"

    # خيارات التحميل حسب الجودة
    if quality == "high":
        ydl_opts = {"outtmpl": output_path, "format": "bestvideo+bestaudio/best"}
    elif quality == "medium":
        ydl_opts = {"outtmpl": output_path, "format": "best[height<=480]"}
    elif quality == "audio":
        ydl_opts = {
            "outtmpl": output_path,
            "format": "bestaudio/best",
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
            ],
        }
    else:
        ydl_opts = {"outtmpl": output_path, "format": "best"}

    # التحميل
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    # إرسال الملف للمستخدم
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
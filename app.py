import os
from flask import Flask, render_template, request, send_file
from pytube import YouTube

app = Flask(__name__)

# Create downloads folder if not exists
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()  # Get highest quality video
            video_path = os.path.join(DOWNLOAD_FOLDER, yt.title + ".mp4")
            video.download(DOWNLOAD_FOLDER)
            return send_file(video_path, as_attachment=True)  # Serve the file for download
        except Exception as e:
            return f"Error: {e}"
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

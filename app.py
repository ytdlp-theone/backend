from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

DOWNLOAD_PATH = "downloads"

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)


def get_available_formats(url):
    """Retrieve all available formats for a given URL."""
    try:
        with yt_dlp.YoutubeDL({'noplaylist': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            available_formats = []

            for fmt in formats:
                format_info = {
                    'format_id': fmt.get('format_id'),
                    'ext': fmt.get('ext'),
                    'resolution': f"{fmt.get('width', 'N/A')}x{fmt.get('height', 'N/A')}" if fmt.get('height') else "Audio only",
                    'size': f"{round(fmt.get('filesize', 0) / (1024 * 1024), 2)} MB" if fmt.get('filesize') else "Unknown"
                }
                available_formats.append(format_info)

            return available_formats

    except Exception as e:
        return str(e)


def download_media(url, format_id):
    """Download a media file with the specified format ID."""
    try:
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_PATH}/%(title)s.%(ext)s',  # Save file with proper name
            'format': format_id,  # Download the selected format
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            return file_path

    except Exception as e:
        return str(e)


@app.route('/formats', methods=['POST'])
def get_formats():
    """API endpoint to retrieve available formats for a given video."""
    try:
        data = request.json
        url = data.get('url')

        if not url:
            return jsonify({"error": "Missing 'url' in request."}), 400

        available_formats = get_available_formats(url)

        if isinstance(available_formats, str):  # Error occurred
            return jsonify({"error": available_formats}), 500

        return jsonify({"formats": available_formats})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download', methods=['POST'])
def download():
    """API endpoint to download a video/audio in a specific format."""
    try:
        data = request.json
        url = data.get('url')
        format_id = data.get('format_id')

        if not url or not format_id:
            return jsonify({"error": "Missing 'url' or 'format_id' in request."}), 400

        file_path = download_media(url, format_id)

        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "Download failed or file not found."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Get the port from the environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  # Listen on all available network interfaces and the specified port

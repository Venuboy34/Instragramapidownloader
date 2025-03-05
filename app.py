from flask import Flask, jsonify, request, Response
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    
    # Check if the URL is missing
    if not url:
        return jsonify({"error": "URL is missing"}), 400

    # Options for yt-dlp
    ydl_opts = {
        'format': 'best',  # Best quality format
        'quiet': True,
        'noplaylist': True,  # Avoid playlist downloads
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info for the video without downloading
            info_dict = ydl.extract_info(url, download=False)
            
            # Extract the download URL
            download_url = info_dict.get('url')
            if not download_url:
                return jsonify({"error": "Could not fetch download URL"}), 404

            # Return the download URL as a JSON response
            return jsonify({"success": True, "downloadUrl": download_url})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

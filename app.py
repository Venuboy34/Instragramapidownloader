from flask import Flask, jsonify, request
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    
    # Debugging: Log the URL being received
    print(f"Received URL: {url}")

    # Check if the URL is None or empty
    if not url:
        return jsonify({"error": "URL is missing"}), 400

    # Options for yt-dlp
    ydl_opts = {
        'format': 'best',  # Best quality format
        'outtmpl': './downloads/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Extracting info for URL: {url}")  # Log the URL being processed
            info_dict = ydl.extract_info(url, download=False)
            
            # Debugging: Log the info_dict to see if it's extracting info correctly
            print(f"Info dict: {info_dict}")
            
            download_url = info_dict.get('url')
            if not download_url:
                return jsonify({"error": "Could not fetch download URL"}), 404

            # Debugging: Log the final download URL
            print(f"Download URL: {download_url}")

        return jsonify({"success": True, "downloadUrl": download_url})
    
    except Exception as e:
        # Debugging: Log the exception if there's any error
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

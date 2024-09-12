from weapondetector.utils import upload_media
import threading
import json
from flask import Flask, request, jsonify
from waitress import serve

app = Flask(__name__)


@app.route('/uploadvideo', methods=['POST'])
def uploadvideo():
    try:
        data = json.loads(request.json)
        print(data)

        thread = threading.Thread(target=upload_media, args=(data['video_file_path'],
                                                             data['img_file_path'],
                                                             data['camera_name'],
                                                             data['acc']))
        thread.daemon = True
        thread.start()
        return data, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":

    serve(app, host="0.0.0.0", port=8000)

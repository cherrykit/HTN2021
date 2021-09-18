from flask import Flask, request, json, jsonify
from flask_cors import CORS
import moviepy.editor as mpy
import string
import random
import base64
import time

app = Flask(__name__)

# inputs: list of (input, length) pairs (TODO: support videos?)
# audio: link to audio file
PHONE_RESOLUTION = (360, 640)
def combine(inputs, audio, output):
    image_videos = [
        mpy.ImageClip(pair[0]).
        set_position(('center', 0)).
        resize(width=PHONE_RESOLUTION[0], height=PHONE_RESOLUTION[1]).
        set_duration(pair[1])
        for pair in inputs
    ]
    # idk why, but unless I create a CompositeVideoClip and set the size variable the output video doesn't work
    # temp solution: wrap the output in a CompositeVideoClip
    video_clip = mpy.CompositeVideoClip(
        [mpy.concatenate_videoclips(image_videos, method="compose").
        set_position(('center', 0))],
        size=PHONE_RESOLUTION
    )
    audio_clip = mpy.AudioFileClip(audio)
    video_clip.audio = audio_clip
    video_clip.write_videofile(output, fps=24)

# combine([("photo1.jpg", 10), ("photo2.jpeg", 17)], "audio1.mp3", "test.mp4")

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

DUMMY_RESULT = [5, 2, 2, 2, 2]
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    data = request.get_json()
    audio_data = data['audio_data']
    file_type = data['file_type']
    audio_name = str(time.gmtime()) + ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
        )
    with open("./audio/" + audio_name + "." + file_type, "wb") as f:
        f.write(base64.b64decode(audio_data))
    # Claire's stuff here
    result = DUMMY_RESULT
    return jsonify({'num_inputs': len(result), 'input_lengths': result, 'audio_name': audio_name})


@app.route('/upload_images', methods=['POST'])
def upload_music():
    data = request.get_json()
    input_lengths = data['input_lengths']
    inputs = data['inputs']
    audio_name = data['audio_name']
    file_type = data['file_type']
    combine(
        list(zip(inputs, input_lengths)), 
        "./audio/" + audio_name + "." + file_type, 
        "./video/" + audio_name + ".mp4"
        )
    video_encoding = ""
    with open("./video/" + audio_name + ".mp4", "rb") as f:
        video_encoding = base64.b64encode(f.read())
    return jsonify({'video_encoding': video_encoding, 'file_type': 'mp4'})
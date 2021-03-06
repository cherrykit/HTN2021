#!/usr/bin/python3
from flask import Flask, request, json, jsonify
from flask_cors import CORS
from mimetypes import guess_extension
import moviepy.editor as mpy
import string
import random
import base64
import time
import climax_process as cp
import moviepy.audio.fx.all as afx
import moviepy.video.fx.all as vfx

app = Flask(__name__)

# inputs: list of (input, length) pairs (TODO: support videos?)
# audio: link to audio file
PHONE_RESOLUTION = (360, 640)
def combine(inputs, audio, output, effects, message=""):
    print(inputs)
    image_videos = [
        mpy.ImageClip(pair[0]).
        set_position(('center', 0)).
        resize(width=PHONE_RESOLUTION[0], height=PHONE_RESOLUTION[1]).
        set_duration(pair[1])
        for pair in inputs
    ]
    # print(message)
    # if len(message) > 0:
    #     text_clip = mpy.TextClip(message, fontsize=50, color='black')
    #     text_clip = text_clip.set_pos('center').set_duration(5)
    #     image_videos[0] = mpy.CompositeVideoClip([image_videos[0], text_clip])
    # idk why, but unless I create a CompositeVideoClip and set the size variable the output video doesn't work
    # temp solution: wrap the output in a CompositeVideoClip
    video_clip = mpy.CompositeVideoClip(
        [mpy.concatenate_videoclips(image_videos, method="compose").
        set_position(('center', 0))],
        size=PHONE_RESOLUTION
    )
    audio_clip = mpy.AudioFileClip(audio).fx(afx.audio_fadein, 1.0).fx(afx.audio_fadeout, 5.0)
    video_clip.audio = audio_clip
    for e in effects:
        if e == 'bw':
            video_clip = video_clip.fx(vfx.blackwhite)
        elif e == 'bright':
            video_clip = video_clip.fx(vfx.colorx, 2)
        elif e == 'dark':
            video_clip = video_clip.fx(vfx.colorx, 0.5)
        elif e == 'invert':
            video_clip = video_clip.fx(vfx.invert_colors)
        elif e == 'horizontal':
            video_clip = video_clip.fx(vfx.mirror_x)
        elif e == 'vertical':
            video_clip = video_clip.fx(vfx.mirror_y)
        elif e == 'painting':
            video_clip = video_clip.fx(vfx.painting)
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
    audio_name = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
        )
    with open("./audio/" + audio_name + "." + file_type, "wb") as f:
        f.write(base64.b64decode(audio_data))
    input_lengths, audio_path = cp.main("./audio/" + audio_name + "." + file_type)
    return jsonify({'num_inputs': len(input_lengths), 'input_lengths': input_lengths, 'audio_name': audio_path[:-4], 'file_type': 'mp3'})


@app.route('/upload_images', methods=['POST'])
def upload_images():
    data = request.get_json()
    input_lengths = data['input_lengths']
    input_encodings = data['inputs']
    input_files = []
    effectsSelected = data['effectsSelected']
    message = data['message']

    for encoding in input_encodings:
        file_name = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
            )
        # I don't think this is working properly, but it also doesn't seem to matter for using moviepy...
        # TODO: clean this up?
        file_type = guess_extension(encoding[encoding.index('image/'):encoding.index(';base64')])
        with open("./images/" + file_name + file_type, "wb") as f:
            f.write(base64.b64decode(encoding[encoding.index(',')+1:]))
            input_files.append("./images/" + file_name + file_type)
    audio_name = data['audio_name'] if 'audio_name' in data else 'audio1'
    audio_file_type = data['file_type']
    combine(
        list(zip(input_files, input_lengths)), 
        audio_name + "." + audio_file_type, 
        audio_name + ".mp4",
        effectsSelected,
        message
        )
    video_encoding = ""
    with open(audio_name + ".mp4", "rb") as f:
        video_encoding = str(base64.b64encode(f.read()))
    return jsonify({'video_encoding': video_encoding, 'file_type': 'mp4'})
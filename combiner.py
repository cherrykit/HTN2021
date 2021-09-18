import moviepy.editor as mpy

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
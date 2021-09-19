# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 23:07:30 2021

@author: Claire

This works if you do `pip install pychorus` and run it using python3 on the student linux environment
Use scp to copy files back and forth

"""
import pychorus
from pychorus import find_and_output_chorus
import numpy as np
import sys
import librosa
from pydub import AudioSegment
import os
'''
def compute_similarity_matrix_slow(chroma):
    """Slow but straightforward way to compute time time similarity matrix"""
    num_samples = chroma.shape[1]
    time_time_similarity = np.zeros((num_samples, num_samples))
    for i in range(num_samples):
        for j in range(num_samples):
            # For every pair of samples, check similarity
            time_time_similarity[i, j] = 1 - (
                np.linalg.norm(chroma[:, i] - chroma[:, j]) / sqrt(12))

    return time_time_similarity
'''
#chroma = pychorus.create_chroma("Coldplay - Fix You.mp3")

'''
num_samples = chroma.shape[1]
M = np.zeros((num_samples, num_samples))
for i in range(num_samples):
    for j in range(num_samples):
        # For every pair of samples, check similarity
        M[i, j] = 1 - (  
            np.linalg.norm(chroma[:, i] - chroma[:, j]) / sqrt(12))

T = np.zeros((num_samples, num_samples))
for i in range(num_samples):
    for j in range(num_samples):
        T[i,j]= (M[i,i-j] if i - j >= 0 else 0)
'''

def bpm(audio_file):
    '''Produces the bpm given an audio file'''
    y, sr = librosa.load(audio_file)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print('Estimated tempo: {:0.2f} beats per minute'.format(tempo))
    return tempo
    
def cut_audio(audio_file, chorus_start_sec, tempo):
    sound = AudioSegment.from_file(audio_file)
    # clip starts 5 seconds before chorus
    input_lengths = [5]
    chorus_start_sec = (chorus_start_sec*1000) - 5000
    chorus_end_sec = chorus_start_sec + 25000
    audio_clip = sound[chorus_start_sec:chorus_end_sec]
    
    # if path doesn't exist, then create new folder for music
    path = "./" + str(audio_file[:-4])
    if not os.path.exists(path):
        os.mkdir(path)
    audio_clip.export(path + "/0_full.mp3", format="mp3")
    audio_path = path + "/0_full.mp3"
    # cut audio by tempo
    video = sound[chorus_start_sec:chorus_start_sec+5000]
    video.export(path + "/1_video.mp3", format="mp3")
    ms = 60000 / tempo
    
    # for how many bpm fit into 10 seconds, create split up audio
    start = chorus_start_sec+5000
    for i in range(2,int(20000//ms)+2):
        pic = sound[start:start+ms]
        input_lengths.append(float(ms) / 1000)
        pic.export(path + "/" + str(i) + "_pic.mp3", format="mp3")
        start = start+ms
    return input_lengths, audio_path
    
def main(audio_file):
    chorus_start_sec = find_and_output_chorus(audio_file, audio_file.replace(".mp3", "-clipped.wav"), 20)
    tempo = bpm(audio_file)
    input_lengths, audio_path = cut_audio(audio_file, chorus_start_sec, tempo)
    return input_lengths, audio_path

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Stereo-Hearts.mp3")
    

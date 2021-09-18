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

if __name__ == "__main__":
    audio_file = sys.argv[1] if len(sys.argv) > 1 else "Coldplay - Fix You.mp3"
    chorus_start_sec = find_and_output_chorus(audio_file, audio_file.replace(".mp3", "-clipped.wav"), 60)

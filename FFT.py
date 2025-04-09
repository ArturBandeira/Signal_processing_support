import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd

def FFT(csi_matrix):
    csi_transposed = np.transpose(csi_matrix)
    for i in range(len(csi_transposed)): 
        csi_transposed[i] = np.fft.fft(csi_transposed[i])
    FFT_amplitudes = np.abs(csi_transposed)
    FFT_phases =  np.angle(csi_transposed)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(FFT_amplitudes, aspect='auto', cmap='viridis')
    plt.colorbar()
    plt.title('Amplitude FFT')
    plt.xlabel('Índice')
    plt.ylabel('Canal')

    plt.subplot(1, 2, 2)
    plt.imshow(FFT_phases, aspect='auto', cmap='hsv')
    plt.colorbar()
    plt.title('Fase FFT')
    plt.xlabel('Índice')
    plt.ylabel('Canal')

    plt.tight_layout()
    plt.show()

path_to_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = "3_preprocessed_data"

FILE_NAME = sys.argv[1]

file_path = os.path.join(path_to_dir, data_folder, FILE_NAME)
print("Reading data from: " + file_path)
data_parquet = pd.read_parquet(file_path)
FFT(data_parquet)
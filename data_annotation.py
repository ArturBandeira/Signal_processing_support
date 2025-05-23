import matplotlib.pyplot as plt
from datetime import datetime
import os
import glob
import pandas as pd
import numpy as np
import sys
import config
import math

# We use this to display the total sampling area for the annotated region
# This helps avoid user error and superimposing two sampling areas in different events
sampling_area = config.WINDOW_SIZE + (config.WINDOW_SLIDE * config.WINDOW_SAMPLE_AMOUNT * 2)

def plot_csi(csi_matrix):

    path_to_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_folder = "1_raw_data"
    raw_folder_path = os.path.join(path_to_dir, raw_data_folder)
    raw_data_csv_files = glob.glob(os.path.join(raw_folder_path, "*.csv"))

    tem_time_stamp = 0
    
    preprocessed_file_name =("-".join(FILE_NAME.split("-")[1:])).split(".")[0].split("-")[-1]
    mac_file = ":".join(FILE_NAME.split("-")[1:7])
    time_stamps = []
    time_stamps_that_matter = []
    for file in raw_data_csv_files:
        raw_file_name = os.path.basename(file).split(".")[0]
        if(1 == 1):
        #if(raw_file_name == preprocessed_file_name):
            data = pd.read_csv(file, header=0)
            if(len(data.columns) == 27):
                tem_time_stamp = 1
                for j in range(data.shape[0]):
                    mac_adress = data.iloc[j][data.columns[2]]
                    if(mac_adress == mac_file):
                        time_stamps.append(data.iloc[j][data.columns[-1]])
                #time_stamps = data.iloc[:, -1].to_numpy()
                break
    # Event function to handle mouse clicks
    def handleEvent1(event):
        if event.xdata is not None and event.button == 3:
                #show_time_stamp = datetime.fromtimestamp(time_stamps[round(event.xdata)])
                #text_box.set_text(f"Timestamp: {show_time_stamp}")  
                scatter = ax.scatter(event.xdata, event.ydata, color='blue', s=50, edgecolors='black', zorder=3)
                scatter_points.append(scatter)
                bar, = ax.plot([event.xdata-(sampling_area/2), event.xdata+(sampling_area/2)], [event.ydata, event.ydata], color='blue', linewidth=2,alpha=1.0, zorder=2)
                bar_points.append(bar)
                fig.canvas.draw_idle() 
                #print(time_stamps[round(event.xdata)])
                list_of_values.append(round(event.xdata))
                time_stamps_that_matter.append(time_stamps[round(event.xdata)])

    # Event fucntion to delete points created by the user
    def handleEvent2(event):
        if event.xdata is not None and event.key == "ctrl+z" and len(list_of_values)>0:
            scatter_points[-1].remove()
            scatter_points.pop()
            bar_points[-1].remove()
            bar_points.pop()
            list_of_values.pop()
            fig.canvas.draw_idle()

    #Event function to update the timestamp value printed in the graphic
    def handleEvent3(event):
        if event.xdata is not None:
            show_time_stamp = datetime.fromtimestamp(time_stamps[round(event.xdata)])
            text_box.set_text(f"Timestamp: {show_time_stamp}")  
            fig.canvas.draw_idle()

    fig, ax = plt.subplots()

    # Calling the events fucntions 
    if(tem_time_stamp):
        list_of_values = []
        scatter_points = []
        bar_points = []
        valor = 0
        text_box = ax.text(0.95, 0.05, "Timestamp: undefined", fontsize=8,bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'),transform=ax.transAxes, ha="right", va="bottom")
        fig.canvas.mpl_connect("button_press_event", handleEvent1)
        fig.canvas.mpl_connect("key_press_event", handleEvent2)
        fig.canvas.mpl_connect("motion_notify_event", handleEvent3)

    csi_matrix = np.transpose(csi_matrix)
    xlim = csi_matrix.shape[1]
    x_label = "Frame No."
    limits = [0, xlim, 1, csi_matrix.shape[0]] 
    im = ax.imshow(csi_matrix, cmap="jet", extent=limits, aspect="auto")
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Amplitude (dB)")

    plt.xlabel(x_label)
    plt.ylabel("Subcarrier Index")
    plt.title("CSI Amplitude Heatmap Plot")
    plt.show()
    if(tem_time_stamp):
        return list_of_values, time_stamps_that_matter

# Getting the path to all folders and files we need
path_to_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = "3_preprocessed_data"


# Check for missing args
args = sys.argv[1:]
if len(args) < 2:
    print("Argument error: please provide the source file name and the annotated class name")
    exit()


FILE_NAME = sys.argv[1]

file_path = os.path.join(path_to_dir, data_folder, FILE_NAME)
print("Reading data from: " + file_path)
data_parquet = pd.read_parquet(file_path)
frames1, time_stamps_arr = plot_csi(data_parquet)


path_to_dir = os.path.dirname(os.path.abspath(__file__))
raw_data_folder = "1_raw_data"
raw_folder_path = os.path.join(path_to_dir, raw_data_folder)
raw_data_csv_files = glob.glob(os.path.join(raw_folder_path, "*.csv"))
    
preprocessed_file_name =("-".join(FILE_NAME.split("-")[1:])).split(".")[0].split("-")[-1]
mac_file = ":".join(FILE_NAME.split("-")[1:7])
time_stamps = []
mac_dict={}

for file in raw_data_csv_files:
        raw_file_name = os.path.basename(file).split(".")[0]
        if(1 == 1):
        #if(raw_file_name == preprocessed_file_name):
            data = pd.read_csv(file, header=0)
            if(len(data.columns) == 27):
                for j in range(data.shape[0]):
                    mac_adress = data.iloc[j][data.columns[2]]
                    if mac_adress.find("0C:8B:95:") == -1 or mac_adress not in config.VALID_MAC:
                        continue
                    if mac_adress not in mac_dict:
                        mac_dict[mac_adress] = []
                    mac_dict[mac_adress].append(data.iloc[j][data.columns[-1]])
                #time_stamps = data.iloc[:, -1].to_numpy()
                break

mac_frames = { key: [] for key in mac_dict }
print(mac_dict.keys())

for value in time_stamps_arr:
    mac_frames_temporary = { key: [] for key in mac_dict } # dict temporario, verificar continuidade dos timestamps antes de add no dict principal
    for key, lst in mac_dict.items():
        idx_mais_proximo = min(
            range(len(lst)),
            key=lambda i: abs(lst[i] - value)
        )
        mac_frames_temporary[key].append(idx_mais_proximo)
    j = 0
    arr_verify = np.zeros(config.ESP_NUMBER)
    for chave,lista in mac_frames_temporary.items():
        #verificar mac_dict[chave]
        if abs(mac_dict[chave][lista[0]] - value) < config.TIME_CAP and max(mac_dict[chave][lista[0]] - mac_dict[chave][lista[0] - math.floor((config.WINDOW_SIZE/2))], mac_dict[chave][lista[0]+math.floor((config.WINDOW_SIZE/2))] - mac_dict[chave][lista[0]]) < config.TIME_SIZE + config.TIME_TOLERANCE:
            arr_verify[j] = 1
        j+=1
    prod = 1
    for l in  range(config.ESP_NUMBER):
        prod = prod*arr_verify[l]
    if prod == 1:
        for chave,lista in mac_frames_temporary.items():
            mac_frames[chave].append(lista[0])

class_anotated = sys.argv[2]
if os.path.isfile("slicing_source.txt"):
    f = open("slicing_source.txt", "a+")
    f.write("\n")
else:
    f = open("slicing_source.txt", "a+")
    f.write("IN, OUT, FRAMES, TIMESTAMPS\n")

for key in mac_dict.keys():
    f.write("preprocessed-"+key.replace(":", "-")+"-my.parquet" +", " +sys.argv[2]+", ")
    for value in mac_frames[key]:
        if(value == mac_frames[key][-1]):
            f.write(str(value) + ", ")
            break
        f.write(str(value)+" ") 
    for value in mac_frames[key]:
        if(value == mac_frames[key][-1]):
            f.write(str(mac_dict[key][value]) + "\n")
            break
        f.write(str(mac_dict[key][value])+" ") 

# mac_dict: dicionario chaves: mac adress, conteudo: timestamps associados a cada mac_adress
#time_stamp_arr: array com os timestamps selecionados pelo usuario
#mac_frames: dicionario com os frames associados aos timestamps escolhidos pelo usuario para cada mac adress
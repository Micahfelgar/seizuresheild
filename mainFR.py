import cv2
import colorsys
import math
import numpy as np
import random
import time
from tkinter import messagebox
import tkinter as tk

video_output = ""
root = tk.Tk()
root.wm_attributes("-topmost", 1)
root.withdraw()

lightnessMaster = []
hueMaster = []

# Hide logs
cv2.setLogLevel(0)
video_path = input("Coller le chemin vidéo\n").replace('"', '')
video_output = video_path

def warn(frame):
    seconds = math.floor(frame/cap.get(cv2.CAP_PROP_FPS))
    print(
        f"AVERTISSEMENT feux clignotants au image {frame} ({seconds//60}:{seconds%60}). Temps pris: {int((time.time()-startTime)//60)}min {round(time.time()-startTime, 3)%60}s")
    if messagebox.showinfo("AVERTISSEMENT", "Cette vidéo contient des lumières clignotantes rapides. Si vous êtes sujet à des crises d'épilepsie, la discrétion est conseillée."):
        root.destroy()
        input("Appuyez sur « enter » pour quitter")
        exit()

def safe():
    if messagebox.showinfo("Vidéo est sûre", "Cette vidéo a été jugée sûr. Procédez tout de même avec prudence."):
        root.destroy()

# Ouvrir un fichier ou un flux vidéo
cap = cv2.VideoCapture(video_output)
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

currentFrame = 0
difference = 0

dramatic_change_countLight = 0
dramatic_change_countHue = 0
# PARAMÈTRES PERSONNALISÉS
thresholdLight = 50
thresholdHue = 0.275
startTime = time.time()

while currentFrame < frameCount:

    cap.set(cv2.CAP_PROP_POS_FRAMES, currentFrame)

    # Lire une image de la vidéo
    ret, frame = cap.read()
    ret

    # Calculer la couleur moyenne de la trame (format BVR dans OpenCV)
    average_color_per_row = np.mean(frame, axis=0)
    average_color = np.mean(average_color_per_row, axis=0)

    # OpenCV utilise BVR, mais nous pouvons le convertir en RVB pour des raisons de cohérence.
    average_color_rgb = average_color[::-1]  # Inverser pour obtenir RVB

    hls = colorsys.rgb_to_hls(
        average_color_rgb[0], average_color_rgb[1], average_color_rgb[2])
    lightnessMaster.append(math.floor(hls[1]))
    if len(lightnessMaster) > 30:
        lightnessMaster.pop(0)
    for i in range(len(lightnessMaster) - 1):
        difference = abs(lightnessMaster[i] - lightnessMaster[i + 1])
        if difference > thresholdLight:
            dramatic_change_countLight += 1
        if dramatic_change_countLight > 10:
            warn(currentFrame)
    hueMaster.append(round(hls[0], 2))

    if len(hueMaster) > 30:
        hueMaster.pop(0)
    for i in range(len(hueMaster) - 1):
        difference = abs(hueMaster[i] - hueMaster[i + 1])
        if difference > thresholdHue:
            dramatic_change_countHue += 1
        if dramatic_change_countHue > 10:
            warn(currentFrame)
    dramatic_change_countHue = 0
    dramatic_change_countLight = 0
    currentFrame = currentFrame + random.randint(1, 4)

# recheck
currentFrame = 0
safe()
endTime = time.time()
print(f"Temps total : {round(endTime - startTime, 3)}")

cap.release()

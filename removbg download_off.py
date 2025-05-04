import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from rembg import remove
from PIL import Image, ImageTk
import threading
import os

def remove_background(image_path, progress_var, output_path):
    progress_var.set(20)  # Mise à jour de la barre de progression
    root.update_idletasks()

    with open(image_path, "rb") as f:
        input_image = f.read()
    progress_var.set(50)  # Mise à jour intermédiaire
    root.update_idletasks()

    output_image = remove(input_image)
    
    try:
        with open(output_path, "wb") as f:
            f.write(output_image)
        progress_var.set(100)  # Terminé !
        root.update_idletasks()
        display_image(output_path)
    except PermissionError:
        print(f"Erreur : Impossible de sauvegarder l'image dans {output_path}. Essaie un autre dossier.")

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
    if file_path:
        output_folder = filedialog.askdirectory(title="Choisis un dossier de sauvegarde")
        if not output_folder:
            output_folder = os.path.expanduser("~/Desktop")  # Sauvegarde sur le bureau par défaut
        output_path = os.path.join(output_folder, "output.png")

        progress_var.set(0)
        threading.Thread(target=remove_background, args=(file_path, progress_var, output_path)).start()

def display_image(image_path):
    img = Image.open(image_path)
    img = ImageTk.PhotoImage(img)
    
    panel.config(image=img)
    panel.image = img

# Interface graphique
root = tk.Tk()
root.title("Suppression de fond d'image")

btn = tk.Button(root, text="Ouvrir une image", command=open_image)
btn.pack()

# Ajout de la barre de progression
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, length=200, mode="determinate", variable=progress_var)
progress_bar.pack()

panel = tk.Label(root)
panel.pack()

root.mainloop()

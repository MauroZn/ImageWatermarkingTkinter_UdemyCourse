# Importing libraries
import tkinter as tk
from tkinter import Label
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

uploaded_image = None

def imageUploader():
    global uploaded_image
    fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = tk.filedialog.askopenfilename(filetypes=fileTypes)

    if len(path):
        img = Image.open(path)
        max_width = 1920
        max_height = 1080
        width, height = img.size
        if width >= max_width or height >= max_height:
            scale_w = 1280 / width
            scale_h = 720 / height
            scale = min(scale_w, scale_h)

            new_width = int(width * scale)
            new_height = int(height * scale)

            img = img.resize((new_width, new_height))
            window.geometry(f"{new_width + 160}x{new_height + 300}")
        else:
            window.geometry(f"{width + 160}x{height + 300}")

        uploaded_image = img
        pic = ImageTk.PhotoImage(img)
        label.config(image=pic)
        label.image = pic

    else:
        print("No file is chosen, please choose a file.")

def watermarkImage(inputText):
    img_width, img_height = uploaded_image.size

    img = Image.new("RGBA", uploaded_image.size)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", size=90)

    bbox = draw.textbbox((0, 0), inputText, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (img_width - text_width) // 2
    y = (img_height - text_height) // 2

    draw.text((x,y), inputText, font=font, fill=(0, 0, 0, 255))


    uploaded_image.paste(img, (0, 0), img)
    pic = ImageTk.PhotoImage(uploaded_image)
    label.config(image=pic)
    label.image = pic

def downloadImage():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Save PNG image as"
    )
    if file_path:
            uploaded_image.save(file_path, "PNG")

if __name__ == "__main__":

    window = tk.Tk()

    window.title("Adding Watermark to Image")
    window.minsize(560, 270)

    label = tk.Label(window)
    label.pack(pady=10, fill='x', expand=True)

    uploadButton = tk.Button(window, text="Upload Image", command=imageUploader)
    uploadButton.pack(padx=20, pady=20)

    # my_label = Label(window, text="Watermark Text To Add:", font=("Arial", 10, "bold"))
    # my_label.pack(padx=20, pady=20)

    center_frame = tk.Frame(window)
    center_frame.pack(pady=10)

    var = tk.StringVar(value="Watermark")
    watermarkInput = tk.Entry(center_frame, textvariable=var, width=30)
    watermarkInput.pack(side=tk.LEFT, padx=10)

    watermarkButton = tk.Button(center_frame, text="Add Watermark", command=lambda: watermarkImage(var.get()))
    watermarkButton.pack(side=tk.LEFT, padx=10)

    downloadButton = tk.Button(window, text="Download Image", command=downloadImage)
    downloadButton.pack(padx=20, pady=20)

    window.mainloop()
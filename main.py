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

        width, height = img.size
        if width > 1920 or height > 1080:
            new_width = 1280
            new_height = 720
            img = img.resize((new_width, new_height))
            window.update()
        else:
            window.geometry(f"{width + 160}x{height + 100}")

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
    label.pack(pady=10)


    downloadButton = tk.Button(window, text="Download Image", command=downloadImage)
    downloadButton.pack(side=tk.BOTTOM, pady=20)

    watermarkButton = tk.Button(window, text="Add Watermark", command=lambda: watermarkImage(var.get()))
    watermarkButton.pack(side=tk.BOTTOM, pady=20)

    var = tk.StringVar(value="Hello Geeks")
    watermarkInput = tk.Entry(window, textvariable=var, width=30)
    watermarkInput.pack(side=tk.BOTTOM, pady=10)

    my_label = Label(window, text="Watermark Text To Add:", font=("Arial", 10, "bold"))
    my_label.pack(side=tk.BOTTOM)

    uploadButton = tk.Button(window, text="Upload Image", command=imageUploader)
    uploadButton.pack(side=tk.BOTTOM, pady=20)

    window.mainloop()
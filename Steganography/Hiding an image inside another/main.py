import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def encode_image():
    # Pilih gambar utama
    main_image_path = filedialog.askopenfilename(title="Pilih Gambar Utama")
    if not main_image_path:
        return

    # Pilih gambar yang akan disembunyikan
    hidden_image_path = filedialog.askopenfilename(title="Pilih Gambar yang Akan Disembunyikan")
    if not hidden_image_path:
        return

    main_image = Image.open(main_image_path)
    hidden_image = Image.open(hidden_image_path)

    # Resize hidden image to fit into main image
    hidden_image = hidden_image.resize(main_image.size)

    # Convert images to RGBA
    main_image = main_image.convert("RGBA")
    hidden_image = hidden_image.convert("RGBA")

    # Encode hidden image into main image
    encoded_image = Image.new("RGBA", main_image.size)
    for x in range(main_image.width):
        for y in range(main_image.height):
            r1, g1, b1, a1 = main_image.getpixel((x, y))
            r2, g2, b2, a2 = hidden_image.getpixel((x, y))
            # Menggunakan 4 bit terakhir dari setiap channel warna untuk menyembunyikan gambar
            r = (r1 & 0xF0) | (r2 >> 4)
            g = (g1 & 0xF0) | (g2 >> 4)
            b = (b1 & 0xF0) | (b2 >> 4)
            encoded_image.putpixel((x, y), (r, g, b, a1))

    # Save encoded image
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        encoded_image.save(save_path)
        messagebox.showinfo("Sukses", "Gambar berhasil disembunyikan dan disimpan!")

def decode_image():
    # Pilih gambar yang telah disembunyikan
    encoded_image_path = filedialog.askopenfilename(title="Pilih Gambar yang Telah Disembunyikan")
    if not encoded_image_path:
        return

    encoded_image = Image.open(encoded_image_path)
    encoded_image = encoded_image.convert("RGBA")

    # Decode hidden image from encoded image
    decoded_image = Image.new("RGBA", encoded_image.size)
    for x in range(encoded_image.width):
        for y in range(encoded_image.height):
            r, g, b, a = encoded_image.getpixel((x, y))
            # Mengambil 4 bit terakhir dari setiap channel warna untuk mendapatkan gambar tersembunyi
            r_hidden = (r & 0x0F) << 4
            g_hidden = (g & 0x0F) << 4
            b_hidden = (b & 0x0F) << 4
            decoded_image.putpixel((x, y), (r_hidden, g_hidden, b_hidden, 255))

    # Tampilkan gambar yang telah di-decode
    decoded_image.show()

# GUI Setup
root = tk.Tk()
root.title("Steganography: Hiding an Image Inside Another")

frame = tk.Frame(root)
frame.pack(pady=20)

encode_button = tk.Button(frame, text="Sembunyikan Gambar", command=encode_image)
encode_button.grid(row=0, column=0, padx=10)

decode_button = tk.Button(frame, text="Tampilkan Gambar Tersembunyi", command=decode_image)
decode_button.grid(row=0, column=1, padx=10)

root.mainloop()

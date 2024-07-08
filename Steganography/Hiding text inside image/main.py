import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Menu
from PIL import Image, ImageTk
import os

class Steganography:
    @staticmethod
    def _int_to_bin(rgb):
        r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    @staticmethod
    def _bin_to_int(rgb):
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    @staticmethod
    def _merge_rgb(rgb1, rgb2):
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:-1] + r2[0], g1[:-1] + g2[1], b1[:-1] + b2[2])
        return rgb

    @staticmethod
    def _fix_image(image):
        if image.width % 2 != 0 or image.height % 2 != 0:
            new_image = Image.new(image.mode, (image.width + 1, image.height + 1))
            new_image.paste(image, (0, 0))
            return new_image
        return image

    def encode(self, image_path, message, output_path):
        image = Image.open(image_path)
        image = self._fix_image(image)
        binary_message = '0000000000000001' + ''.join(f'{ord(i):08b}' for i in message) + '1111111111111110'  # Start and end delimiters

        if len(binary_message) > image.width * image.height * 3:
            raise ValueError("Message is too long to encode in the image.")

        pixels = iter(image.getdata())
        new_pixels = []
        for i in range(0, len(binary_message), 3):
            pixel = [value for value in next(pixels)[:3]]
            for j in range(3):
                if i + j < len(binary_message):
                    pixel[j] = (pixel[j] & 254) | int(binary_message[i + j])
            new_pixels.append(tuple(pixel))

        image.putdata(new_pixels)
        image.save(output_path, format='PNG')

    def decode(self, image_path):
        image = Image.open(image_path)
        binary_message = ''
        for pixel in image.getdata():
            for value in pixel[:3]:
                binary_message += str(value & 1)

        all_bytes = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
        decoded_message = ''
        start_marker = '0000000000000001'
        end_marker = '1111111111111110'
        start_index = binary_message.find(start_marker)
        end_index = binary_message.find(end_marker)

        if start_index != -1 and end_index != -1:
            binary_message = binary_message[start_index + len(start_marker):end_index]
            all_bytes = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
            for byte in all_bytes:
                decoded_message += chr(int(byte, 2))
            return decoded_message
        return "No valid encoded message found."

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography GUI")
        self.steganography = Steganography()

        self.create_widgets()
        self.create_menu()
        self.create_status_bar()

    def create_widgets(self):
        # Frame untuk judul
        title_frame = tk.Frame(self.root, pady=10)
        title_frame.pack()

        self.label = tk.Label(title_frame, text="Steganography GUI", font=("Helvetica", 16, "bold"))
        self.label.pack()

        # Frame untuk gambar
        image_frame = tk.Frame(self.root, pady=10)
        image_frame.pack()

        self.image_label = tk.Label(image_frame)
        self.image_label.pack()

        # Frame untuk tombol
        button_frame = tk.Frame(self.root, pady=10)
        button_frame.pack()

        self.encode_button = tk.Button(button_frame, text="Encode Message", command=self.encode_message, width=20, bg="lightblue", font=("Helvetica", 12))
        self.encode_button.pack(side=tk.LEFT, padx=5)

        self.decode_button = tk.Button(button_frame, text="Decode Message", command=self.decode_message, width=20, bg="lightgreen", font=("Helvetica", 12))
        self.decode_button.pack(side=tk.RIGHT, padx=5)

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.open_image)
        file_menu.add_command(label="Save Image", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

    def create_status_bar(self):
        self.status = tk.StringVar()
        self.status.set("Welcome to Steganography GUI")
        status_bar = tk.Label(self.root, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.status.set(f"Displayed image: {os.path.basename(image_path)}")

    def open_image(self):
        image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if image_path:
            self.display_image(image_path)

    def save_image(self):
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("BMP Files", "*.bmp")])
        if output_path:
            self.steganography.encode(self.image_path, self.message, output_path)
            messagebox.showinfo("Success", f"Image saved as {output_path}")

    def encode_message(self):
        image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not image_path:
            return

        self.display_image(image_path)

        message = simpledialog.askstring("Input", "Enter the message to encode:")
        if not message:
            return

        self.image_path = image_path
        self.message = message

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("BMP Files", "*.bmp")])
        if not output_path:
            return

        try:
            self.steganography.encode(image_path, message, output_path)
            messagebox.showinfo("Success", f"Message encoded into {output_path}.")
            self.status.set(f"Message encoded into {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Error encoding message")

    def decode_message(self):
        image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not image_path:
            return

        self.display_image(image_path)

        try:
            decoded_message = self.steganography.decode(image_path)
            messagebox.showinfo("Decoded Message", f"Decoded message: {decoded_message}")
            self.status.set("Message decoded successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Error decoding message")

if __name__ == '__main__':
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

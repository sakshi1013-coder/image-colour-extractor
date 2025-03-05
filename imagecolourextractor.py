import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from colorthief import ColorThief
import pyperclip
import random
from tkinter import font as tkFont

color_schemes = {
    'gradient galaxy': ['#0d1b2a', '#1b263b', '#415a77', '#778da9', '#e0e1dd'],
    'nature green': ['#2a4d14', '#4b6b2f', '#6b8f3d', '#a3b18a', '#d9e4dd']
}

def extract_dominant_colors(image_path, num_colors=5):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=num_colors)
    return dominant_color, palette

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        dominant_color, palette = extract_dominant_colors(file_path)
        display_colors(dominant_color, palette)

def display_colors(dominant_color, palette):
    for widget in color_frame_inner.winfo_children():
        widget.destroy()

    colors = [dominant_color] + palette
    for color in colors:
        color_hex = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

        color_frame_item = tk.Frame(color_frame_inner, bg=color_hex, bd=2, relief="solid")
        color_frame_item.pack(pady=5, padx=5, fill="x")

        color_label = tk.Label(color_frame_item, bg=color_hex, width=20, height=2)
        color_label.pack(side=tk.LEFT, padx=5, pady=5)

        hex_label = tk.Label(color_frame_item, text=color_hex, width=10)
        hex_label.pack(side=tk.LEFT, padx=5, pady=5)

        copy_button = tk.Button(color_frame_item, text="Copy", command=lambda c=color_hex: copy_to_clipboard(c))
        copy_button.pack(side=tk.LEFT, padx=5, pady=5)

def copy_to_clipboard(hex_code):
    pyperclip.copy(hex_code)
    messagebox.showinfo("Copied", f"Copied {hex_code} to clipboard!")

def auto_generate_combinations():
    auto_color_frame.pack(pady=10, padx=10, fill="both", expand=True)
    for widget in auto_color_frame_inner.winfo_children():
        widget.destroy()

    for _ in range(5):
        color = [random.randint(0, 255) for _ in range(3)]
        color_hex = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

        color_frame_item = tk.Frame(auto_color_frame_inner, bg=color_hex, bd=2, relief="solid")
        color_frame_item.pack(pady=5, padx=5, fill="x")

        color_label = tk.Label(color_frame_item, bg=color_hex, width=20, height=2)
        color_label.pack(side=tk.LEFT, padx=5, pady=5)

        hex_label = tk.Label(color_frame_item, text=color_hex, width=10)
        hex_label.pack(side=tk.LEFT, padx=5, pady=5)

        copy_button = tk.Button(color_frame_item, text="Copy", command=lambda c=color_hex: copy_to_clipboard(c))
        copy_button.pack(side=tk.LEFT, padx=5, pady=5)

def display_color_scheme(scheme):
    for widget in color_frame_inner.winfo_children():
        widget.destroy()

    for color_hex in scheme:
        color_frame_item = tk.Frame(color_frame_inner, bg=color_hex, bd=2, relief="solid")
        color_frame_item.pack(pady=5, padx=5, fill="x")

        color_label = tk.Label(color_frame_item, bg=color_hex, width=20, height=2)
        color_label.pack(side=tk.LEFT, padx=5, pady=5)

        hex_label = tk.Label(color_frame_item, text=color_hex, width=10)
        hex_label.pack(side=tk.LEFT, padx=5, pady=5)

        copy_button = tk.Button(color_frame_item, text="Copy", command=lambda c=color_hex: copy_to_clipboard(c))
        copy_button.pack(side=tk.LEFT, padx=5, pady=5)

def search_color_scheme():
    user_input = simpledialog.askstring("Input", "Enter a description of the color scheme (e.g., 'Gradient Galaxy', 'Nature Green'):")
    if user_input:
        scheme = color_schemes.get(user_input.lower())
        if scheme:
            display_color_scheme(scheme)
        else:
            messagebox.showinfo("Error", f"No color scheme found for '{user_input}'.")

def close_auto_color_frame():
    auto_color_frame.pack_forget()

app = tk.Tk()
app.title("Image Color Palette Extractor")
app.geometry("800x600")
app.configure(bg="#f0f0f0")

# Load the custom font
custom_font = tkFont.Font(family="Ancient", size=20, weight="bold")

welcome_label = tk.Label(app, text="WELCOME TO COLOUR EXTRACTOR", font=custom_font, fg="#8B4513", bg="#f0f0f0")
welcome_label.pack(pady=10)

header_label = tk.Label(app, text="Image Color Palette Extractor", font=("Helvetica", 16), bg="#f0f0f0")
header_label.pack(pady=10)

open_button = tk.Button(app, text="Open Image", command=open_image, width=25)
open_button.pack(pady=5)

auto_generate_button = tk.Button(app, text="Auto-Generate Color Combinations", command=auto_generate_combinations, width=25)
auto_generate_button.pack(pady=5)

search_button = tk.Button(app, text="Search Color Scheme", command=search_color_scheme, width=25)
search_button.pack(pady=5)

# Create a canvas and a scrollbar for extracted colors
canvas = tk.Canvas(app, bg="#ffffff")
scrollbar = tk.Scrollbar(app, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Create a frame inside the canvas for extracted colors
color_frame_inner = tk.Frame(canvas, bg="#ffffff")

# Configure the canvas for extracted colors
canvas.create_window((0, 0), window=color_frame_inner, anchor="nw")
color_frame_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a separate frame for auto-generated color combinations
auto_color_frame = tk.Frame(app, bg="#f0f0f0")
auto_color_frame.pack(pady=10, padx=10, fill="both", expand=True)

auto_color_frame_label = tk.Label(auto_color_frame, text="Auto-Generated Color Combinations", font=("Helvetica", 14), bg="#f0f0f0")
auto_color_frame_label.pack(pady=5)

auto_color_frame_inner = tk.Frame(auto_color_frame, bg="#ffffff", bd=2, relief="solid")
auto_color_frame_inner.pack(pady=5, padx=5, fill="both", expand=True)

close_button = tk.Button(auto_color_frame, text="Close", command=close_auto_color_frame, width=25)
close_button.pack(pady=5)

app.mainloop()
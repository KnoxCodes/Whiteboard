from tkinter import *
from tkinter import colorchooser
import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab
import sys, os


# ----------------- Helper -----------------
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# ----------------- Functions -----------------
def color_picker():
    # open color chooser
    picked = colorchooser.askcolor()
    if picked[1] is not None:  # if user picked a valid color
        showColor(picked[1])

current_x = 0
current_y = 0
color = 'black'

def locate_xy(work):
    global current_x, current_y
    current_x = work.x
    current_y = work.y

def addLine(work):
    global current_x, current_y
    canvas.create_line((current_x, current_y, work.x, work.y),
                       width=int(scale.get()), fill=color, capstyle=ROUND, smooth=True)
    current_x, current_y = work.x, work.y

def showColor(new_color):
    global color
    color = new_color

current_mode = "draw"  # can be "draw", "circle", "rectangle", etc.

def set_mode(new_mode):
    global current_mode
    current_mode = new_mode

    # Clear previous bindings
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<ButtonRelease-1>")

    if current_mode == "draw":
        # freehand mode
        canvas.bind("<Button-1>", locate_xy)
        canvas.bind("<B1-Motion>", addLine)
    elif current_mode == "text":
        canvas.bind("<Button-1>", place_text)
    elif current_mode == "eraser":
        canvas.bind("<Button-1>", locate_xy)
        canvas.bind("<B1-Motion>", erase_line)
    elif current_mode == "select":
        canvas.bind("<Button-1>", select_item)
        canvas.bind("<B1-Motion>", move_item)
    else:
        # shape modes use press + release
        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)


temp_shape = None

def on_press(event):
    global start_x, start_y, temp_shape
    start_x, start_y = event.x, event.y
    temp_shape = None

def on_drag(event):
    global temp_shape
    # remove old preview
    if temp_shape:
        canvas.delete(temp_shape)
    if current_mode == "rectangle":
        temp_shape = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=color, fill=color if fill_shapes.get() else "",width=2 + int(scale.get()))
    elif current_mode == "circle":
        temp_shape = canvas.create_oval(start_x, start_y, event.x, event.y, outline=color, fill=color if fill_shapes.get() else "", width=2 + int(scale.get()))
    elif current_mode == "line":
        temp_shape = canvas.create_line(start_x, start_y, event.x, event.y, fill=color, width=2 + int(scale.get()))

def on_release(event):
    global temp_shape
    if temp_shape:
        # keep final shape
        temp_shape = None


def place_text(event):
    entry = Entry(root, font=("Arial", 10+int(scale.get())))
    entry.place(x=event.x+100, y=event.y)  # adjust offset for canvas
    entry.focus()

    def save_text(e):
        canvas.create_text(event.x, event.y, text=entry.get(), fill=color, font=("Arial", 10+int(scale.get())))
        entry.destroy()

    entry.bind("<Return>", save_text)
    set_mode("draw")


def save_canvas():
    # Ask user where to save
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")],
        title="Save Drawing"
    )
    
    if not file_path:  # user cancelled
        return

    # Get the absolute coordinates of the canvas
    x = root.winfo_rootx() + canvas.winfo_x() + 70
    y = root.winfo_rooty() + canvas.winfo_y() + 30
    x1 = x + canvas.winfo_width() + 70
    y1 = y + canvas.winfo_height() + 30

    # Capture and save
    ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
    print(f"Saved to {file_path}")


selected_item = None
last_x, last_y = 0, 0

def select_item(event):
    global selected_item, last_x, last_y
    selected_item = canvas.find_closest(event.x, event.y)
    last_x, last_y = event.x, event.y
    if selected_item:
        canvas.tag_raise(selected_item)

def move_item(event):
    global selected_item, last_x, last_y
    if selected_item:
        dx, dy = event.x - last_x, event.y - last_y
        canvas.move(selected_item, dx, dy)
        last_x, last_y = event.x, event.y

def erase_line(event):
    global current_x, current_y
    canvas.create_line((current_x, current_y, event.x, event.y),
                       width=int(scale.get())+5, fill="white", capstyle=ROUND, smooth=True)
    current_x, current_y = event.x, event.y

# ----------------- UI -----------------
root = Tk()
root.title("White board")
root.geometry("1050x570+150+50")
root.configure(bg="#f2f3f5")
root.resizable(False, False)

image_icon = PhotoImage(file=resource_path("assets/logo1.png"))
root.iconphoto(False, image_icon)

# sidebar for colors
colors = Canvas(root, bg="#ffffff", width=50, height=480, bd=0)
colors.place(x=20, y=20)

# button for custom color picker
color_icon = PhotoImage(file=resource_path("assets/color.png"))
Button(root, image=color_icon, command=color_picker, width=30, height=30).place(x=30, y=40)

# eraser button (just sets color to white)
eraser = PhotoImage(file=resource_path("assets/eraser.png"))
Button(root, image=eraser, bg="#f2f3f5", width=30, height=30,
       command=lambda: set_mode("eraser")).place(x=30, y=90)

reset_icon = PhotoImage(file=resource_path("assets/reset.png"))
Button(root, image=reset_icon, command=lambda: canvas.delete("all"), width=30, height=30).place(x=30, y=140)

pen_icon = PhotoImage(file=resource_path("assets/pen.png"))
Button(root, image=pen_icon, command=lambda: set_mode("draw"), width=30, height=30).place(x=30, y=190)

circle_icon = PhotoImage(file=resource_path("assets/circle.png"))
Button(root, image=circle_icon, command=lambda: set_mode("circle"), width=30, height=30).place(x=30, y=240)
rectangle_icon = PhotoImage(file=resource_path("assets/rectangle.png"))
Button(root, image=rectangle_icon, command=lambda: set_mode("rectangle"), width=30, height=30).place(x=30, y=290)
line_icon = PhotoImage(file=resource_path("assets/line.png"))
Button(root, image=line_icon, command=lambda: set_mode("line"), width=30, height=30).place(x=30, y=340)

select_icon = PhotoImage(file=resource_path("assets/select.png"))
Button(root, image=select_icon, command=lambda: set_mode("select"), width=30, height=30).place(x=30, y=390)

text_icon = PhotoImage(file=resource_path("assets/text.png"))
Button(root, image=text_icon, command=lambda: set_mode("text"), width=30, height=30).place(x=30, y=440)

fill_shapes = tk.BooleanVar(value=False)
Checkbutton(root, text="Fill Shapes", variable=fill_shapes, font=('Arial',14,'bold')).place(x=400, y=520)

# drawing canvas
canvas = Canvas(root, width=930, height=500, background="white", cursor="hand2")
canvas.place(x=100, y=10)


Label(root, text="Scale", font=('Arial',18,'bold')).place(x=20, y=520)
scale = Scale(root, from_=0, to=20, length=200, orient=HORIZONTAL)
scale.place(x=100, y=510)

Button(root, text="Save", command=save_canvas, font=('Arial',14,'bold')).place(x=600, y=520)


root.mainloop()
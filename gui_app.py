import customtkinter as ctk
import threading
from main import start_camera

from PIL import Image, ImageTk
import os
import main

selected_exercise = None

# ✅ GLOBAL IMAGE REFERENCES (IMPORTANT FIX)
current_image = None
current_photo = None


# 🎯 Select Exercise
def select_exercise(ex):
    global selected_exercise
    selected_exercise = ex
    status_label.configure(text=f"Selected: {ex}")


# ▶️ Start Workout
def start_workout():
    if selected_exercise is None:
        status_label.configure(text="Select exercise first")
        return

    status_label.configure(text=f"{selected_exercise} Running...")

    def run():
        start_camera(selected_exercise)

        import time
        time.sleep(1)

        show_report()
        show_graph()

    threading.Thread(target=run).start()


# 🛑 Stop Workout
def stop_workout():
    main.stop_flag = True
    status_label.configure(text="Stopping...")


# 📄 Show Report
def show_report():
    try:
        report_box.delete("0.0", "end")

        with open("final_report.txt", "r", encoding="utf-8") as f:
            report_box.insert("0.0", f.read())

    except Exception as e:
        report_box.insert("0.0", f"Error: {e}")


# 📊 Show Graph (FIXED)
def show_graph():
    global current_image, current_photo

    try:
        file = f"{selected_exercise}_rep_graph.png"

        if not os.path.exists(file):
            graph_label.configure(text="Graph not found")
            return

        img = Image.open(file)

        current_image = img.copy()  # store original safely
        current_photo = ImageTk.PhotoImage(img)

        graph_label.configure(image=current_photo, text="")
        graph_label.image = current_photo

    except Exception as e:
        graph_label.configure(text=f"Error: {e}")


# 🔍 Zoom Graph
def zoom_graph():
    global current_image, current_photo

    if current_image is None:
        status_label.configure(text="No graph to zoom")
        return

    new_width = int(current_image.width * 1.5)
    new_height = int(current_image.height * 1.5)

    zoomed = current_image.resize((new_width, new_height))

    current_photo = ImageTk.PhotoImage(zoomed)

    graph_label.configure(image=current_photo)
    graph_label.image = current_photo


# 🪟 Open Graph in New Window
def open_new_window():
    global current_image

    if current_image is None:
        status_label.configure(text="No graph available")
        return

    new_win = ctk.CTkToplevel(app)
    new_win.title("Graph Viewer")
    new_win.geometry("1000x800")

    img = current_image.copy()
    photo = ImageTk.PhotoImage(img)

    label = ctk.CTkLabel(new_win, image=photo, text="")
    label.image = photo
    label.pack(expand=True)


# 🎨 UI SETUP
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("AI Fitness Trainer")
app.geometry("850x1000")


# 🏷️ Title
ctk.CTkLabel(app, text="AI Fitness Trainer", font=("Arial", 26)).pack(pady=20)

# 📌 Exercise Buttons
for ex in ["Squat", "Pushup", "Bicep Curl", "Shoulder Press", "Front Double Biceps", "Side Chest"]:
    ctk.CTkButton(app, text=ex, command=lambda e=ex: select_exercise(e)).pack(pady=5)

# ▶️ Start & Stop Buttons
ctk.CTkButton(app, text="Start Workout", command=start_workout).pack(pady=10)
ctk.CTkButton(app, text="Stop Workout", command=stop_workout).pack(pady=10)

# 📊 Status
status_label = ctk.CTkLabel(app, text="Select exercise")
status_label.pack(pady=10)

# 📄 Report
report_box = ctk.CTkTextbox(app, width=750, height=200)
report_box.pack(pady=10)

# 📊 Scrollable Graph Container
graph_frame = ctk.CTkScrollableFrame(app, width=800, height=400)
graph_frame.pack(pady=20, fill="both", expand=True)

graph_label = ctk.CTkLabel(graph_frame, text="")
graph_label.pack(pady=10)

# 🔥 EXTRA FEATURES
ctk.CTkButton(app, text="🔍 Zoom Graph", command=zoom_graph).pack(pady=5)
ctk.CTkButton(app, text="🪟 Open in New Window", command=open_new_window).pack(pady=5)

# 🚀 Run App
app.mainloop()
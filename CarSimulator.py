import tkinter as tk
from random import randint
import time

class CarSimulation(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.car_position = 0
        self.objects = []
        self.create_objects()
        self.is_moving = False
        self.start_time = 0

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=800, height=300)
        self.canvas.pack(side="top")

        # Draw the road
        self.canvas.create_rectangle(0, 100, 800, 200, fill="gray")
        # Draw the lanes
        for i in range(10, 800, 30):
            self.canvas.create_line(i, 145, i+20, 145, fill="white")

        self.start_button = tk.Button(self, text="Start", command=self.start_car)
        self.start_button.pack(side="left")

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_car)
        self.stop_button.pack(side="left")

        self.log_label = tk.Label(self, text="Detection Log:")
        self.log_label.pack(side="top")

        self.log_text = tk.Text(self, height=10, width=70)
        self.log_text.pack(side="bottom")

        # Car shape
        self.car = self.canvas.create_rectangle(50, 130, 100, 170, fill="blue")

    def create_objects(self):
        object_width = 20
        for _ in range(5):
            x0 = randint(150, 750)
            y0 = 130
            x1 = x0 + object_width
            y1 = 170
            self.objects.append({
                'id': self.canvas.create_rectangle(x0, y0, x1, y1, fill="red"),
                'detected': False,
                'detect_time': None
            })

    def start_car(self):
        if not self.is_moving:
            self.is_moving = True
            self.start_time = time.time()
            self.move_car()

    def stop_car(self):
        self.is_moving = False

    def move_car(self):
        if self.is_moving:
            self.car_position += 2
            self.canvas.move(self.car, 2, 0)
            self.detect_objects()
            if self.car_position > 700:
                self.stop_car()
            else:
                self.master.after(50, self.move_car)

    def detect_objects(self):
        car_coords = self.canvas.coords(self.car)
        for obj in self.objects:
            if not obj['detected']:
                object_coords = self.canvas.coords(obj['id'])
                if car_coords[2] >= object_coords[0]:  # Car's right edge crosses object's left edge
                    current_time = time.time()
                    obj['detected'] = True
                    obj['detect_time'] = current_time - self.start_time
                    self.log_detection(obj['id'], obj['detect_time'])

    def log_detection(self, object_id, detect_time):
        self.log_text.insert(
            "end",
            f"Object {object_id} detected at {detect_time:.2f}s. "
            f"Detection delay: {detect_time:.2f}s\n"
        )

root = tk.Tk()
root.title("Car Object Detection Simulation")
app = CarSimulation(master=root)
app.mainloop()

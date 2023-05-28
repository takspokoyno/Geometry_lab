import tkinter as tk
import math
import random
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def generate_random_points(amount):
    min_value = 0
    max_value = 99
    points = []
    for _ in range(amount):
        x = random.uniform(min_value, max_value)
        y = random.uniform(min_value, max_value)
        points.append((x, y))
    return points    

def save_points_to_csv(points, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['X', 'Y'])  # Write header
        writer.writerows(points)  # Write points

#Calculate the orientation of three points (p, q, r)
def orientation(p, q, r):
    value = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if value == 0:
        return 0    # Collinear
    elif value > 0:
        return 1    # Clockwise
    else:
        return 2    # Counterclockwise

def graham_scan(points):
    if len(points) < 3:
        return []

    points = list(set(points))
    n = len(points)

    # Find the point with the lowest y-coordinate
    min_y = min(points, key=lambda point: point[1])
    pivot_index = points.index(min_y)

    # Swap pivot with the first point
    points[0], points[pivot_index] = points[pivot_index], points[0]

    # Sort points based on polar angle
    points[1:] = sorted(points[1:], key=lambda point: (
        math.atan2(point[1] - min_y[1], point[0] - min_y[0]),
        math.dist(point, min_y)
    ))

    stack = [points[0], points[1], points[2]]  # Initialize stack with first three points

    for i in range(3, n):
        while len(stack) > 1 and orientation(stack[-2], stack[-1], points[i]) != 2:
            stack.pop()

        stack.append(points[i])

    return stack 

def create_simple_plot():
    # Read points from the given_points.csv file
    x_coords = []
    y_coords = []
    with open("given_points.csv", mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            x = row[0]
            y = row[1]
            x_coords.append(float(x.strip()))  # Extract and append the x coordinate
            y_coords.append(float(y.strip()))  # Extract and append the y coordinate

    # Read points from the convex_hull.csv file
    hull_x_coords = []
    hull_y_coords = []
    with open("convex_hull.csv", mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            x = row[0]
            y = row[1]
            hull_x_coords.append(float(x.strip()))  # Extract and append the x coordinate
            hull_y_coords.append(float(y.strip()))  # Extract and append the y coordinate

    # Append the first point to the end to close the polygon
    hull_x_coords.append(hull_x_coords[0])
    hull_y_coords.append(hull_y_coords[0])

    # Create a new window
    plot_window = tk.Toplevel()
    plot_window.title("Scatter Plot with Convex Hull")

    # Create a Figure and an axis
    fig = Figure(figsize=(6, 6))
    ax = fig.add_subplot(111)

    # Create a scatter plot of the given points on the axis
    ax.scatter(x_coords, y_coords, label='Given Points')

    # Create a line plot of the convex hull points on the axis
    ax.plot(hull_x_coords, hull_y_coords, 'r-', label='Convex Hull')

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Scatter Plot')
    ax.legend()

    # Create a FigureCanvasTkAgg object to display the plot in the window
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()

    # Pack the canvas into the window
    canvas.get_tk_widget().pack()

    # Display the window
    plot_window.mainloop()


def button_auto_click():
    input_text = entry.get()
    if not input_text.isdigit() or int(input_text)>10000:
        result_label.config(text="Invalid input! Please enter a valid number")
        return
    n = int(input_text)  # Get the number of points from the entry field
    points = generate_random_points(n)
    save_points_to_csv(points, "given_points.csv")
    convex_hull = graham_scan(points)
    save_points_to_csv(convex_hull, "convex_hull.csv")
    result_label.config(text="Success!")
    create_simple_plot()
    

def button_confirm_click():
    input_text = text_area.get("1.0", tk.END).strip()

    # Parse the input text as CSV
    points = []
    try:
        lines = input_text.split("\n")
        for line in lines:
            x, y = map(float, line.split(","))
            points.append((x, y))
    except ValueError:
        result_label.config(text="Invalid input format! Please enter points in CSV format.")
        return

    save_points_to_csv(points, "given_points.csv")
    convex_hull = graham_scan(points)
    save_points_to_csv(convex_hull, "convex_hull.csv")
    result_label.config(text="Convex hull created and saved to 'convex_hull.csv'.")
    create_simple_plot()

def button_manual_click():
    text_area.config(state=tk.NORMAL)

def button_clear_click():
    text_area.delete('1.0', tk.END)    

window = tk.Tk()
window.title("Convex Hull")
window.geometry("380x350")
window.resizable(False, False) 

label = tk.Label(window, text="Enter number of points:", width=20)
label.grid(row=0, column=0)

entry = tk.Entry(window, width=20)
entry.grid(row=0, column=1)

button_frame = tk.Frame(window)
button_frame.grid(row=1, column=0, columnspan=2)

button_auto = tk.Button(button_frame, text="Automatic mode", command=button_auto_click, width=20)
button_auto.pack(side=tk.LEFT)

button_manual = tk.Button(button_frame, text="Manual Input", command=button_manual_click, width=20)
button_manual.pack(side=tk.LEFT)

text_area = tk.Text(window, height=10, width=40)
text_area.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
text_area.config(state=tk.DISABLED)

button_frame2 = tk.Frame(window)
button_frame2.grid(row=3, column=0, columnspan=2)

button3 = tk.Button(button_frame2, text="Confirm", command=button_confirm_click, width=20)
button3.pack(side=tk.LEFT)

button_clear = tk.Button(button_frame2, text="Clear", command=button_clear_click, width=20)
button_clear.pack(side=tk.LEFT)

result_label = tk.Label(window, text="")
result_label.grid(row=4, column=0, columnspan=2)

window.mainloop()
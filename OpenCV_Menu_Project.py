import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
def detect_objects(image_path):
    # Read the image
    img = cv2.imread(image_path)
    # Convert the image to HSV format
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color ranges for each object
    color_ranges = {
        'red':    ((160, 50, 50), (180, 255, 255)),
        'green':  ((40, 40, 40), (80, 255, 255)),
        'blue':   ((100, 100, 100), (140, 255, 255)),
        'yellow': ((20, 100, 100), (40, 255, 255)),
    }

    # Define food and drink items for each shape and color combination
    menu_items = {
        'red_square': 'Cola',
        'red_round': 'Water',
        'red_triangle': 'Wine',
        'red_star': 'Beer',
        'green_square': 'Tomato Soup',
        'green_round': 'French Onion Soup',
        'green_triangle': 'Vegetable Soup',
        'green_star': 'Broccoli Soup',
        'blue_square': 'Spaghetti',
        'blue_round': 'Chicken Fajitas',
        'blue_triangle': 'Tricolore Skillet Lasagna',
        'blue_star': 'Pistachio Crusted Rack of Lamb',
        'yellow_square': 'Banana Pudding Pops',
        'yellow_round': 'Cheesecake',
        'yellow_triangle': 'Crème Brûlée',
        'yellow_star': 'Bakewell Tart',
    }

    # Define prices for each item
    item_prices = {
        'Cola': 20.50,
        'Water': 10.50,
        'Wine': 80.00,
        'Beer': 60.00,
        'Tomato Soup': 40.00,
        'French Onion Soup': 45.50,
        'Vegetable Soup': 50.00,
        'Broccoli Soup': 55.50,
        'Spaghetti': 100.00,
        'Chicken Fajitas': 120.00,
        'Tricolore Skillet Lasagna': 150.00,
        'Pistachio Crusted Rack of Lamb': 180.00,
        'Banana Pudding Pops': 60.00,
        'Cheesecake': 70.00,
        'Crème Brûlée': 80.00,
        'Bakewell Tart': 90.00,
    }

    # Define a kernel for morphological operations
    kernel = np.ones((5, 5), np.uint8)

    detected_shapes = set()

    for color, (lower, upper) in color_ranges.items():
        # Create a mask for the specified color
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

        # Apply morphological operations to remove noise
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Process each contour
        for contour in contours:
            # Approximate the shape of the contour
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Get the number of vertices (corners)
            vertices = len(approx)

            # Determine the shape of the object based on the number of vertices
            if vertices == 3:
                shape = "triangle"
            elif vertices == 4:
                shape = "square"
            elif vertices == 10:
                shape = "star"
            else:
                shape = "round"

            # Combine color and shape to create a unique identifier
            identifier = f'{color}_{shape}'

            # Add the detected shape to the set
            detected_shapes.add(identifier)

    # If four different shapes are detected, create a menu
    if len(detected_shapes) == 4:
        menu = [menu_items[shape] for shape in detected_shapes]
        total_price = sum(item_prices[item] for item in menu)

        # Print menu and total price
        print("Menu:", menu)
        print(f"Total Price: {total_price}TL")

        # Return menu and total price
        return menu, total_price
    else:
        print("Not enough items to crate menu")
    return None, None

def display_receipt(menu, total_price, window):
    item_prices = {
        'Cola': 20.50,
        'Water': 10.50,
        'Wine': 80.00,
        'Beer': 60.00,
        'Tomato Soup': 40.00,
        'French Onion Soup': 45.50,
        'Vegetable Soup': 50.00,
        'Broccoli Soup': 55.50,
        'Spaghetti': 100.00,
        'Chicken Fajitas': 120.00,
        'Tricolore Skillet Lasagna': 150.00,
        'Pistachio Crusted Rack of Lamb': 180.00,
        'Banana Pudding Pops': 60.00,
        'Cheesecake': 70.00,
        'Crème Brûlée': 80.00,
        'Bakewell Tart': 90.00,
    }
    # Display the receipt without the original image
    receipt_text = "Receipt\n"
    for item in menu:
        receipt_text += f"{item}: {item_prices[item]:.2f}TL\n"
    receipt_text += f"Total Price: {total_price:.2f}TL"

    receipt_label.config(text=receipt_text)

# Function to handle the "Confirm" button click
def choose_button_click():
    # Open a file dialog to choose an image
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])

    # If a file is selected, process the image
    if file_path:
        # Detect objects and create a menu
        menu, total_price = detect_objects(file_path)

        # If a menu is created, display the receipt on the GUI window
        if menu is not None:
            display_receipt(menu, total_price, root)
        else:
            messagebox.showerror("Error", "Not enough items to create menu")

# Create the main Tkinter window
root = tk.Tk()
root.title("Menu and Receipt")

# Create a frame to hold the image
image_frame = tk.Frame(root)
image_frame.pack()

# Create a label to display the image
image_label = tk.Label(image_frame)
image_label.pack()

# Create a "Confirm" button
confirm_button = tk.Button(root, text="Choose Menu", command=choose_button_click)
confirm_button.pack()

# Create a label to display the receipt
receipt_label = tk.Label(root, text="")
receipt_label.pack()

# Run the Tkinter event loop
root.mainloop()
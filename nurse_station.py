import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Control Panel")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window to a fraction of the screen size
window_size = f"{int(screen_width * 1)}x{int(screen_height * 1)}"
root.geometry(window_size)

# Calculate button width and height as a fraction of the screen size
button_width = int(screen_width * 0.125)
button_height = int(screen_height * 0.125)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)


# Function to simulate button press
def button_press(number):
    print(f"Button {number} pressed")


buttons = {}
for i in range(1, 51):
    row = (i - 1) // 10
    column = (i - 1) % 10
    if i == 33 or i == 20 or i == 15 or i == 11:
        buttons[i] = tk.Button(button_frame, text=str(i), command=lambda i=i: button_press(i), bg="red")
    elif i == 35 or i == 27 or i == 38 or i == 50 or i == 41:
        buttons[i] = tk.Button(button_frame, text=str(i), command=lambda i=i: button_press(i), bg="green")
    elif i == 2 or i == 24 or i == 8 or i == 47:
        buttons[i] = tk.Button(button_frame, text=str(i), command=lambda i=i: button_press(i), bg="blue")
    else:
        buttons[i] = tk.Button(button_frame, text=str(i), command=lambda i=i: button_press(i))
    buttons[i].grid(row=row, column=column, padx=5, pady=5)
    # Adjust button size
    buttons[i].config(height=button_height//20, width=button_width//10)

buttons[23] = tk.Button(bg="red")
# Create indicator lights
indicator_frame = tk.Frame(root)
indicator_frame.pack(pady=5)

# Run the main loop
root.mainloop()

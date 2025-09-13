#!/usr/bin/env python3
"""
RGB Color Explorer

A GUI application that allows users to explore colors using RGB sliders.
Features red, green, and blue sliders that control a large color display square.
"""

import tkinter as tk
from tkinter import ttk
import sys


class RGBColorExplorer:
    """Main application class for the RGB Color Explorer."""
    
    def __init__(self, root):
        """Initialize the RGB Color Explorer application."""
        self.root = root
        self.root.title("RGB Color Explorer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure the main window
        self.root.configure(bg='#f0f0f0')
        
        # RGB values (0-255)
        self.red_var = tk.IntVar(value=128)
        self.green_var = tk.IntVar(value=128)
        self.blue_var = tk.IntVar(value=128)
        
        # Set up the GUI
        self.create_widgets()
        self.update_color()
        
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="RGB Color Explorer", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Color display square
        self.color_frame = tk.Frame(main_frame, width=300, height=200, 
                                   relief='solid', borderwidth=2)
        self.color_frame.grid(row=1, column=0, columnspan=2, pady=(0, 30), 
                             padx=20, sticky='ew')
        self.color_frame.grid_propagate(False)  # Maintain fixed size
        
        # Color value display
        self.color_value_label = ttk.Label(main_frame, 
                                          font=('Courier', 12, 'bold'))
        self.color_value_label.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        # Red slider
        red_frame = ttk.LabelFrame(main_frame, text="Red", padding="10")
        red_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=5)
        red_frame.columnconfigure(1, weight=1)
        
        ttk.Label(red_frame, text="0").grid(row=0, column=0, padx=(0, 5))
        self.red_scale = ttk.Scale(red_frame, from_=0, to=255, 
                                  variable=self.red_var, orient='horizontal',
                                  command=self.on_scale_change)
        self.red_scale.grid(row=0, column=1, sticky='ew', padx=5)
        ttk.Label(red_frame, text="255").grid(row=0, column=2, padx=(5, 0))
        
        self.red_value_label = ttk.Label(red_frame, text="128", 
                                        font=('Arial', 10, 'bold'))
        self.red_value_label.grid(row=0, column=3, padx=(10, 0))
        
        # Green slider
        green_frame = ttk.LabelFrame(main_frame, text="Green", padding="10")
        green_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=5)
        green_frame.columnconfigure(1, weight=1)
        
        ttk.Label(green_frame, text="0").grid(row=0, column=0, padx=(0, 5))
        self.green_scale = ttk.Scale(green_frame, from_=0, to=255, 
                                    variable=self.green_var, orient='horizontal',
                                    command=self.on_scale_change)
        self.green_scale.grid(row=0, column=1, sticky='ew', padx=5)
        ttk.Label(green_frame, text="255").grid(row=0, column=2, padx=(5, 0))
        
        self.green_value_label = ttk.Label(green_frame, text="128", 
                                          font=('Arial', 10, 'bold'))
        self.green_value_label.grid(row=0, column=3, padx=(10, 0))
        
        # Blue slider
        blue_frame = ttk.LabelFrame(main_frame, text="Blue", padding="10")
        blue_frame.grid(row=5, column=0, columnspan=2, sticky='ew', pady=5)
        blue_frame.columnconfigure(1, weight=1)
        
        ttk.Label(blue_frame, text="0").grid(row=0, column=0, padx=(0, 5))
        self.blue_scale = ttk.Scale(blue_frame, from_=0, to=255, 
                                   variable=self.blue_var, orient='horizontal',
                                   command=self.on_scale_change)
        self.blue_scale.grid(row=0, column=1, sticky='ew', padx=5)
        ttk.Label(blue_frame, text="255").grid(row=0, column=2, padx=(5, 0))
        
        self.blue_value_label = ttk.Label(blue_frame, text="128", 
                                         font=('Arial', 10, 'bold'))
        self.blue_value_label.grid(row=0, column=3, padx=(10, 0))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Reset to Gray", 
                  command=self.reset_to_gray).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Random Color", 
                  command=self.random_color).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Copy RGB", 
                  command=self.copy_rgb).grid(row=0, column=2, padx=5)
        
    def on_scale_change(self, event=None):
        """Handle slider value changes."""
        self.update_color()
        
    def update_color(self):
        """Update the color display and value labels."""
        # Get current RGB values
        r = int(self.red_var.get())
        g = int(self.green_var.get())
        b = int(self.blue_var.get())
        
        # Update value labels
        self.red_value_label.config(text=str(r))
        self.green_value_label.config(text=str(g))
        self.blue_value_label.config(text=str(b))
        
        # Create hex color string
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Update color display
        self.color_frame.config(bg=hex_color)
        
        # Update color value label
        rgb_text = f"RGB({r}, {g}, {b})"
        hex_text = f"HEX: {hex_color.upper()}"
        self.color_value_label.config(text=f"{rgb_text} | {hex_text}")
        
    def reset_to_gray(self):
        """Reset all sliders to middle gray (128, 128, 128)."""
        self.red_var.set(128)
        self.green_var.set(128)
        self.blue_var.set(128)
        self.update_color()
        
    def random_color(self):
        """Set sliders to a random color."""
        import random
        self.red_var.set(random.randint(0, 255))
        self.green_var.set(random.randint(0, 255))
        self.blue_var.set(random.randint(0, 255))
        self.update_color()
        
    def copy_rgb(self):
        """Copy the current RGB values to clipboard."""
        r = int(self.red_var.get())
        g = int(self.green_var.get())
        b = int(self.blue_var.get())
        rgb_string = f"rgb({r}, {g}, {b})"
        
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(rgb_string)
            # Show temporary feedback
            original_text = self.color_value_label.cget('text')
            self.color_value_label.config(text="RGB values copied to clipboard!")
            self.root.after(2000, lambda: self.color_value_label.config(text=original_text))
        except Exception as e:
            print(f"Could not copy to clipboard: {e}")


def main():
    """Main function to run the RGB Color Explorer application."""
    try:
        # Create the main window
        root = tk.Tk()
        
        # Create and run the application
        app = RGBColorExplorer(root)
        
        # Start the GUI event loop
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

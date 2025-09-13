#!/usr/bin/env python3
"""
RGB Color Explorer Mini

A compact GUI application that allows users to explore colors using RGB sliders.
Features red, green, and blue sliders that control a color display in a small window.
Optimized for 465x442 pixel window size.
"""

import tkinter as tk
from tkinter import ttk
import sys


class RGBColorExplorerMini:
    """Main application class for the RGB Color Explorer Mini."""
    
    # Common color names and their RGB values (reduced set for compact display)
    COMMON_COLORS = {
        "Custom Color": None,  # Default selection - no auto-change
        "Black": (0, 0, 0),
        "White": (255, 255, 255),
        "Red": (255, 0, 0),
        "Green": (0, 128, 0),
        "Blue": (0, 0, 255),
        "Yellow": (255, 255, 0),
        "Cyan": (0, 255, 255),
        "Magenta": (255, 0, 255),
        "Orange": (255, 165, 0),
        "Pink": (255, 192, 203),
        "Purple": (128, 0, 128),
    }
    
    def __init__(self, root):
        """Initialize the RGB Color Explorer Mini application."""
        self.root = root
        self.root.title("RGB Color Explorer Mini")
        
        # Configure window close behavior for proper cleanup
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set compact window size
        self.root.geometry("465x442")
        self.root.minsize(465, 442)  # Fixed size for mini version
        self.root.resizable(False, False)  # Fixed size window
        
        # Center the window on screen
        self.center_window()
        
        # Configure the main window
        self.root.configure(bg='#f0f0f0')
        
        # RGB values (0-255)
        self.red_var = tk.IntVar(value=128)
        self.green_var = tk.IntVar(value=128)
        self.blue_var = tk.IntVar(value=128)
        
        # Animation control variables
        self.animate_red = tk.BooleanVar(value=False)
        self.animate_green = tk.BooleanVar(value=False)
        self.animate_blue = tk.BooleanVar(value=False)
        self.animation_active = False
        self.animation_direction = {"red": 1, "green": 1, "blue": 1}  # 1 for increasing, -1 for decreasing
        self.animation_speed = 2  # pixels per update (adjustable)
        self.animation_timer = None
        
        # Set up the GUI
        self.create_widgets()
        self.update_color()
        
    def get_dropdown_values(self):
        """Generate dropdown values with color names and hex codes."""
        dropdown_values = []
        for color_name, rgb_values in self.COMMON_COLORS.items():
            if rgb_values is None:
                # Custom Color entry
                dropdown_values.append(color_name)
            else:
                r, g, b = rgb_values
                hex_code = f"#{r:02X}{g:02X}{b:02X}"
                dropdown_values.append(f"{color_name} ({hex_code})")
        return dropdown_values
        
    def extract_color_name(self, dropdown_text):
        """Extract the color name from dropdown text that includes hex code."""
        if '(' in dropdown_text:
            return dropdown_text.split(' (')[0]
        return dropdown_text
        
    def create_widgets(self):
        """Create and arrange all GUI widgets in compact layout."""
        # Main frame with minimal padding for compact layout
        main_frame = ttk.Frame(self.root, padding="8")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title (smaller font)
        title_label = ttk.Label(main_frame, text="RGB Color Explorer Mini", 
                               font=('Arial', 12, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 8))
        
        # Color selection dropdown (compact)
        color_selection_frame = ttk.Frame(main_frame)
        color_selection_frame.grid(row=1, column=0, columnspan=2, pady=(0, 8))
        
        ttk.Label(color_selection_frame, text="Colors:", 
                 font=('Arial', 9, 'bold')).grid(row=0, column=0, padx=(0, 5))
        
        self.color_combobox = ttk.Combobox(color_selection_frame, 
                                          values=self.get_dropdown_values(),
                                          state="readonly", width=18, font=('Arial', 8))
        self.color_combobox.grid(row=0, column=1)
        self.color_combobox.set("Custom Color")  # Default selection
        self.color_combobox.bind('<<ComboboxSelected>>', self.on_color_selected)
        
        # Color display area (maximum width for better pixel viewing)
        self.color_frame = tk.Frame(main_frame, width=420, height=60, 
                                   relief='solid', borderwidth=2)
        self.color_frame.grid(row=2, column=0, columnspan=2, pady=(0, 8), 
                             padx=(5, 5))
        self.color_frame.grid_propagate(False)  # Maintain fixed size
        
        # Color value display (smaller font)
        self.color_value_label = ttk.Label(main_frame, 
                                          font=('Courier', 8, 'bold'))
        self.color_value_label.grid(row=3, column=0, columnspan=2, pady=(0, 8))
        
        # Red slider (compact)
        red_frame = ttk.LabelFrame(main_frame, text="Red", padding="4")
        red_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=2)
        red_frame.columnconfigure(1, weight=1)
        
        ttk.Label(red_frame, text="0", font=('Arial', 8)).grid(row=0, column=0, padx=(0, 3))
        self.red_scale = ttk.Scale(red_frame, from_=0, to=255, 
                                  variable=self.red_var, orient='horizontal',
                                  command=self.on_scale_change, length=200)
        self.red_scale.grid(row=0, column=1, sticky='ew', padx=3)
        ttk.Label(red_frame, text="255", font=('Arial', 8)).grid(row=0, column=2, padx=(3, 0))
        
        self.red_value_label = ttk.Label(red_frame, text="0x80", 
                                        font=('Arial', 8, 'bold'))
        self.red_value_label.grid(row=0, column=3, padx=(5, 0))
        
        # Green slider (compact)
        green_frame = ttk.LabelFrame(main_frame, text="Green", padding="4")
        green_frame.grid(row=5, column=0, columnspan=2, sticky='ew', pady=2)
        green_frame.columnconfigure(1, weight=1)
        
        ttk.Label(green_frame, text="0", font=('Arial', 8)).grid(row=0, column=0, padx=(0, 3))
        self.green_scale = ttk.Scale(green_frame, from_=0, to=255, 
                                    variable=self.green_var, orient='horizontal',
                                    command=self.on_scale_change, length=200)
        self.green_scale.grid(row=0, column=1, sticky='ew', padx=3)
        ttk.Label(green_frame, text="255", font=('Arial', 8)).grid(row=0, column=2, padx=(3, 0))
        
        self.green_value_label = ttk.Label(green_frame, text="0x80", 
                                          font=('Arial', 8, 'bold'))
        self.green_value_label.grid(row=0, column=3, padx=(5, 0))
        
        # Blue slider (compact)
        blue_frame = ttk.LabelFrame(main_frame, text="Blue", padding="4")
        blue_frame.grid(row=6, column=0, columnspan=2, sticky='ew', pady=2)
        blue_frame.columnconfigure(1, weight=1)
        
        ttk.Label(blue_frame, text="0", font=('Arial', 8)).grid(row=0, column=0, padx=(0, 3))
        self.blue_scale = ttk.Scale(blue_frame, from_=0, to=255, 
                                   variable=self.blue_var, orient='horizontal',
                                   command=self.on_scale_change, length=200)
        self.blue_scale.grid(row=0, column=1, sticky='ew', padx=3)
        ttk.Label(blue_frame, text="255", font=('Arial', 8)).grid(row=0, column=2, padx=(3, 0))
        
        self.blue_value_label = ttk.Label(blue_frame, text="0x80", 
                                         font=('Arial', 8, 'bold'))
        self.blue_value_label.grid(row=0, column=3, padx=(5, 0))
        
        # Control buttons (compact)
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=8)
        
        ttk.Button(button_frame, text="Reset", 
                  command=self.reset_to_gray).grid(row=0, column=0, padx=2)
        ttk.Button(button_frame, text="Random", 
                  command=self.random_color).grid(row=0, column=1, padx=2)
        ttk.Button(button_frame, text="Copy", 
                  command=self.copy_rgb).grid(row=0, column=2, padx=2)
        
        # Animation Controls (compact)
        animation_frame = ttk.LabelFrame(main_frame, text="Animation", padding="4")
        animation_frame.grid(row=8, column=0, columnspan=2, sticky='ew', pady=(8, 0))
        
        # Checkboxes for independent channel animation (smaller)
        checkbox_frame = ttk.Frame(animation_frame)
        checkbox_frame.grid(row=0, column=0, columnspan=2, sticky='ew')
        
        ttk.Checkbutton(checkbox_frame, text="R", variable=self.animate_red, 
                       command=self.on_animation_change).grid(row=0, column=0, padx=5)
        ttk.Checkbutton(checkbox_frame, text="G", variable=self.animate_green, 
                       command=self.on_animation_change).grid(row=0, column=1, padx=5)
        ttk.Checkbutton(checkbox_frame, text="B", variable=self.animate_blue, 
                       command=self.on_animation_change).grid(row=0, column=2, padx=5)
        
        # Control buttons (compact)
        ttk.Button(checkbox_frame, text="Start All", 
                  command=self.start_all_animation).grid(row=0, column=3, padx=(10, 5))
        ttk.Button(checkbox_frame, text="Stop All", 
                  command=self.stop_all_animation).grid(row=0, column=4, padx=5)
        
        # Animation speed control (compact)
        speed_frame = ttk.Frame(animation_frame)
        speed_frame.grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky='ew')
        
        ttk.Label(speed_frame, text="Speed:", font=('Arial', 8)).grid(row=0, column=0, padx=(0, 3))
        self.speed_scale = ttk.Scale(speed_frame, from_=1, to=10, orient='horizontal', 
                                    length=100, command=self.on_speed_change)
        self.speed_scale.set(3)  # Default speed
        self.speed_scale.grid(row=0, column=1, padx=3)
        ttk.Label(speed_frame, text="Slow", font=('Arial', 7)).grid(row=0, column=2, padx=(3, 0))
        ttk.Label(speed_frame, text="Fast", font=('Arial', 7)).grid(row=0, column=3, padx=(8, 0))
        
    def on_scale_change(self, event=None):
        """Handle slider value changes."""
        self.update_color()
        self.update_combobox_selection()  # Set to "Custom Color" when manually adjusted
    
    def on_animation_change(self):
        """Handle animation checkbox changes."""
        # Check if any channels are set to animate
        any_active = self.animate_red.get() or self.animate_green.get() or self.animate_blue.get()
        
        if any_active and not self.animation_active:
            self.start_animation()
        elif not any_active and self.animation_active:
            self.stop_animation()
    
    def start_all_animation(self):
        """Start all channel animations."""
        self.animate_red.set(True)
        self.animate_green.set(True)
        self.animate_blue.set(True)
        if not self.animation_active:
            self.start_animation()
    
    def stop_all_animation(self):
        """Stop all channel animations."""
        self.animate_red.set(False)
        self.animate_green.set(False)
        self.animate_blue.set(False)
        self.stop_animation()
    
    def on_speed_change(self, value):
        """Handle animation speed changes."""
        pass  # Speed is handled by the animation timer
    
    def start_animation(self):
        """Start the color animation for enabled channels."""
        self.animation_active = True
        self.animate_color()
    
    def stop_animation(self):
        """Stop the color animation."""
        self.animation_active = False
        if hasattr(self, 'animation_job'):
            self.root.after_cancel(self.animation_job)
    
    def animate_color(self):
        """Main animation loop that updates color values for active channels."""
        if not self.animation_active:
            return
        
        speed = int(self.speed_scale.get())
        step_size = speed  # 1-10 based on speed scale
        
        # Animate Red channel if enabled
        if self.animate_red.get():
            current_val = int(self.red_var.get())
            direction = self.animation_direction["red"]
            next_val = current_val + (step_size * direction)
            
            if next_val >= 255:
                next_val = 255
                self.animation_direction["red"] = -1
            elif next_val <= 0:
                next_val = 0
                self.animation_direction["red"] = 1
            
            self.red_var.set(next_val)
        
        # Animate Green channel if enabled
        if self.animate_green.get():
            current_val = int(self.green_var.get())
            direction = self.animation_direction["green"]
            next_val = current_val + (step_size * direction)
            
            if next_val >= 255:
                next_val = 255
                self.animation_direction["green"] = -1
            elif next_val <= 0:
                next_val = 0
                self.animation_direction["green"] = 1
            
            self.green_var.set(next_val)
        
        # Animate Blue channel if enabled
        if self.animate_blue.get():
            current_val = int(self.blue_var.get())
            direction = self.animation_direction["blue"]
            next_val = current_val + (step_size * direction)
            
            if next_val >= 255:
                next_val = 255
                self.animation_direction["blue"] = -1
            elif next_val <= 0:
                next_val = 0
                self.animation_direction["blue"] = 1
            
            self.blue_var.set(next_val)
        
        # Update the display
        self.update_color()
        
        # Calculate delay based on speed
        delay = max(20, 200 - (speed * 15))  # 20ms to 185ms delay
        
        # Schedule next animation frame
        self.animation_job = self.root.after(delay, self.animate_color)
    
    def on_closing(self):
        """Handle application closing with proper cleanup."""
        self.stop_animation()
        self.root.destroy()
        
    def update_color(self):
        """Update the color display and value labels."""
        # Get current RGB values
        r = int(self.red_var.get())
        g = int(self.green_var.get())
        b = int(self.blue_var.get())
        
        # Update value labels to show hex values with 0x prefix
        self.red_value_label.config(text=f"0x{r:02X}")
        self.green_value_label.config(text=f"0x{g:02X}")
        self.blue_value_label.config(text=f"0x{b:02X}")
        
        # Create hex color string
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Update color display
        self.color_frame.config(bg=hex_color)
        
        # Update color value label (shorter format for compact display)
        self.color_value_label.config(text=f"RGB({r},{g},{b}) | {hex_color.upper()}")
        
    def on_color_selected(self, event=None):
        """Handle color selection from dropdown."""
        selected_text = self.color_combobox.get()
        selected_color = self.extract_color_name(selected_text)
        
        if selected_color == "Custom Color" or selected_color not in self.COMMON_COLORS:
            return
            
        rgb_values = self.COMMON_COLORS[selected_color]
        if rgb_values is not None:
            r, g, b = rgb_values
            self.red_var.set(r)
            self.green_var.set(g)
            self.blue_var.set(b)
            self.update_color()
            
    def update_combobox_selection(self):
        """Update combobox to show 'Custom Color' when user manually adjusts sliders."""
        current_selection = self.extract_color_name(self.color_combobox.get())
        if current_selection != "Custom Color":
            self.color_combobox.set("Custom Color")
        
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
            self.color_value_label.config(text="Copied!")
            self.root.after(1500, lambda: self.color_value_label.config(text=original_text))
        except Exception as e:
            print(f"Could not copy to clipboard: {e}")
            
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Get window dimensions
        window_width = 465
        window_height = 442
        
        # Calculate center position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")


def main():
    """Main function to run the RGB Color Explorer Mini application."""
    try:
        # Create the main window
        root = tk.Tk()
        
        # Create and run the application
        app = RGBColorExplorerMini(root)
        
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
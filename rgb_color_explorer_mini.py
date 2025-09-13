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
    
    # Common color names and their RGB values (full set restored)
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
        "Silver": (192, 192, 192),
        "Gray": (128, 128, 128),
        "Maroon": (128, 0, 0),
        "Olive": (128, 128, 0),
        "Lime": (0, 255, 0),
        "Aqua": (0, 255, 255),
        "Teal": (0, 128, 128),
        "Navy": (0, 0, 128),
        "Fuchsia": (255, 0, 255),
        "Purple": (128, 0, 128),
        "Orange": (255, 165, 0),
        "Pink": (255, 192, 203),
        "Brown": (165, 42, 42),
        "Coral": (255, 127, 80),
        "Crimson": (220, 20, 60),
        "Gold": (255, 215, 0),
        "Indigo": (75, 0, 130),
        "Ivory": (255, 255, 240),
        "Khaki": (240, 230, 140),
        "Lavender": (230, 230, 250),
        "Lemon": (255, 250, 205),
        "Mint": (245, 255, 250),
        "Peach": (255, 218, 185),
        "Plum": (221, 160, 221),
        "Salmon": (250, 128, 114),
        "Tan": (210, 180, 140),
        "Turquoise": (64, 224, 208),
        "Violet": (238, 130, 238),
        "Wheat": (245, 222, 179),
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
                                          state="readonly", width=28, font=('Arial', 8))
        self.color_combobox.grid(row=0, column=1)
        self.color_combobox.set("Custom Color")  # Default selection
        self.color_combobox.bind('<<ComboboxSelected>>', self.on_color_selected)
        
        # Add keyboard navigation for real-time color changes
        self.color_combobox.bind('<KeyPress>', self.on_combobox_keypress)
        self.color_combobox.bind('<Up>', self.on_combobox_navigate)
        self.color_combobox.bind('<Down>', self.on_combobox_navigate)
        self.color_combobox.bind('<Return>', self.on_color_selected)
        
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
        
        # Red slider (compact with text entry)
        red_frame = ttk.LabelFrame(main_frame, text="Red", padding="4")
        red_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=2)
        red_frame.columnconfigure(1, weight=1)
        
        ttk.Label(red_frame, text="0", font=('Arial', 8)).grid(row=0, column=0, padx=(0, 3))
        self.red_scale = ttk.Scale(red_frame, from_=0, to=255, 
                                  variable=self.red_var, orient='horizontal',
                                  command=self.on_scale_change, length=150)
        self.red_scale.grid(row=0, column=1, sticky='ew', padx=3)
        ttk.Label(red_frame, text="255", font=('Arial', 8)).grid(row=0, column=2, padx=(3, 0))
        
        self.red_value_label = ttk.Label(red_frame, text="0x80", 
                                        font=('Arial', 8, 'bold'))
        self.red_value_label.grid(row=0, column=3, padx=(5, 0))
        
        # Red value entry box
        self.red_entry = ttk.Entry(red_frame, width=6, font=('Courier', 8))
        self.red_entry.grid(row=0, column=4, padx=(3, 0))
        self.red_entry.insert(0, "128")
        self.red_entry.bind('<Return>', lambda e: self.on_entry_change('red'))
        self.red_entry.bind('<FocusOut>', lambda e: self.on_entry_change('red'))
        
        # Green slider (compact with text entry)
        green_frame = ttk.LabelFrame(main_frame, text="Green", padding="4")
        green_frame.grid(row=5, column=0, columnspan=2, sticky='ew', pady=2)
        green_frame.columnconfigure(1, weight=1)
        
        ttk.Label(green_frame, text="0", font=('Arial', 8)).grid(row=0, column=0, padx=(0, 3))
        self.green_scale = ttk.Scale(green_frame, from_=0, to=255, 
                                    variable=self.green_var, orient='horizontal',
                                    command=self.on_scale_change, length=150)
        self.green_scale.grid(row=0, column=1, sticky='ew', padx=3)
        ttk.Label(green_frame, text="255", font=('Arial', 8)).grid(row=0, column=2, padx=(3, 0))
        
        self.green_value_label = ttk.Label(green_frame, text="0x80", 
                                          font=('Arial', 8, 'bold'))
        self.green_value_label.grid(row=0, column=3, padx=(5, 0))
        
        # Green value entry box
        self.green_entry = ttk.Entry(green_frame, width=6, font=('Courier', 8))
        self.green_entry.grid(row=0, column=4, padx=(3, 0))
        self.green_entry.insert(0, "128")
        self.green_entry.bind('<Return>', lambda e: self.on_entry_change('green'))
        self.green_entry.bind('<FocusOut>', lambda e: self.on_entry_change('green'))
        
        # Blue slider (compact with text entry)
        blue_frame = ttk.LabelFrame(main_frame, text="Blue", padding="4")
        blue_frame.grid(row=6, column=0, columnspan=2, sticky='ew', pady=2)
        blue_frame.columnconfigure(1, weight=1)
        
        ttk.Label(blue_frame, text="0", font=('Arial', 8)).grid(row=0, column=0, padx=(0, 3))
        self.blue_scale = ttk.Scale(blue_frame, from_=0, to=255, 
                                   variable=self.blue_var, orient='horizontal',
                                   command=self.on_scale_change, length=150)
        self.blue_scale.grid(row=0, column=1, sticky='ew', padx=3)
        ttk.Label(blue_frame, text="255", font=('Arial', 8)).grid(row=0, column=2, padx=(3, 0))
        
        self.blue_value_label = ttk.Label(blue_frame, text="0x80", 
                                         font=('Arial', 8, 'bold'))
        self.blue_value_label.grid(row=0, column=3, padx=(5, 0))
        
        # Blue value entry box
        self.blue_entry = ttk.Entry(blue_frame, width=6, font=('Courier', 8))
        self.blue_entry.grid(row=0, column=4, padx=(3, 0))
        self.blue_entry.insert(0, "128")
        self.blue_entry.bind('<Return>', lambda e: self.on_entry_change('blue'))
        self.blue_entry.bind('<FocusOut>', lambda e: self.on_entry_change('blue'))
        
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
        self.speed_scale.set(1)  # Default to slowest speed
        self.speed_scale.grid(row=0, column=1, padx=3)
        ttk.Label(speed_frame, text="Slow", font=('Arial', 7)).grid(row=0, column=2, padx=(3, 0))
        ttk.Label(speed_frame, text="Fast", font=('Arial', 7)).grid(row=0, column=3, padx=(8, 0))
        
    def on_scale_change(self, event=None):
        """Handle slider value changes."""
        self.update_color()
        self.update_combobox_selection()  # Set to "Custom Color" when manually adjusted
    
    def on_entry_change(self, color_channel):
        """Handle text entry changes with validation for decimal and hex values."""
        self._updating_from_entry = True  # Prevent circular updates
        
        try:
            if color_channel == 'red':
                entry_widget = self.red_entry
                var = self.red_var
            elif color_channel == 'green':
                entry_widget = self.green_entry
                var = self.green_var
            elif color_channel == 'blue':
                entry_widget = self.blue_entry
                var = self.blue_var
            else:
                return
            
            value_str = entry_widget.get().strip()
            
            # Try to parse the value
            value = self.parse_color_value(value_str)
            
            if value is not None:
                # Valid value - update the variable and slider
                var.set(value)
                self.update_color()
                self.update_combobox_selection()  # Set to "Custom Color" when manually entered
                # Reset any error styling
                entry_widget.configure(style='TEntry')
            else:
                # Invalid value - show error styling
                self.show_entry_error(entry_widget)
                
        except Exception as e:
            print(f"Error processing entry change: {e}")
            self.show_entry_error(entry_widget)
        finally:
            self._updating_from_entry = False
            
    def parse_color_value(self, value_str):
        """Parse color value from string - supports decimal (0-255) and hex (00-FF, 0x00-0xFF)."""
        if not value_str:
            return None
            
        value_str = value_str.strip().lower()
        
        try:
            # Try decimal format first
            if value_str.isdigit():
                value = int(value_str)
                if 0 <= value <= 255:
                    return value
                return None
            
            # Try hexadecimal formats
            if value_str.startswith('0x'):
                # Format: 0x00 to 0xFF
                value = int(value_str, 16)
                if 0 <= value <= 255:
                    return value
                return None
            elif len(value_str) <= 2 and all(c in '0123456789abcdef' for c in value_str):
                # Format: 00 to FF (assume hex if all hex digits)
                value = int(value_str, 16)
                if 0 <= value <= 255:
                    return value
                return None
                
        except ValueError:
            pass
            
        return None
        
    def show_entry_error(self, entry_widget):
        """Show visual feedback for invalid entry."""
        # Create a simple error indication by temporarily changing the background
        try:
            entry_widget.configure(background='#ffcccc')  # Light red background
            # Reset after 1.5 seconds
            self.root.after(1500, lambda: entry_widget.configure(background='white'))
        except:
            # Fallback if styling doesn't work
            pass
    
    def on_combobox_keypress(self, event):
        """Handle any keypress in combobox."""
        # Allow a small delay for the combobox to update its selection
        self.root.after(10, self.apply_current_selection)
        
    def on_combobox_navigate(self, event):
        """Handle Up/Down arrow navigation in combobox."""
        # Allow the default navigation to happen first
        self.root.after(10, self.apply_current_selection)
        
    def apply_current_selection(self):
        """Apply the currently highlighted color in the combobox."""
        try:
            # Get the current value from the combobox
            current_value = self.color_combobox.get()
            if current_value:
                # Extract color name and apply it
                color_name = self.extract_color_name(current_value)
                if color_name in self.COMMON_COLORS and self.COMMON_COLORS[color_name] is not None:
                    rgb_values = self.COMMON_COLORS[color_name]
                    r, g, b = rgb_values
                    self.red_var.set(r)
                    self.green_var.set(g)
                    self.blue_var.set(b)
                    self.update_color()
        except Exception as e:
            # Silently handle any errors during navigation
            pass
    
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
        step_size = 1  # Always 1 for smooth animation in mini version
        
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
        
        # Calculate delay for half speed compared to original
        base_delay = max(20, 200 - (speed * 15))  # Original timing
        delay = base_delay * 2  # Double the delay for half speed
        
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
        
        # Update entry boxes to stay synchronized (only if not currently being edited)
        if not hasattr(self, '_updating_from_entry'):
            self.red_entry.delete(0, tk.END)
            self.red_entry.insert(0, str(r))
            self.green_entry.delete(0, tk.END)
            self.green_entry.insert(0, str(g))
            self.blue_entry.delete(0, tk.END)
            self.blue_entry.insert(0, str(b))
        
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
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from timetable import *

class HomePage:
    def __init__(self, master):
        self.master = master
        master.title("Application Home Page")
        master.geometry("800x600")
        master.configure(bg='#f0f0f0')
        
        # Header
        self.header = tk.Label(master, text="Welcome to My Application Suite", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0')
        self.header.pack(pady=20)
        
        # Button frame
        self.button_frame = tk.Frame(master, bg='#f0f0f0')
        self.button_frame.pack(expand=True)
        
        # Create buttons
        self.create_image_buttons()
        
        # Footer
        self.footer = tk.Label(master, text="© 2023 My Applications. All rights reserved.", 
                             font=('Arial', 10), bg='#f0f0f0')
        self.footer.pack(side='bottom', pady=10)
    
    def create_image_buttons(self):
        # Button 1
        try:
            img1 = Image.open("meeting-room.png") if self.image_exists("meeting-room.png") else self.create_default_image()
            img1 = img1.resize((200, 200), Image.LANCZOS)
            self.photo1 = ImageTk.PhotoImage(img1)  # Store as attribute
            self.btn1 = tk.Button(self.button_frame, image=self.photo1, 
                                 command=lambda: self.open_application("App 1"),
                                 borderwidth=0, bg='#f0f0f0')
            self.btn1.grid(row=0, column=0, padx=20, pady=10)
            self.label1 = tk.Label(self.button_frame, text="Discussion Room\n    Booking", 
                                 font=('Arial', 12), bg='#f0f0f0')
            self.label1.grid(row=1, column=0)
        except Exception as e:
            self.create_text_button("App 1", 0)
        
        # Button 2
        try:
            img2 = Image.open("reminder.png") if self.image_exists("reminder.png") else self.create_default_image()
            img2 = img2.resize((200, 200), Image.LANCZOS)
            self.photo2 = ImageTk.PhotoImage(img2)  # Store as attribute
            self.btn2 = tk.Button(self.button_frame, image=self.photo2, 
                                 command=lambda: self.open_application("App 2"),
                                 borderwidth=0, bg='#f0f0f0')
            self.btn2.grid(row=0, column=1, padx=20, pady=10)
            self.label2 = tk.Label(self.button_frame, text="Reminder", 
                                 font=('Arial', 12), bg='#f0f0f0')
            self.label2.grid(row=1, column=1)
        except Exception as e:
            self.create_text_button("App 2", 1)
        
        # Button 3
        try:
            img3 = Image.open("schedule.png") if self.image_exists("schedule.png") else self.create_default_image()
            img3 = img3.resize((200, 200), Image.LANCZOS)
            self.photo3 = ImageTk.PhotoImage(img3)  # Store as attribute
            self.btn3 = tk.Button(self.button_frame, image=self.photo3, 
                                 command=lambda: self.open_application("App 3"),
                                 borderwidth=0, bg='#f0f0f0')
            self.btn3.grid(row=0, column=2, padx=20, pady=10)
            self.label3 = tk.Label(self.button_frame, text="Timetable", 
                                 font=('Arial', 12), bg='#f0f0f0')
            self.label3.grid(row=1, column=2)
        except Exception as e:
            self.create_text_button("App 3", 2)
    
    def image_exists(self, filename):
        # Simple check if image file exists
        try:
            with open(filename, 'rb'):
                return True
        except IOError:
            return False
    
    def create_default_image(self):
        # Create a default image if the specified image is not found
        from PIL import ImageDraw
        img = Image.new('RGB', (200, 200), color='#cccccc')
        draw = ImageDraw.Draw(img)
        draw.text((50, 80), "Button Image", fill='black')
        return img
    
    def create_text_button(self, text, column):
        # Fallback text button if image loading fails
        btn = tk.Button(self.button_frame, text=text, 
                        command=lambda: self.open_application(text),
                        font=('Arial', 14), width=15, height=5)
        btn.grid(row=0, column=column, padx=20, pady=10)
        label = tk.Label(self.button_frame, text=text.replace("App", "Application"), 
                         font=('Arial', 12), bg='#f0f0f0')
        label.grid(row=1, column=column)
    
    def open_application(self, app_name):
        if app_name == "App 3":
            import timetable
            timetable_win = tk.Toplevel(self.master)
            timetable.TimetableWindow(timetable_win)
        else:
            messagebox.showinfo("Info", f"Opening {app_name}\n(This will be replaced with actual application code)")

if __name__ == "__main__":
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, simpledialog
from tkcalendar import Calendar, DateEntry
import hpage
import json
import os
from datetime import datetime, timedelta
from tkinter import messagebox, Listbox, Scrollbar
from PIL import Image, ImageTk, ImageDraw, ImageFont


TIMETABLE_FILE = "timetable_data.json"

class TimetableWindow:
    def __init__(self, master):
        self.master = master
        master.title("Timetable")
        master.geometry("1500x700")  # Adjusted width and height for better layout

        self.events = [
            {"date": "2025-06-23", "day": "Monday", "subject": "Math", "time": "09:00 - 10:00", "category": "Class", "color": "#AED6F1", "invite": ""},
            {"date": "2025-06-23", "day": "Monday", "subject": "English", "time": "10:00 - 11:00", "category": "Class", "color": "#AED6F1", "invite": ""},

        ]
        self.load_events()

        self.view_mode = tk.StringVar(value="Weekly")
        self.selected_week = tk.StringVar(value="Week 1: 2025-06-23 ~ 2025-06-29")
        self.week_ranges = self.generate_week_ranges(start_date="2025-06-23", weeks=14)

        # Header
        label = tk.Label(master, text="Class Timetable", font=('Arial', 16, 'bold'))
        label.pack(pady=10)

        # Weekly, Daily, and Monthly selection in one line, centered
        selection_frame = tk.Frame(master)
        selection_frame.pack(pady=10, fill=tk.X)

        # Center the selection_frame contents
        selection_inner = tk.Frame(selection_frame)
        selection_inner.pack(anchor="center")

        # Weekly selection
        tk.Label(selection_inner, text="Weekly:").pack(side=tk.LEFT, padx=5)
        self.week_combo = ttk.Combobox(selection_inner, values=self.week_ranges, textvariable=self.selected_week, width=30, state="readonly")
        self.week_combo.pack(side=tk.LEFT, padx=5)
        tk.Button(selection_inner, text="Go", command=self.refresh_table).pack(side=tk.LEFT, padx=5)

        # Daily view picker
        tk.Label(selection_inner, text="Daily:").pack(side=tk.LEFT, padx=10)
        self.daily_date_picker = DateEntry(selection_inner, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        self.daily_date_picker.pack(side=tk.LEFT, padx=5)
        tk.Button(selection_inner, text="Show Daily View", command=self.show_selected_daily_view).pack(side=tk.LEFT, padx=5)

        # Monthly view picker
        tk.Label(selection_inner, text="Monthly:").pack(side=tk.LEFT, padx=10)
        self.month_var = tk.StringVar(value=datetime.now().strftime('%m'))
        self.year_var = tk.StringVar(value=datetime.now().strftime('%Y'))
        month_combo = ttk.Combobox(selection_inner, values=[f"{i:02}" for i in range(1,13)], textvariable=self.month_var, width=3, state="readonly")
        month_combo.pack(side=tk.LEFT, padx=5)
        tk.Button(selection_inner, text="Show Monthly View", command=self.show_selected_monthly_view).pack(side=tk.LEFT, padx=5)

        # Table frame
        self.table_frame = tk.Frame(master)
        self.table_frame.pack(pady=10)
        
        self.refresh_table()

        # Legend frame (for color categories)
        self.legend_frame = tk.Frame(master)
        self.legend_frame.pack(pady=10)
        self.create_legend()

        # Add event button
        add_event_button = tk.Button(master, text="Add Event", command=self.show_add_event_dialog)
        add_event_button.pack(pady=10)
        
        # Delete event button
        delete_event_button = tk.Button(master, text="Delete Event", command=self.show_delete_event_dialog)
        delete_event_button.pack(pady=5)

        # Back button
        back_button = tk.Button(master, text="Back", command=master.destroy)
        back_button.pack(pady=10)

    def generate_week_ranges(self, start_date, weeks):
        """Generate 14 weeks starting from the given start date."""
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        week_ranges = []
        for i in range(weeks):
            week_start = start_date + timedelta(weeks=i)
            week_end = week_start + timedelta(days=6)
            week_ranges.append(f"Week {i + 1}: {week_start.strftime('%Y-%m-%d')} ~ {week_end.strftime('%Y-%m-%d')}")
        return week_ranges

    def refresh_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Create timetable grid
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        times = [f"{hour:02}:00" for hour in range(8, 18)]  # From 08:00 to 17:00

        # Create headers for time slots
        tk.Label(self.table_frame, text="Day/Time", font=('Arial', 12, 'bold'), width=12, borderwidth=1, relief="solid").grid(row=0, column=0)
        for col, time in enumerate(times, start=1):
            tk.Label(self.table_frame, text=time, font=('Arial', 12, 'bold'), width=12, borderwidth=1, relief="solid").grid(row=0, column=col)

        # Create rows for days
        for row, day in enumerate(days, start=1):
            tk.Label(self.table_frame, text=day, font=('Arial', 12, 'bold'), width=12, borderwidth=1, relief="solid").grid(row=row, column=0)

        # Filter events based on selected week
        events_to_show = self.filter_events_by_view()

        # Place events in the timetable grid
        for event in events_to_show:
            day_index = days.index(event["day"]) + 1
            start_time = int(event["time"].split(" - ")[0].split(":")[0]) - 8  # Adjust to grid index
            end_time = int(event["time"].split(" - ")[1].split(":")[0]) - 8
            label_text = f"{event['subject']}\n{event['time']}\n{event['date']}"
            for col in range(start_time + 1, end_time + 1):
                tk.Label(
                    self.table_frame,
                    text=label_text,
                    font=('Arial', 10),
                    bg=event["color"],
                    width=12,
                    borderwidth=1,
                    relief="solid"
                ).grid(row=day_index, column=col)

    def filter_events_by_view(self):
        selected_week = self.selected_week.get()
        week_start, week_end = selected_week.split(": ")[1].split(" ~ ")
        return [
            e for e in self.events
            if "date" in e and week_start <= e["date"] <= week_end
        ]

    def create_legend(self):
        """Create legend for color categories."""
        categories = {
            "Class": "#AED6F1",        # Light blue
            "Event": "#A9DFBF",        # Light green
            "Meeting": "#F9E79F",      # Light yellow
            "Appointment": "#F5B7B1"   # Light pink
        }
        for category, color in categories.items():
            tk.Label(self.legend_frame, text=category, font=('Arial', 10), bg=color, width=20, borderwidth=1, relief="solid").pack(side=tk.LEFT, padx=5)

    # Add Event Dialog
    def show_add_event_dialog(self):
        """Show a dialog for adding an event."""
        dialog = tk.Toplevel(self.master)
        dialog.title("Add Event")
        dialog.geometry("400x600")

        tk.Label(dialog, text="Select Date:").pack(pady=5)
        calendar = DateEntry(dialog, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        calendar.pack(pady=5)

        tk.Label(dialog, text="Subject:").pack(pady=5)
        subject_entry = tk.Entry(dialog)
        subject_entry.pack(pady=5)

        tk.Label(dialog, text="Time:").pack(pady=5)
        # Generate available 1-hour time slots (08:00 - 17:00)
        all_times = [f"{hour:02}:00 - {hour+1:02}:00" for hour in range(8, 17)]
        time_var = tk.StringVar()
        time_combo = ttk.Combobox(dialog, values=all_times, textvariable=time_var, state="readonly")
        time_combo.pack(pady=5)

        # Error label for validation feedback
        error_label = tk.Label(dialog, text="", fg="red")
        error_label.pack(pady=2)

        tk.Label(dialog, text="Category:").pack(pady=5)
        category_combo = ttk.Combobox(dialog, values=["Class", "Event", "Meeting", "Appointment"], state="readonly")
        category_combo.pack(pady=5)

        tk.Label(dialog, text="Invite (comma-separated emails):").pack(pady=5)
        invite_entry = tk.Entry(dialog)
        invite_entry.pack(pady=5)

        # Validate and add event
        def validate_and_add():
            date = calendar.get_date()
            selected_time = time_var.get()
            subject = subject_entry.get().strip()
            category = category_combo.get().strip()

            # 1. Check for empty fields
            if not subject:
                error_label.config(text="Please enter a subject.")
                return
            if not selected_time:
                error_label.config(text="Please select a time slot.")
                return
            if not category:
                error_label.config(text="Please select a category.")
                return

            # 2. Check for time conflict
            conflict = any(
                e.get("date") == date.strftime('%Y-%m-%d') and e.get("time") == selected_time
                for e in self.events
            )

            if conflict:
                error_label.config(text="This time slot is already taken on this day. Please choose another time.")
                # No need to clear the combo box, just let the user re-select.
                return
            
            # 3. If all validation passes, add the event
            self.add_event_from_dialog(calendar, subject_entry, time_combo, category_combo, invite_entry, dialog)

        tk.Button(dialog, text="Add", command=validate_and_add).pack(pady=10)

    def add_event_from_dialog(self, calendar, subject_entry, time_entry, category_combo, invite_entry, dialog):
        """Add an event from the dialog."""
        category_colors = {
            "Class": "#AED6F1",
            "Event": "#A9DFBF",
            "Meeting": "#F9E79F",
            "Appointment": "#F5B7B1"
        }
        date_obj = calendar.get_date()
        date = date_obj.strftime("%Y-%m-%d")
        day = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
        subject = subject_entry.get()
        time = time_entry.get()
        category = category_combo.get()
        invite = invite_entry.get()

        color = category_colors.get(category, "#FFFFFF")
        
        # Now, create and append the new event
        new_event = {
            "date": date,
            "day": day,
            "subject": subject,
            "time": time,
            "category": category,
            "color": color,
            "invite": invite or ""
        }
        
        self.events.append(new_event)
        self.events.sort(key=lambda x: (x['date'], x['time'])) # Optional: keep events sorted
        self.refresh_table()
        self.save_events()
        dialog.destroy()

    def save_events(self):
        with open(TIMETABLE_FILE, "w") as f:
            json.dump(self.events, f)

    def load_events(self):
        if os.path.exists(TIMETABLE_FILE):
            with open(TIMETABLE_FILE, "r") as f:
                self.events = json.load(f)

    def get_monthly_view(self, date_str):
        import calendar
        date = datetime.strptime(date_str, '%Y-%m-%d')
        year, month = date.year, date.month
        output = f"Monthly View: {calendar.month_name[month]} {year}\n"
        num_days = calendar.monthrange(year, month)[1]
        has_events = False
        for day in range(1, num_days + 1):
            day_str = f"{year:04d}-{month:02d}-{day:02d}"
            events = [e for e in self.events if e.get('date') == day_str]
            if events:
                has_events = True
                output += f"\n{day_str}:\n"
                for event in events:
                    output += f"{event.get('time')}: {event.get('subject')} ({event.get('category')})\n"
        if not has_events:
            output += "\nNo events scheduled.\n"
        return output

    def get_daily_view(self, date_str):
        output = f"Daily View: {date_str}\n"
        events = [e for e in self.events if e.get('date') == date_str]
        if not events:
            output += "\nNo events scheduled.\n"
        else:
            for event in events:
                output += f"\n{event.get('time')}: {event.get('subject')} ({event.get('category')})\n"
        return output

    def show_selected_daily_view(self):
        date_obj = self.daily_date_picker.get_date()
        date_str = date_obj.strftime('%Y-%m-%d')
        result = self.get_daily_view(date_str)
        self.show_result_popup("Daily View", result)

    def show_selected_monthly_view(self):
        year = self.year_var.get()
        month = self.month_var.get()
        date_str = f"{year}-{month}-01"
        result = self.get_monthly_view(date_str)
        self.show_result_popup("Monthly View", result)

    def show_result_popup(self, title, result):
        win = tk.Toplevel(self.master)
        win.title(title)
        text = tk.Text(win, width=80, height=30)
        text.pack()
        text.insert(tk.END, result)

    def show_delete_event_dialog(self):
        """Show a dialog for deleting an event."""
        dialog = tk.Toplevel(self.master)
        dialog.title("Delete Event")
        dialog.geometry("600x400")

        tk.Label(dialog, text="Select an event to delete:").pack(pady=10)

        # Create a listbox to display events
        event_listbox_frame = tk.Frame(dialog)
        event_listbox_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        event_listbox = Listbox(event_listbox_frame, selectmode=tk.SINGLE)
        scrollbar = Scrollbar(event_listbox_frame, orient=tk.VERTICAL, command=event_listbox.yview)
        event_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        event_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Populate the listbox with events
        for i, event in enumerate(self.events):
            display_text = f"{event.get('date')} | {event.get('time')} | {event.get('subject')} ({event.get('category')})"
            event_listbox.insert(tk.END, display_text)
            event_listbox.bind('<Double-Button-1>', lambda event: self.confirm_delete(event_listbox, dialog))

        def delete_selected_event():
            try:
                selected_index = event_listbox.curselection()[0]
                self.confirm_delete(selected_index, dialog)
            except IndexError:
                messagebox.showwarning("No Selection", "Please select an event to delete.")

        tk.Button(dialog, text="Delete Selected Event", command=delete_selected_event).pack(pady=10)

    def confirm_delete(self, selected_index, dialog):
        """Asks for confirmation before deleting an event."""
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this event?"):
            self.events.pop(selected_index)
            self.save_events()
            self.refresh_table()
            dialog.destroy()
            messagebox.showinfo("Success", "Event deleted successfully.")



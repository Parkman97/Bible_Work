import tkinter as tk
from tkinter import Listbox
from tkinterweb import HtmlFrame
import webbrowser
import requests
from bs4 import BeautifulSoup
from get_data import get_random_Verse, daily_devotional, online_daily_devotional, daily_devotional, video_urls, get_video


# Flashcard Frame
class FlashcardFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.flashcards = get_random_Verse()  # Initialize flashcards

        # Display question
        self.question_label = tk.Label(self, text=self.flashcards[0], font=("Helvetica", 18))
        self.question_label.pack(pady=20)

        # Flip button functionality
        def flip_card():
            answer = self.flashcards[1]
            self.question_label.config(text=answer)

        def next_card():
            self.flashcards = get_random_Verse()  # Get new random verse
            self.question_label.config(text=self.flashcards[0])

        # Buttons for flipping and moving to next card
        flip_button = tk.Button(self, text="Show Answer", command=flip_card)
        flip_button.pack(pady=10)

        next_button = tk.Button(self, text="Next Question", command=next_card)
        next_button.pack(pady=10)

class DevotionalFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        label = tk.Label(self, text="Daily Devotional Content", font=("Helvetica", 18))
        label.pack(pady=20)

        # Create buttons
        self.pdf_button = tk.Button(self, text="PDF Devotional", command=self.load_pdf_devotional)
        self.pdf_button.pack(side="top", pady=10)

        self.online_button = tk.Button(self, text="Seeking God's Face", command=self.load_online_devotional)
        self.online_button.pack(side="top", pady=10)

        # Create a Canvas widget with a scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the devotional text
        self.text_frame = tk.Frame(self.canvas)

        # Create a Label to display the devotional content inside the frame
        self.devotional_label = tk.Label(self.text_frame, font=("Helvetica", 12), wraplength=600)
        self.devotional_label.pack(padx=10, pady=10)

        # Create a frame for the "Back" button
        self.back_button_frame = tk.Frame(self)
        self.back_button = tk.Button(self.back_button_frame, text="Back", command=self.show_buttons)
        self.back_button.pack()

    def load_pdf_devotional(self):
        self.devotional = daily_devotional()
        self.show_devotional_content()

    def load_online_devotional(self):
        self.devotional = online_daily_devotional()
        self.show_devotional_content()

    def show_devotional_content(self):
        # Remove buttons
        self.pdf_button.pack_forget()
        self.online_button.pack_forget()

        # Add canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add the "Back" button frame at the bottom center
        self.back_button_frame.pack(side="bottom", pady=10)

        # Update the devotional content
        self.update_devotional_content()

    def update_devotional_content(self):
        self.devotional_label.config(text=self.devotional)
        self.text_frame.update_idletasks()  # Ensure that the text frame is sized correctly

        # Calculate the center coordinates of the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        text_frame_width = self.text_frame.winfo_width()
        text_frame_height = self.text_frame.winfo_height()

        x_center = (canvas_width - text_frame_width) / 2
        y_center = (canvas_height - text_frame_height) / 2

        # Create the window at the center coordinates
        self.canvas.create_window((x_center, y_center), window=self.text_frame, anchor="nw")

        # Update the scrollable region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def show_buttons(self):
        # Remove canvas, scrollbar, and back button frame
        self.canvas.pack_forget()
        self.scrollbar.pack_forget()
        self.back_button_frame.pack_forget()

        # Show the original buttons
        self.pdf_button.pack(side="top", pady=10)
        self.online_button.pack(side="top", pady=10)

    def reset_frame(self):
        # Reset the frame to its initial state
        self.show_buttons()


# Saved Bible Verses Frame (example frame for saved verses)
class SavedVersesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        label = tk.Label(self, text="Saved Bible Verses", font=("Helvetica", 18))
        label.pack(pady=20)

# Other Resources Frame (example frame for resources)
class OtherResourcesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        label = tk.Label(self, text="Other Resources", font=("Helvetica", 18))
        label.pack(pady=20)

class VideosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        label = tk.Label(self, text="Videos", font=("Helvetica", 18))
        label.pack(pady=20)

        # Create two scrollable sections
        self.left_listbox = self.create_scrollable_listbox("left")
        self.right_listbox = self.create_scrollable_listbox("right")

        # Dictionaries to store the mapping between listbox items and URLs
        self.left_urls = {}
        self.right_urls = {}

        # Load video URLs and display them in the listboxes
        old_anchors, new_anchors = video_urls()
        self.load_listbox(self.left_listbox, self.extract_href(old_anchors), self.left_urls)
        self.load_listbox(self.right_listbox, self.extract_href(new_anchors), self.right_urls)

        # Create a frame for displaying the video
        self.video_frame = HtmlFrame(self, horizontal_scrollbar="auto")
        self.video_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def create_scrollable_listbox(self, side):
        # Create a frame for the scrollable listbox
        section_frame = tk.Frame(self)
        section_frame.pack(side=side, fill="both", expand=True, padx=10, pady=10)

        # Create a listbox widget with a scrollbar
        listbox = Listbox(section_frame)
        scrollbar = tk.Scrollbar(section_frame, orient="vertical", command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)

        # Pack the listbox and scrollbar
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind the listbox selection event
        listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        return listbox

    def load_listbox(self, listbox, items, url_dict):
        for key, value in items.items():
            listbox.insert(tk.END, key)
            url_dict[key] = value

    def on_listbox_select(self, event):
        listbox = event.widget
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            key = listbox.get(index)
            if listbox == self.left_listbox:
                url = self.left_urls[key]
            else:
                url = self.right_urls[key]
            video_url = get_video(url)
            self.display_video(video_url)

    def display_video(self, video_url):
        self.video_frame.load_website(video_url)

    def extract_href(self, list_anchors):
        links = {}
        for anchor in list_anchors:
            href = anchor.get("href")
            div_text = anchor.find("div").text if anchor.find("div") else "No div found"
            if href:
                links[div_text] = href
        return links

# Main Application Window
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FaithStack")
        self.geometry("1000x800")

        # Initialize frames
        self.frames = {}
        self.frames["flashcards"] = FlashcardFrame(self)
        self.frames["devotional"] = DevotionalFrame(self)
        self.frames["saved_verses"] = SavedVersesFrame(self)
        self.frames["other_resources"] = OtherResourcesFrame(self)
        self.frames["videos"] = VideosFrame(self)
        self.previous_frame = None

        # Create navigation buttons
        self.create_navigation()


    # Create navigation buttons to switch between frames
    def create_navigation(self):
        nav_frame = tk.Frame(self)
        nav_frame.pack(side="top", pady=10)

        flashcards_button = tk.Button(nav_frame, text="Flashcards", command=lambda: self.show_frame("flashcards"))
        flashcards_button.grid(row=0, column=0, padx=10)

        devotional_button = tk.Button(nav_frame, text="Daily Devotional", command=lambda: self.show_frame("devotional"))
        devotional_button.grid(row=0, column=1, padx=10)

        saved_verses_button = tk.Button(nav_frame, text="Saved Verses", command=lambda: self.show_frame("saved_verses"))
        saved_verses_button.grid(row=0, column=2, padx=10)

        resources_button = tk.Button(nav_frame, text="Other Resources", command=lambda: self.show_frame("other_resources"))
        resources_button.grid(row=0, column=3, padx=10)

        resources_button = tk.Button(nav_frame, text="Videos", command=lambda: self.show_frame("videos"))
        resources_button.grid(row=0, column=4, padx=10)

    # Show the selected frame
    def show_frame(self, frame_name):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()

        # Show the selected frame
        self.frames[frame_name].pack(expand=True, fill="both")

        frame = self.frames[frame_name]
        if frame_name == "devotional":
            frame.reset_frame()
        
        self.previous_frame = frame_name


# Run the application
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
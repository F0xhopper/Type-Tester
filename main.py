import tkinter as tk
from datetime import datetime
import random
import time
import threading

class TypingTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Initialize the tkinter application
        self.title("TypeTrial.io")
        self.config(padx=30, pady=30, background='black')
        # Define paragraphs to be copied
        self.paragraphs = ["The sun dipped below the horizon, casting long shadows across the \nlandscape. The sky turned a vibrant orange, painting a breathtaking scene for\n those who cared to look. Nature's beauty never failed to inspire awe.",
                           "High in the mountains, the air was crisp and thin, carrying the scent of \npine and snow. The silence was profound, broken only by the occasional chirp\n of a bird or the rustle of leaves in the breeze. It was a place of tranquility,\n far removed from the noise of the world below.",
                           "The moon cast a silver glow over the sleepy town, illuminating empty streets.\n Shadows danced with the gentle breeze, whispering secrets to the night. In \nthe distance, a lone owl hooted its melancholic melody, adding to the\n nocturnal symphony."]
        # Initialize variables
        self.current_paragraph = random.choice(self.paragraphs)
        self.running = False
        self.username = ""
        self.counter = 0
        self.total_inputs = 0
        self.total_mistakes = 0
        # Make username input pop up appear
        self.get_username()
        # Create GUI widgets
        self.create_widgets()
        # Load highscores from file
        self.load_highscore()

    def create_widgets(self):
        # Create title label
        self.title = tk.Label(self, justify="left", text="TypeTrial.io", background='black', fg='white', font=("Helvetica", 35))
        self.title.grid(column=1, row=0,padx=110)
        # Create label for highscores
        self.highscore_label = tk.Label(self, justify="left", anchor="w", background='black', fg='white', font=("Helvetica", 14))
        self.highscore_label.grid(column=0, row=0, columnspan=1)
        # Create label for displaying username
        self.name_label = tk.Label(self, width=21,justify="right", anchor="e", background='black', fg='white', font=("Helvetica", 14))
        self.name_label.grid(column=2, row=0, columnspan=1,padx=20)
        # Create frame for statistics
        self.stats_frame = tk.Frame(background='black')
        self.stats_frame.grid(column=1, row=1, pady=10)
        # Create labels for timer, accuracy, and words per minute (WPM)
        self.timer = tk.Label(self.stats_frame, text="0 cpm", borderwidth=3, relief="solid", fg='white', highlightcolor='black', background='black', font=("Helvetica", 20))
        self.timer.grid(column=0, row=0, pady=2, ipadx=20, ipady=0)
        self.accuracy_label = tk.Label(self.stats_frame, text="0% Accuracy", borderwidth=3, relief="solid", fg='white', highlightcolor='black', background='black', font=("Helvetica", 20))
        self.accuracy_label.grid(column=0, row=2, pady=2, ipadx=20, ipady=0)
        self.wpm_label = tk.Label(self.stats_frame, text="0 wpm", borderwidth=3, relief="solid", fg='white', highlightcolor='black', background='black', font=("Helvetica", 20))
        self.wpm_label.grid(column=0, row=1, pady=2, ipadx=20, ipady=0)
        # Create label for displaying paragraph to type
        self.paragraph = tk.Label(self, text=self.current_paragraph, fg='white', background='black', font=("Helvetica", 17), width=60, height=4)
        self.paragraph.grid(row=2, column=0, columnspan=3, pady=10)
        # Create text input widget for typing
        self.text_input = tk.Text(height=8, background='white', fg='black', font=(24))
        self.text_input.grid(row=3, column=0, columnspan=3, pady=(10))
        self.text_input.bind("<KeyRelease>", self.start)
        # Create button for restarting the typing test
        self.restart = tk.Button(text='Restart', highlightbackground="black", highlightthickness=1, background='black', command=self.reset)
        self.restart.config(height=2, width=6)
        self.restart.grid(row=4, column=1, pady=10)

    # Method for getting the users username
    def get_username(self):
        # Initialize the popup
        username_window = tk.Toplevel(self)
        username_window.title("Enter Username")
        username_window.config(padx=20, pady=20)
        # Create label for instructions
        username_label = tk.Label(username_window, text="Enter your username:", font=("Helvetica", 14))
        username_label.pack()
        # Create input for username
        self.username_entry = tk.Entry(username_window)
        self.username_entry.pack()
        # Set entry in focus
        self.username_entry.focus_set()
        # Create submit button
        submit_button = tk.Button(username_window, text="Submit", command=self.save_username)
        submit_button.pack()

    # Method for saving the entered username
    def save_username(self):
        # Set username vairable to the one entered by user
        self.username = self.username_entry.get()
        # Checkts if the input is empty, destroys popup, clears input and initiates typing test if not
        if self.username.strip() != "":
            self.name_label.config(text=f'User playing: {self.username}')
            self.username_entry.delete(0, tk.END)
            self.username_entry.master.destroy()

    # Method triggered when typing to calculate if paragraph is matching or wrong
    def start(self, event):
        # Count the amount typed
        self.total_inputs += 1
        # If not already running start keeping count of scores and time
        if not self.running:
            self.running = True
            t = threading.Thread(target=self.update_time_scores)
            t.start()
        # If input doesn't match paragraph makes input text red and adds a mistake onto mistake counter
        if not self.current_paragraph.replace("\n", "").startswith(self.text_input.get("1.0", "end-1c")):
            self.text_input.config(fg='red')
            self.total_mistakes += 1
        else:
          
            self.text_input.config(fg='black')
        # When the paragraph is completely typed end session, save score to file and turn text green
        if self.current_paragraph.replace("\n", "") == self.text_input.get("1.0", "end-1c"):
            self.running = False
            self.text_input.config(fg='green')
            self.set_new_score()
            self.load_highscore()

    # Method for updating time and scores
    def update_time_scores(self):
        while self.running:
            # Calculate every 0.1 seconds
            time.sleep(0.1)
            self.counter += 0.1 
            # Initialize accuracy variable
            accuracy = 100
            # Initialize total words/characters variables
            total_characters = len(''.join(self.text_input.get("1.0","end-1c").split(' ')))
            total_words = len(self.text_input.get("1.0","end-1c").split(' '))
            # When a mistake is made calculate the new accuracy
            if self.total_mistakes != 0:
                accuracy = int((self.total_inputs - self.total_mistakes) / self.total_inputs *100 )
            # When the times is started calculate new wpm and cpm
            if self.counter != 0:  
                self.wpm = total_words // (self.counter / 60.0)
                cpm = total_characters // (self.counter / 60.0)
            else:
                self.wpm = 0
                cpm = 0
            # Update the accuracy, timer and wpm labels
            self.accuracy_label.config(text=f'{accuracy:.0f}% Accuracy')
            self.timer.config(text=f'{cpm:.1f} cpm')
            self.wpm_label.config(text=f'{self.wpm:.0f} wpm')

    # Method loading the highest scores from the txt file
    def load_highscore(self):
      try:
            with open("highscore.txt", "r") as score_file:
                lines = score_file.readlines()
                # Initialize scores variable
                scores = []
                # read and add scores username and date to the scores array as tuple
                for line in lines:
                    parts = line.strip().split(":")
                    username = parts[0]
                    wpm = float(parts[1])
                    date = parts[2]
                    scores.append((username, wpm, date))
                # Sort scores into order based on wpm
                scores.sort(key=lambda x: x[1], reverse=True)
                # Initialize top_3_scores_label_text variable and read, format and append the top 3 scores to top_3_scores_label_text from scores array
                top_3_scores_label_text = []
                for i, (username, wpm, date) in enumerate(scores[:3]):
                    top_3_scores_label_text.append(f'{i+1}. {username}: {wpm:.0f} wpm {date}')
                # Update highscores label
                self.highscore_label.config(text='\n'.join(top_3_scores_label_text))
      except FileNotFoundError:
            print("Error: highscore file not found.")
      except Exception as e:
            print(f"An error occurred while loading highscores: {e}")

    # Method for writing new score with date to the txt file        
    def set_new_score(self):
        # Get current date
        current_date = datetime.now().strftime("%d--%m-%Y") 
        with open("highscore.txt", "a") as score_file:
            score_file.write(f'{self.username}:{self.wpm}:{current_date}\n')
    
    # Method for restarting the test    
    def reset(self):
        # Wait 0.1 second for update_time_scores function to finish
        time.sleep(0.1)
        # Clear input
        self.text_input.delete("1.0","end-1c") 
        # Reset variables
        self.running = False
        self.counter = 0.0
        self.total_inputs = 0
        self.total_mistakes = 0
        self.wpm = 0
        #  Update labels
        self.timer.config(text='0 cpm')
        self.wpm_label.config(text='0 wpm')
        self.current_paragraph = random.choice(self.paragraphs)
        self.paragraph.config(text=self.current_paragraph)
        self.accuracy_label.config(text='0% Accuracy')



if __name__ == "__main__":
    app = TypingTestApp()
    app.mainloop()
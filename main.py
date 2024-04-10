import tkinter as tk
from tkinter import messagebox
import random
import math
import time
import threading
class TypingTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Test")
        self.config(padx=20,pady=20,background='black')
        self.paragraphs = ["The cat lazily stretched out in the warmth of the afternoon sun.",'Books lined the shelves, their spines bearing the weight of countless stories.','With a flick of the switch, the room was bathed in soft, golden light.']
        self.current_paragraph = random.choice(self.paragraphs)
        self.running = False
        self.username = ""
        self.get_username()
        self.counter = 0
        self.highscore = 0 
        self.highscore_username = ''
        self.total_letters_types = 0
        self.total_mistakes = 0
        self.create_widgets()
        self.load_highscore()

    def create_widgets(self):
        self.title = tk.Label(self, justify="left", text="TypeTest.io", background='black', fg='white', font=("Helvetica", 35))     
        self.title.grid(column=1, row=0)

        self.highscore_label = tk.Label(self, justify="left", anchor="w", text=f'Highest: {self.highscore_username} {self.highscore:.0f} w/m', wraplength=200, background='black', fg='white', font=("Helvetica", 14))     
        self.highscore_label.grid(column=0, row=0, columnspan=1)
          
        self.name_label = tk.Label(self, width=16, text=f'User playing:{self.username}', background='black', fg='white', font=("Helvetica", 14))     
        self.name_label.grid(column=2, row=0, columnspan=1)

        self.stats_frame = tk.Frame(background='black')
        self.stats_frame.grid(column=1, row=1, pady=10)
      
        self.timer = tk.Label(self.stats_frame, text="0 cpm", borderwidth=3, relief="solid", fg='white', highlightcolor='black', background='black', font=("Helvetica", 20))
        self.timer.grid(column=0, row=0, pady=2, ipadx=20, ipady=0)
      
        self.accuracy_label = tk.Label(self.stats_frame, text="0% Accuracy", borderwidth=3, relief="solid", fg='white', highlightcolor='black', background='black', font=("Helvetica", 20))
        self.accuracy_label.grid(column=0, row=2, pady=2, ipadx=20, ipady=0)

        self.wpm_label = tk.Label(self.stats_frame, text="0 wpm", borderwidth=3, relief="solid", fg='white', highlightcolor='black', background='black', font=("Helvetica", 20))
        self.wpm_label.grid(column=0, row=1, pady=2, ipadx=20, ipady=0)

        self.paragraph = tk.Label(self, text=self.current_paragraph, fg='white', background='black', font=("Helvetica", 17), width=60, height=4)
        self.paragraph.grid(row=2, column=0, columnspan=3, pady=10)

        self.text_input = tk.Text(height=8, width=60, background='white', fg='black', font=(14))      
        self.text_input.grid(row=3, column=0, columnspan=3, pady=(10))
        self.text_input.bind("<KeyRelease>", self.start)
       
        self.restart = tk.Button(text='Restart', highlightbackground="black", highlightthickness=1, background='black', command=self.reset)
        self.restart.config(height=2, width=6)
        self.restart.grid(row=4, column=1, pady=10)
    
    def get_username(self):
        username_window = tk.Toplevel(self)
        username_window.title("Enter Username")
        username_window.config(padx=20, pady=20)
        username_label = tk.Label(username_window, text="Enter your username:", font=("Helvetica", 14))
        username_label.pack()
        self.username_entry = tk.Entry(username_window)
        self.username_entry.pack()
        self.username_entry.focus_set()
        submit_button = tk.Button(username_window, text="Submit", command=self.save_username)
        submit_button.pack()

    def save_username(self):
        self.username = self.username_entry.get()
        if self.username.strip() != "":
  
 
            self.name_label.config(text=f'Playing:{self.username}')
            self.username_entry.delete(0, tk.END)
            self.username_entry.master.destroy()
    def start(self,event):
        self.total_letters_types +=1 
        if not self.running:
            self.running = True
            t = threading.Thread(target=self.update_times_scores)
            t.start()
        if not self.paragraph.cget("text").startswith(self.text_input.get("1.0","end-1c")):
            self.text_input.config(fg='red')
            self.total_mistakes += 1
            
        else:
            self.text_input.config(fg='black')
        if self.paragraph.cget("text") == self.text_input.get("1.0","end-1c"):
             self.running = False
             self.text_input.config(fg='green')
             if self.wpm > self.highscore:
                self.set_new_highscore()
                self.load_highscore()

    def update_times_scores(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1 
            accuracy = 100
            characters = len(''.join(self.text_input.get("1.0","end-1c").split(' ')))
            if self.total_mistakes != 0:
                accuracy = int((self.total_letters_types - self.total_mistakes) / self.total_letters_types *100 )
            words = len(self.text_input.get("1.0","end-1c").split(' '))
            self.wpm = words // (self.counter / 60)
            cpm = characters // (self.counter / 60)
            self.accuracy_label.config(text=f'{accuracy:.0f}% Accuracy')
            self.timer.config(text=f'{cpm:.1f} cpm')
            self.wpm_label.config(text=f'{self.wpm:.0f} wpm')

    def load_highscore(self):
      with open("highscore.txt", "r") as score_file:
        lines = score_file.readlines()
        self.highscores = []
        for line in lines:
            parts = line.strip().split(":")
            username = parts[0]
            wpm = float(parts[1])
            self.highscores.append((username, wpm))
        # Sort highscores based on WPM, highest first
        self.highscores.sort(key=lambda x: x[1], reverse=True)
        # Display the top 3 scores
        top_3_scores_label_text = []
        for i, (username, wpm) in enumerate(self.highscores[:3]):
            top_3_scores_label_text.append(f'{i+1}. {username}: {wpm:.0f} wpm')
        self.highscore_label.config(text='\n'.join(top_3_scores_label_text))
            
    def set_new_highscore(self):
        with open("highscore.txt", "a") as score_file:
            score_file.write(f'{self.username}:{self.wpm}\n')
    
        
    def reset(self):
        self.running = False
        self.counter = 0
        self.total_letters_types = 0
        self.total_mistakes = 0
        self.text_input.delete("1.0","end-1c") 
        self.timer.config(text=f'{0} s')
        self.wpm_label.config(text=f'{0} w/m')
        self.current_paragraph = random.choice(self.paragraphs)
        self.paragraph.config(text=f'{self.current_paragraph}')
        self.accuracy_label.config(text=f'0% Accuracy')



if __name__ == "__main__":
    app = TypingTestApp()
    app.mainloop()
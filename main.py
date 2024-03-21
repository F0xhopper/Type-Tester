import tkinter as tk
import random
from datetime import datetime

class TypingTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Test")
        self.config(padx=20,pady=20,background='lightgrey')
        self.paragraphs = ["The leather jacked showed the scars of being his favorite for years.\n It wore those scars with pride, feeling that they enhanced his presence rather than diminishing it. The scars gave it character and had not overwhelmed to the point \nthat it had become ratty. The jacket was in its prime and it knew it.", "The computer wouldn't start. She banged on the side and \ntried again. Nothing. She lifted it up and dropped it to the table. Still nothing. She banged her closed fist against\n the top. It was at this moment she saw the irony of trying to fix the machine with violence."]
        self.current_paragraph = random.choice(self.paragraphs)
        self.start_time = None
        self.create_widgets()
        
    def create_widgets(self):
        self.title = tk.Label(self, text="Type_Test.IO",background='lightgrey',fg='black', font=("Helvetica", 24))
        self.title.grid(column=1,row=0)
        self.stats_frame = tk.Frame(background='lightgrey')
        self.stats_frame.grid(column=1,row=1,pady=10)
        self.timer = tk.Label(self.stats_frame, text="0.00s", borderwidth=3, relief="solid",fg='black',highlightcolor='black',background='lightgrey', font=("Helvetica", 24))
        self.timer.grid(column=0,row=0,pady=10,ipadx=20,ipady=10)
        self.wpm = tk.Label(self.stats_frame, text="0w/m", borderwidth=3, relief="solid",fg='black',highlightcolor='black',background='lightgrey', font=("Helvetica", 24))
        self.wpm.grid(column=1,row=0,pady=10,ipadx=20,ipady=10)

        self.paragraph = tk.Label(self, text=self.current_paragraph,fg='black',background='lightgrey', font=("Helvetica", 17))
        self.paragraph.grid(row=2,column=0,columnspan=3,pady=10)
        self.text_input = tk.Text( height=8, width=70,background='white',fg='black',font=(14))
        self.text_input.grid(row=3,column=0,columnspan=3,pady=10)
        self.restart = tk.Button(text='Restart',highlightbackground = "black",  
                         highlightthickness = 1,background='black');self.restart.config(height = 2, width = 6)
        self.restart.grid(row=4,column=1,pady=10)
if __name__ == "__main__":
    app = TypingTestApp()
    app.mainloop()
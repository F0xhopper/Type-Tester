import tkinter as tk
import random
from datetime import datetime
import time
import threading
class TypingTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Test")
        self.config(padx=20,pady=20,background='lightgrey')
        self.paragraphs = ["The cat lazily stretched out in the warmth of the afternoon sun.",'Books lined the shelves, their spines bearing the weight of countless stories.','With a flick of the switch, the room was bathed in soft, golden light.']
        self.current_paragraph = random.choice(self.paragraphs)
        self.running = False
        self.counter = 0
        self.create_widgets()
        
    def create_widgets(self):
        self.title = tk.Label(self, text="Typey_test",background='lightgrey',fg='black', font=("Helvetica", 24))
      
        self.title.grid(column=1,row=0)
      
        self.stats_frame = tk.Frame(background='lightgrey')
        self.stats_frame.grid(column=1,row=1,pady=10)
      
        self.timer = tk.Label(self.stats_frame, text="0 s", borderwidth=3, relief="solid",fg='black',highlightcolor='black',background='lightgrey', font=("Helvetica", 24))
        self.timer.grid(column=0,row=0,pady=10,ipadx=20,ipady=10)
     
        self.wpm = tk.Label(self.stats_frame, text="0 w/m", borderwidth=3, relief="solid",fg='black',highlightcolor='black',background='lightgrey', font=("Helvetica", 24))
        self.wpm.grid(column=1,row=0,pady=10,ipadx=20,ipady=10)

        self.paragraph = tk.Label(self, text=self.current_paragraph,fg='black',background='lightgrey', font=("Helvetica", 17))
        self.paragraph.grid(row=2,column=0,columnspan=3,pady=10)

        self.text_input = tk.Text( height=8, width=70,background='white',fg='black',font=(14))
        self.text_input.grid(row=3,column=0,columnspan=3,pady=10)
        self.text_input.bind("<KeyRelease>", self.start)
       
        self.restart = tk.Button(text='Restart',highlightbackground = "black",  
                         highlightthickness = 1,background='black',command=self.reset)
        self.restart.config(height = 2, width = 6)
        self.restart.grid(row=4,column=1,pady=10)

    def start(self,event):
        if not self.running:
            self.running = True
            t = threading.Thread(target=self.times)
            t.start()
        if not self.paragraph.cget("text").startswith(self.text_input.get("1.0","end-1c")):
            self.text_input.config(fg='red')
        else:
            self.text_input.config(fg='black')
        if self.paragraph.cget("text") == self.text_input.get("1.0","end-1c"):
             self.running = False
             self.text_input.config(fg='green')

    def times(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            seconds = self.counter
            words = len(self.text_input.get("1.0","end-1c").split(' '))
            wpm = words // (seconds / 60)
            self.timer.config(text=f'{seconds:.1f} s')
            self.wpm.config(text=f'{wpm:.0f} w/m')
    def reset(self):
        self.running = False
        self.counter = 0
        self.text_input.delete("1.0","end-1c") 
        self.timer.config(text=f'{0} s')
        self.wpm.config(text=f'{0} w/m')
        self.current_paragraph = random.choice(self.paragraphs)
        self.paragraph.config(text=f'{self.current_paragraph}')




if __name__ == "__main__":
    app = TypingTestApp()
    app.mainloop()
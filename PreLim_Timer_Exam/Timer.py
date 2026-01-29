import tkinter as tk                                                    #Used to build the window and widgets,etc
import winsound


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("800x500")
        self.window.title("TIMER")
        self.window.configure(bg='#1c1c1c')

        self.amount_time = tk.DoubleVar()                               #Value used for timer comes from
        self.show_input_screen()

        self.text_label = TextLabel(self.window, self.amount_time)      #Lets "TextLabel" for composition "self.window and self.amount_time" and lets the use for a class additionally holds the value for the "self.amount_time"
        self.start_button = StartButton(self.window, self.start_timer)  #Lets "StartButton" for composition "self.window, self.start_timer" and lets the use for a class additionally holds the trigger for "start_timer"

        self.window.mainloop()

    def show_input_screen(self):
        for widget in self.window.winfo_children():                     #loops the "self.window" widgets
            widget.destroy()                                            #Destroys the looped widgets

        # After being deleted reestablishes the widgets again
        self.text_label = TextLabel(self.window, self.amount_time)
        self.start_button = StartButton(self.window, self.start_timer)

    def start_timer(self):
        for widget in self.window.winfo_children(): #Loop all the widgets from self.window
            widget.destroy()                        #Delets the widgets with the loop


        total_seconds = self.amount_time.get()      #Gets the amount from the entrybox widget
        self.timer_label = tk.Label(                #Makes the text label for the timer
            self.window,
            text="",
            fg="white",
            bg="#1c1c1c",
            font=("Times new roman", 80)
        )
        self.timer_label.pack(expand=True)
        self.countdown(total_seconds)

    def countdown(self, remaining):
        if remaining > 0:                #calculation for time
            hours = int(remaining // 3600)
            minutes = int((remaining // 60) % 60)
            seconds = int(remaining % 60)
            milliseconds = int((remaining - int(remaining)) * 100)

            time_str = f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds:02}" #For formatting
            self.timer_label.config(text=time_str)

            #Update every 10 ms
            self.window.after(10, self.countdown,  remaining - 0.01)
        else:
            self.timer_label.config(text="Time's up!")
            winsound.PlaySound("alarm.wav", winsound.SND_FILENAME | winsound.SND_ASYNC) #Play sound when countdown is 0

            self.restart_button = tk.Button(
                self.window,
                text="Restart",
                font=("Times new roman", 50),
                command=self.show_input_screen              # Calls the method to restart and ask for an amount of time
            )
            self.restart_button.pack(pady=50)



class TextLabel:
    def __init__(self, parent, variable):
        self.label = tk.Label(
            parent,
            text="Enter in SECONDS",
            fg="white",
            bg="#1c1c1c",
            font=("Times new roman", 50),
        )
        self.label.pack(pady=50)

        self.entrybox = tk.Entry(
            parent,
            font=("Times new roman", 50),
            textvariable = variable
        )
        self.entrybox.pack(padx=10, pady=0)



class StartButton:
    def __init__(self, parent, command):
        self.button = tk.Button(
            parent,
            text="Press to Start",
            font=("Times new roman", 50),
            command=command
        )
        self.button.pack(padx=0, pady=30)



def main():
    MainWindow()
if __name__ == "__main__":
    main()
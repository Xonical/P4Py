import sys
import tkinter as tk
import tkinter.font as tkFont
import subprocess

''' Subprocess '''
class MySubprocess:
    @staticmethod
    def run_command() -> [str]:
        # /B -> only names, /A:-D ->only files, "*.txt"-> only text files, /A:-H -> no hidden files, "/s" -> full file names
        cmd = ["dir", "/B", "/A:-D", "*.txt", "/A:-H", "/s"]
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp1252')
        output, error = process.communicate()
        if process.returncode != 0:
            print(f"Fehler beim Ausfuehren des Befehls {cmd}:")
            print(error)
            return []
        return output.splitlines()

''' Button '''
class MyButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.configure(bg = "#e9e9ed")
        ft = tkFont.Font(family='Times',size=16)
        self.configure(font = ft)
        self.configure(width = 40)
        self.configure(fg = "#000000")
        self.configure(anchor= 'w')
        self.bind("<Button-1>", self.on_triggered)
        self.bind("<Return>", self.on_triggered)
        self.bind('<FocusIn>', self.button_focus_in)
        self.bind('<FocusOut>', self.button_focus_out)

    def on_triggered(self, event):
        if(self["text"] == "Anwendung beenden"):
            sys.exit()
        print(self["text"])
        subprocess.Popen(["notepad.exe", self["text"]])
    
    def button_focus_in(self, event):
        event.widget.configure(background='red')

    def button_focus_out(self, event):
        event.widget.configure(background='SystemButtonFace')

''' Top Level Window '''
class WindowContainer(object):
    def __init__(self, window: tk.Tk, process_output: [str]):
 
        # Frameless
        window.overrideredirect(True)
        
        # wisdth, height, x, y
        window.geometry("480x720+600+300")

        # Always on top                 
        window.attributes("-topmost", True)

        my = MyButton(window, text="Anwendung beenden")
        my.grid(row=0, column=0)
        my.focus()

        for index, line in enumerate(process_output):
            my = MyButton(window, text=line)
            my.grid(row=index + 1, column=0)

if __name__ == "__main__":
     process_output: [str] = MySubprocess.run_command()
     window = tk.Tk()
     WindowContainer(window, process_output)
     window.mainloop()
    
import sys
import tkinter as tk
import tkinter.font as tkFont
import subprocess


''' Subprocess '''
class MySubprocess:
    @staticmethod
    def run_command() -> [str]:
        # Replace p4out.exe to p4 and add parameter like p4 changes -c CLIENT -s pending
        cmd = ["p4out.exe"]
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
        ft = tkFont.Font(family='Times',size=14)
        self.configure(font = ft)
        self.configure(width = 80)
        self.configure(fg = "#000000")
        self.configure(anchor= 'w')
        self.bind("<Button-1>", self.on_triggered)
        self.bind("<Return>", self.on_triggered)
        self.bind('<FocusIn>', self.button_focus_in)
        self.bind('<FocusOut>', self.button_focus_out)
        filename: str = "c:\\dev\\project_foo\\bar.cpp"
        self.p4_open_cmd = self.create_open_command(filename)

    def create_open_command(self, filename: str) -> str:
        changelistnumber = self["text"][7:13]
        return f"p4 open -c {changelistnumber} {filename}"

    def on_triggered(self, event):
        if(self["text"] == "Anwendung beenden"):
            sys.exit()
        print(self.p4_open_cmd)
        sys.exit()
    
    def button_focus_in(self, event):
        event.widget.configure(background='red')

    def button_focus_out(self, event):
        event.widget.configure(background='SystemButtonFace')

''' Top Level Window '''
class WindowContainer(object):
    def __init__(self, window: tk.Tk, process_output: [str]):
 
        # Framelessdir
        window.overrideredirect(True)
        
        # width, height, x, y
        width = 780
        height = 296
        screenwidth = window.winfo_screenwidth()
        screenheight = window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 4)
        window.geometry(alignstr)

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
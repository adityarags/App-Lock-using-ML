import tkinter as tk                
from tkinter import BOTTOM, font as tkfont
from tkinter.constants import END
from tkinter.ttk import *
from unicodedata import digit
from PIL import ImageGrab
import DigitRecognizerModule
import FaceRecognizerModule




class ApplicationMaster(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)


        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in [StartScreen,FaceRecognitionScreen,DigitRecognitionScreen,WrongAuthenticationScreen,ApplicationEntryScreen]:
            
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.showFrame("StartScreen")

    def showFrame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller

        TextOnScreen1= tk.Label(self,text="PLEASE AUTHENTICATE YOURSELF!")
        TextOnScreen1.config(font=('Helvatical bold',20))
        TextOnScreen1.pack()

        ButtonOnScreen1 = tk.Button(self,text="Face Recognition",command =lambda: controller.showFrame("FaceRecognitionScreen"))
        ButtonOnScreen1.config(height=5, width=55)
        ButtonOnScreen1.pack(side = "left")

        ButtonOnScreen2 = tk.Button(self,text="Digit Recognition",command =lambda: controller.showFrame("DigitRecognitionScreen"))
        ButtonOnScreen2.config(height=5, width=55)
        ButtonOnScreen2.pack(side = "right")

class FaceRecognitionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ButtonOnScreen1 = tk.Button(self,text="Capture your Face",command =lambda: self.finalizeFace())
        ButtonOnScreen1.config(height=5, width=20)
        ButtonOnScreen1.pack()


        ButtonOnScreen2 = tk.Button(self,text="Go Back",command =lambda: controller.showFrame("StartScreen"))
        ButtonOnScreen2.config(height=5, width=20)
        ButtonOnScreen2.pack()
    
    def finalizeFace(self):
        x = FaceRecognizerModule.showFace(FaceRecognizerModule.readCamera())
        if x:
            self.controller.showFrame("ApplicationEntryScreen")

        else:
            self.controller.showFrame("WrongAuthenticationScreen")


class DigitRecognitionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.passwd = ""
        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "black", cursor="cross")
        self.label = tk.Label(self, text="Write Your Digit", font=("Helvetica", 20))
        self.classify_btn = tk.Button(self, text = "Add Digit", command = self.addDigit) 
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)

        self.canvas.grid(row=0, column=0, pady=2 )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

        
    def clear_all(self):
        self.canvas.delete("all")
        self.passwd = ""
        self.label.configure(text=self.passwd)


    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='white',outline="")

    def addDigit(self):
        self.canvas.delete("all")
        ImageGrab.grab((10,95,350,400)).save("digit" + '.jpg')
        val = DigitRecognizerModule.predict_img()
        self.passwd += str(val)
        self.label.configure(text=self.passwd)
        if len(self.passwd) == 4:
            if self.passwd == "6246":
                self.passwd = ""
                self.controller.showFrame("ApplicationEntryScreen")
            else:
                self.controller.showFrame("WrongAuthenticationScreen")

class ApplicationEntryScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        TextOnScreen1= tk.Label(self,text="You are Authorized to Access the Application!")
        TextOnScreen1.config(font=('Helvatical bold',20))
        TextOnScreen1.pack()
        ButtonOnScreen1 = tk.Button(self,text = "Log Out", command = lambda : self.openApp())
        ButtonOnScreen1.pack()
    
    def openApp(self):
        self.controller.showFrame("StartScreen")
class WrongAuthenticationScreen(tk.Frame):
    def __init__(self, parent, controller):
        self.__name__="WrongAuthenticationScreen"
        tk.Frame.__init__(self, parent)
        self.controller = controller
        TextOnScreen1= tk.Label(self,text="Not Authenticated")
        TextOnScreen1.config(font=('Helvatical bold',20))
        TextOnScreen1.pack()
        ButtonOnScreen1 = tk.Button(self,text = "Log Out", command = lambda : controller.showFrame("StartScreen"))
        ButtonOnScreen1.pack()
        
def main():
    application = ApplicationMaster()
    application.geometry("740x400")
    application.title("Our Application")
    application.mainloop()


main()
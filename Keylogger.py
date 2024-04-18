import tkinter as tk

def press(event):
     print("Keypress detected!")    
     key = event.keysym
     with open("hi.txt", "a") as f:
         f.write(key + "\n")
     with open("hi.txt", "r") as f:
         a = f.readlines()
         print(a)
root = tk.Tk()

root.title("keylogger")
label = tk.Label(root, text= "click this button to start the keylogger")
label.pack()
root.geometry("300x300")

button = tk.Button(root, text="start")
root.bind("<KeyPress>", press)
button.pack()

root.mainloop()

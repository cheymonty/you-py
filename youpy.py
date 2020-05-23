import sqlite3
import re
import sys
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import font as font
from pytube import YouTube



Label(text="YouTube link").pack()
linkentry = Entry()
linkentry.pack()
Label(text="Save video as").pack()
titleentry = Entry()
titleentry.pack()


v = IntVar()
v.set(0)

output = ["360p", "720p", "1080p (VIDEO ONLY)"]
Label(text="Select resolution").pack()

for i, res in enumerate(output):
    Radiobutton(text=res, variable=v, value=i).pack()

extension = IntVar()
Label(text="Select type").pack()
types = ["Audio", "Video"]
for i, ex in enumerate(types):
    Radiobutton(text=ex, variable=extension,value=i).pack()

connection = sqlite3.connect("videodata.db")
db = connection.cursor()

def download():
    link = linkentry.get()
    title = titleentry.get()
    ex = extension.get()
    if len(link) == 0:
        messagebox.showwarning("Warning", "Insert a link!")
        return

    # DO SANITIZATION

    try:   
        yt = YouTube(link)
    except:
        messagebox.showwarning("Link", "Invalid Link!")
        return
    
    if ex == 0:
        streams = yt.streams.filter(only_audio=True)
    elif v.get() == 0 or v.get() == 1:
        streams = yt.streams.filter(progressive=True, file_extension='mp4', resolution = output[v.get()])
    else:
        streams = yt.streams.filter(file_extension='mp4', resolution = "1080p")
       
    directory = filedialog.askdirectory(initialdir="/", title='Select a directory') 

    if len(title) == 0:
        title = yt.title

    try:
        path = streams[0].download(directory, title)
    except:
        message = title + " is not available in " + output[v.get()]
        messagebox.showerror("Error", message)
        return

    if ex == 0:
        ex = "Audio"
    else:
        ex = "Video"

    db.execute("INSERT INTO VideoData VALUES (?,?,?)", (title, link, ex))
    connection.commit()
   
    
    pathmessage = "Download is complete, the video is saved at " + path 
    messagebox.showinfo("Download Complete!", pathmessage)


   
def myexit():
    connection.close()
    exit()


def history():
    historywin = Tk()
    historywin.title('Download History')
    historywin.geometry("500x500")
    db.execute("SELECT Title,Link,Format FROM VideoData")
    history = db.fetchall()

    count = 1
    if not history:
        Label(historywin, text="You haven't downloaded any videos yet!").pack()
    else:
        for data in history:
            Label(historywin, text=count, font='Helvetica 22 bold').pack()
            t = "Title: " + data[0] 
            l = "Link: " + data[1]
            f = "Format: " + data[2]
            Label(historywin,text=t, font='Helvetica 18').pack(anchor = "w")
            Label(historywin,text=l, font='Helvetica 18').pack(anchor = "w")
            Label(historywin,text=f, font='Helvetica 18').pack(anchor = "w")
            count += 1

    historywin.mainloop()


root = Tk()
root.title('YouPy Downloader')
root.geometry("600x600")
root.withdraw()

Button(text="Download!", command=lambda: download()).pack()
Button(text="Exit", command=lambda: myexit()).pack()
Button(text="Show download history", command=lambda: history()).pack()


root.mainloop()




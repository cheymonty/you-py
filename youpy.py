import sqlite3
import sys
from tkinter import Label,Button,Entry,IntVar,Radiobutton,Tk,messagebox, filedialog, font
from pytube import YouTube

Label(text="YOUPY", fg='red', font='Courier 35 bold').grid(row=0,column=2,padx=10,pady=10)

Label(text="YouTube link").grid(row=1, column=0, padx=5, pady=10)
linkentry = Entry()
linkentry.grid(row=2, column=0, padx=5, pady=10)


Label(text="Save as").grid(row=5, column=0, padx=10, pady=10)
titleentry = Entry()
titleentry.grid(row=6, column=0, padx=10, pady=10)


v = IntVar()
v.set(0)

output = ["360p", "720p", "1080p"]
Label(text="Select resolution (1080p video is silent):").grid(row=1, column=2, padx=10, pady=10)

col = 3
r = 1
for i, res in enumerate(output):
    if col == 5:
        col = 3
        r = 2
    Radiobutton(text=res, variable=v, value=i).grid(row=r, column=col, padx=10, pady=10)
    col += 1


extension = IntVar()
Label(text="Select format:").grid(row=4, column=2, padx=10, pady=10)
types = ["Audio", "Video"]

col = 3
for i, ex in enumerate(types):
    Radiobutton(text=ex, variable=extension,value=i).grid(row=4, column=col, padx=10, pady=10)
    col += 1

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
    else:
        streams = yt.streams.filter(progressive=True, file_extension='mp4', resolution = output[v.get()])
       
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

Button(text="Download!", command=lambda: download()).grid(row=7, column=2, padx=10, pady=10)
Button(text="Download history", command=lambda: history()).grid(row=7, column=3, padx=10, pady=10)
Button(text='Exit', command=lambda: myexit()).grid(row=8, column=2, padx=10, pady=10)



root.mainloop()




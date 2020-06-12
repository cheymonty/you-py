import sqlite3
import sys
from tkinter import Label,PhotoImage,Button,END,Entry,StringVar,OptionMenu,Radiobutton,Tk,messagebox, filedialog, font
from pytube import YouTube

bg = "#fe7a47"
font = "Helvetica 20"
text_color = "#fcfdfe"

root = Tk()

root.title('You-Py Downloader')
root.geometry("800x500")
root.configure(bg=bg)


Label(root,text="You-Py", fg=text_color,bg=bg, font='Arial 60 bold').grid(row=0,column=2,padx=10,pady=10)

Label(root,text="YouTube link", bg=bg, fg=text_color, font=font).grid(row=1, column=0, padx=5, pady=10)
linkentry = Entry(root,bg=bg,fg=text_color)
linkentry.grid(row=2, column=0, padx=5, pady=10)


Label(root,text="Save as", bg=bg, font=font, fg=text_color).grid(row=5, column=0, padx=10, pady=10)
titleentry = Entry(root, bg=bg, fg=text_color)
titleentry.grid(row=6, column=0, padx=10, pady=10)


output = ["360p", "720p", "1080p-Silent"]
Label(root, text="Select resolution:", bg=bg, fg=text_color, font=font).grid(row=1, column=3, padx=10, pady=10)

v = StringVar()
v.set(output[0])

OptionMenu(root, v, *output).grid(row=1,column=4)



Label(root, text="Select format:", bg=bg, fg=text_color, font=font).grid(row=4, column=3, padx=10, pady=10)
types = ["Video","Audio"]
extension = StringVar()
extension.set(types[0])

OptionMenu(root, extension, *types).grid(row=4,column=4)

connection = sqlite3.connect("videodata.db")
db = connection.cursor()

poweroff_image = PhotoImage(file="images/poweroff.png")
poweroff_image = poweroff_image.subsample(2, 2) 


Button(root, text="Download!", command=lambda: download(), fg=bg).grid(row=7, column=3, padx=10, pady=10)
Button(root,text="Download history", command=lambda: history(), fg=bg).grid(row=7, column=4, padx=10, pady=10)
Button(root, image=poweroff_image, command=lambda: myexit(), fg=bg).grid(row=8, column=2, padx=10, pady=10)

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
    
    if ex == 'Audio':
        streams = yt.streams.filter(only_audio=True)
    else:
        streams = yt.streams.filter(progressive=True, file_extension='mp4', resolution = v.get().replace(" (Silent)", ""))
       
    directory = filedialog.askdirectory(initialdir="/", title='Select a directory') 

    if len(title) == 0:
        title = yt.title

    try:
        path = streams[0].download(directory, title)
    except:
        message = title + " is not available in " + v.get().replace(" (Silent)","")
        messagebox.showerror("Error", message)
        return

    db.execute("INSERT INTO VideoData VALUES (?,?,?)", (title, link, ex))
    connection.commit()
   
    
    pathmessage = "Download is complete, the video is saved at " + path 
    messagebox.showinfo("Download Complete!", pathmessage)
    linkentry.delete(0,END)
    titleentry.delete(0,END)

    return

   
def myexit():
    connection.close()
    exit()


def history():
    bg_color = "#1995ad"
    t_color = 'white'
    historywin = Tk()
    historywin.title('Download History')
    historywin.geometry("500x500")
    historywin.configure(bg=bg_color)
    db.execute("SELECT Title,Link,Format FROM VideoData")
    history = db.fetchall()

    count = 1
    if not history:
        Label(historywin, text="You haven't downloaded any videos yet!", bg=bg_color, fg=t_color).pack()
    else:
        for data in history:
            Label(historywin, text=count, font='Arial 22 bold', bg=bg_color, fg=t_color).pack()
            t = "Title: " + data[0] 
            l = "Link: " + data[1]
            f = "Format: " + data[2]
            Label(historywin,text=t, font='Helvetica 18', bg=bg_color, fg=t_color).pack(anchor = "w")
            Label(historywin,text=l, font='Helvetica 18', bg=bg_color, fg=t_color).pack(anchor = "w")
            Label(historywin,text=f, font='Helvetica 18', bg=bg_color, fg=t_color).pack(anchor = "w")
            count += 1

    historywin.mainloop()



root.mainloop()

from tkinter import *
import pygame
import threading
import time
from mutagen.mp3 import MP3
from tkinter.messagebox import *
from tkinter import ttk
from PIL import Image,ImageTk
import socket
import pickle

class Audio:
    def __init__(self, master,song_list):
        self.master=master
        self.song_list = song_list

        pygame.init()
        pygame.mixer.init()
        
        PLAY="◀"
        PAUSE="⏸"
        UNPAUSE="⏵"
        RWD="⏪"
        FWD="⏩"
        mute= "🔇"
        unmute= "🔊"
        vol_mute=0.0
        vol_unmute=1

        #Listbox
        self.scroll = Scrollbar(master)
        self.play_list = Listbox(master, font="Arial 12 bold", bd=1,
              bg="gray12", width=36, height=29, selectbackground="black")
        self.play_list.place(x=650, y=50)
        self.scroll.place(x=974, y=50, height=584, width=16)
        self.scroll.config(command=self.play_list.yview)
        self.play_list.config(yscrollcommand=self.scroll.set)
        self.song_list.reverse();  
        for x in self.song_list: 
            self.play_list.insert(0,x.replace(".mp3",""))
        index=0
        self.play_list.selection_set(index)
        self.play_list.see(index)
        self.play_list.activate(index)
        self.play_list.selection_anchor(index)
        
        #Background photo
        self.back_img= Image.open("photo.png")
        self.back_img= self.back_img.resize((647,632),Image.ANTIALIAS)
        self.img=ImageTk.PhotoImage(self.back_img)
        self.img_label= Label(master)
        self.img_label.grid(row=0,column=0)
        self.img_label["compound"]= LEFT
        self.img_label["image"]= self.img

        #Audiobook title
        self.var=StringVar()
        self.var.set(".......... WELCOME .......... ")
        self.song_title= Label(master,font="Arial 14 bold",bg="gray9",fg="white",width=50,textvariable=self.var)
        self.song_title.place(x=17,y=520)

        # FUNCTIONS
        #Duration of the audiobook
        def get_duration():
            global current_time
            current_time=pygame.mixer.music.get_pos()/1000
            formatted_time=time.strftime("%H:%M:%S",time.gmtime(current_time))
            next_one=self.play_list.curselection()
            song=self.play_list.get(next_one)
            song_timer=MP3("AudiobookFiles/"+song+".mp3")
            song_length=int(song_timer.info.length)
            format_for_length=time.strftime("%H:%M:%S",time.gmtime(song_length))
            self.label_time2.config(text=f"{format_for_length}")
            self.label_time1.config(text=f"{formatted_time}")
            self.progress["maximum"]=song_length
            self.progress["value"]=int(current_time)
            master.after(100,get_duration)

        #Play audiobook
        def play_music():
            track=self.play_list.get(ACTIVE) 
            pygame.mixer.music.load("AudiobookFiles/"+track+".mp3")
            self.var.set(track)
            pygame.mixer.music.play()
            get_duration()
                
        def play_thread():
            threads=threading.Thread(target=play_music)
            threads.start()
        
        master.bind("<p>",lambda x: play_thread())

        #Pause audiobook
        def pause_music():
            if self.play["text"]==PAUSE:
                pygame.mixer.music.pause()
                self.play["text"]=UNPAUSE
            elif self.play["text"]==UNPAUSE:
                pygame.mixer.music.unpause()
                self.play["text"]=PAUSE

        def pause_thread():
            threads=threading.Thread(target=pause_music)
            threads.start()
        
        master.bind("<space>",lambda x: pause_thread())

        #Volume control
        def volume(x):
            pygame.mixer.music.set_volume(self.volume_slider.get())

        #Mute and unmute function
        def muted():
            if self.mute["text"]==unmute:
                pygame.mixer.music.set_volume(vol_mute)
                self.volume_slider.set(vol_mute)
                self.mute["fg"]="red"
                self.mute["text"]=mute
            elif self.mute["text"]==mute:
                pygame.mixer.music.set_volume(vol_unmute)
                self.volume_slider.set(vol_unmute)
                self.mute["fg"]="white"
                self.mute["text"]=unmute
        
        def mut():
            threads=threading.Thread(target=muted)
            threads.start()
        self.master.bind("<m>", lambda x: mut())

        #Next audiobook file
        def next_song():
            next_one= self.play_list.curselection()
            next_one= next_one[0]+1
            song= self.play_list.get(next_one)
            pygame.mixer.music.load("AudiobookFiles/"+song+".mp3")
            pygame.mixer.music.play()
            self.play_list.select_clear(0,END)
            self.play_list.activate(next_one)
            self.play_list.selection_set(next_one,last=None)
            self.var.set(song)
            get_duration()
            self.play_list.see(next_one)

        def next():
            threads=threading.Thread(target=next_song)
            threads.start()

        #Previous audiobook file
        def prev_song():
            next_one= self.play_list.curselection()
            next_one= next_one[0]-1
            song= self.play_list.get(next_one)
            pygame.mixer.music.load("AudiobookFiles/"+song+".mp3")
            pygame.mixer.music.play()
            self.play_list.select_clear(0,END)
            self.play_list.activate(next_one)
            self.play_list.selection_set(next_one,last=None)
            self.var.set(song)
            get_duration()
            self.play_list.see(next_one)

        def prev():
            threads=threading.Thread(target=prev_song)
            threads.start()

        self.master.bind("<Left>", lambda x: prev())
        self.master.bind("<Right>", lambda x: next())

        #Shortcut1
        def about():
            top= Toplevel()
            top.title("ABOUT LiZn")
            top.geometry("740x220")
            top.resizable(width=0, height=0)
            top.iconbitmap('icon.ico')
            user_manual=[
                "LiZn is an audiobook streaming application founded in the year 2022. ",
                "It was found by Deeban Sankar as part of a project for the subject COMPUTER NETWORKS during his 3rd year. ",
                "This is a application which is coded using the programming language Python. ",
                "The server side and client side of LiZn are linked by using TCP Socket."
            ]
            for i in user_manual:
                manual= Label(top, text=i, width=50, height=3, font="Helvetica, 11",bg="gray12", fg="white")
                manual.pack(side=TOP, fill="both")

        #Shortcut2
        def shortcut():
            top=Toplevel()
            top.title("SHORTCUT KEYS")
            top.geometry("220x375")
            top.resizable(width=0,height=0)
            top.iconbitmap('icon.ico')
            user_manual=[
                "PLAY ---> p button",
                "PAUSE ---> Space button",
                "UNPAUSE ---> Space button",
                "RWD= ---> Left Arrow button",
                "FWD ---> Right Arrow button",
                "MUTE ---> m button",
                "UNMUTE ---> m button"
            ]
            for i in user_manual:
                manual= Label(top, text=i, width=50, height=3, font="Helvetica, 11",bg="gray12", fg="white")
                manual.pack(side=TOP, fill="both")

        
        self.menu=Menu(self.img_label,font="Helvetica, 3")
        master.config(menu=self.menu)
        self.menu.add_command(label="ABOUT",command=about)
        self.menu.add_command(label="SHORTCUTS",command=shortcut)
        
        self.separator=ttk.Separator(self.img_label, orient="horizontal")
        self.separator.place(relx=0, rely=0.87, relwidth=1, relheight=1)

        #Buttons
        self.play= Button(self.master, text=PLAY, width=2,height=1, bd=1, bg="gray12", fg="white", font="Helvetica, 15", command=play_thread)
        self.play.place(x=287,y=590)
        self.play= Button(self.master, text=PAUSE, width=2,height=1, bd=1, bg="gray12", fg="white", font="Helvetica, 15",command=pause_thread)
        self.play.place(x=318,y=590)
        self.next= Button(self.master, text=FWD, width=3, bd=1, bg="gray12", fg="white", font="Helvetica, 15",command=next)
        self.next.place(x=349, y=590)
        self.prev= Button(self.master, text=RWD, width=3, bd=1, bg="gray12", fg="white", font="Helvetica, 15",command=prev)
        self.prev.place(x=245, y=590)
        self.mute= Button(self.master, text=unmute, width=3, bd=1, bg="gray12", fg="white", font="Helvetica, 15",command=muted)
        self.mute.place(x=475, y=590)
        
        #Volume slider
        self.style= ttk.Style()
        self.style.configure("myStyle.Horizontal.TScale",background="black")
        self.volume_slider= ttk.Scale(self.img_label,from_=0,to_=1, orient=HORIZONTAL, value=5, length=120,style="myStyle.Horizontal.TScale", command=volume)
        self.volume_slider.place(x=525, y=595)

        #Progress bar
        self.progress= ttk.Progressbar(self.img_label,orient=HORIZONTAL, value=0, length =400 , mode='determinate')
        s=ttk.Style()
        s.theme_use('clam')
        s.configure("blue.Horizontal.TProgressbar",foreground='white',background='white')
        self.progress.place(x=115,y=560)

        #Duration1
        self.label_time1= Label(master,text="00:00:00",width=8, font="Arial, 10",bg="gray12", fg="white")
        self.label_time1.place(x=38, y=560)

        #Duration2
        self.label_time2= Label(master,text="00:00:00",width=8, font="Arial, 10",bg="gray12", fg="white")
        self.label_time2.place(x=528, y=560)

        self.label_playlist=Label(master, text="📕 AudioBook Playlist 📕",width=20,bg="gray12",fg="white", font="Arial 16 bold")
        self.label_playlist.place(x=691,y=10)

#FTP Client
def netcode():
    csFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csFT.connect((socket.gethostname(), 8757))
    music_file = 'music.mp3'
    list = pickle.loads(csFT.recv(500000))
    print(list)
    print("Receiving..")
    for f in list:
        with open("AudiobookFiles/{}".format(f), 'wb') as fw:
            while True:
                data = csFT.recv(2048)
                if data == b'EOF':
                    break
                fw.write(data)
            fw.close()
        print("Received..{}".format(f))
    
    print("All Files received successfully")
    csFT.close()
    return list ; 

    
def main(list):
    #Define window
    root=Tk()
    ui=Audio(root,list)
    root.title('LiZn')
    root.iconbitmap('icon.ico')
    root.geometry('990x635')
    root.config(bg='gray12')
    root.resizable(width=0,height=0)
    #Runs the window in a loop
    root.mainloop()

if __name__=="__main__":
    list = netcode()
    main(list)


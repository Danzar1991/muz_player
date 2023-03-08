from tkinter import *
import pygame
import eyed3
import os
from tkinter import filedialog
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from PIL import ImageTk, Image
from tkinter import messagebox
import random
from threading import Timer
import time


class Musical_Timer:
    def __init__(self, timeout, function):
        self.timeout = timeout
        self.function = function
        self.timer = Timer(self.timeout, self.function)

        self.start_time = None
        self.cancel_time = None

    def stop(self):
        self.timer.cancel()

    def start(self):
        self.start_time = time.time()
        self.timer.start()

    def pause(self):
        self.cancel_time = time.time()
        self.timer.cancel()
        return self.remaining_time()

    def resume(self):
        self.timeout = self.remaining_time()
        self.timer = Timer(self.timeout, self.function)
        self.start_time = time.time()
        self.timer.start()

    def remaining_time(self):
        if self.start_time is None or self.cancel_time is None:
            return self.timeout
        return self.timeout - (self.cancel_time - self.start_time)


# Defining MusicPlayer Class
class MusicPlayer:
    # Defining Constructor
    def __init__(self, root):
        self.root = root
        # Title of the window
        self.root.title("Music Player")
        self.root.geometry("591x588")
        self.root.resizable(False, False)

        self.photo = PhotoImage(file="images\\phone.png")
        self.win = Label(self.root, image=self.photo)
        self.win.pack()

        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable

        self.value = DoubleVar()
        self.index = IntVar()
        self.size = IntVar()
        self.playdict = {}
        self.play = True
        self.next = False
        self.prev = False
        self.pause = False
        self.count_rand = 0
        self.count_repeat = 0


        # Inserting Play Button
        self.photo_play = PhotoImage(file="images\\play.png")
        self.play_btn = Button(self.win, image=self.photo_play, command=self.playsong, borderwidth=None, bg="grey23")
        self.play_btn.place(x=25, y=270)

        self.photo_pause = PhotoImage(file="images\\pause.png")
        self.pause_btn = Button(self.win, image=self.photo_pause, command=self.pausesong, borderwidth=None, bg="grey23")
        self.pause_btn.place(x=467, y=370)

        self.photo_open = PhotoImage(file="images\\open.png")
        self.open_btn = Button(self.win, image=self.photo_open, command=self.open_file, borderwidth=None, bg="grey23")
        self.open_btn.place(x=30, y=370)

        self.photo_prev = PhotoImage(file="images\\previos.png")
        self.prev_btn = Button(self.win, image=self.photo_prev, command=self.previoussong, borderwidth=None, bg="grey23")
        self.prev_btn.place(x=377, y=370)

        self.photo_next = PhotoImage(file="images\\next.png")
        self.next_btn = Button(self.win, image=self.photo_next, command=self.nextsong, borderwidth=None, bg="grey23")
        self.next_btn.place(x=513, y=370)

        self.photo_repeat = PhotoImage(file="images\\repeat.png")
        self.repeat_btn = Button(self.win, image=self.photo_repeat, command=self.repeatsong, borderwidth=None, bg="grey23")
        self.repeat_btn.place(x=78, y=370)

        self.photo_random = PhotoImage(file="images\\random.png")
        self.random_btn = Button(self.win, image=self.photo_random, command=self.randomsong, borderwidth=None, bg="grey23")
        self.random_btn.place(x=124, y=370)

        self.photo_stop = PhotoImage(file="images\\stop.png")
        self.stop_btn = Button(self.win, image=self.photo_stop, command=self.stopsong, borderwidth=None, bg="grey23")
        self.stop_btn.place(x=423, y=370)

        self.vol_scaler = Scale(self.win, variable =self.value, length=465, from_=0, to=20, label='Volume', bd="0", orient='horizontal', fg='black',
                         bg='grey23',  command=self.volume, width="30")
        self.vol_scaler.set(5)
        self.vol_scaler.place(x=94, y=270)

        # Creating Playlist Frame
        self.rounded_frame = PhotoImage(file="images\\rounded_frame.png")
        roundedframe = Label(self.root, image=self.rounded_frame)
        roundedframe.place(x=5, y=435)
        songsframe = LabelFrame(self.root, text="Song Playlist", font=("times new roman", 15, "bold"), bg="grey23",
                                fg="white", bd=5, relief=FLAT)
        songsframe.place(x=10, y=440, width=572, height=142)
        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        # Inserting Playlist listbox
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectbackground="grey23", selectmode=SINGLE,
                                font=("times new roman", 12, "bold"), bg="grey", fg="black", bd=5, relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)




    def volume(self, value):
        pygame.mixer.music.set_volume(self.value.get()/20)

    def stopsong(self):
        pygame.mixer.music.stop()
        self.timer.stop()


    def playsong(self):

        self.size = self.playlist.size()
        if self.size > 0:
            if self.play:
                if self.playlist.curselection():
                    self.index = self.playlist.curselection()[0]
                else:
                    self.index = 0

                self.playlist.selection_clear(0, END)
                self.playlist.selection_set(self.index)

                if self.count_rand%2 != 0:
                    self.index= random.randint(0, self.size-1)
                    self.playlist.selection_clear(0, END)
                    self.playlist.selection_set(self.index)
                    self.next = False
                    self.prev = False

                if self.next:
                    self.next = False
                    self.index = (self.index + 1) % self.size
                    self.playlist.selection_clear(0, END)
                    self.playlist.selection_set(self.index)

                if self.prev:
                    self.prev = False
                    if self.index - 1 >= 0:
                        self.index = self.index - 1
                    else:
                        self.index = self.index - 1 + self.size
                    self.playlist.selection_clear(0, END)
                    self.playlist.selection_set(self.index)



                # Loading Selected Song
                song = self.playdict[self.playlist.get(self.index)]
                pygame.mixer.music.load(song)
                mutagen_file = ID3(song)  # mutagen can automatically detect format and type of tags
                mutagen_info = int(round(MP3(song).info.length, 0))
                if self.count_repeat%2 == 0:
                    pygame.mixer.music.play()
                    self.timer = Musical_Timer(mutagen_info, self.nextaction)
                    self.timer.start()
                else:
                    pygame.mixer.music.play(-1)
                    self.timer = Musical_Timer(mutagen_info, self.nextaction)
                    self.timer.start()


                # Playing Selected Song

                icon = mutagen_file.get("APIC:3.jpeg")
                if icon:
                    with open('image.jpg', 'wb') as img:
                        img.write(icon.data)
                    img = Image.open('image.jpg')
                    new_img = img.resize((228, 228))
                    self.album_cover = ImageTk.PhotoImage(new_img)
                    image = Label(self.root, image=self.album_cover, borderwidth=0, relief="ridge")
                    image.place(x=185, y=30)
                else:
                    img = Image.open("C:\\Users\\User\\Desktop\\муз_плеер\\11-02-2023_18-05-49\\non_album_cover.png")
                    new_img = img.resize((228, 228))
                    self.album_cover = ImageTk.PhotoImage(new_img)
                    image = Label(self.root, image=self.album_cover, borderwidth=0, relief="ridge")
                    image.place(x=185, y=30)

            if self.pause:
                pygame.mixer.music.unpause()
                self.pause = False
                self.play = True
                self.timer.pause()
                self.pause_btn.configure(bg="grey23")


        else:
            messagebox.showerror('Ошибка','В плейлисте нет песен. Добавьте композиции в плейлист!')

    def nextaction(self):
        if self.count_repeat%2 != 0:
            return self.playsong()
        else:
            return self.nextsong()



    def nextsong(self):
        # Displaying Status
        self.next = True
        return self.playsong()

    def previoussong(self):
        # Displaying Status
        self.prev = True
        return self.playsong()


    def pausesong(self):
        self.size = self.playlist.size()
        if self.size > 0:
            pygame.mixer.music.pause()
            self.pause = True
            self.play = False
            self.timer.pause()
            self.pause_btn.configure(bg="PeachPuff4")
        else:
            messagebox.showerror('Ошибка','В плейлисте нет песен. Добавьте композиции в плейлист!')

    def repeatsong(self):
        self.count_repeat += 1
        if self.count_repeat % 2 != 0:
            self.repeat_btn.configure(bg="PeachPuff")
        else:
            self.repeat_btn.configure(bg="grey23")


    def randomsong(self):
        self.count_rand += 1
        if self.count_rand % 2 != 0:
            self.random_btn.configure(bg="PeachPuff")
        else:
            self.random_btn.configure(bg="grey23")


    def open_file(self):

        filepath = filedialog.askopenfilename()
        audiofile = eyed3.load(filepath)
        new_filename = "{0}-{1}.mp3".format(audiofile.tag.artist, audiofile.tag.title)
        if filepath != "":
            self.playlist.insert(END, new_filename)
            self.playdict[new_filename] = filepath




# Creating TK Container
root = Tk()
MusicPlayer(root)
def on_closing():
    if messagebox.askokcancel("Quit", "Вы действительно хотите закрыть плеер?"):
        root.destroy()
        os._exit(0)


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
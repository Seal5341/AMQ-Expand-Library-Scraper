# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 11:15:21 2021

@author: Seal
"""

import pandas as pd
import tkinter as tk

csvfile = 'combined.csv'

df = pd.read_csv(csvfile,encoding='utf-8')

window = tk.Tk()
window.title('Read AMQ Database GUI')
window.geometry('+1096+137')
window.resizable(True,True)
window.attributes('-topmost',True)

output_anime = tk.Label(window, text='Anime')
output_song = tk.Label(window, text='Song')
output_artist = tk.Label(window, text='Artist')

def getsonginfo(event='event'):
    filename = searchinput.get().split('/')[-1]
    search.configure(text='Search: ' + filename)
    songname, artistname = '', ''
    global output_anime, output_song, output_artist
    try:
        if filename.split('.')[-1] == 'webm':
            selection = df.loc[df['Webm Link'] == filename]
        else:
            if filename.split('.')[-1] != 'mp3':
                filename += '.mp3'
            selection = df.loc[df['Mp3 Link'] == filename]
        animename = str(selection['Anime Name'].values[0])
        songtype = str(selection['Song Type'].values[0])
        songname = str(selection['Song Name'].values[0])
        artistname = str(selection['Song Artist'].values[0])
        window.clipboard_clear()
        window.clipboard_append(animename)
    except:
        animename = 'Not Found'
        songtype = ''
        songname = 'Not Found'
        artistname = 'Not Found'
    output_anime.configure(text=animename + ' ' + songtype)
    output_song.configure(text='Song: ' + songname)
    output_artist.configure(text='Artist: ' + artistname)
    samesongartist(animename,songname,artistname)
    searchinput.delete('0', 'end')

def copysongtoclipboard():
    window.clipboard_clear()
    window.clipboard_append('/as ')
    window.clipboard_append(output_song['text'].split(' ')[1:])

def copyartisttoclipboard():
    window.clipboard_clear()
    window.clipboard_append('/aa ')
    window.clipboard_append(output_artist['text'].split(' ')[1:])
    
def copyall():
    window.clipboard_clear()
    window.clipboard_append('a/ ')
    window.clipboard_append(output_anime['text'].split(' ')[:-1])
    window.clipboard_append(' | ')
    window.clipboard_append(output_song['text'].split(' ')[1:])
    window.clipboard_append(' | ')
    window.clipboard_append(output_artist['text'].split(' ')[1:])

def samesongartist(animename,songname,artistname):
    try:
        dfsongartist = df.loc[df['Anime Name'] != animename].loc[df['Song Name'] == songname].loc[df['Song Artist'] == artistname]
    except:
        pass
    if len(dfsongartist) == 0:
        txt = 'No Dupe Found'
    else:
        txt = 'Dupes:'
        for i in range(len(dfsongartist)):
            txt += '\n' + dfsongartist['Anime Name'].values[i] + ' ' + dfsongartist['Song Type'].values[i]
    dupeanime1.configure(text=txt)

def frosty():
    window.clipboard_clear()
    window.clipboard_append(':muscle: 𐌅Ṝ๏𝓼Ƭץ :muscle:')

frosty_button = tk.Button(text='💪𐌅Ṝ๏𝓼Ƭץ💪', command=frosty)
frosty_button.grid(column=0, row=0)

button1 = tk.Button(text='Get Song Info', command=getsonginfo)
button3 = tk.Button(text='Copy Song to Clipboard', command=copysongtoclipboard)
button4 = tk.Button(text='Copy Artist to Clipboard', command=copyartisttoclipboard)
button5 = tk.Button(text='Copy All Metadata', command=copyall)

search = tk.Label(window, text='Search')
search.grid(column=0, row=1)
searchinput = tk.Entry(window)
searchinput.bind('<Return>', getsonginfo)
searchinput.grid(column=0, row=2)
button1.grid(column=0, row=3)

output_anime.grid(column=0, row=4)
output_song.grid(column=0, row=5)
output_artist.grid(column=0, row=6)
button3.grid(column=0, row=7)
button4.grid(column=0, row=8)
button5.grid(column=0, row=9)

dupeanime1 = tk.Label(window,text='Dupes')
dupeanime1.grid(column=0, row=10, rowspan=3)

def addsong():
    global df
    animename = animenameinput.get()
    songtype = songtypeinput.get()
    songname = songnameinput.get()
    songartist = songartistinput.get()
    mp3link = mp3linkinput.get().split('/')[-1]
    webmlink = webmlinkinput.get().split('/')[-1]
    new_row = {'Anime Name':animename, 'Song Type':songtype, 'Song Name':songname, 'Song Artist': songartist, 'Mp3 Link': mp3link, 'Webm Link': webmlink}
    df = df.append(new_row, ignore_index=True)
    df.to_csv(csvfile,index=False)
    animenameinput.delete('0', 'end')
    songtypeinput.delete('0', 'end')
    songnameinput.delete('0', 'end')
    songartistinput.delete('0', 'end')
    mp3linkinput.delete('0', 'end')
    webmlinkinput.delete('0', 'end')

tk.Label(window, text='Anime Name').grid(column=1, row=0)
animenameinput = tk.Entry(window)
animenameinput.grid(column=1, row=1)
tk.Label(window, text='Song Type').grid(column=1, row=2)
songtypeinput = tk.Entry(window)
songtypeinput.grid(column=1, row=3)
tk.Label(window, text='Song Name').grid(column=1, row=4)
songnameinput = tk.Entry(window)
songnameinput.grid(column=1, row=5)
tk.Label(window, text='Song Artist').grid(column=1, row=6)
songartistinput = tk.Entry(window)
songartistinput.grid(column=1, row=7)
tk.Label(window, text='Mp3 Link').grid(column=1, row=8)
mp3linkinput = tk.Entry(window)
mp3linkinput.grid(column=1, row=9)
tk.Label(window, text='Webm Link').grid(column=1, row=10)
webmlinkinput = tk.Entry(window)
webmlinkinput.grid(column=1, row=11)
addsongbutton = tk.Button(text='Add Song', command=addsong).grid(column=1, row=12)

window.mainloop()
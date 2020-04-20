# Arthur Xu
# Spotify Test
# April 8th, 2020

import spotipy, requests, random, time
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
from tkinter import *

cid = 'Enter spotify CID'
secret = 'Enter spotify secret code'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Make a list of last year's popular artists
page = requests.get("https://www.billboard.com/charts/year-end/2019/top-r-and-b-hip-hop-artists")
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.findAll(class_="ye-chart-item__title")
pool = []
for tabs in results:
    name = tabs.find('a')
    name = (name.text.strip())
    pool.append(name)

score = 0
highScore = 0
correctAnswer = ""
userGuess = ""


# Creating the window
window = Tk()
window.title("Spotify Guessing Game")
window.geometry('600x300')
window.configure(bg="#f060aa")


lbl1 = Label(window, text="Name #1")
lbl1.place(x=100, y=10)
lbl2 = Label(window, text="Name #2")
lbl2.place(x = 300, y= 10)
lbl3 = Label(window, text = "Result")
lbl3.place(x = 50, y = 100)

# Generate new people
def newPeople():

    global correctAnswer
    global userGuess
    
    correctAnswer = ""
    userGuess = ""
    
    one = random.choice(pool)
    two = random.choice(pool)

    while True:
        if one == two:
            two = random.choice(pool)
        else:
            break

    name = []
    name.append(one)
    name.append(two)
    lbl1.config(text=one)
    lbl2.config(text=two)

    popularity = []

    for i in name:
        results = sp.search('artist:'+i, type="artist", limit = 1)

        beans = results['artists']['items']
        if len(beans) > 0:
            artist = beans[0]
            url = artist['images'][0]['url']
            popularity.append(artist['popularity'])
            
    correctAnswer = "Beans"
    if popularity[0] > popularity[1]:
        correctAnswer = "1"
    else:
        correctAnswer = "2"

newPeople()

# When the user guesses artist 1
def clicked1():

    global correctAnswer
    global userGuess
    global score
    global highScore


    userGuess = "1"
    if userGuess == correctAnswer:
        score += 1
        if score > highScore:
            highScore = score
        lbl3.configure(text="Correct! Your score is now %s and your high score is %s" % (score, highScore))
    else:
        lbl3.configure(text="Incorrect! You loose! You ended with a score of %s and your high score is %s" % (score, highScore))
        score = 0
    lbl1.configure(text="")
    lbl2.configure(text="")
    newPeople()

# When the user guesses artist 2
def clicked2():
    global correctAnswer
    global userGuess
    global score
    global highScore
    
    userGuess = "2"
    if userGuess == correctAnswer:
        score += 1
        if score > highScore:
            highScore = score
        lbl3.configure(text="Correct! Your score is now %s and your high score is %s" % (score, highScore))
    else:
        lbl3.configure(text="Incorrect! You loose! You ended with a score of %s and your high score is %s" % (score, highScore))
        score = 0
    lbl1.configure(text="")
    lbl2.configure(text="")
    newPeople()

# Create buttons
btn1 = Button(window, text="Name #1", command = clicked1)
btn2 = Button(window, text="Name #2", command = clicked2)
btn1.place(x=100, y=50)
btn2.place(x=300, y=50)

window.mainloop()

# Getting Started



#### Requirements:
```
-Python 3.6+
-Notepad++ (Or some other decent text editor)
```


## Step 1
**Make a new bot application**
Head over to [Discord Developers](https://discordapp.com/developers/applications/me).
Login and create a new application. You can name it whatever you want, put description and set icon. (*You can always return back to that page and enter a different name, description and application icon.*)
*Look at the GIF below.*

![](http://i.imgur.com/5HaHpT0.gif)


## Step 2
Download [Python](https://www.python.org/ftp/python/3.6.2/python-3.6.2.exe).
Once you've downloaded Python, install it and make sure you select `Add To The Path`.

Afterwards, head over to Start and start writing `Command Prompt`. A black icon should appear, click on it.
After `Command Prompt` opens, type the following: 

```css
python -m pip install discord.py
python -m pip install colorama
python -m pip install requests
```

**If there are any `errors`, make a new [issue](https://github.com/Kyousei/YotsugiBot/issues) or ask in [Yotsugi Support Server](https://discord.gg/Fj9uwmT).**



## Step 3

Open `Command Prompt` and type: `git clone https://github.com/Kyousei/YotsugiBot.git`.
This will clone the Windows version of the bot to your PC and make a `YotsugiBot` folder.
The folder will contain `launcher.sh`, use that when updating or launching the bot for easier access.

Once you've downloaded and installed the bot, open `credentials.py` and edit `BotToken`, `Owner`, `Prefix` & `EmbedColor` section. 
For `EmbedColor`, put `0xHEX`, `HEX` being the HEX code of the color you want to use.
(*Use Notepad++ or some other decent text editing software*)
**See below**

**Here's How To Get Token**
![](http://i.imgur.com/jMHu1SQ.gif)


**Here's How To Get Your User ID**
![](http://g.recordit.co/iUm1PONr8i.gif)

Once you've edited `BotToken`, `Owner`, `Prefix` and `EmbedColor`, save the file.



## Step 4

To start your bot, double click on **`YotsugiMain.py`** and wait for it to load.
Once it's like in the image below, you can **minimize** it and start using the bot. *Warning: Closing `YotsugiMain.py` will make your bot go offline!*
*See Step 3, you can both use this and that above.*


If there are any errors, make a new [issue](https://github.com/Kyousei/YotsugiBot/issues) or ask in [Yotsugi Support Server](https://discord.gg/Fj9uwmT).

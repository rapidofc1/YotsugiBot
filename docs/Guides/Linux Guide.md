# Getting Started

## Step 1
Make a new bot application. Head over to Discord Developers. Login and create a new application. You can name it whatever you want, put description and set icon. *(You can always return back to that page and enter a different name, description and application icon.) Look at the GIF below.*


![](http://i.imgur.com/5HaHpT0.gif)

## Step 2
(Most recent Ubuntu builds have python3 installed by default, incase you don't(for whatever reason):
Open the command console via `CTRL + ALT + T` or open the Dash by clicking the Ubuntu icon in the upper-left, type "`terminal`", and select the Terminal application and copypaste or type `sudo apt-get install python3`.)

## Step 3
Incase you dont need to do Step 2, first thing you need to do is open the Console:
Open the command console via `CTRL + ALT + T` or open the Dash by clicking the Ubuntu icon in the upper-left, type "`terminal`", and select the Terminal application.
After that, copy and paste or type:

```python3 -m pip install discord.py
python3 -m pip install discord.py
python3 -m pip install colorama
python3 -m pip install requests
```

## Step 3
Now type `git clone -b linux https://github.com/Kyousei/YotsugiBot` to download the files.

## Step 4
Editing the credentials:
Use `cd YotsugiBot` to move into the newly created folder, then type `nano credentials.py` and edit in the information. 

`BotToken` is Your Bots unique token in the Discord Developers section. The gif below shows you how to get it.
`Owner` requires your unique User ID, the Gif below shows how to get it.
`Prefix` defines the variable you are going to use in front of the commands in order for the bot to respond.
`EmbedColor` will show a colored border around embed messages of the bot. To change it, put `0xHEX`, `HEX` being the HEX code of the color you want to use.

Press `CTRL + O` and enter to save afterwards, and `CTRL + X` to close it. 

## Step 5
Now create a new tmux session via `tmux new -s Yotsugi` . You can replace Yotsugi with whatever you want as long as you remember it.
In the new session type `python3 YotsugiMain.py` to start the bot. It should show some Bot Information, then the bot should log in.

## Step 6
Inviter the bot to your server with an invite link
https://discordapp.com/oauth2/authorize?client_id=ID_HERE&scope=bot&permissions=0

Replace `ID_HERE` with your Bots ID. (You can find it under the Discord Developers Section above the Token.) 
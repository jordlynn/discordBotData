===READ THIS===
Using the Discord client you should have a pretty solid understanding of multitasking, if you're coming from javascript this is just known as async calls. In this API they're called 'async' if you're building using < python 3.5 then you'll get a bunch of syntax errors about the 'async' and 'await' calls. I don't want to go through and translate  all these, upgrade or die! Just kidding, you can go make your own branch.

===Installation & Requirements===
You'll need to install a few things, first you'll need a working python build **with version >= 3.5** if you are going to use something lower you'll need to translate some of the code, and make your own branch. This will also go much smoother if you have ``pip`` installed, if you're on a *nix OS just run something like:

Arch Linux ``sudo pacman -Syu python-pip``
Debian/Ubuntu ``sudo apt-get install python-pip``

Once python is fully put together with pip you can follow the instructions on the discord.py git repo, I'll also post the Arch instructions below.

https://github.com/Rapptz/discord.py

==Arch install instructions==
Open a terminal and type

``sudo python3 -m pip install -U discord.py``

opus should already be on your system if not that's just a package manager call away. Next install psutil which reports system temps, ect.

``sudo python3 -m pip install -U psutil``

If all goes well you're ready to run!

===Running Bot===
The bot has the private key and server ID it needs (I know not great in a public repo, fingers crossed I guess until I figure something out).

Just issue a call from ``python`` or ``python3`` depending on where your **python >= 3.5** is:

``python data.py``

Give it a few seconds to authenticate and login and Data should be ready for commands. **Try to keep the testing chatter in the "bottesting" chat room plz**.

===Bugs & Reporting===
Use the feature/bug report section of the git repo. thanx.
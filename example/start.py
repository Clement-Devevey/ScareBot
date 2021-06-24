import os, sys
# Configuration drivers
os.environ['SDL_VIDEODRIVER'] = 'fbcon'
os.environ["SDL_FBDEV"] = "/dev/fb0"                          
os.environ["SDL_NOMOUSE"] = "1"
os.environ['SDL_AUDIODRIVER'] = 'alsa'
os.system('sh /etc/init.d/S00gif stop')
os.system('python3 ./menu.py&')
sys.exit()
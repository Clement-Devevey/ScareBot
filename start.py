import sys,subprocess


musique_boucle = subprocess.Popen(["while true; do aplay /game/Resources/musiques/8bit.wav -N --test-nowait ; sleep 2; done"], shell = True)
subprocess.Popen(["amixer cset numid=1 70%"],shell=True)
musique_boucle.terminate()
subprocess.Popen(['kill -9 $(ps aux | grep "aplay /game/Resources/musiques/8bit.wav -N --test-nowait" | grep -v "grep" |tr -s " "| cut -d " " -f 2)'],  shell=True )
sys.exit()

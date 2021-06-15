import subprocess, time, os
i=0
subprocess.Popen(["aplay", "sfxMenuScarebotSelect.wav", "-N",  "--test-nowait"], creationflags=subprocess.DETACHED_PROCESS)

while 1:
	subprocess.Popen(["aplay", "8bit.wav", "-N",  "--test-nowait"])
	print("1")
	subprocess.Popen(["aplay 8bit.wav", "-N",  "--test-nowait"])
	print("2")
	subprocess.Popen(["aplay 8bit.wav", "-N",  "--test-nowait"])
	print("3")
	subprocess.Popen(["aplay 8bit.wav", "-N",  "--test-nowait"])
	print("4")
	subprocess.Popen(["aplay 8bit.wav", "-N",  "--test-nowait"])
	print("5")
	subprocess.Popen(["aplay 8bit.wav", "-N",  "--test-nowait"])
	print("6")
	subprocess.Popen(["aplay 8bit.wav", "-N",  "--test-nowait"])


  








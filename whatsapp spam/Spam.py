import pyautogui
import time

Pesan = "oooo" 
n = 1000

print ("Siap-siap")

count = 5
while (count != 0):
	time.sleep(1)
	count -= 1

print ("\n Mengirim....")

for i in range(0, n):
	pyautogui.typewrite(Pesan + '\n')
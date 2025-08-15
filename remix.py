from uiutils import *
# /home/pi/RaspberryPi-CM4-main/language/language.ini
lang=language()
print(lang)
if lang=='cn':
	print('lang = cn')
	os.system('sudo python3 main.py')
	 
else:
     print('lang = en')
     os.system('sudo -E python3 main.py')



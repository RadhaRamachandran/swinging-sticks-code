from gpiozero import LightSensor
ldr = LightSensor(17)
print(ldr.value)
ldr.wait_for_dark()
print('stop!')

while (True):	
	if (ldr.value <  0.2):
		print(ldr.value)
		print('flip!')
		break


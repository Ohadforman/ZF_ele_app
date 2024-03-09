from skidl import *

# Define the components
leds = [Part('Device', 'LED', ref='LED'+str(i)) for i in range(3)]
music_player = Part('Device', 'SoundPlayer')
motion_sensor = Part('Device', 'MotionSensor')
time_sensor = Part('Device', 'TimeSensor')

# Define the conditions
if time_sensor.time > 18:
    for led in leds:
        led += VCC
    music_player.play_music()
else:
    for led in leds:
        led += GND
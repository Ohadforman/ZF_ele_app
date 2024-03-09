from skidl import *

# Define the components
led = Part('device', 'LED', footprint='LED_SMD')
buzzer = Part('device', 'Buzzer', footprint='BUZZER_SMD')
fire_sensor = Part('device', 'FIRE_SENSOR', footprint='SENSOR_SMD')

# Create the circuit
led[1, 'A'] += Vcc
buzzer[1] += led[2, 'K']
fire_sensor[1, 'G'] += Net('GND')

# Define the power and ground nets
Vcc = Net('Vcc')
GND = Net('GND')
Vcc += Part('power', 'VCC')
GND += Part('power', 'GND')

# Print the circuit
generate_netlist()


###
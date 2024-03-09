from skidl import *

# Define components
led = Part('device', 'LED')
buzzer = Part('device', 'BUZZER')

# Define circuit
net_1, net_2 = Net(), Net()

led_n1, led_n2 = Net(), Net()

led[1, 2] += led_n1, net_1
led[2, 1] += led_n2, net_2

buzzer[1, 2] += net_2, Net()

# Define a blinker using a capacitor
c = Part('device', 'C', value='1uF')

led_n2 += c[1], V

gnd += c[2], Net(), buzzer[2]

# Generate the netlist
generate_netlist()
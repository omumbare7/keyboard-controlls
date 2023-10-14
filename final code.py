import serial
import keyboard
import time

# Define the serial port and baud rate
#ser = serial.Serial('COM13', 9600)  # Replace 'COM1' with the actual serial port

def send_command(left_speed, right_speed, x_angle, y_angle, toggle_value):
    command = f" $,{left_speed},{right_speed},{x_angle},{y_angle},{toggle_value},& "
    #if command != " $,0,0,90,90,l,& ":
    #ser.write(command.encode())
    print(command)
     

# Variables for speed control       
max_speed = 39321.6  # Maximum speed of the tank (adjust as needed)
acceleration = 1024  # Speed increment per second (adjust as needed)
current_speed = 0  # Current speed of the tank
deceleration = 1024
x_servo_angle = 90  # Centered position (adjust as needed)
y_servo_angle = 90

# Timestamps for keypress tracking
key_pressed_time = {}

# Flags for combination keys
w_pressed = False
s_pressed = False
a_pressed = False
d_pressed = False
toggle_value = "l"

# Main control loop
try:
    while True:
        # Check for 'w' keypress
        if keyboard.is_pressed('w'):
            # Calculate the speed based on how long 'w' is held down
            if not w_pressed:
                key_pressed_time['w'] = time.time()
                w_pressed = True
            
            time_pressed = time.time() - key_pressed_time['w']
            current_speed = min(max_speed, current_speed + acceleration * time_pressed * 2)
            send_command(int(current_speed), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
        else:
            if w_pressed:
                # Decelerate when 'w' is released
                while current_speed > 0:
                    time.sleep(0.3)
                    current_speed = max(0, current_speed - deceleration * (time.time() - key_pressed_time['w'])*2)
                    send_command(int(current_speed), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
            w_pressed = False
            #current_speed = 15000
            #send_command(int(15000), int(15000), x_servo_angle, y_servo_angle, toggle_value)
            if 'w' in key_pressed_time:
                del key_pressed_time['w']

        # Check for 's' keypress
        if keyboard.is_pressed('s'):
            # Calculate the speed based on how long 's' is held down
            if not s_pressed:
                key_pressed_time['s'] = time.time()
                s_pressed = True
            
            time_pressed = time.time() - key_pressed_time['s']
            current_speed = max(-max_speed, current_speed - acceleration * time_pressed )
            send_command(int(current_speed), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
        else:
           if s_pressed:
                # Decelerate when 's' is released
                while current_speed < 0:
                    time.sleep(0.3)
                    current_speed = min(0, current_speed + deceleration * (time.time() - key_pressed_time['s'])*2)
                    send_command(int(current_speed), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
                s_pressed = False
                
            #current_speed = 15000
            #send_command(int(15000), int(15000), x_servo_angle, y_servo_angle, toggle_value)
                if 's' in key_pressed_time:
                    del key_pressed_time['s']

        # Check for 'a' keypress
        if keyboard.is_pressed('a'):
            # Calculate the speed based on how long 'a' is held down
            if not a_pressed:
                key_pressed_time['a'] = time.time()
                a_pressed = True
            
            time_pressed = time.time() - key_pressed_time['a']
            if w_pressed:
                # If 'w' is also pressed, turn right while moving forward
                send_command(int(current_speed), int(current_speed / 2.4), x_servo_angle, y_servo_angle, toggle_value)
            elif s_pressed:
                # If 's' is also pressed, turn right while moving backward
                send_command(int(current_speed / 2.4), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
            else:
                # If 'a' is pressed alone, rotate clockwise
                send_command(max_speed / 2.4, -max_speed / 2.4, x_servo_angle, y_servo_angle, toggle_value)
        else:
            a_pressed = False
            if 'a' in key_pressed_time:
                del key_pressed_time['a']

        # Check for 'd' keypress
        if keyboard.is_pressed('d'):
            # Calculate the speed based on how long 'd' is held down
            if not d_pressed:
                key_pressed_time['d'] = time.time()
                d_pressed = True
            
            time_pressed = time.time() - key_pressed_time['d']
            if w_pressed:
                # If 'w' is also pressed, turn left while moving forward
                send_command(int(current_speed / 2.4), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
            elif s_pressed:
                # If 's' is also pressed, turn left while moving backward
                send_command(int(current_speed), int(current_speed / 2.4), x_servo_angle, y_servo_angle, toggle_value)
            else:
                # If 'd' is pressed alone, rotate clockwise
                send_command(-max_speed / 2.4, max_speed / 2.4, x_servo_angle, y_servo_angle, toggle_value)
        else:
            d_pressed = False
            if 'd' in key_pressed_time:
                del key_pressed_time['d']
                
        if keyboard.is_pressed('l'):
            toggle_value = 'l'
            send_command(int(current_speed), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
                
        if keyboard.is_pressed('k'):
            toggle_value = 'k'
            send_command(int(current_speed), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
            
        if keyboard.is_pressed('left'):
            x_servo_angle -= 5
            if x_servo_angle > 180:
                x_servo_angle = 180
            if x_servo_angle < 0:
                x_servo_angle = 0
            send_command(int(current_speed), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
        elif keyboard.is_pressed('right'):
            x_servo_angle += 5
            if x_servo_angle > 180:
                x_servo_angle = 180
            if x_servo_angle < 0:
                x_servo_angle = 0
            send_command(int(current_speed), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
        elif keyboard.is_pressed('up'):
            y_servo_angle += 5
            if y_servo_angle > 180:
                y_servo_angle = 180
            if y_servo_angle < 0:
                y_servo_angle = 0
            send_command(int(current_speed), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)
        elif keyboard.is_pressed('down'):
            y_servo_angle -= 5
            if y_servo_angle > 180:
                y_servo_angle = 180
            if y_servo_angle < 0:
                y_servo_angle = 0
            send_command(int(current_speed), int(current_speed), x_servo_angle, y_servo_angle, toggle_value)

        # Delay to control the loop speed
        time.sleep(0.4)

except KeyboardInterrupt:
    pass

# Close the serial connection when done
ser.close()

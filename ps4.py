import pygame
from math import ceil
import json
from datetime import datetime
pygame.init()


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

def import_json_data(path='data.json'):
    try:
        with open(path, 'r') as file:
            fc = json.load(file)
            return fc
    except:
        return None

def main():
    # Set the width and height of the screen (width, height), and name the window.
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("Joystick example")

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Get ready to print.
    text_print = TextPrint()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    done = False
    #zero_st = datetime.now()
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        try:
            events = pygame.event.get()
        except:
            continue
        

        for event in events:
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255, 255, 255))
        text_print.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        text_print.tprint(screen, f"Number of joysticks: {joystick_count}")
        text_print.indent()

        # For each joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()

            text_print.tprint(screen, f"Joystick {jid}")
            text_print.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            text_print.tprint(screen, f"Joystick name: {name}")

            guid = joystick.get_guid()
            text_print.tprint(screen, f"GUID: {guid}")

            power_level = joystick.get_power_level()
            text_print.tprint(screen, f"Joystick's power level: {power_level}")

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()
            text_print.tprint(screen, f"Number of axes: {axes}")
            text_print.indent()



            

            #axis 1
            axis = joystick.get_axis(1)
            up = -axis if axis <= 0 else 0
            down = axis if axis >= 0 else 0

            up = ceil(up*100)
            down = ceil(down*100)

            text_print.tprint(screen, f"up: {(up)}")
            text_print.tprint(screen, f"down: {(down)}")


            #axis 2
            axis = joystick.get_axis(0)
            turnr = axis if axis >= 0 else 0
            turnl = -axis if axis <= 0 else 0

            turnr = ceil(turnr*100)
            turnl = ceil(turnl*100)

            text_print.tprint(screen, f"turnr: {(turnr)}")
            text_print.tprint(screen, f"turnl: {(turnl)}")

            #axis 3
            axis = joystick.get_axis(3)
            forward = -axis if axis <= 0 else 0
            back = axis if axis >= 0 else 0

            forward = ceil(forward*100)
            back = ceil(back*100)

            text_print.tprint(screen, f"forward: {(forward)}")
            text_print.tprint(screen, f"back: {(back)}")
            drone_id = 1
            role = 'LEADER'

            #if(turnl == 0 and turnr == 0 and up == 0 and down == 0 and forward == 0 and back == 0 and (datetime.now()-zero_st).total_seconds() <= 0.1):
            #    zero_st = datetime.now()
            #    continue

            data = {
                drone_id : {
                    'time': datetime.now().isoformat(),
                    'role': role,
                    'turnl': (turnl),
                    'turnr': (turnr),
                    'up': (up),
                    'down': (down),
                    'forward': (forward),
                    'back': (back)
                }
            }

            export(data)
            
            # for i in range(axes):
            #     axis = joystick.get_axis(i)
            #     text_print.tprint(screen, f"Axis {i} value: {axis:>6.3f}")
            # text_print.unindent()

            # buttons = joystick.get_numbuttons()
            # text_print.tprint(screen, f"Number of buttons: {buttons}")
            # text_print.indent()

            # for i in range(buttons):
            #     button = joystick.get_button(i)
            #     text_print.tprint(screen, f"Button {i:>2} value: {button}")
            # text_print.unindent()

            # hats = joystick.get_numhats()
            # text_print.tprint(screen, f"Number of hats: {hats}")
            # text_print.indent()

            # # Hat position. All or nothing for direction, not a float like
            # # get_axis(). Position is a tuple of int values (x, y).
            # for i in range(hats):
            #     hat = joystick.get_hat(i)
            #     text_print.tprint(screen, f"Hat {i} value: {str(hat)}")
            # text_print.unindent()

            text_print.unindent()

        # print follower data by pulling it out of data.json
        data = import_json_data()
        if data is None:
            print("no data yet")
        else:
            follower_1_data = data['drones']['2']
            follower_2_data = data['drones']['3']
            text_print.tprint(screen, f"", {()})

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)

def export(data,path = 'data.json'):
    try:
        fc = {}
        try:
            with open(path, 'r') as file:
                fc = json.load(file)
        except:
            pass
        
        with open(path,'w') as file:
            if 'drones' not in fc.keys():
                fc['drones']={}
            for k,v in data.items():
                fc['drones'][k]=v
            
            json.dump(fc, file, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
    # while True:
    #     try:
    #         main()
    #     except KeyError:
    #         break
    #     except:
    #         break
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
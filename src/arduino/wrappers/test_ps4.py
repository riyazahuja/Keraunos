from ps4_controller import MyController

controller = MyController('/dev/input/js0')
controller.listen()

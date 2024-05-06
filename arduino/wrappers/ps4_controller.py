from pyPS4Controller.controller import Controller

class MyController(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface=interface, connecting_using_ds4drv=False)

    def on_L3_up(self, val):
        print("L3 up")

    def on_L3_down(self, val):
        print("L3 down")

    def on_L3_left(self, val):
        print("L3 left")

    def on_L3_right(self, val):
        print("L3 right")

    def on_R3_up(self, val):
        print("R3 up")

    def on_R3_down(self, val):
        print("R3 down")

    def on_R3_left(self, val):
        print("R3 left")

    def on_R3_right(self, val):
        print("R3 right")

    def on_L3_x_at_rest(self):
        pass

    def on_L3_y_at_rest(self):
        pass

    def on_R3_x_at_rest(self):
        pass

    def on_R3_y_at_rest(self):
        pass

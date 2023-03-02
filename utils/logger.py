from utils.decorator import singleton


@singleton
class MyClass:
    def __init__(self):
        print('11111111111111111')
        self.name = "MyClass"

    def print_name(self):
        print("My name is {}".format(self.name))





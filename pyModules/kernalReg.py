# -[ Python Modules ]- #
import time

# -[ Classes ]- #
class register():
    def __init__(self, newRegistry):
        self.newregistry = newRegistry
        self.register = {}

class newRegister(register):
    def __init__(self):
        super().__init__(self)

    def get(self, index):
        while self.register.get(index) == None: time.sleep(.1)

        return self.register[index]

    def set(self, index, value):
        self.register[index] = value
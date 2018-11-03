
class Screen(object):

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
         self._width = int(value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = int(value)

    @property
    def resolution(self):
        return self.width * self.height

if __name__ == '__main__':
    screen = Screen()
    screen.width = 10
    screen.height = 12
    print screen.resolution
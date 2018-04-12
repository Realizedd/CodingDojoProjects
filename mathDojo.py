class MathDojo(object):
    def __init__(self):
        self.result = 0

    def add(self, *args):
        for element in args:
            if type(element) is list or type(element) is tuple:
                for num in element:
                    if type(num) is int or type(num) is float:
                        self.result += num
            elif type(element) is float or type(element) is int:
                self.result += element
        return self

    def subtract(self, *args):
        for element in args:
            if type(element) is list or type(element) is tuple:
                for num in element:
                    if type(num) is int or type(num) is float:
                        self.result -= num
            elif type(element) is float or type(element) is int:
                self.result -= element
        return self


print MathDojo().add([1], 3, 4).add([3, 5, 7, 8], [2, 4.3, 1.25]).subtract(2, [2, 3], [1.1, 2.3]).result


class Zebra:
    body = 'zebra'
    heads = 'heads'

    def result(self):
        return self.body + self.heads

class Vobla:
    body = 'vobla'
    legs = 'legs'

    def result(self):
        return self.body + self.legs

class SuperPupkin:
    body ='SuperPupkin'

    def result(self):
        return self.body


class Mutant(Zebra,Vobla):
    pass


z = Mutant()
print(z.result())
print(z.body)

try:
    print(z.legs)
except:
    print('no legs')

try:
    print(z.heads)
except:
    print('no heads')
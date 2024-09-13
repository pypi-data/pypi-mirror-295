from breakword import track


# for i in range(5):
#     groups.pinson.logbrk(i)
#     groups.aardvark.logbrk(i)


class Bob:
    def __init__(self, i):
        self.i = i

    def __str__(self):
        return f"Bob{self.i}"


for i in range(10):
    b = Bob(i)
    track(i)
    track(b)
    print(track(b, all=True), b.breakword)


# # from breakword import *


# # def f(x):
# #     y = x
# #     for i in range(10):
# #         # logword(y)
# #         # breakword()
# #         breakpoint(log=i)
# #         # logbrk(group='honey')
# #         y = g(y)
# #     return y


# # def g(x):
# #     return x + 1


# # f(11)


# class Bonk:
#     pass


# track_creation(Bonk)


# def test_thing():
#     # groups.hoop.logbrk(1, 2)
#     # groups.plantain.logbrk(3, 4)
#     # groups.plantain.logbrk(3, 4)
#     # groups.plantain.logbrk(3, 4)
#     # breakpoint(1, 2, 3)
#     # breakpoint("hoho!")
#     # # if after("standard"):
#     # #     print("ok")
#     # assert False

#     bs = [Bonk() for i in range(10)]
#     for b in bs:
#         print(b.breakword)
#     assert False

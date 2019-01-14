#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: sunyueqing
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: sunyueqinghit@163.com
@File : Lab_1.py
@Time : 2018/10/14 10:07
@Site : 
@Software: PyCharm
'''

'''
class State: Define the state of the system
'''


class State:
    def __init__(self, monkey=-1, box=0, banana=1, monkeybox=-1):
        self.monkey = monkey  # -1:monkey at A ; 0:B ; 1:C
        self.box = box  # -1:box at A ; 0:B ; 1:C
        self.banana = banana  # 1:banana at C
        self.monkeybox = monkeybox  # -1:monkey is not on the box ; 1:monkey is on the box


'''
CopyState function:Copy from a previous state
'''


def CopyState(preState):
    newState = State()
    newState.monkeybox = preState.monkeybox
    newState.monkey = preState.monkey
    newState.box = preState.box
    newState.banana = preState.banana
    return newState


'''
monkeyGoto function: Monkey moves between A, B, C
'''


def MonkeyGoto(at, i):
    if at == -1:
        Route.insert(i, "Monkey go to A.")
        StatesList[i + 1] = CopyState(StatesList[i])
        StatesList[i + 1].monkey = -1
    elif at == 0:
        Route.insert(i, "Monkey go to B.")
        StatesList[i + 1] = CopyState(StatesList[i])
        StatesList[i + 1].monkey = 0
    elif at == 1:
        Route.insert(i, "Monkey go to C.")
        StatesList[i + 1] = CopyState(StatesList[i])
        StatesList[i + 1].monkey = 1
    else:
        print("The parameter is not in the status range.")


'''
MoveBox function: Monkey moving box
'''


def MoveBox(at, i):
    if at == -1:
        Route.insert(i, "Monkey move box to A.")
        StatesList[i + 1] = CopyState(StatesList[i])
        StatesList[i + 1].monkey = -1
        StatesList[i + 1].box = -1
    elif at == 0:
        Route.insert(i, "Monkey move box to B.")
        StatesList[i + 1] = CopyState(StatesList[i])
        StatesList[i + 1].monkey = 0
        StatesList[i + 1].box = 0
    elif at == 1:
        Route.insert(i, "Monkey move box to C.")
        StatesList[i + 1] = CopyState(StatesList[i])
        StatesList[i + 1].monkey = 1
        StatesList[i + 1].box = 1
    else:
        print("The parameter is not in the status range.")


'''
ClimbOntoBox function: monkey climb onto the box
'''


def ClimbOntoBox(i):
    Route.insert(i, "Monkey climb onto box")
    StatesList[i + 1] = CopyState(StatesList[i])
    StatesList[i + 1].monkeybox = 1


'''
DownBox function: monkey climb down the box
'''


def DownBox(i):
    Route.insert(i, "Monkey climb down fron box")
    StatesList[i + 1] = CopyState(StatesList[i])
    StatesList[i + 1].monkeybox = -1


'''
PickBanana function: Monkey picks up banana
'''


def PickBanana(i):
    Route.insert(i, "Monkey picking banana")


'''
ShowStep function: Print every step
'''


def ShowStep(i):
    print("The step sequences is: \n")
    for a in range(i + 1):
        print("Step %d : %s \n" % (a + 1, Route[a]))
    print("\n")


'''
nextStep function: Calculate the next step according to the previous step
'''


def nextStep(i):
    if i > 150:
        print("The step is to long, something was wrong.")
        exit(0)
    if (StatesList[i].monkeybox == 1 and StatesList[i].monkey == StatesList[i].box and StatesList[i].monkey ==
            StatesList[i].banana):
        ShowStep(i)
        exit(0)
    j = i + 1
    if StatesList[i].banana == StatesList[i].box:
        if StatesList[i].monkey == StatesList[i].banana:
            if StatesList[i].monkeybox == -1:
                ClimbOntoBox(i)
                PickBanana(i + 1)
                nextStep(j)
            else:
                PickBanana(i + 1)
                nextStep(j)
        else:
            MonkeyGoto(StatesList[i].box, i)
            nextStep(j)
    else:
        if StatesList[i].monkey == StatesList[i].box:
            if StatesList[i].monkeybox == -1:
                MoveBox(StatesList[i].banana, i)
                nextStep(j)
            else:
                DownBox(i)
                nextStep(j)
        else:
            MonkeyGoto(StatesList[i].box, i)
            nextStep(j)


if __name__ == '__main__':
    s = input("please input state: monkey(-1/0/1), box(-1/0/1), banana(-1/0/1), monkeybox(-1/1): \n")
    parameters = s.split(" ")
    initialState = State(int(parameters[0]), int(parameters[1]), int(parameters[2]), int(parameters[3]))
    StatesList = [None] * 150
    Route = [None] * 150
    StatesList.insert(0, initialState)
    nextStep(0)

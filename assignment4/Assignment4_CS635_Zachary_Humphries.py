# Zachary Humphries
# Assignment 3
# CS 635
# December 12, 2023

from abc import ABC, abstractmethod, ABCMeta

from math import *

PI = 3.14159

# Create Abstract Class 
class AbstractExpression(ABC):

    @abstractmethod
    def interpret(self):
        return None



class Point(AbstractExpression):
    def __init__(self, a, b):
        self.X = int(a)
        self.Y = int(b)

    def interpret(self):
        return [self.X, self.Y]

    def __repr__(self):
        return (f'{self.X}, {self.Y}')
    

    
class Number(AbstractExpression):

    def __init__(self, value):
        self.value = int(value)

    def interpret(self):
        return self.value

    def __repr__(self):
        return str(self.value)   



class TurtleData(Point, Number):
    def __init__(self, degrees: int, X: int, Y: int):
        self.degrees = Number(degrees).value
        self.coordinates = Point(X, Y)

    def __repr__(self):
        return (f'coordinates = ({self.coordinates}), direction = {self.degrees} degrees')


class Variable(TurtleData):
    def __init__(self, variableName, value):
        self.variableName = variableName
        self.value = self.value

    def interpret(self):
        return [self.variableName, self.value]

    def __repr__(self):
        return f'{self.variableName} = {self.value}'



# Terminal Expression
class Turtle(TurtleData):

    def __init__(self, dataTurtle: TurtleData):
        if (dataTurtle == None):
            self.data = TurtleData(0, 0, 0)
        else:
            self.data = dataTurtle
        

    def interpret(self):
        return self.data
        
    def direction(self) -> float:
        return self.data.degrees
    
    def location(self) -> Point:
        return self.data.coordinates
    
    def distanceTo(self, coordinates: Point) -> float:
        diffX = coordinates.X - self.data.coordinates.X
        diffY = coordinates.Y - self.data.coordinates.Y

        distance = sqrt(diffX*diffX + diffY*diffY)
        return float(round(distance))
    
    def bearingTo(self, coordinates: Point) -> float:
        slope = (coordinates.Y - self.data.coordinates.Y)/(coordinates.X - self.data.coordinates.X)
        radians = atan(slope)
        angle = float(round(radians * 180/PI) % 360)
        return angle
    
    def turn(self, degrees: int):
        newDegrees = (self.data.degrees + degrees) % 360
        self.data.degrees = newDegrees
        return None
    
    def move(self, distance: int):
        radians = self.data.degrees * PI / 180

        deltaX = cos(radians) * distance
        deltaY = sin(radians) * distance

        newX = round(self.data.coordinates.X + deltaX)
        newY = round(self.data.coordinates.Y + deltaY)

        self.data.coordinates.X = newX
        self.data.coordinates.Y = newY
        return None
    
    def iterator(self, function, parameter):
        return function(self, parameter)
    
    def __repr__(self):
        return self.data
    


class Move(Turtle):

    def __init__(self, root, distance: int):
        super().__init__(root.data)
        self.distance = distance

    def interpret(self):
        self.move(self.distance)
        return Turtle(self.data).interpret()

    def __repr__(self):
        return f'move {self.distance}'



class Turn(Turtle):

    def __init__(self, root, turnDegrees: int):
        super().__init__(root.data)
        self.turnDegrees = turnDegrees

    def interpret(self):
        self.turn(self.turnDegrees)
        return Turtle(self.data).interpret()

    def __repr__(self):
        return f'turn {self.turnDegrees}'

    

class BearingTo(Turtle):

    def __init__(self, root, point: Point):
        super().__init__(root.data)
        self.point = point

    def interpret(self):
        angle = self.bearingTo(self.point)
        return angle
    
    def __repr__(self):
        return f'bearingTo {self.point}'
    


class DistanceTo(Turtle):

    def __init__(self, root, point: Point):
        super().__init__(root.data)
        self.point = point

    def interpret(self):
        difference = self.distanceTo(self.point)
        return difference
    
    def __repr__(self):
        return f'distanceTo {self.point}'
    

class Repeat(Turtle):
    def __init__(self, root, numRepeated, *args):
        super().__init__(root.data)
        self.numRepeated = int(numRepeated)
        self.args = args

    def interpret(self):
        for numRep in range(self.numRepeated):
            for numFunc in range(len(self.args)):
                function = self.args[numFunc][0]
                parameter = self.args[numFunc][1]
                self.root = self.iterator(function, parameter)
                self.root.interpret()
        return Turtle(self.data).interpret()


# class Variables(Turtle):
#     def __init__(self, root, tempVariable: str, tempValue):
#         super().__init__(root.data)
#         self.dictionary = {}
#         self.tempVariable = tempVariable
#         self.tempValue = tempValue

#     def interpret(self):
#         self.dictionary.update({self.tempVariable : self.tempValue})
#         return self.dictionary
    
#     def __repr__(self):
#         outputString = str()
#         for key, value in self.dictionary:
#             outputString = outputString + f'#{key} = {value} \n'
#         return outputString
    
# class Number(AbstractExpression):

#     def __init__(self, value):
#         self.value = int(value)

#     def interpret(self):
#         return self.value

#     def __repr__(self):
#         return str(self.value)
    
class Parser:
    
    def __init__(self, sentence: str):
        self.turtle = Turtle(None)
        self.sentence = sentence

        self.actionDictionary = {"move": Move, "turn": Turn, "distanceTo": DistanceTo, "bearingTo": BearingTo, "repeat": Repeat, "#": Variable, "P": Point}

    def variableDeclaration(token):
        if token[0:1] == "#P":
            return Point
        else:
            return Variable
        
    

    def defineAction(self, token):

        action = self.actionFunctionDictionary.get(token)
        return action
    


    def cleanSentence(self, sentence, cleanArray):
        for deletedItem in cleanArray:
            sentence = sentence.replace(deletedItem, "")
        return sentence



    def separateRepeat(self, sentence):

        splitSentence =  [lines for lines in sentence.split("repeat") if lines]

        for numLine in range(1, len(splitSentence)):
            splitSentence[numLine] = "repeat" + splitSentence[numLine]

        newSplitSentence = []
        for line in splitSentence:
            tempSplit = line.split("end")
            for tempLine in tempSplit:
                if tempLine != '':
                    newSplitSentence.append(tempLine)
        
        return newSplitSentence

    def searchAction(self, lines):
        action = self.actionDictionary.get(lines)
        if (lines != '' and action is not None):
            return action
        elif (lines != '' and lines.isdigit() ):
            return Number(lines)
        elif (lines != ''):
            return lines
        

    def pointReput(self, sectionCommands, splitOrder):
        if splitOrder[0][0] != "P":
            for numLine in range(0, len(sectionCommands)-1):
                sectionCommands[numLine] = splitOrder[0][0] + sectionCommands[numLine]
                action = self.searchAction(sectionCommands[numLine])
                if action is not None:
                    sectionCommands[numLine] = action
            action = self.searchAction(sectionCommands[len(sectionCommands)-1])
            if action is not None:
                sectionCommands[len(sectionCommands)-1] = action

        elif splitOrder[0][0] == "P":
            for numLine in range(1, len(sectionCommands)):
                sectionCommands[numLine-1] = sectionCommands[numLine]
                sectionCommands[numLine] = splitOrder[0][0]
                action = self.searchAction(sectionCommands[numLine-1])
                if action is not None:
                    sectionCommands[numLine-1] = action
            action = self.searchAction(sectionCommands[len(sectionCommands)-1])
            if action is not None:
                sectionCommands[len(sectionCommands)-1] = action


        return sectionCommands
    
    def stringtoCommand(self, string):
        



    
    def separateIntoCommands(self, commandArray, splitOrder, endRecursionFlag):

        if not(endRecursionFlag):
            sectionCommands = []
            if type(commandArray) is str:
                action = self.searchAction(commandArray)
                if action is not None:
                    commandArray = action
                    return commandArray
                
                if(commandArray != ""):
                    sectionCommands.extend(commandArray.split(splitOrder[0][0]))

                    # for sectionCommand in sectionCommands:
                    #     if len(splitOrder) > 1:
                    #         commandArray[numSection] = self.separateIntoCommands(sectionCommand, splitOrder[1:], False)
                    #     else:
                    #         commandArray[numSection] = self.separateIntoCommands(sectionCommand, splitOrder[0], True)



            if type(commandArray) is not str:
                if (len(commandArray) == 1 and type(commandArray) is object):
                    
                    

                for numSection in range(len(commandArray)):


                    if len(splitOrder) > 1:
                        commandArray[numSection] = self.separateIntoCommands(sectionCommand, splitOrder[1:], False)
                    else:
                        commandArray[numSection] = self.separateIntoCommands(sectionCommand, splitOrder[0], True)
                        


            else:
                if(commandArray != ""):
                    sectionCommands.extend(commandArray.split(splitOrder[0][0]))

                    if splitOrder[0][1]:
                        sectionCommands = self.pointReput(sectionCommands, splitOrder)
                    else:
                        for sectionCommand in sectionCommands:
                            action = self.searchAction(sectionCommand)
                            if action is not None:
                                sectionCommand = action
                                continue
                            else:
                                if len(splitOrder) > 1:
                                    commandArray[numSection] = self.separateIntoCommands(sectionCommand, splitOrder[1:], False)
                                else:
                                    commandArray[numSection] = self.separateIntoCommands(sectionCommand, splitOrder[0], True)
                                    continue

                    





                
                # sectionCommands = []
                # print(str(numSection) + str(commandArray))
                # if len(commandArray) > 1 and commandArray != '':
                #     tempLines = commandArray[numSection]
                # elif commandArray == '':
                #     continue
                # else:
                #     tempLines = commandArray
                

                # if type(tempLines) is str:

                #     if(tempLines == ""):
                #         continue

                #     print(str(type(tempLines)) + ": " + str(tempLines))
                #     print(tempLines.split(splitOrder[0][0]))

                #     sectionCommands.extend(tempLines.split(splitOrder[0][0]))
                #     
                    
                #     else:
                #         for numLine in range(0, len(sectionCommands)):
                #             action = self.searchAction(sectionCommands[numLine])
                #             if action is not None:
                #                 sectionCommands[numLine] = action

                            

            
                


                # if len(tempLines) == 1:
                #     print(tempLines)
                #     sectionCommands[len(sectionCommands)] = tempLines
                # else:
                    # if type(commandArray[numSection]) is str:
                    #     if len(splitOrder) > 1:
                    #         commandArray = self.separateIntoCommands(sectionCommands, splitOrder[1:], False)
                    #     else:
                    #         commandArray = self.separateIntoCommands(sectionCommands, splitOrder[0], True)
                    #         continue
                    # else:
                #     

        return commandArray

        
    #def performActions(commandArray):





    def parse(self):

        sentence = self.cleanSentence(self.sentence, ["    ", "\t", ","])
        
        splitRepeatsInSentence = self.separateRepeat(sentence)

        tree = []

        for splitRepeat in splitRepeatsInSentence:


            commands = self.separateIntoCommands(splitRepeat, [["\n", False], [" = ", False], [" ", False], ["#", True], ["P", True]], False)

            treeBranch = []

            for numCommand in range(len(commands)):
                treeBranch.append(self.determineLeftNode(treeBranch, commands[numCommand]))

            tree.append(treeBranch)
            

        print(tree)

            

    def determineLeftNode(self, trees, command):
        if type(command) is not list :
            return trees
        

        for line in command:
            treeBranch = []
            if type(line) is not list :
                treeBranch.extend([line])
                self.determineLeftNode(trees, command.pop(0))
            else:
                self.determineLeftNode(trees, command[0])
            
            if treeBranch and treeBranch != ['']:
                trees.append(treeBranch)

        return trees


        
        













    
if __name__ == "__main__":

    # turtle1 = Turtle(None)
    # print(turtle1.interpret())
    # turtle1 = Move(turtle1, 10)
    # print(turtle1.interpret())
    # turtle1 = Turn(turtle1, 90)
    # print(turtle1.interpret())
    # turtle1 = Move(turtle1, 20)
    # print(turtle1.interpret())
    # turtle1 = Turn(turtle1, -60)
    # print(turtle1.interpret())
    # turtle1 = Move(turtle1, 15)
    # print(turtle1.interpret())

    sentence = \
        "#Ps = 10, 10\n\
        #Pt = 10, 20\n\
        #d = distanceTo #s\n\
        #a = bearingTo #s\n\
        turn #a\n\
        move #d\n\
        #u = bearingTo #t\n\
        move 5\n\
        turn 90\n\
        move 5\n\
        repeat 4\n\
        turn 90\n\
        move 10\n\
        end\n\
        #side = 15\n\
        move #side\n\
        turn 90"
    
    print(Parser(sentence).parse())
    






    # turtle1 = Repeat(turtle1, 3, [Move, 2])
    # print(turtle1.interpret())
    # distance1 = DistanceTo(turtle1, Point(0,10)).interpret()
    # print(distance1)
    # angle1 = BearingTo(turtle1, Point(16,0)).interpret()
    # print(angle1)



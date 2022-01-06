import time
import random
import os
import numpy

class Game():
    def __init__(self, fileName, config):
        self.fileName = fileName
        self.config = self.loadConfig(config)

    def playGame(self):
        lineToType = self.getLine()
        userString, timeTaken = self.giveUserLine(lineToType)
        percentCorrect = self.calcPercent(userString, lineToType)
        wpm = self.calcWPM(len(userString), timeTaken)

        sRawWpm = str(round(wpm, 2))
        sBalWpm = str(round(wpm * (percentCorrect/100), 2))
        sPercentCorrect = str(round(percentCorrect, 1))
        sTimeTaken = str(round(timeTaken, 2))

        accuracy = ""
        if percentCorrect == 100:
            accuracy = "Perfect"
        elif percentCorrect == 0:
            accuracy = "Fail"
        elif percentCorrect < 50:
            accuracy = "Very inacurate"
        elif percentCorrect < 75:
            accuracy = "Moderately accurate"
        elif percentCorrect < 100:
            accuracy = "Mostly accurate"
        else:
            accuracy = "Error in accuracy description section: percentCorrect = " + str(percentCorrect)

        print(f"""
STATS
-------------------------
Time Taken: {sTimeTaken} seconds
Percentage Correct: {sPercentCorrect}%
Raw WPM: {sRawWpm}
Balanced WPM: {sBalWpm}

Accuracy: {accuracy}
-------------------------
        """)

        if self.config['inTerminal'] != True:
            time.sleep(5)

    def readLines(self, fileName):
        fileDir = os.path.dirname(__file__)
        fullPath = os.path.join(fileDir, fileName)
        f = open(fullPath, "r")
        lines = f.readlines()
        f.close()
        return lines

    def isNewLine(self, string):
        if string != "\n":
            return True
        else:
            return False

    def getLine(self):
        lines = self.readLines("thingsToType.txt")
        lines = list(filter(self.isNewLine, lines))
        line = lines[random.randint(0, len(lines)-1)]
        if line[-1] == "\n":
            line = line[:-1]
        return line

    def getWords(self, inputSting):
        wordList = inputSting.split()
        return wordList

    def levenshteinDistanceDP(self, token1, token2):
        distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

        for t1 in range(len(token1) + 1):
            distances[t1][0] = t1

        for t2 in range(len(token2) + 1):
            distances[0][t2] = t2

        a = 0
        b = 0
        c = 0

        for t1 in range(1, len(token1) + 1):
            for t2 in range(1, len(token2) + 1):
                if (token1[t1-1] == token2[t2-1]):
                    distances[t1][t2] = distances[t1 - 1][t2 - 1]
                else:
                    a = distances[t1][t2 - 1]
                    b = distances[t1 - 1][t2]
                    c = distances[t1 - 1][t2 - 1]

                    if (a <= b and a <= c):
                        distances[t1][t2] = a + 1
                    elif (b <= a and b <= c):
                        distances[t1][t2] = b + 1
                    else:
                        distances[t1][t2] = c + 1

        return distances[len(token1)][len(token2)]

    def calcPercent(self, userPhrase, correctPhrase):
        print("user phrase: " + userPhrase)
        print("correct phrase: " + correctPhrase)
        distance = self.levenshteinDistanceDP(str(userPhrase), str(correctPhrase))
        if len(userPhrase) >= len(correctPhrase):
            length = len(userPhrase)
        else:
            length = len(correctPhrase)
        percentage = (1 - distance/length) * 100
        return percentage

    def calcWPM(self, chars, timeTaken):
        mins = timeTaken/60
        words = chars/5
        return words/mins

    def giveUserLine(self, lineToType):
        print("The phrase is '" + lineToType + "'")
        input("Press enter to start")
        startTime = time.time()
        userString = input(lineToType + "\n")
        endTime = time.time()
        timeTaken = endTime - startTime
        return userString, timeTaken


    def loadConfig(self, fileName):
        fileDir = os.path.dirname(__file__)
        fullPath = os.path.join(fileDir, fileName)
        with open(fullPath, 'r') as f:
            inTerminal = f.readline().split('=')[1][:-1]


        if inTerminal == 'True':
            isInTerminal = True
        else:
            isInTerminal = False

        dict = {
            'inTerminal': isInTerminal
                }

        return dict

class QuoteCreator():
    def __init__(self, fileName):
        self.fileName = fileName

    def createQuote(self):
        choice = '-1'
        while choice != 'y':
            phrase = self.getPhrase()
            choice = self.validatePhrase(phrase)
        self.addToFile(phrase)

    def addToFile(self, toAdd):
        fileDir = os.path.dirname(__file__)
        fullPath = os.path.join(fileDir, self.fileName)
        with open(fullPath, 'a') as f:
            f.write('\n')
            f.write(toAdd)

    def getPhrase(self):
        phrase = input('Enter the phrase to type:\n>')
        return phrase

    def validatePhrase(self, phrase):
        print(phrase)
        choice = input("Is this correct?\n>").lower()

        while choice != 'y' and choice != 'n':
            print("Invalid enter either 'y' or 'n'")
            print(phrase)
            choice = input("Is this correct?\n>").lower()

        return choice




def displayMenu():
    print("1: play game\n2: create quote\n9: quit")
    return(input(">"))

def main():
    game = Game('thingsToType.txt', 'config.txt')
    creator = QuoteCreator('thingsToType.txt')
    choice = "-1"

    while choice != "9":
        choice = displayMenu()
        if choice == "1":
            game.playGame()
        elif choice == '2':
            creator.createQuote()



if __name__ == "__main__":
    main()

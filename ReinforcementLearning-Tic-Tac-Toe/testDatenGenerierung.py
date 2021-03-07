# Für die testerzeugung der RF Daten in einer höheren anzahl mit keinen Performance einschränkungen der GUI
import reinforcement
import gewinnlogik
import random
from matplotlib import pyplot as plt
import numpy as np
bussines_logik = gewinnlogik.gewinnlogik()

class ReinforcementLearningTestDaten(object):
    spielFelder         = 9
    spielfeld           = [""] * spielFelder
    currentPlayer       = "O"
    autoTurn            = 0
    autoTurnCounter     = 0
    durchlaeufe         = 0
    durchlaeufeCounter  = 0 
    spielfeld[0]        = currentPlayer
    tmpQTable           = []
    dict_Daten = {
        "xWinn": 0,
        "oWinn": 0,
        "unent": 0,
        "totalgames": 0}

    firstAgent = reinforcement.Agent()
    secondAgent = reinforcement.Agent()
    arrayDictData = []
    def __init__(self):
        self.spielfeld = [""] * self.spielFelder
    
    def writeData(self):
        saveString = "./save/testDaten"
        tmpWinChance = []
        tmpNumberOfGames = []
        tmpXWinchance = []
        with open(saveString, "w+") as file:
            for item in self.arrayDictData:
                file.writelines(str(item)+ "\n" )
                print(item['oWinn'])
                prozWinn = (item['oWinn'] * 100) / self.autoTurn
                print("proz; ", prozWinn )
                tmpWinChance.append( prozWinn )
                prozWinn = (item['xWinn'] * 100) / self.autoTurn
                tmpXWinchance.append( prozWinn)
                tmpNumberOfGames.append( item['totalgames'] )
        print(tmpWinChance)
        plt.plot(tmpNumberOfGames,tmpWinChance)
        plt.xlabel("Runden mit je %s Spiele" % self.autoTurn)
        plt.ylabel("% gewinn chance")
        plt.title("Überblick mit Lernrate %s" % self.firstAgent.lernrate)
        plt.grid()
        plt.legend(["KI-Agent Winn", "XAgent Winn"])
        plt.show()

    def resetDicData(self):
        tdict_Daten = {
            "xWinn": 0,
            "oWinn": 0,
            "unent": 0,
            "totalgames": 0
        }
        self.dict_Daten = tdict_Daten

    def tmpSaveData(self,dict):
        self.arrayDictData.append(dict)

    def getQTableFromKIAgent(self):
        return self.tmpQTable

    def createTestDaten(self, repeatGameTurns, turnsPerRepeatTurn, lernrate = 0.65):
        self.durchlaeufe            = repeatGameTurns
        self.autoTurn               = turnsPerRepeatTurn
        self.firstAgent.lernrate    = lernrate
        # n-fache durchrechnung
        while self.durchlaeufeCounter < self.durchlaeufe:
            while self.autoTurnCounter < self.autoTurn:
                #if self.autoTurnCounter % 25 == 0:
                #    self.secondAgent = reinforcement.Agent()
                #    self.secondAgent.lernrate = random.uniform(0.0001, 0.9999)

                for index in range(self.spielFelder):
                    self.currentPlayer = "O"  # ki startet
                    firstKiAction = self.firstAgent.getAction()
                    self.firstAgent.setTurn(firstKiAction)
                    self.secondAgent.setTurn(firstKiAction)
                    self.spielfeld[firstKiAction] = self.currentPlayer

                    if bussines_logik.checkStatus(firstKiAction, self.spielfeld):
                        self.firstAgent.qlearning('winn', self.firstAgent.getNotValidTurns())
                        self.secondAgent.qlearning('lose', self.secondAgent.getNotValidTurns())
                        self.autoTurnCounter += 1
                        self.spielfeld = [''] * self.spielFelder
                        self.firstAgent.resetENVTurns()
                        self.secondAgent.resetENVTurns()

                        self.dict_Daten["oWinn"] += 1
                        break
                    elif index == 4:
                        self.dict_Daten["unent"] += 1
                        self.autoTurnCounter += 1
                        self.firstAgent.qlearning('unent', self.firstAgent.getNotValidTurns())
                        self.secondAgent.qlearning('unent', self.secondAgent.getNotValidTurns())
                        self.firstAgent.resetENVTurns()
                        self.secondAgent.resetENVTurns()
                        break

                    else:
                        if self.firstAgent.getValidTurns() != 0:
                            self.currentPlayer = "X"  # playerTurn

                            secondKiAction = self.secondAgent.getAction()
                            self.spielfeld[secondKiAction] = self.currentPlayer
                            self.secondAgent.setTurn(secondKiAction)
                            self.firstAgent.setTurn(secondKiAction)

                            if bussines_logik.checkStatus(secondKiAction, self.spielfeld):
                                self.dict_Daten["xWinn"] += 1
                                self.firstAgent.qlearning('lose', self.firstAgent.getNotValidTurns())
                                self.secondAgent.qlearning(
                                    'winn', self.secondAgent.getNotValidTurns())
                                self.autoTurnCounter += 1
                                self.spielfeld = [''] * self.spielFelder
                                self.firstAgent.resetENVTurns()
                                self.secondAgent.resetENVTurns()
                                break

                self.firstAgent.resetENVTurns()
                self.secondAgent.resetENVTurns()
            self.durchlaeufeCounter += 1
            self.autoTurnCounter = 0
            self.dict_Daten['totalgames'] = self.durchlaeufeCounter
            self.tmpSaveData(self.dict_Daten)
            self.resetDicData()
            self.tmpQTable = self.firstAgent.getQTable()
            self.firstAgent = reinforcement.Agent()
            self.secondAgent = reinforcement.Agent()   
        self.writeData()

#unit test
a = ReinforcementLearningTestDaten()
a.createTestDaten(300,100)
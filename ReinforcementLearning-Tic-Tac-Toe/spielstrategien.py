import minmax_search

#beinhaltet und handelt alle spielstrategien/bewertungsfunktionen
"""
Einfachste Computer-Spielstrategie ist diezufällige Auswahl eines gültigen Spielzuges.

Die Umsetzung der Spielstrategie „Mensch“ besteht aus:
–  dem Warten auf die Eingabe eines Vektorfeldes, 
–  der Überprüfung dessen Gültigkeit und 
–  der Ausführung des Spielzuges.


WEitere Strategien
    Gewichtung der Positionen im Spielfeld
    Berechnung des Scores aus der Gewichtung der Positionen
"""

#Umsetzung einfacher spielzug nach validen spielfeld
#TODO: Spielzug nach MinxMax -> AlphaBeta
class strategie(object):
    ki_type = None
    RF_DATA = None
    #MODUS
    """
        0 = Simple /Random valid ki turn
        1 = MinMax Alpha Beta
    """
    def __init__(self, modus = 1):
        if modus == 1 :
            self.ki_type = minmax_search.alpabeta()
        #default, error managment
        else:
            modus = 1
    
    #triggert die eingebundene strategie
    def kiTurn(self):
        pass
    
    #gibt für den zug aus den numeric field die entsprechende
    #button number zurück
    def getButtonNumber(self):
        pass

    #-----------------------------------------------------------------------------------
    #   Gibt die RF-Data herraus zum Speichern
    #-----------------------------------------------------------------------------------
    def getRFData(self):
        return self.listTOStringConvert()

    def listTOStringConvert(self):
        r1 = None
        r2 = None
        r3 = None
        r4 = None
        r5 = None
        for item in self.ki_type.nummericGameField:
            if r1 == None:
                r1 = ''.join(str(item))
            elif r2 == None:
                r2 = ''.join(str(item))
            elif r3 == None:
                r3 = ''.join(str(item))
            elif r4 == None:
                r4 = ''.join(str(item))
            elif r5 == None:
                r5 = ''.join(str(item))            
        tmpRows = " RFDATA ["+  r1 + r2 + r3 + r4 + r5+"]"
        return tmpRows
    #-----------------------------------------------------------------------------------
    
    #-----------------------------------------------------------------------------------
    #   Simple Logik
    #-----------------------------------------------------------------------------------
    #einfache Spiellogik wo die "KI" ein random zug macht
    def simpleTurn(self):
        return minmax_search.rn.randint(0,8)
    

    #-----------------------------------------------------------------------------------
    #   Max Zahl der Validen züge ausrechnen
    def sortList(self, lst):
        return lst.sort()

    def maxValidElement(self, lst, sortetList, trys, lenOfSortetList):
        #größte Zahl ist valider zug
        maxLstElement = sortetList[lenOfSortetList]
        returnIndexButtonNumber = 0

        for index in range(len(lst)):
            if maxLstElement == lst[index]:
                returnIndexButtonNumber = index
                index = len(lst) + 1

        return returnIndexButtonNumber
    #-----------------------------------------------------------------------------------

    def simple1StepTurn(self, kiTurn):
        lst = []
        for index in range(0,8):
            lst.append(self.ki_type.nummericGameField[kiTurn][index])
        maxLstElement = max(lst)
        returnIndexButtonNumber = 0
        for index in range(len(lst)):
            if maxLstElement == lst[index]:
                returnIndexButtonNumber = index
                index = len(lst) + 1
        return returnIndexButtonNumber

    #-----------------------------------------------------------------------------------
    #TODO FEHLER !!!! ENDLOSLOOP 
    #einfache nach untengerichteter Turn mit beachtung der Werten Ohne veränderung dieser
    def simple1StepTurnWithLearning(self, kiTurn, trys):
        lst = []
        for index in range(0,9):
            lst.append(self.ki_type.nummericGameField[kiTurn][index])

        sortetList = lst.copy()
        self.sortList(sortetList) #sotiert nummeric
   
        lenOfSortetList = len(sortetList)-1 - trys #der jeweilige nummeric zug
        #print(lenOfSortetList)
        if lenOfSortetList < 0:
            lenOfSortetList = 0
        buttonNumber = self.maxValidElement(lst, sortetList, trys, lenOfSortetList)
        return buttonNumber
    #-----------------------------------------------------------------------------------

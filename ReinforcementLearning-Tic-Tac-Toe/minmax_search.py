import random as rn
#legte jeden edge mit einer randnumber fest
#legt vor jeden "0" zug inital -> wenn keine Nummer vorhanden (random number)
#wenn bereits vorhanden ist dann ignorieren

#Implementierung MINMAX _> AlphaBetha Suche
#Nicht implementiert -> Ba MinMax Allgemein

class allgemein(object):
    #MinMax Suche Allgemein
    #1) brauch ein array mit dem spielfeld als zahlen
        #init die ersten 9 felder für den start zug wird random hinterlegt
    #2) nach jeden zug von X werden alle mögliche züge des arrays gelogt mit rand Zahlen
        #jedoch nur wenn der wert noch nicht hinterlegt wurde
    #3) wenn das Spiel gewonnen wurde werden die gewichte/werte erhöht ! > 10
    #   wenn verloren dann wird verrintert bis ! < -10
    #   wenn unentschieden dann wird veringert bis ! < 0
    pass

class alpabeta(object):
    
    """#MinMax Suche AlphaBeta
        #1) brauch ein arry mit spielfeld als zahlen
        #   init die ersten 9 Zahlen als rand
        #2) nach jeden zug von X werden für weitere (3) Spielzüge die möglichkeiten berechnent
        #       - hierführ wird von der 3 ebene zu 2 ebene geschaut was der größere wert ist und alles kleiner unbeachtet
        #       - dies wird weiterverfolgt von 2 zu 1 ebene
        #3) wenn das Spiel gewonnen wurde werden die gewichte/werte erhöht ! > 10
        #   wenn verloren dann wird verrintert bis ! < -10
        #   wenn unentschieden dann wird veringert bis ! < 0
        #bekommt von jedenspielzug den wert gespeichert 
        #berechnete werte werden von hier an pygraph weitergereicht
    """
    ##LOGIK
    #repressentiert das Spielfeld mit Werten für die Verarbeitung
    nummericGameField           = None
    #repressentiert den möglichen spielzug als nummeriche darstellung
    turnOption                  = None

    #TODO: momentan max 5 ebenen
    const_maxTurnOptions        = None
    const_maxFields             = None

    usedFieldsWithButtonNumber  = None


    def __init__(self):
        self.nummericGameField          = []
        self.turnOption                 = []
        self.const_maxTurnOptions       = 5
        self.const_maxFields            = 9
        #für die entsprechende züge zum nachlernen
        self.usedFieldsWithButtonNumber = []

        self.firstInitEmptyField()

    #INIT beim erststart/reset der Lokalen Daten das vorhanden Feld an Numeric
    def firstInitEmptyField(self):
        #for jeden zug der ki(anzahl der möglichen züge)
        for index1 in range(self.const_maxTurnOptions):
            #for jeden turnOption zug der ki (0-9)
            for index2 in range(self.const_maxFields):
                self.turnOption.append(self.getRandNumber())
            #copyen und zurück setzten
            self.nummericGameField.append(self.turnOption.copy())
            self.turnOption.clear()

    def getRandNumber(self, start = -10, end = 10):
        return rn.randint(start,end)

    #Editiert ites element von einer einfachen liste
    def editItesElement(self,liste, i, value):
        liste.pop(i)
        liste.insert(i,value)

    #TODO
    #lernt den baum an um lose/win verstäkrt 
    #Winn lose für die KI
    def lerning(self, status):
        if status == "winn":
            for index in range(len(self.usedFieldsWithButtonNumber)):
                tmp = self.nummericGameField[index][ self.usedFieldsWithButtonNumber[index] ] #tmp zwischen speicher des alten value

                self.nummericGameField[index].pop(self.usedFieldsWithButtonNumber[index]) #löschen des eintrages
                tmp += 1
                if tmp > 10:
                    tmp = 10
                self.nummericGameField[index].insert(self.usedFieldsWithButtonNumber[index], tmp) #einfügen mit der manipulation

        elif status == "lose":
            for index in range(len(self.usedFieldsWithButtonNumber)):
                tmp = self.nummericGameField[index][ self.usedFieldsWithButtonNumber[index] ] #tmp zwischen speicher des alten value

                self.nummericGameField[index].pop(self.usedFieldsWithButtonNumber[index]) #löschen des eintrages
                tmp -= 2
                if tmp < -10:
                    tmp = -10
                self.nummericGameField[index].insert(self.usedFieldsWithButtonNumber[index], tmp) #einfügen mit der manipulation

        elif status =="unentschieden":

            for index in range(len(self.usedFieldsWithButtonNumber)):
                tmp = self.nummericGameField[index][ self.usedFieldsWithButtonNumber[index] ] #tmp zwischen speicher des alten value

                self.nummericGameField[index].pop(self.usedFieldsWithButtonNumber[index]) #löschen des eintrages
                tmp -= 1
                if tmp < -10:
                    tmp = -10
                self.nummericGameField[index].insert(self.usedFieldsWithButtonNumber[index], tmp) #einfügen mit der manipulation
        else:
            #default
            print("ERROR with LERNING in minmax_search.py!!")
            pass
    
    #TODO
    def getLoggingElement(self):
        pass

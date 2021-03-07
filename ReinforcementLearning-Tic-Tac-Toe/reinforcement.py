import numpy as np
import math
#-------------------------------------------------------------------------------
class Agent(object):
    lernrate            = None  #lernrate
    alpha               = None  #wert der ueber die anzahl der Spiele verringert wird um die auswirkungen nach x Spielen zu veringern
    spielrunden         = None  #speicher fuer die anzahl der Spielrunden, fuer den Exponent
    q_table             = []    #lering daten
    env_validTurns      = None  #list mit allen verfuegbaren turns in den Spielzug (int werte fuer die buttons)
    env_notValidTurns   = None  #list mit bereits gewaehlten turns (int werte fuer die buttons)

    def __init__(self):
        #init q table und jenv table auf 0
        self.q_table            = np.zeros((9,9))
        self.lernrate           = 0.65                  #einheitliche lernrate zum testen
        self.env_validTurns     = [0,1,2,3,4,5,6,7,8]   #liste aller noch zur verfuegung stehenden turns als int vom button
        self.env_notValidTurns  = []                    #liste aller bereits genommenen turns in der reihenfolge
        self.alpha              = 0.95                  #moeglichst grosser wert der exponent ist n == Spiele
        self.spielrunden        = 0                     #Init Wert start bei 0

    #setzt alle listen eigenschaften zurueck
    def resetENVTurns(self):
        self.env_validTurns     = [0,1,2,3,4,5,6,7,8]
        self.env_notValidTurns  = []

    #fuegt der liste ein weiteren turn hinzu
    def setTurn(self, buttonNumber):
        if buttonNumber == None:
            print("ButtonNumber None : " , buttonNumber)
        else:
            self.env_notValidTurns.append(buttonNumber)
            self.env_validTurns.remove(buttonNumber)

    #gibt die list mit bereits genommenen spielzuege zurueck in der richtigen reihenfolge
    def getNotValidTurns(self):
        return self.env_notValidTurns

    #gibt die list mit noch zur verfuegungstehenden turns zurueck
    def getValidTurns(self):
        return self.env_validTurns

    #gibt eine gerundetet Nummer zurueck, dies kann beliebig im dezimal veraendert werden
    def roundNumber(self, number, dezimalstelle=6): #obsolet
        number = round(number, dezimalstelle)
        return number

    #y ist die der turn , x ist der value fuer den turn
    def getQTableValue(self, yIndex,xIndex):
        return self.q_table[yIndex][xIndex]
    
    #gibt die gesamte qtable zurueck
    def getQTable(self):
        return self.q_table
    
    #setzt die qtabe mit vorhandenen Daten
    def setQTable(self, qtable):
        self.q_table = qtable

    #gibt einzelne ebene am qtable zurueck  
    def getQTableEbene(self, ebene):
        return self.q_table[ebene]

    #y ist die der turn , x ist der value fuer den turn, value wird gespeichert
    def setQTableValue(self,yIndex, xIndex, value):
        #minus 1 weil bei 0 beginnend
        xIndex = xIndex -1
        self.q_table[yIndex][xIndex] += value

    #rechnet für ein gemachtes Spiel die Values und uebergibt es "q_tableLearn" fuer die speicherung
    #bekommt, lst_turns fuer die lsite aller gemachten turns in der richtigen reihenfolge
    #bekommt diese werte aus der application.py
    def qlearning(self,status,lst_turns):
        isPlayerTurn = False
        if status == "lose":
            tmpStatusEndValue   = -1
            isPlayerTurn        = True
        elif status == "winn":
            tmpStatusEndValue = 1
            isPlayerTurn        = False
        elif status == "unent":
            tmpStatusEndValue = -0.5
        else:
            tmpStatusEndValue = -1000 
            print("ERROR: Agent, qlerning, falscher status: ", status)
            return

        lst_tmpTurnValues           = np.zeros( (len(lst_turns)) )          #liste mit den values zu den zugehoerigen turns
        helpingExponentForLernrate  = 1
        for turnIndex in range(len(lst_turns)-1,-1,-1):             #zaehlt die lsite von hinten nach vorn
            if turnIndex < len(lst_turns)-1:
                if isPlayerTurn:
                    #player turn
                    tmpEndValue =  round( self.learnCalculate( tmpStatusEndValue, self.getQTableValue(turnIndex ,lst_turns[turnIndex]), helpingExponentForLernrate),5)  #minus 1 weil qtable bei 0 anfangen hat
                    isPlayerTurn        = not isPlayerTurn
                else:
                    #ki turn
                    tmpEndValue =  round( self.learnCalculate(tmpStatusEndValue, self.getQTableValue(turnIndex ,lst_turns[turnIndex]), helpingExponentForLernrate), 5)  #minus 1 weil qtable bei 0 anfangen hat
                    isPlayerTurn        = not isPlayerTurn
                #tmpEndValue =  round( self.learnCalculate(tmpEndValue, self.getQTableValue(turnIndex ,lst_turns[turnIndex])), 3)  #minus 1 weil qtable bei 0 anfangen hat
                lst_tmpTurnValues[turnIndex] = lst_tmpTurnValues[turnIndex] + tmpEndValue
                helpingExponentForLernrate += 1
            else:
                lst_tmpTurnValues[turnIndex] = lst_tmpTurnValues[turnIndex] + tmpStatusEndValue
                isPlayerTurn        = not isPlayerTurn

        #die errechneten daten werden gespeichert in der qtable
        #ersetzt alle werte in die qtable
        for index in range(len(lst_tmpTurnValues)-1,-1,-1):
            if index >= 0:
                #TODO set add zum addieren !
                self.setQTableValue(index, lst_turns[index], lst_tmpTurnValues[index] )

    #rechnet die values fuer ein turn aus 
    def learnCalculate(self, value, oldCurrentTurnValue, helpingExponentForLernrate):
        #TODO: ,65 * 0,95^1 = QValue 
        value =  oldCurrentTurnValue + ( value * (self.lernrate**helpingExponentForLernrate *( self.alpha**(self.spielrunden) ) ) )
        self.spielrunden += 1
        return value    

    #gibt eine aktion zurueck
    #immer den groesten wert
    #wenn identische werte sind, dann wird der hoechste wert von der letzten stelle der lst genommen
    def getAction(self ):#anzahl der elemente ist von 8 start 0 last turn
        tmpQTableIndex          = 9 - len(self.env_validTurns) #-1 weil bei 0 beginnend
        tmpQTableEbeneValues    = self.getQTableEbene(tmpQTableIndex)

        validTurnQValues = []
        for index in range( len(self.env_validTurns) ):
            validTurnQValues.append( tmpQTableEbeneValues[ self.env_validTurns [index] -1 ] )

        maxTurnIndex            = np.argmax(validTurnQValues)#TODO nur die validen turns der index != tictactoe feld
        #gibt den turn von lst_validTurns zurück anhand des maxTurnIndex
        return self.env_validTurns[maxTurnIndex]
#-------------------------------------------------------------------------------




















#------------------------------------------------------------------------------- 
class MinMax(object):
    searchLvl           = None  #Gibt die Suchtiefe von MinMax an
    env_data            = None  #gesamte Spielfeld Informationen(alle Turns)
    env_validTurns      = None  #list mit allen verfuegbaren turns in den Spielzug (int werte fuer die buttons)
    env_notValidTurns   = None  #list mit bereits gewaehlten turns (int werte fuer die buttons)
    DEFAULT_SEARCHLVL   = 3     #Default wert fuer das searchlvl von MinMax
    DEFAULT_MAXSEARCHLVL= 9     #Default wert fuer das max lvl von MinMax

    def __init__(self):
        self.searchLvl          = self.DEFAULT_SEARCHLVL#tiefen suche von minmax
        self.env_data           = np.zeros((9,9))       #alle daten aus spielzuegen vom rf learning
        self.env_validTurns     = [0,1,2,3,4,5,6,7,8]   #liste aller noch zur verfuegung stehenden turns als int vom button
        self.env_notValidTurns  = []                    #liste aller bereits genommenen turns in der reihenfolge

    #gibt die list mit noch zur verfuegungstehenden turns zurueck
    def getValidTurns(self):
        return self.env_validTurns

    #gibt die list mit bereits genommenen spielzuege zurueck in der richtigen reihenfolge
    def getNotValidTurns(self):
        return self.env_notValidTurns

    #setzt das Searchlevel von MinMax um
    def setSearchLvl(self, lvl):
        if lvl > 9 or lvl < 1:
            print("ERROR: setSearchLVL ungueltiges LVL eingegeben: ", lvl )    
        else:
            self.searchLvl = lvl

    #gibt das aktuelle searchlvl der MinMax zurueck
    def getSearchLVL(self):
        return self.searchLvl

    #setzt alle listen eigenschaften zurueck
    def resetENVTurns(self):
        self.env_validTurns     = [0,1,2,3,4,5,6,7,8]
        self.env_notValidTurns  = []

    #fuegt der liste ein weiteren turn hinzu
    def setTurn(self, buttonNumber):
        if buttonNumber == None:
            print("ButtonNumber None : " , buttonNumber)
        else:
            self.env_notValidTurns.append(buttonNumber)
            self.env_validTurns.remove(buttonNumber)

    #speicherung der values in der ENV_DATA
    def saveENVDATA(self,turn,buttonNumber,value):
        self.env_data[turn][buttonNumber] = value
    
    #setzt die learning werte von der qtable /agent in die evndata ein
    def setEnvDataAfterLearning(self, qTable):
        #fuer jeden spielzug von der qtable den wert einfuegen
        #jeder spielzug
        for turnIndex in range(len(qTable)):
            #fuer jeden buttonwert/spielzug wert
            for buttonIndex in range(len(qTable[turnIndex])):
                #setzt den qtable wert in die env data ein fuer minmax
                self.env_data[turnIndex][buttonIndex] = qTable[turnIndex][buttonIndex]  


    def getTurnEbeneTagKIOrPlayerLevel(self, number):
        #gibt zurueck, ob die ausgewaelte ebene fuer den Spieler oder der KI ist
        #player turn = mod2 == 0 else ki
        if number % 2 == 0:
            return True
        else:
            return False

    
    #MINMAX Searching anhand der Daten nach dem Algorithmus "AlphaBetah Suche , minmaxABSearch"
    #Wird für jeden turn ausgefuerht in der ki
    #valid turns sind von 0 anfangend deklariert
    def minmaxABSearch(self, qtabale, lst_InputvalidTurns):
        #fuer die verfuegbaren turns anhand der searchtiefe
        #max 9turns lvl min 1turn lvl

        lst_validTurns      = lst_InputvalidTurns   #alle verfuegbaren turns

        lst_optionalTurns   = []                    #ideale turns fuer ki
        tmpTurnValues       = 0

        #ueberprueft ob das searchlvl bei weiteren spielverlauf nicht out of index laeuft
        if self.searchLvl > len(lst_validTurns):
            print("searchlvl > len :", self.searchLvl)
            self.setSearchLvl(len(lst_validTurns))


        #searchlvl ist index für qtable, und von unten nach oben full turn dann edit turn
        for searchIndex in range(self.searchLvl-1,-1,-1):
            
            tmpTurn = self.getHighestLowestTurn(self.getTurnEbeneTagKIOrPlayerLevel(searchIndex+1), lst_validTurns, qtabale, searchIndex) #+1 weil index um 1 verringert wurde fuer die lsiten
            print("Turn: ", tmpTurn)
            print("ValidTurnList : ", lst_validTurns)
            
            lst_optionalTurns.append(tmpTurn)                                                                       #optional bester turn laut ki rueckwerts 
            lst_validTurns.remove(tmpTurn)                                                                          #aktualliserung der valid turns
            
            tmpTurnValues += qtabale[searchIndex][tmpTurn]                                                           #wert fuer den betrachteten turn
            #TODO in env speichern fuer den turn, löschen der validen turns
        
        #test
        print(lst_optionalTurns)
        return tmpTurnValues



    #gibt den hoechsten/lowsten turn je nach ki/player zurueck
    #flag==1 => player, flag==0 => ki
    #hoechsten/niedrigesten wert wenn doppel dann von vorne zuerst nach hinten
    def getHighestLowestTurn(self, flag, lst_validTurns,qtable, qtableSeachrEbene):
        tmpValue = 0
        tmpTurn = 0
        
        if flag == True:    #Player
            for index in range(len(lst_validTurns)):
                if tmpValue >= qtable[qtableSeachrEbene][index]:
                    tmpValue    = qtable[qtableSeachrEbene][index]
                    tmpTurn     = lst_validTurns[index]

        
        else:               #KI
            for index in range(len(lst_validTurns)):
                if tmpValue <= qtable[qtableSeachrEbene][index]:
                    tmpValue    = qtable[qtableSeachrEbene][index]
                    tmpTurn     = lst_validTurns[index]
        print("Status: ", flag)
        return tmpTurn
#-------------------------------------------------------------------------------



















#-------------------------------------------------------------------------------
#Unit Test
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#Ki-Agent Testing
#a = Agent()

#QTable Learning
#turnexample1 = [5,7,9,4,6,1] #x winn
#turnexample2 = [1,3,2,5,4] #o winn
#turnexample3 = [7,1,5,2,3] #o winn

#a.qlearning("lose",turnexample1)
#a.qlearning("winn",turnexample2)
#a.qlearning("winn",turnexample3)


#validTurns1 = [1,2,3,4,5,6,7,8,9]
#validTurns2 = [2,4,5,6,7,8,9]
#validTurns3 = [4,6,7,8,9]

#print("action: ", a.getAction(validTurns1))
#print("action: ", a.getAction(validTurns2))
#print("action: ", a.getAction(validTurns3))


#qtable = a.getQTable()
#Get turn Actionf from Agent
#print("Agent Button Action: ", a.getAction(qtable[0]) )
#-------------------------------------------------------------------------------


#MinMax Env Testing
#-------------------------------------------------------------------------------
#b = MinMax()
#print(b.getTurnEbeneTagKIOrPlayerLevel(3) )
#tmp = b.getHighestLowestTurn(0,qtable[1])
#print("TMP :", tmp)
#b.setSearchLvl(9)
#print( b.minmaxABSearch(qtable, [0,1,2,3,4,5,6,7,8]))
#print( qtable)

#-------------------------------------------------------------------------------




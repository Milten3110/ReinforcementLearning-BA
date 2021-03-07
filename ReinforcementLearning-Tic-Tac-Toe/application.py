import tkinter as tk
import spielzugverwaltung
import gewinnlogik
import reinforcement as rf

#akzeptierter gewinnstatus: winn, lose, unent

class App(object):
    #----------------------------------------------------------------------------------------------------
    #       self Application Variables
    #----------------------------------------------------------------------------------------------------
    const_reinforcementAgentTurnCounter = 600
    counterAutoTurnRestart              = 0
    totalXWinn                          = 0
    totalOWinn                          = 0
    totalUnentschieden                  = 0
    
    minMaxSearch                        = None
    agent                               = None
    secondAgent                         = None
    datenGenerator                      = None

    turnManager                         = None
    bussines_logik                      = None

    currentTurnsInSession               = None #gesammt Spiele

    #The main Window Size
    windowHeight            = 500
    windowWidth             = 300

    windowGameHeight        = 500
    windowGameWidth         = 300

    #MainFrame
    main                    = None
    mainFrame               = None

    #representiert das Spielfeld
    spielfeldButtons        = 9
    spielfeld = [""] * spielfeldButtons

    #Anordnung der Buttons im Spielfeld
    buttonColumn            = [0,100,200]
    buttonRow               = [0,100,200]

    #ButtonArray
    #TODO: 2d List, ebene
    buttons = [None] * spielfeldButtons
    buttonStates                        = ["normal"] * spielfeldButtons
    currentPLayer                       = "O" #TODO: eventuell auf 0 und 1 als Kodierung für den Spieler umsteigen
    
    label_currentPLayerNameObj          = None

    label_currentPlayerValueObj         = None
    label_currentPlayerValue            = currentPLayer
    
    label_currentTurnNameObj            = None
    label_currentTurnValueObj           = None
    button_restart                      = None

    button_resetLocalData               = None
    button_showLocalData                = None
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #       INIT
    #----------------------------------------------------------------------------------------------------
    def __init__(self):
        # MainWindow Grid
        self.currentTurnsInSession  = 0

        self.main                   = tk.Tk()
        self.mainFrame              = tk.Frame(self.main, width=self.windowWidth, height=self.windowHeight, relief="sunken")
        self.mainFrame.pack()
    
        self.turnManager            = spielzugverwaltung.spielzugverwaltung() #Instanz der Spielzugverwaltung
        self.bussines_logik         = gewinnlogik.gewinnlogik()

        self.main.protocol("WM_DELETE_WINDOW", self.closingWindow )

        self.minMaxSearch           = rf.MinMax()   #ist fuer das scoreing der turns
        self.agent                  = rf.Agent()    #ist der entscheider anhand von parametern
        self.secondAgent            = rf.Agent()    #secondAgent zum testDatenGenerierung
        self.agent.lernrate         = 0.5
        
        #self.secondAgent.lernrate   = 0.5

        #TODO zuerst der Ki Turn
        self.kiTurnFirst()
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #   Closing Window Methode zum Speichern Persistent
    #----------------------------------------------------------------------------------------------------
    def closingWindow(self):
        self.turnManager.saveHandler.persistSave(self.turnManager.pygraph.getGraphAsString(),self.turnManager.strategy.getRFData() )
        self.main.destroy()
    #----------------------------------------------------------------------------------------------------



    #----------------------------------------------------------------------------------------------------
    #   Erste KI Turn
    #----------------------------------------------------------------------------------------------------  
    def kiTurnFirst(self):
        kiAction = self.agent.getAction()
        #self.minMaxSearch.setTurn( kiAction )
        print("DEBUG: KI will Turn: ", kiAction)
        self.playerChange(kiAction)

    def kiTurnRegular(self):
        #getAction meint den indice von validturns
        kiAction = self.agent.getAction()
        print("DEBUG: KI will Turn: ", kiAction)
        return kiAction

    def secondKiRegularturn(self):
        secondKiAction = self.secondAgent.getAction()
        return secondKiAction
    #----------------------------------------------------------------------------------------------------



    #----------------------------------------------------------------------------------------------------
    #       Setzt das Spielfeld zurück, es fängt immer "O" an
    #----------------------------------------------------------------------------------------------------
    def reset_game(self):
        #States zurücksetzen
        self.currentTurnsInSession += 1

        self.buttonStates = ["normal"] * self.spielfeldButtons
        self.spielfeld = [""] * self.spielfeldButtons
        self.currentPLayer = "O" # zur Verkleinerung des Spielbaums fängt immer der gleiche Spieler an
        #playCounter zurücksetzen
        self.turnManager.currentTurn = 0
        self.minMaxSearch.resetENVTurns()    #setzt minmax env turn data zurueck
    #----------------------------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------------------------
    #       Sperrt alle Buttons, wenn das Spiel gewonnen wurde
    #----------------------------------------------------------------------------------------------------
    def closed_game_activity(self):
        self.buttonStates = ["disabled"] * self.spielfeldButtons
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #       Ändert den aktuellen Spieler
    #----------------------------------------------------------------------------------------------------
    def togglePlayer(self):
        if self.currentPLayer == "O":
            self.currentPLayer = "X"
        else:
            self.currentPLayer = "O"
    # wenn die Spieler mit 0 und 1 codiert wären, dann könnte man einfach den Wert berechnen:
    # self.currentPlayer = 1 - self.currentPlayer
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #       Spiel Logik
    #----------------------------------------------------------------------------------------------------
    #auslagerung, abfrage ist gewonnen/verloren
    def abfrageIsWinn(self):
        self.closed_game_activity()
        
        #log den Status des Spieles
        self.turnManager.loggEndStatus(self.turnManager.treeText,"winn", self.currentPLayer)
        #die beiden folgenden Labels werden nicht angezeigt
        self.label_currentPlayerValue += " hat gewonnen!"



        #KI Learning, akzeptierte status
        if self.currentPLayer == "X":
            #self.turnManager.strategy.ki_type.lerning("lose")
            
            #learning des agenten anhand der turns
            self.agent.qlearning('lose', self.minMaxSearch.getNotValidTurns() )
            #self.secondAgent.qlearning('winn', self.minMaxSearch.getNotValidTurns() )
            self.totalXWinn += 1
            
        else:
            #self.turnManager.strategy.ki_type.lerning("winn")
            
            #learning des agenten anhand der turns
            self.agent.qlearning('winn', self.minMaxSearch.getNotValidTurns())
            #self.secondAgent.qlearning('lose', self.minMaxSearch.getNotValidTurns() )
            self.totalOWinn += 1

        #print neues netz
        #print("\nanpassung: " , self.agent.getQTable(), "\n")

    #auslagerung abfrage is unentschieden
    def unentschieden(self):
       #log den Status des Spieles
        self.turnManager.loggEndStatus(self.turnManager.treeText,"unentschieden",self.currentPLayer)
        self.label_currentPlayerValue = " unentschieden!"
        self.totalUnentschieden += 1


    def playerChange(self, buttonNumber, kiFirst = False, isPlayerCalled = False, kiTurnIsTrue = False):
        
        treeTextOld = self.turnManager.treeText

        if self.turnManager.numberOfKiTurn == 0:
            self.turnManager.strategy.ki_type.usedFieldsWithButtonNumber.append(buttonNumber)

        self.spielfeld[buttonNumber] = self.currentPLayer
        self.turnManager.edite_treeText(buttonNumber,self.currentPLayer)
        self.buttonStates[buttonNumber] = "disabled" # beendet die Funktion des Buttons
        
        #Gewinnlogik Loggen
        yIndex = len(self.minMaxSearch.getNotValidTurns())
        xIndex = buttonNumber
        qvalue = self.agent.getQTableValue(yIndex,xIndex)
        self.turnManager.spielzug_logg(treeTextOld, self.turnManager.treeText, buttonNumber, self.currentPLayer, qvalue)        

        
        #self.minMaxSearch.setTurn(buttonNumber)
        self.agent.setTurn(buttonNumber)

        #abfrage ob gewonnen/verloren oder unentschieden
        if self.bussines_logik.checkStatus(buttonNumber, self.spielfeld):
            self.abfrageIsWinn()
            print("IsWinCalled")
            self.agent.resetENVTurns()
            
            #autoturnsCounter 
            if self.counterAutoTurnRestart < self.const_reinforcementAgentTurnCounter:
                self.restart_new_game()

                
            
        #unentschieden
        elif self.turnManager.currentTurn == 9:
            self.unentschieden()
            self.agent.resetENVTurns()
            
            #autoturnsCounter 
            if self.counterAutoTurnRestart < self.const_reinforcementAgentTurnCounter:
                self.restart_new_game()
                              
        
        #KITURN
        elif self.currentPLayer == "X":
            kiButton = self.kiTurnRegular()
           

            self.togglePlayer()
            self.label_currentPlayerValue = self.currentPLayer
            self.playerChange(kiButton)

        elif self.currentPLayer == "O":
            #secondKiButton = self.secondKiRegularturn()

            self.togglePlayer()
            self.label_currentPlayerValue = self.currentPLayer
            #if self.counterAutoTurnRestart  < self.const_reinforcementAgentTurnCounter:
            #    self.playerChange(secondKiButton)
                 
        
        
        self.init_window()
        
        
        

    #----------------------------------------------------------------------------------------------------



    #----------------------------------------------------------------------------------------------------
    #       Erstelle die GUI für die eigentliche Spielinteraktion
    #----------------------------------------------------------------------------------------------------
    def buildGui(self, frame):
        #Garbage
        self.clearFrame(frame)

        self.init_window()
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #       Erstellung der Haupt Scene
    #----------------------------------------------------------------------------------------------------
    def init_window(self):
        self.spielfeldFrame = tk.Frame(self.mainFrame, width=self.windowGameWidth, height=self.windowGameHeight, relief="sunken")
        self.spielfeldFrame.place(x=10, y=10)

        # ausgelagerte erstellung
        for x in range(self.spielfeldButtons):
            self.initSpielfeldElement(x)
        self.initAnzeigeElemente()
        self.updateAnzeigeElemente()

        #self.main.mainloop()

    #----------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------
    #       Erstellung der Spiel-Elemente
    # ----------------------------------------------------------------------------------------------------
    def initSpielfeldElement(self, x):
        self.buttons[x] = tk.Button(self.spielfeldFrame, height=4, width=8, text=self.spielfeld[x], state=self.buttonStates[x], command=lambda: self.playerChange(x) )
        self.buttons[x].place(x=self.buttonColumn[x % 3], y=self.buttonRow[int(x/3)] )

    #----------------------------------------------------------------------------------------------------
    #       Erstellung der Spiel-Elemente
    #----------------------------------------------------------------------------------------------------
    def initAnzeigeElemente(self):
        #Spieler Anzeige
        self.label_currentPlayerValueObj    = tk.Label(self.spielfeldFrame, text=self.label_currentPlayerValue)
        self.label_currentPLayerNameObj     = tk.Label(self.spielfeldFrame, text="Aktueller Spieler : ")

        self.label_currentTurnValueObj      = tk.Label(self.spielfeldFrame, text = str(self.turnManager.currentTurn) )
        self.label_currentTurnNameObj       = tk.Label(self.spielfeldFrame, text="Aktueller Spielzug : ")

        #neu start
        self.button_restart                 = tk.Button(self.spielfeldFrame, text="Neues Spiel", command= lambda: self.restart_new_game() )
        #TODO visual Graph
        self.button_showLocalData           = tk.Button(self.spielfeldFrame, text="Graph Anzeigen", command= lambda: self.showGraph())
        #TODO reset LocalData
        self.button_resetLocalData          = tk.Button(self.spielfeldFrame, text="Locale Daten löschen!", command= lambda: self.resetLocalData())

        #TODO zurück zum Menü


    #----------------------------------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------------------------------
    #       Update der Gui Elemente
    #----------------------------------------------------------------------------------------------------
    def updateAnzeigeElemente(self):
        #Texte
        self.label_currentPLayerNameObj.place(x=30, y=300)
        self.label_currentPlayerValueObj.place(x=150, y=300)

        self.label_currentTurnNameObj.place(x=30, y=320)
        self.label_currentTurnValueObj.place(x=150, y=320)

        #Buttons zum Steuern
        self.button_restart.place(x=30, y=350)
        self.button_showLocalData.place(x=30, y=400)
        self.button_resetLocalData.place(x=150, y=400)


    #----------------------------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------------------------
    #       Setzt das Spiel zurück für ein neuen Durchlauf
    #----------------------------------------------------------------------------------------------------
    def restart_new_game(self):
        
        
        self.counterAutoTurnRestart += 1

        self.bussines_logik.reset_gamefield()
        self.turnManager.reset_treeText()
        
        self.reset_game()
        self.label_currentPlayerValue = self.currentPLayer
        
        self.turnManager.strategy.ki_type.usedFieldsWithButtonNumber.clear() #setzt liste der gemachten zuge (mit numeric), zurück
        self.kiTurnFirst()
        print("Status: x wins: ", self.totalXWinn, ", o wins: ", self.totalOWinn, ", unentschieden: ", self.totalUnentschieden)
        self.init_window()
    #----------------------------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------------------------
    #       Graph Visualisieren
    #----------------------------------------------------------------------------------------------------
    def showGraph(self):
        self.turnManager.show_tree()
    #----------------------------------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------------------------------
    #       Graphdaten zurück setzten auf Blackbox //spielzugverwaltung.py(->.create_file)
    #----------------------------------------------------------------------------------------------------
    def resetLocalData(self):
        self.turnManager.create_file()
    #----------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------------------------
    #       Löscht alte Frames, beim wechsel
    #----------------------------------------------------------------------------------------------------
    def clearFrame(self, frame):
        frame.destroy()
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #       Start Menü
    #----------------------------------------------------------------------------------------------------
    #TODO main menue vor start erstellen, wird gerade nicht mehr angezeigt
    # Start, Load, Import, Beenden
    def showStartMenue(self):
        #Start Menü
        menueFrame = tk.Frame(self.mainFrame, width=self.windowWidth, height=self.windowHeight)
        menueFrame.place(x=10,y=10)

        button  = tk.Button(menueFrame, text="Start", command= lambda: self.buildGui(menueFrame) )
        button.pack()

        #TODO MAINLOOP
        #self.main.mainloop()
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #       StartHandler der selflikation
    #----------------------------------------------------------------------------------------------------
    def start(self):
        self.showStartMenue()
        return 0
    #----------------------------------------------------------------------------------------------------

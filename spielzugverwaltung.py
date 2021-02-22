from graphviz import Source
from graphviz import Digraph
import gvGraphToPyData # repressent a pythoneditable graph
import spielstrategien # ki logik
import speichermanagement


#Speichert die Informationen Persistent
class spielzugverwaltung(object):
    #Global Variables
    #filename = "localgraphdata.gv"
    #directory = "./save"

    #Speicherlogik
    saveHandler = None
    
    #Basis Text für den anfang = 0 ebenenCount
    currentTurn = 0
    numberOfKiTurn = None
    treeText = "- | - | - \n - | - | - \n - | - | - "

    buttontextIndices = [0,4,8,12,16,20,24,28,32]
    #Indice Werte
    """"
      0 | 4  | 8  
     12 | 16 | 20 
     24 | 28 | 32 
    """


    #Maximal 9 Ebenen, 0 ist hierbei die Init ebene
    #representiert die Zeile von wo an die entsprechene Ebene anfängt, um hier eine einfügung zu machen
    ebenenInGVDatei = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

    #lines für die Einzelnen Ebenen in der GV Datei
    #wird bei jeder änderung neu geladen
    pygraph         = None

    #verwendete Spielstrategie
    strategy        = None

    def __init__(self):
        self.pygraph            = gvGraphToPyData.pygraph()
        self.strategy           = spielstrategien.strategie(1)
        self.numberOfKiTurn     = 0 #represent the ebene in der ki
        self.saveHandler        = speichermanagement.manager()

    #obsolet
    """
    def set_ebenen_dict(self):
        tmpLineCount = 1

        with open(self.directory+self.filename,"r+") as file:
            for item in file.readlines():
                #Durch Scennen und die Ebenen einzeln finden
                if item.strip(" \n") == "//ebene 1":
                    self.ebenenInGVDatei[1] = tmpLineCount

                if item.strip(" \n") == "//ebene 2":
                    self.ebenenInGVDatei[2] = tmpLineCount
                                    
                if item.strip(" \n") == "//ebene 3":
                    self.ebenenInGVDatei[3] = tmpLineCount
                                    
                if item.strip(" \n") == "//ebene 4":
                    self.ebenenInGVDatei[4] = tmpLineCount
                                    
                if item.strip(" \n") == "//ebene 5":
                    self.ebenenInGVDatei[5] = tmpLineCount
                                    
                if item.strip(" \n") == "//ebene 6":
                    self.ebenenInGVDatei[6] = tmpLineCount
                    
                if item.strip(" \n") == "//ebene 7":
                    self.ebenenInGVDatei[7] = tmpLineCount
                    
                if item.strip(" \n") == "//ebene 8":
                    self.ebenenInGVDatei[8] = tmpLineCount
                                    
                if item.strip(" \n") == "//ebene 9":
                    self.ebenenInGVDatei[9] = tmpLineCount
                    
                tmpLineCount += 1
        print("Test EbeneLines : ", self.ebenenInGVDatei)
    """


    #macht aus der liste einen verständlichen string
    def list_to_string(self):
        lst = list(self.treeText)
        tmpString = ""
        for item in lst:
            tmpString += item
        print (tmpString)


    #Verändert den Textbaum für den aktuellen Zug
    def edite_treeText(self, button, player):
        self.currentTurn +=1
        lst = list(self.treeText)
        lst[self.buttontextIndices[button]] = player
        self.treeText = ""
        for item in lst:
            self.treeText += item

    #NONE wird durch den berechneten wert der Bewertungsfunktion hinterlegt
    def spielzug_logg(self, spielzug_old, spielzug_current, buttonNumber, player, qvalue):
        #lesen = r, schreiben = w, anhängen = a
        #Schreibt in die Datei
        #hängt eine Verbindung zwischen old -> current ein
        
        #gibt den nummeric wert des feldes an TODO
        #bewertung = self.strategy.ki_type.nummericGameField[self.numberOfKiTurn][buttonNumber]
        bewertung = qvalue
        
        if player == "O": #kiTurn ++
            self.numberOfKiTurn += 1          


        self.pygraph.addEdge(spielzug_old,spielzug_current, bewertung ,"red") #get Logget PyGraph

        #Speichert die Daten temp
        self.saveHandler.localSave(self.pygraph.getGraphAsString() )
        #with open(self.directory+self.filename,"w") as file:
        #    file.write(self.pygraph.getGraphAsString())
        
        return True
    
    #hinterlegt einen zusätzlichen Node für die INformation 
    #ob über den Weg gewonnen wurde
    def loggEndStatus(self,spielzug_current,status,currentPlayer):
        color = "red"
        writeStauts = currentPlayer + " " + status
        if status == "unentschieden":
            writeStauts = status

        self.pygraph.addEdge(spielzug_current, writeStauts,None,color)
        
        #Speichert temp die Session
        self.saveHandler.localSave(self.pygraph.getGraphAsString() )
        
        #with open(self.directory+self.filename,"w") as file:
        #    file.write(self.pygraph.getGraphAsString())

    # erstellt eine blackbox datei für die folgenden Spielverläufe
    def create_file(self):
        self.saveHandler.localSave(self.pygraph.resetGraph() )
        
        #with open(self.directory+self.filename, "w") as file:
        #    file.write(self.pygraph.resetGraph() )        
        self.show_tree()
    
    def update_file(self):
        self.saveHandler.localSave(self.pygraph.getGraphAsString() )
        #with open(self.directory+self.filename,"w") as file:
        #   file.write(self.pygraph.getGraphAsString())

    #TODO: vorherige Session nicht überschreiben , zeigt momentan immer aktuelle Session an
    def show_tree(self):
        tmp_Data = Source.from_file(self.saveHandler.local_dateipfad)
        tmp_Data.render(filename=self.saveHandler.localfilename,directory= self.saveHandler.directory,format="svg", view=True)
    
    #Setzt bei neustart den treeText auf den Anfang zurück
    #auserdem setzt es die farben des graphen auf black um den neuen spielverlauf zu verdeutlichen
    def reset_treeText(self):
        self.treeText = "- | - | - \n - | - | - \n - | - | - "
        self.pygraph.newGameTurn()
        self.update_file()
        self.numberOfKiTurn = 0

#Stellt eine Interne Representation von einfachen Dot struktur dar
#   speichert eine Session als Graph
class pygraph(object):
    #Dies ist das Zeichen , welches anstelle des \n Zeilenumbruchs geschrieben wird
    #Es wird beim Anzeigen des Grpahen jedoch ersetzt um die Übersicht wieder zu Normalisieren
    secureBreakZeichen = "Q"
    #----------------------------------------------------------------------------------------
    #   ClassValue
    #----------------------------------------------------------------------------------------

    #Graph need
    """
        graph{
            nodes{
                color :str
                label :str
            }
            edge{
                color :str
                node[label] -> node[label] :str
                label //minMax :int
            }
            turn{
                old :str
                current :str
                label //Win/Lose/UNent. :str
            }
        }
    """
    
    pygraph_graph       = [] # Spiegelt alle veränderungen etc wieder
    #Graph Items
    pygraph_node        = []
    pygraph_edge        = []

    edgeInsertedIndex = None

    def __init__(self, startNode = "INIT_NODE"):
        self.pygraph_graph.append("digraph G {")
        self.pygraph_node.append("node [color=blue]")
        self.pygraph_graph.append(self.pygraph_node[0])
        self.pygraph_graph.append("}")
        self.pygraph_graph.insert( self.insert() , startNode)
        self.edgeInsertedIndex = 0

    #fügt am ende der liste neue elemente ein um so den spielverlauf nachzubilden
    def insert(self):
        return len(self.pygraph_graph) -1
    
    def syncGraph(self, value):
        self.pygraph_graph.insert(self.insert(), value)

    #TODO: update Number Label für die Visualisierung des Lernens
    #über den Index soll später alle änderungen in der edge dann auf dem Graph übertragen werden
    def addEdge(self, preTurn, succTurn, name = None, color="black"):
        insertIndex = self.insert()
        canWrite = True #prüfvalue für das Doppelte Loggen

        #drop dublicates and change the color
        tmpDic = {"edgeGraphIndex":insertIndex, "preTurn": "\"" + preTurn + "\"","succTurn": "\"" + succTurn + "\"","name":name,"color":color}
        for index in range(len(self.pygraph_edge)):
            tmpVergleichValue = [ self.pygraph_edge[index]['preTurn'], self.pygraph_edge[index]['succTurn'] ]
            tmpLoggValue = [ tmpDic['preTurn'], tmpDic['succTurn'] ]
            if tmpLoggValue == tmpVergleichValue:
                canWrite = False
                self.pygraph_edge[index]['color']   = "red"
                self.pygraph_edge[index]['name']    = name
                self.updateEdges()
                
        
        if canWrite:
            self.pygraph_edge.append( {"edgeGraphIndex":insertIndex, "preTurn": "\"" + preTurn + "\"","succTurn": "\"" + succTurn + "\"","name":name,"color":color} )
            self.syncGraph( self.getEdgeString(self.edgeInsertedIndex) )
            self.edgeInsertedIndex += 1 # erhöht die Max EdgeCounter

    
    def getEdgeString(self, edgeIndex):
        tmpList = []
        tmpList.append(self.pygraph_edge[edgeIndex]['preTurn'])
        tmpList.append(self.pygraph_edge[edgeIndex]['succTurn'])
        tmpList.append(self.pygraph_edge[edgeIndex]['color'])
        tmpList.append(self.pygraph_edge[edgeIndex]['name'])        
        tmpString = "/*edgeIndex: " + str(edgeIndex) + "*/ " + tmpList[0] + " -> " + tmpList[1] + " [color=" + tmpList[2] + ", label= " +  str(tmpList[3]) + "]" 
        return tmpString

    def getGraphAsString(self):
        tmp = " ".join(self.pygraph_graph)
        #BATest, Q ist ein secure zeichen, welches ein zeilenumbruch darstellt, aber seperat gespeichert werden soll
        tmp = tmp.replace("\n", "\\n")
        return tmp

    def resetGraph(self):
        #Cleaning Lists
        self.pygraph_graph.clear()
        self.pygraph_edge.clear()
        self.pygraph_node.clear()

        #create reset graph
        self.pygraph_graph.append("digraph G {")
        self.pygraph_node.append("node [color=blue]")
        self.pygraph_graph.append(self.pygraph_node[0])
        self.pygraph_graph.append("}")
        self.edgeInsertedIndex = 0

        return self.getGraphAsString()
    
    def updatePyGraph(self, value):
        self.pygraph_graph.clear()
        self.pygraph_graph.append("digraph G {")
        self.pygraph_node.append("node [color=blue]")
        self.pygraph_graph.append(value)
        self.pygraph_graph.append("}")

    #update all edges and rewrite it in the pygraph
    def updateEdges(self):
        tmpString = ""
        for index in range(len(self.pygraph_edge)):
            tmpString += self.getEdgeString(index)
        self.updatePyGraph(tmpString)

    #Wenn neues Spiel angefangen wird, werden alle makierungen des altenspielverlaufs (farb) auf black gesetzt um den neuen Spielverlauf
    #hier deutlich zu sehen
    #alle edges werden modifiziert und der graph wird anschliesend neu geschrieben
    def newGameTurn(self):
        tmpString = ""
        for index in range(len(self.pygraph_edge)):
            self.pygraph_edge[index]['color'] = "black"
            tmpString += self.getEdgeString(index)
        #print("newGameTurn String: ", tmpString)
        self.updatePyGraph(tmpString)
        
#UnitTest   
#a = pygraph()
#a.addEdge("A","B","test")
#a.addEdge("B","1", 2)
#a.addEdge("B","2", 13, "red")
#a.newGameTurn()
#a.addEdge("B","3")
#a.addEdge("B","C")
#a.addEdge("C","A")
#print(a.getGraphAsString())
#turn.show_tree()

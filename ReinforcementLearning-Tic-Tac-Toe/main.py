import application          #imports the main gui programm

#TEST
import sys
#sys.setrecursionlimit(1500)
sys.setrecursionlimit(5000)
#END TEST

App = application.App()     #init

#Endlessloop
#App.main.protocol("WM_DELETE_WINDOW", App.turnManager.saveHandler.persistSave(App.turnManager.pygraph.getGraphAsString() ) )

#App.buildGui()
App.start()                 #start the main programm

App.main.mainloop()
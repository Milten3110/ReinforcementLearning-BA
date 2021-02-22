#Zuständig für die Speicherung der Localen und Persisten Daten
class manager(object):
    #Global Variable
    localfilename   = "localgraphdata.gv"   #name der LocalenDaten
    persistfilename = "persistSave"         #name der PersistDaten
    directory       = "./save/"              #name des ordners für die Speicherung der Gesamten Daten
    local_dateipfad = None                  #der Pfad für die Datei
    

    def __init__(self):
        self.local_dateipfad  = self.directory+self.localfilename

    #Persister Speichervorgang
    def persistSave(self, dataset, rfdataset):
        with open(self.directory+self.persistfilename, "a+") as file:
            file.writelines( dataset + rfdataset + "\n" )


    def persistLoad(self):
        pass
    
    #Localer Speichervorgang
    def localSave(self, data):
        with open(self.directory+self.localfilename, "w") as file:
            file.write(data)

    def localLoad(self):
        pass

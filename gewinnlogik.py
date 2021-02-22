
#Erkennt ob das Spiel gewonnen ist, oder Verloren & Unentschieden
class gewinnlogik(object):
    #TODO bessere Logik implementiern
    gamefield = [""] * 9

    def reset_gamefield(self):
        self.gamefield = [""] * 9
        #print("DEBUGLOG:gewinnlogik.reset_gamefield:: ", self.gamefield[i])

    #gibt True zurück, wenn Spieler gewonnen hat
    #TODO: prüfen, ob gamefield, set_gamefield, reset_gamefield, checkStatusX noch gebraucht wird
    def set_gamefield(self, buttonNumber, player):
        self.gamefield[buttonNumber] = player
        return self.checkStatusX(buttonNumber)

    def checkStatusX(self, buttonNumber):
        # prüft wagerecht
        startPoint = int(buttonNumber/3)*3
        if self.gamefield[startPoint] == self.gamefield[startPoint+1] == self.gamefield[startPoint+2]:
            return True

        # prüft senkrecht
        startPoint = buttonNumber % 3
        if self.gamefield[startPoint] == self.gamefield[startPoint+3] == self.gamefield[startPoint+6]:
            return True

        # prüft diagonal links-oben nach rechts-unten
        if buttonNumber % 4 == 0 and self.gamefield[0] == self.gamefield[4] == self.gamefield[8]:
            return True

        # prüft diagonal rechts-oben nach links-unten
        if (buttonNumber % 4 == 2 or buttonNumber == 4) and self.gamefield[2] == self.gamefield[4] == self.gamefield[6]:
            return True

    # gibt True zurück, wenn aktueller Spieler gewonnen hat
    def checkStatus(self, buttonNumber, gameVector):
        # prüft wagerecht
        startPoint = int(buttonNumber/3)*3
        if gameVector[startPoint] == gameVector[startPoint+1] == gameVector[startPoint+2]:
            return True

        # prüft senkrecht
        startPoint = buttonNumber % 3
        if gameVector[startPoint] == gameVector[startPoint+3] == gameVector[startPoint+6]:
            return True

        # prüft diagonal links-oben nach rechts-unten
        if buttonNumber % 4 == 0 and gameVector[0] == gameVector[4] == gameVector[8]:
            return True

        # prüft diagonal rechts-oben nach links-unten
        if (buttonNumber % 4 == 2 or buttonNumber == 4) and gameVector[2] == gameVector[4] == gameVector[6]:
            return True


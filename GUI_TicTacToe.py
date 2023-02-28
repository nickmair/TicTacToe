#Nick Mair Load and Save Function

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QGridLayout, QGroupBox, QMessageBox, QFileDialog
)
from PyQt6.QtCore import QFile, QIODevice, QDataStream

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        #Hier wird ein minimum,der größe des Windows, festgelegt
        self.setMinimumSize(200, 200) 
        

        #Erstellt das Spielfeld (als Liste mit 9 Nullen)
        self.board = [0] * 9
        # Player 1 startet
        self.turn = 0  
        #leere Liste für die Buttons erstellt
        self.buttons = []
        self.boardGroupBox = QGroupBox()
        # Die Buttons auf dem Spielfeld anzuordnen
        self.boardLayout = QGridLayout(self.boardGroupBox)
        # Schleife über die Zeilen und Spalten des Spielfelds
        for i in range(3):
            for j in range(3):
                button = QPushButton("", self.boardGroupBox)
                button.clicked.connect(self.handleButtonClicked)
                self.boardLayout.addWidget(button, i, j)
                self.buttons.append(button)

        # Erstellt ein QLabel-Objekt, um den Spielstatus anzuzeigen
        self.statusLabel = QLabel("Player 1's turn")

        #Erstellt Button Speichern,Laden und Verlassen des Spieles
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveGame)
        self.loadButton = QPushButton("Load")
        self.loadButton.clicked.connect(self.loadGame)
        self.leaveButton = QPushButton("Leave")
        self.leaveButton.clicked.connect(self.leaveGame)

        # Erstellt ein QGridLayout-Objekt, um die Widgets anzuordnen
        layout = QGridLayout(self)
        layout.addWidget(self.statusLabel, 0, 0)
        layout.addWidget(self.saveButton, 0, 1)
        layout.addWidget(self.loadButton, 0, 2)
        layout.addWidget(self.leaveButton, 0, 3)
        layout.addWidget(self.boardGroupBox, 1, 0, 1, 4)

        #Zeigt Fenster 
        self.setWindowTitle("Tic Tac Toe")
        self.show()

    #Funktion zum Verlassen
    def leaveGame(self):
        #Man bekommt Bestätigunsnachricht wo man auf Ja drücken muss um zu verlassen
        reply = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to leave the game?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

    #Funktion wird aufgerufen wenn ein Button auf dem Spiel geklickt wird
    def handleButtonClicked(self):
        button = self.sender()
        index = self.buttons.index(button)
        
        #Wenn Feld Leer ist, wird Zeichen des aktuellen spielers gesetzt
        if self.board[index] == 0:  
            if self.turn == 0:
                button.setText("X")
                self.board[index] = 1
                self.turn = 1
                self.statusLabel.setText("Player 2's turn")
                
                
            else:
                button.setText("O")
                self.board[index] = 2
                self.turn = 0
                self.statusLabel.setText("Player 1's turn")
                
                
            #Es wird überprüft ob Spieler gewonnen 
            winner = self.checkWinner()
            if winner:
                QMessageBox.information(self, "Winner", f"Player {winner} wins!")
                self.resetBoard()
    
    def checkWinner(self):
        #Überprüft ob Spieler gewonnen hat
        for i in range(3):
            # Überprüft die Zeilen des Spielbretts
            row = self.board[3*i:3*i+3]
            if row.count(1) == 3:
                return 1
            elif row.count(2) == 3:
                return 2

            # Überprüft die Spalten des Spielbretts
            col = self.board[i::3]
            if col.count(1) == 3:
                return 1
            elif col.count(2) == 3:
                return 2
            
        # Überprüft die Diagonalen des Spielbretts
        diag1 = self.board[::4]
        if diag1.count(1) == 3:
            return 1
        elif diag1.count(2) == 3:
            return 2

        diag2 = self.board[2:7:2]
        if diag2.count(1) == 3:
            return 1
        elif diag2.count(2) == 3:
            return 2

        # Überprüft, ob es ein Unentschieden gibt
        if 0 not in self.board:
            QMessageBox.information(self, "Draw", "It's a draw!")
            self.resetBoard()

        return 0

    def resetBoard(self):
        #Setzt Spielbrett zurück
        for button in self.buttons:
            button.setText("")
        self.board = [0] * 9
        self.turn = 0
    def saveGame(self):
        # Öffnet einen Dialog, um den Speicherort und den Namen der zu speichernden Datei auszuwählen
        filename, _ = QFileDialog.getSaveFileName(self, "Spiel speichern", "", "Tic Tac Toe Dateien (*.txt)")
        if filename:
            # Öffnet die Datei zum Schreiben
            file = QFile(filename)
            if file.open(QIODevice.OpenModeFlag.WriteOnly):
                # Erstellt einen Datenstrom, um Daten in die Datei zu schreiben
                stream = QDataStream(file)
                # Schreibt die aktuelle Spielrunde in die Datei
                stream.writeInt(self.turn)
                # Schreibt die aktuellen Spielzüge in die Datei
                for row in range(3):
                    for col in range(3):
                        stream.writeInt(self.board[row * 3 + col])
                file.close()
                print(f"Spiel wurde unter {filename} gespeichert")
            else:
                QMessageBox.warning(self, "Fehler", "Konnte nicht in die Datei {} schreiben".format(filename))

    def loadGame(self):
        # Öffnet einen Dialog, um die zu ladende Datei auszuwählen
        filename, _ = QFileDialog.getOpenFileName(self, "Spiel laden", "", "Tic Tac Toe Dateien (*.txt)")
        if filename:
            # Öffnet die Datei zum Lesen
            file = QFile(filename)
            if file.open(QIODevice.OpenModeFlag.ReadOnly):
                # Erstellt einen Datenstrom, um Daten aus der Datei zu lesen
                stream = QDataStream(file)
                # Liest die Spielrunde aus der Datei
                self.turn = stream.readInt()
                print(f"Runde gelesen: {self.turn}")
                # Liest die Spielzüge aus der Datei
                self.board = []
                for i in range(9):
                    cell = stream.readInt()
                    self.board.append(cell)
                print(f"Spielzüge gelesen: {self.board}")
                # Aktualisiert die Beschriftungen der Buttons, um den Spielverlauf wiederherzustellen
                for i, value in enumerate(self.board):
                    if value == 1:
                        self.buttons[i].setText("X")
                    elif value == 2:
                        self.buttons[i].setText("O")
                # Aktualisiert den Status des Spiels, um den aktuellen Spieler anzuzeigen
                if self.turn == 0:
                    self.statusLabel.setText("Spieler 1 ist am Zug")
                else:
                    self.statusLabel.setText("Spieler 2 ist am Zug")
                QMessageBox.information(self, "Geladen", f"Spiel wurde aus {filename} geladen <3")
                file.close()
            else:
                QMessageBox.warning(self, "Fehler", "Konnte die Datei {} nicht lesen ;( )".format(filename))



     
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = TicTacToe()
    game.show()
    sys.exit(app.exec())

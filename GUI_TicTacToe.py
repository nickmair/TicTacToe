#Filip Stojanovic 4ahel HTL_Anichstrasse--> GUI

#module werden importiert
import sys 
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QGridLayout, QGroupBox
)




class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200) #festlegung der minimum größe des fensters
        

        # erstellt Spielbrett auf
        self.board = [0] * 9 # Die Liste für das Spielfeld
        self.turn = 0  # das der Spieler 1 beginnt
        self.buttons = [] # Liste für Buttons wird angelegt
        self.boardGroupBox = QGroupBox()
        self.boardLayout = QGridLayout(self.boardGroupBox) # Layout für das Spielbrett wird angelegt
        for i in range(3):
            for j in range(3):
                button = QPushButton("", self.boardGroupBox) # Button für jedes Feld wird angelegt
                self.boardLayout.addWidget(button, i, j) # Button wird dem Layout hinzugefügt
                self.buttons.append(button) # Buttons wird der Liste hinzugefügt

        # Label für Spielstatus & Buttons für Speichern/Laden werden angelegt
        self.statusLabel = QLabel("Player 1's turn") # Label für den Spielstatus
        self.saveButton = QPushButton("Save") # Button für das Speichern des Spiels
        self.loadButton = QPushButton("Load") # Button für das Laden eines gespeicherten Spiels
        self.leaveButton = QPushButton("Leave") # Button für das Beenden des Spiels
        

        # Layout für das gesamte Fenster wird angelegt
        layout = QGridLayout(self)
        layout.addWidget(self.statusLabel, 0, 0)
        layout.addWidget(self.saveButton, 0, 1)
        layout.addWidget(self.loadButton, 0, 2)
        layout.addWidget(self.leaveButton, 0, 3)
        layout.addWidget(self.boardGroupBox, 1, 0, 1, 4)

        self.setWindowTitle("Tic Tac Toe") #Window Titel wird festgelegt
        self.show() # Fenster wird angezeigt

if __name__ == '__main__':
    app = QApplication(sys.argv) #rstellt eine Instanz der Qt-Anwendung, sys.argv sind die Argumente->die dem Skript übergeben werden
    game = TicTacToe() #
    game.show() #Zeigt das TicTacToe-Spiel an 
    sys.exit(app.exec())# Die Anwendung wird gestartet und ausgeführt

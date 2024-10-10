from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMessageBox as mb
from PyQt5.QtGui import QPixmap
import random
import string

cls, wnd = uic.loadUiType("PM_hangman.ui")


class Hangman(wnd, cls):
    def __init__(self, parent = None):
        super().__init__(parent) 
        self.setupUi(self)
        self.no_disp()
        self.gB.setStyleSheet("QGroupBox#gB {border:0;}")
        self.gB2.setStyleSheet("QGroupBox#gB2 {border:0;}")
        self.gB3.setStyleSheet("QGroupBox#gB3 {border:0;}");
        self.pBAnimals.setStyleSheet("QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}"
                             )
        self.start_game()
        self.displ_hangman(8)
    
    
    @pyqtSlot()
    def no_disp(self):
        self.gB.setEnabled(False)
        self.gB2.setEnabled(False)
        self.gB3.setEnabled(False)
        self.gB.setVisible(False)
        self.gB2.setVisible(False)
        self.gB3.setVisible(False)
        self.lError.setVisible(False)
    
    
    @pyqtSlot()
    def disp(self):
        self.gB.setEnabled(True)
        self.gB2.setEnabled(True)
        self.gB.setVisible(True)
        self.gB2.setVisible(True)


    @pyqtSlot()
    def keyPressEvent(self, event):
        if '_' in self.unders: 
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.on_pBSubmit_clicked()                       
    
    
    
    @pyqtSlot()
    def start_game(self):
        self.guessed_letters = []
        self.guesses = 0
    
    
    @pyqtSlot()
    def displ_hangman(self, x):
        for i in range(1,9):
            if i == x:
                image = f'hangman{i}.png'
                self.pix = QPixmap(image)
                self.scene = QGraphicsScene()
                self.graphicsView.setScene(self.scene)
                self.pixmap_item = QGraphicsPixmapItem(self.pix)
                self.scene.addItem(self.pixmap_item)
                self.graphicsView.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio) 
    
    
    @pyqtSlot()    
    def reset(self):
        self.scene.clear()
        self.pTWord.clear()
        self.tEGuessedLetters.clear()
        self.gB2.setEnabled(False)
    
   
    @pyqtSlot()    
    def on_actionNew_game_triggered(self):
        try:
            mb.information(None, "Information", "The  answer was {}".format(self.word.lower()))
            self.disp() 
            self.reset()
            self.start_game()
        except:
            pass
        
        
    @pyqtSlot()    
    def on_actionExit_triggered(self):
        if mb.question(self, "Exit?", "You sure?") == mb.Yes:
            exit()
        else:
            pass


    @pyqtSlot()
    def on_pBStart_clicked(self):
        if self.pBStart.isChecked() == True:
            self.gB.setVisible(True)
            self.gB.setEnabled(True)
            self.pBStart.setVisible(False)
        else:
            self.gB.setVisible(False)
          
          
    @pyqtSlot()
    def on_pBAnimals_clicked(self):   
        if self.pBStart.isChecked() == True:
            self.gB2.setVisible(True)
            self.gB2.setEnabled(True)
            self.gB3.setVisible(True)
            self.gB3.setEnabled(True)

        filename = 'animals.txt'
        with open(filename, 'r') as plik:
                file = plik.read()
                #self.test.setPlainText(animals)
                file = file.split()
                fileInd = random.randint(0, len(file) - 1)
                self.word =  file[fileInd]
                print(self.word)
                self.unders = '_ ' * len(self.word)
                self.pTWord.setText(self.unders) 
                self.gB.setEnabled(False)                
    
    
    @pyqtSlot()    
    def on_pBFood_clicked(self):   
        if self.pBStart.isChecked() == True:
            self.gB2.setVisible(True)
            self.gB2.setEnabled(True)
            self.gB3.setVisible(True)
            self.gB3.setEnabled(True)
            
        filename = 'food.txt'
        with open(filename, 'r') as plik:
                file = plik.read()
                file = file.split()
                fileInd = random.randint(0, len(file) - 1)
                self.word =  file[fileInd]
                print(self.word)
                self.unders = '_ ' * len(self.word)
                self.pTWord.setText(self.unders) 
                self.gB.setEnabled(False)
     
     
    @pyqtSlot() 
    def on_pBSubmit_clicked(self):
        l = string.ascii_lowercase
        L = string.ascii_uppercase
        ch = l + L       
        letter = self.lEInput.text().upper()    
    
        if letter not in self.guessed_letters and letter in ch:
            guess_wrong = True
            self.guessed_letters.append(letter)
            self.tEGuessedLetters.setPlainText(' '.join(self.guessed_letters))
            self.list_und = self.unders.split()

            #Checking if the guess is correct
            if self.guesses < 7 or '_' not in self.unders:
            
                self.lError.setVisible(False)
                for i, j in enumerate(self.word):
                    if j == letter:
                        guess_wrong = False
                        self.list_und[i] = j
                if guess_wrong and self.lEInput.text():
                    self.guesses += 1
                    print(self.guesses)
                    self.displ_hangman(self.guesses)
                               
                #Updating Label  with underscores  
                update = ' '.join(self.list_und)    
                self.updated_label = ''
                for s1, s2 in zip(self.unders, update):
                    if s1 != s2:
                        self.updated_label += s2
                    else:
                        self.updated_label += s1
                if len(self.unders) < len(update):
                    self.updated_label += update[len(self.unders):]
                self.unders = self.updated_label
                self.pTWord.setText(self.unders)                           
            
                if '_' not in self.unders:
                    mb.information(None, "Congratulations", "You have won !")
                    if mb.question(None, "Question", "Do you want to play again?") == mb.Yes:
                        self.disp()
                        self.reset()
                        self.start_game()
                    else:
                        exit()            
            #else:
                elif self.guesses == 7 and '_' in self.unders:
                    self.displ_hangman(7)
                    mb.information(None, "You lost", "The  answer was {}".format(self.word.lower()))
                    if mb.question(None, "Question", "Do you want to play again?") == mb.Yes:
                        self.disp()
                        self.reset()
                        self.start_game()
                    else:
                        exit()
        else:
            self.lError.setVisible(True)
        self.lEInput.clear()

  
                 
                 
        
if __name__ == "__main__":
    nasza = QApplication([])
    okno = Hangman()
    okno.show()
    
    nasza.exec()
    
    
 
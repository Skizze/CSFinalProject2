import os.path
from PyQt5.QtWidgets import *
from view import *

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QMainWindow, Ui_MainWindow):
    #alphabet of values for letters
    alphabet = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8,
                "J": 9, "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16,
                "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25, "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8,
                "j": 9, "k": 10, "l": 11, "m": 12, "n": 13, "o": 14, "p": 15, "q": 16,
                "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25}
    def __init__(self, *args, **kwargs):
        '''
        Initializer method
        :param args: miscellaneous parameters
        :param kwargs: miscellaneous parameters
        '''
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.aInput.hide()
        self.bInput.hide()
        self.fileOut.hide()
        self.aLabel.hide()
        self.bLabel.hide()
        self.vigenereLabel.hide()
        self.fileName.hide()
        self.outputOption2.clicked.connect(lambda: self.file_display(True))
        self.outputOption1.clicked.connect(lambda: self.file_display(False))
        self.cipherOption1.clicked.connect(lambda: self.shiftShow(1))
        self.cipherOption2.clicked.connect(lambda: self.shiftShow(2))
        self.cipherOption3.clicked.connect(lambda: self.shiftShow(3))

        self.go_button.clicked.connect(lambda: self.cipher_prepare())

    def file_display(self, show:bool):
        '''
        Toggles the file name box depending on the output selected
        :param show: Boolean on whether to toggle the box on or off
        :return:
        '''
        if show:
            self.fileName.show()
            self.fileOut.show()
        else:
            self.fileName.hide()
            self.fileOut.hide()

    def shiftShow(self, op:int) -> None:
        '''
        Changes the shift/key/a,b input boxes depending on cipher chosen
        :param op: Int value of 1,2, or 3 depending on cipher
        :return: None
        '''
        self.vigenereLabel.hide()
        self.caesarLabel.hide()
        self.aLabel.hide()
        self.bLabel.hide()
        if op == 3:
            self.shiftInput.hide()
            self.aInput.show()
            self.bInput.show()
            self.aLabel.show()
            self.bLabel.show()
        if op < 3:
            self.shiftInput.show()
            self.aInput.hide()
            self.bInput.hide()
        if op == 1:
            self.caesarLabel.show()
        elif op == 2:
            self.vigenereLabel.show()

    def cipher_prepare(self) -> None:
        '''
        Readies the cipher calls with exception handling
        :return: None
        '''
        try:
            self.cipher()
        except ValueError:
            self.outputLabel.setText("Error:\nInvalid input\n")
        except Exception as error:
            self.outputLabel.setText("Error:\n" + str(error))

    def cipher(self) -> None:
        '''
        Handles which method to call and what parameters to pass for the ciphers
        :return: None
        '''
        output = ""
        if self.buttonGroup_1.checkedButton().text() == "Caesar":
            if self.buttonGroup_2.checkedButton().text() == "Encrypt":
                output = self.caesar(self.textEdit.text(), int(self.shiftInput.text()), True)
            if self.buttonGroup_2.checkedButton().text() == "Decrypt":
                output = self.caesar(self.textEdit.text(), int(self.shiftInput.text()), False)

        if self.buttonGroup_1.checkedButton().text() == "Vigenere":
            if self.buttonGroup_2.checkedButton().text() == "Encrypt":
                output = self.vigenere(self.textEdit.text(), self.shiftInput.text(), True)
            if self.buttonGroup_2.checkedButton().text() == "Decrypt":
                output = self.vigenere(self.textEdit.text(), self.shiftInput.text(), False)

        if self.buttonGroup_1.checkedButton().text() == "Affine":
            if self.buttonGroup_2.checkedButton().text() == "Encrypt":
                output = self.affine(self.textEdit.text(), int(self.aInput.text()), int(self.bInput.text()), True)
            if self.buttonGroup_2.checkedButton().text() == "Decrypt":
                output = self.affine(self.textEdit.text(), int(self.aInput.text()), int(self.bInput.text()), False)

        if self.buttonGroup_3.checkedButton().text() == "In app":
            self.outputLabel.setText(output)
        else:
            if not(os.path.isfile(self.fileOut.text())):
                outputFile = open(self.fileOut.text() + ".txt", 'w')
                outputFile.write(output)
                outputFile.close()


    def toLetter(self, num:int) -> str:
        '''
        Converts a number into its corresponding letter value
        :param num: int value to be converted to a letter
        :return:
        '''
        while num > 25:
            num %= 26
        while num < 0:
            num += 26
        keys = list(self.alphabet.keys())
        return keys[num]

    def caesar(self, word:str, shift:int, encode:bool) -> str:
        '''
        Method to apply caesar cipher
        :param word: word to convert
        :param shift: amount to shift each letter
        :param encode: whether to encrypt (true) or decrypt (false)
        :return: the encoded/decoded word
        '''
        newWord = ""
        if encode:
            for letter in word:
                if letter == " " or letter == "." or letter == "!" or letter == "?" or letter == ",":
                    newWord += letter
                    continue
                if letter not in self.alphabet:
                    raise Exception("Invalid symbol present\nin message.")
                newWord += self.toLetter(self.alphabet[letter] + shift)
        else:
            for letter in word:
                if letter == " " or letter == "." or letter == "!" or letter == "?" or letter == ",":
                    newWord += letter
                    continue
                if letter not in self.alphabet:
                    raise Exception("Invalid symbol present\nin message.")
                newWord += self.toLetter(self.alphabet[letter] - shift)
        return newWord

    def vigenere(self, word:str, crib:str, encode:bool) -> str:
        '''
        Method to apply vigenere cipher to word
        :param word: word to encrypt/decrypt
        :param crib: crib value to encrypt/decrypt with
        :param encode: whether to encrypt (true) or decrypt (false)
        :return: the encoded/decoded word
        '''
        newCrib = []
        for letter in crib:
            if letter not in self.alphabet:
                raise Exception("Invalid symbol in key\nonly letters a-z")
            newCrib.append(self.alphabet[letter])
        crib = newCrib
        newWord = ""
        if encode:
            for i in range(0, len(word)):
                if word[i:i + 1] == " " or word[i:i + 1] == "." or word[i:i + 1] == "!" or word[i:i + 1] == "?" or word[i:i + 1] == ",":
                    newWord += word[i:i + 1]
                    continue
                if word[i:i + 1] not in self.alphabet:
                    raise Exception("Invalid symbol in message\nonly letter a-z\nand punctuation")
                newWord += self.caesar(word[i:i + 1], crib[i % len(crib)], True)
        else:
            for i in range(0, len(word)):
                if word[i:i + 1] == " " or word[i:i + 1] == "." or word[i:i + 1] == "!" or word[i:i + 1] == "?" or word[i:i + 1] == ",":
                    newWord += word[i:i + 1]
                    continue
                if word[i:i + 1] not in self.alphabet:
                    raise Exception("Invalid symbol in message\nonly letter a-z\nand punctuation")
                newWord += self.caesar(word[i:i + 1], crib[i % len(crib)], False)
        return newWord

    def affine(self, word:str, a:int, b:int, encode:bool) -> str:
        '''
        Applies affine cipher to a word
        :param word: word to encrypt/decrypt
        :param a: alpha value in encryption/decryption
        :param b: beta value in encryption/decryption
        :param encode: whether to encode (true) or decode (false)
        :return: new word with cipher applied
        '''
        if a % 2 == 0 or a % 13 == 0 or a < 3 or a > 25:
            raise Exception("Invalid alpha value.\nmust be an odd int\nbetween 3 and 25\nand not 13")
        if b < 0 or b > 25:
            raise Exception("Invalid beta value.\nints 0-25 only")
        newWord = ""
        if encode:
            for letter in word:
                if letter == " " or letter == "." or letter == "!" or letter == "?" or letter == ",":
                    newWord += letter
                    continue
                if letter not in self.alphabet:
                    raise Exception("Invalid symbol in message\nonly letters a-z\nand punctuation.")
                newWord += self.toLetter(self.alphabet[letter] * a + b)
        else:
            for letter in word:
                if letter == " " or letter == "." or letter == "!" or letter == "?" or letter == ",":
                    newWord += letter
                    continue
                if letter not in self.alphabet:
                    raise Exception("Invalid symbol in message\nonly letters a-z\nand punctuation.")
                value = self.alphabet[letter]
                while (value - b) % a != 0:
                    value += 26
                newWord += self.toLetter(int((value - b) / a))
        return newWord

alphabet = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8,
            "J": 9, "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16,
            "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25}
def toLetter(num):
    while num > 25:
        num %= 26
    while num < 0:
        num += 26
    keys = list(alphabet.keys())
    return keys[num]

def Caesar(word, shift, encode):
    newWord = ""
    if encode:
        for letter in word:
            if letter == " ":
                newWord += " "
                continue
            newWord += toLetter(alphabet[letter] + shift)
    else:
        for letter in word:
            if letter == " ":
                newWord += " "
                continue
            newWord += toLetter(alphabet[letter] - shift)
    return newWord

def Vigenere(word, crib, encode):
    newCrib = []
    for letter in crib:
        newCrib.append(alphabet[letter])
    crib = newCrib
    newWord = ""
    if encode:
        for i in range(0, len(word)):
            if word[i:i+1] == " ":
                newWord += " "
                continue
            newWord += Caesar(word[i:i+1], crib[i % len(crib)], True)
    else:
        for i in range(0, len(word)):
            if word[i:i+1] == " ":
                newWord += " "
                continue
            newWord += Caesar(word[i:i+1], crib[i % len(crib)], False)
    return newWord

def Affine(word, a, b, encode):
    newWord = ""
    if encode:
        for letter in word:
            if letter == " ":
                newWord += " "
                continue
            newWord += toLetter(alphabet[letter] * a + b)
    else:
        for letter in word:
            if letter == " ":
                newWord += " "
                continue
            value = alphabet[letter]
            while (value - b) % a != 0:
                value += 26
            newWord += toLetter(int((value - b) / a))
    return newWord

print(Vigenere("ASDF", "HI", True))
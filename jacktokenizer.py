import jacktoken

class JackTokenizer:
    def __init__(self, jack_code):
        self.jack_code = jack_code
        self.tack_code = None #Tokenized Jack Code

    def make_tokens(self):
        pass









test_list = ['class Square {', 'field int x, y;', 'constructor Square new(int Ax, int Ay, int Asize) {', 'let x = Ax;',
             'do Memory.deAlloc(this);', 'do Screen.drawRectangle(x, y, x, y);', 'if (size) {', '}', 'return;',
             'if (((y + size) < 254) & ((x + size) < 510)) {']




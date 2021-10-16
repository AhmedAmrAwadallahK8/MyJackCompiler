import jacktoken as t


class JackTokenizer:
    keyword = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
               'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
    #integerConstant
    #StringConstant "sadjaodoa"
    #identifier (names of method or vars etc)

    def __init__(self, jack_code):
        self.jack_code = jack_code
        self.tack_code = [] #Tokenized Jack Code

    def get_tack_code(self):
        '''Getter

        :return: (List) List of JackToken objects
        '''
        return self.tack_code

    def make_tokens(self):
        '''Converts Jack code into Tokenized Jack Code. This information is stored in the object variable tack_code

        :return: None
        '''
        print('enetered make tokens')
        def handle_string(substr):
            '''Takes in a substring and extracts information necessary for making a StringConstant token

            :param substr: (String) substring that contains a StringConstant
            :return: (Int) Length of the StringConstant within the substr
                     (String) The extracted StringConstant from the substr
            '''
            end_ind = substr.find('"')
            return len(substr[:end_ind]), '"' + substr[:end_ind] + '"'

        def handle_int(substr):
            '''Takes in a substring and extracts information necessary for making a integerConstant token

            :param substr: (String) substring that contains an integerConstant
            :return: (Int) Length of the integerConstant within the substr
                     (String) The extracted integerConstant within the substr
            '''
            end_ind = 0
            for i, char in enumerate(substr):
                if char.isdigit():
                    end_ind = i + 1
                else:
                    break

            out_int = substr[:end_ind]
            return len(out_int), out_int

        for line in self.jack_code:
            print(line)
            mid_line = ''
            o_i = 0
            i = 1
            while i <= len(line):
                print(line)
                mid_line = line[o_i:]
                tok = line[o_i:i]
                next_char = line[i:i+1]
                print('___________________')
                print('CurrentTok:' + tok)
                print('NextTokChar:' + next_char)
                if tok == ' ':
                    o_i = i
                elif tok == '"':
                    print('Entered String')
                    len_str_tok, str_tok = handle_string(mid_line[1:])
                    self.tack_code.append(t.JackToken('StringConstant', str_tok))
                    i += 1 + len_str_tok
                    o_i = i
                elif tok.isdigit():
                    print('Entered Integer')
                    len_int_tok, int_tok = handle_int(mid_line)
                    self.tack_code.append(t.JackToken('integerConstant', int_tok))
                    i += len_int_tok - 1
                    o_i = i
                elif tok in self.symbol:
                    print('Entered Symbol')
                    self.tack_code.append(t.JackToken('symbol', tok))
                    o_i = i
                elif tok in self.keyword:
                    print('Entered Keyword')
                    self.tack_code.append(t.JackToken('keyword', tok))
                    o_i = i
                elif next_char in self.symbol or next_char == ' ':
                    print('Entered identifier statement')
                    self.tack_code.append(t.JackToken('identifier', tok))
                    o_i = i
                i += 1


test_list1 = ['field int x, y;']


test_list2 = ['class Square {', 'field int x, y;', 'constructor Square new(int Ax, int Ay, int Asize) {', 'let x = Ax;',
              'do Memory.deAlloc(this);', 'do Screen.drawRectangle(x, y, x, y);', 'if (size) {', '}', 'return;',
              'if (((y + size) < 254) & ((x + size) < 510)) {', 'let x = "Hello World"; let y = 10; ']
test_symbol = [',']


tokenize = JackTokenizer(test_list2)
tokenize.make_tokens()
token_list = tokenize.get_tack_code()
print(token_list)
for token in token_list:
    print(token.get_data())







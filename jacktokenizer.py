import jacktoken as t


class JackTokenizer:
    keyword = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
               'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def __init__(self, file_name, jack_code):
        self.file_name = file_name
        self.jack_code = jack_code
        self.index = 0
        self.tack_code = []  # Tokenized Jack Code
        self.make_tokens()

    def get_file_name(self):
        """Getter

        :return: (String) The String the represents the name of the life
        """
        return self.file_name

    def get_tack_code(self):
        """Getter

        :return: (List) List of JackToken objects
        """
        return self.tack_code

    def get_ind_token(self):
        """Getter

        :return: JackToken object at the index specified
        """
        return self.tack_code[self.index]

    def get_ind(self):
        """Getter

        :return: (int) The current index value
        """
        return self.index

    def peek_next_token(self):
        """Method for when parsing becomes LL[2] which occurs when handling expressions

        :return: JackToken object that is ahead of the current JackToken
        """
        return self.tack_code[self.index+1]

    def advance(self):
        """Increment index by 1 if index is within the lists length otherwise set index to be equal to -1

        :return: None
        """
        if self.index < len(self.tack_code) - 1 and self.index > -1:
            self.index += 1
        else:
            self.index = -1

    def make_tokens(self):
        """Converts Jack code into Tokenized Jack Code. This information is stored in the object variable tack_code

        :return: None
        """

        def handle_string(substr):
            """Takes in a substring and extracts information necessary for making a StringConstant token

            :param substr: (String) substring that contains a StringConstant
            :return: (Int) Length of the StringConstant within the substr
                     (String) The extracted StringConstant from the substr
            """
            end_ind = substr.find('"')
            return len(substr[:end_ind]), substr[:end_ind]

        def handle_int(substr):
            """Takes in a substring and extracts information necessary for making a integerConstant token

            :param substr: (String) substring that contains an integerConstant
            :return: (Int) Length of the integerConstant within the substr
                     (String) The extracted integerConstant within the substr
            """
            end_ind = 0
            for i, char in enumerate(substr):
                if char.isdigit():
                    end_ind = i + 1
                else:
                    break

            out_int = substr[:end_ind]
            return len(out_int), out_int

        for line in self.jack_code:
            mid_line = ''
            o_i = 0  # Index where the line has already been processed up to
            i = 1
            while i <= len(line):
                mid_line = line[o_i:]  # Rest of the line that hasn't been tokenized yet
                tok = line[o_i:i]  # Possible token of size i - o_i
                next_char = line[i:i+1]  # Next character in the in the line
                if tok == ' ':  # Skip Spaces
                    o_i = i
                elif tok == '"':  # Quotes indicate a StringConstant Token
                    len_str_tok, str_tok = handle_string(mid_line[1:])
                    self.tack_code.append(t.JackToken('stringConstant', str_tok))
                    i += 1 + len_str_tok  # Move the index past the entire string that handle_string found
                    o_i = i
                elif tok.isdigit():  # Condition indicates a integerConstant Token is present
                    len_int_tok, int_tok = handle_int(mid_line)
                    self.tack_code.append(t.JackToken('integerConstant', int_tok))
                    i += len_int_tok - 1  # Move the index past the entire integer that handle_int found
                    o_i = i
                elif tok in self.symbol:  # Condition indicates a Symbol Token is present
                    '''if tok == '<':
                        self.tack_code.append(t.JackToken('symbol', '&lt;'))
                    elif tok == '>':
                        self.tack_code.append(t.JackToken('symbol', '&gt;'))
                    elif tok == '&':
                        self.tack_code.append(t.JackToken('symbol', '&amp;'))
                    else:'''
                    self.tack_code.append(t.JackToken('symbol', tok))
                    o_i = i
                elif tok in self.keyword:  # Condition indicates a Keyword Token is present
                    self.tack_code.append(t.JackToken('keyword', tok))
                    o_i = i
                elif next_char in self.symbol or next_char == ' ' or i == len(line):  # Condition indicates a Identifier token is present
                    self.tack_code.append(t.JackToken('identifier', tok))
                    o_i = i
                i += 1
        self.tack_code.append(t.JackToken('end', 'final token'))


'''test_list1 = ['field int x, y']


test_list2 = ['class Square {', 'field int x, y;', 'constructor Square new(int Ax, int Ay, int Asize) {', 'let x = Ax;',
              'do Memory.deAlloc(this);', 'do Screen.drawRectangle(x, y, x, y);', 'if (size) {', '}', 'return;',
              'if (((y + size) < 254) & ((x + size) < 510)) {', 'let x = "Hello World"; let y = 10; ']
test_symbol = [',']


tokenize = JackTokenizer('test.jack', test_list1)
token_list = tokenize.get_tack_code()
#print(token_list)
for token in token_list:
    print(token.get_data())'''








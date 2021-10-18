import jacktokenizer as jt


class CompilationEngine:
    def __init__(self, file_data):
        self.tokenizers = []
        self.tokenizer_ind = 0
        self.tab_num = 0
        for file in file_data:
            # First and second element of file store the file_name and the file_contents respectively
            self.tokenizers.append(jt.JackTokenizer(file[0], file[1]))
        self.current_tokenizer = self.tokenizers[self.tokenizer_ind]
        self.current_token = self.current_tokenizer.get_ind_token()

    def next_token(self):
        self.current_tokenizer.advance()
        if self.current_tokenizer.get_ind != -1:
            self.current_token = self.current_tokenizer.get_ind_token()
        else:
            print('No more tokens left')

    def xml_snippet_ll_1(self):
        xml_code = '\t' * self.tab_num
        xml_code += '<' + self.current_token.get_variety() + '> '
        xml_code += self.current_token.get_val()
        xml_code += ' </' + self.current_token.get_variety() + '>\n'
        self.next_token()
        return xml_code

    def compile_class_var_dec(self):
        """Responsible for parsing a class variable declaration

        :return: (String) XML representation
        """
        self.tab_num += 1
        out_xml = '\t'*self.tab_num
        out_xml += '<classVarDec>\n'
        if self.current_token.get_val() == 'static' or self.current_token.get_val() == 'field':
            self.tab_num += 1
            # Expect Keyword = static or field
            out_xml += self.xml_snippet_ll_1()
            # Expect a type
            out_xml += self.xml_snippet_ll_1()
            # Expect a variable name
            out_xml += self.xml_snippet_ll_1()
            # Expect ; or expect more variable names
            while self.current_token.get_val() != ';':
                # Expect a comma
                out_xml += self.xml_snippet_ll_1()
                # Expect a variable name
                out_xml += self.xml_snippet_ll_1()
            # Expect a ;
            out_xml += self.xml_snippet_ll_1()
            self.tab_num -= 1
        out_xml += '\t' * self.tab_num
        out_xml += '</classVarDec>\n'
        self.tab_num -= 1
        return out_xml

    def compile_var_dec(self):
        """Responsible for parsing a variable declaration

        :return: (String) XML representation
        """
        self.tab_num += 1
        out_xml = '\t' * self.tab_num
        out_xml += '<varDec>\n'
        if self.current_token.get_val() == 'var':
            self.tab_num += 1
            # Expect Keyword = var
            out_xml += self.xml_snippet_ll_1()
            # Expect a type
            out_xml += self.xml_snippet_ll_1()
            # Expect a variable name
            out_xml += self.xml_snippet_ll_1()
            # Expect ; or expect more variable names
            while self.current_token.get_val() != ';':
                # Expect a comma
                out_xml += self.xml_snippet_ll_1()
                # Expect a variable name
                out_xml += self.xml_snippet_ll_1()
            # Expect a ;
            out_xml += self.xml_snippet_ll_1()
            self.tab_num -= 1
        out_xml += '\t' * self.tab_num
        out_xml += '</varDec>\n'
        self.tab_num -= 1
        return out_xml

    def compile_expression(self):
        return "Incomplete method"

    def compile_statements(self):
        return "Incomplete method"

    def compile_while_statement(self):
        self.tab_num += 1
        out_xml = '\t'*self.tab_num
        out_xml += '<whileStatement>\n'
        self.tab_num += 1
        # Expect a While
        out_xml += self.xml_snippet_ll_1()
        # Expect a (
        out_xml += self.xml_snippet_ll_1()
        # Expect a expression
        out_xml += self.compile_expression()
        # Expect a )
        out_xml += self.xml_snippet_ll_1()
        # Expect a {
        out_xml += self.xml_snippet_ll_1()
        # Expect statements
        out_xml += self.compile_statements()
        # Lastly expect a }
        out_xml += self.xml_snippet_ll_1()
        self.tab_num -= 1
        out_xml += '\t'*self.tab_num
        out_xml += '</compileWhile>\n'
        return out_xml










test_file_data1 = [('Data1.jack', ['class Square {', 'field int x, y;', 'constructor Square new(int Ax, int Ay, int Asize) {']), ('Data2.jack', ['field int x, y;'])]
test_file_data2 = [('Data2.jack', ['var int x, y;'])]

a = CompilationEngine(test_file_data2)
print(a.compile_var_dec())


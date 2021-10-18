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
        """Advance to the next token if there is one otherwise report no tokens left to console

        :return: (None)
        """
        self.current_tokenizer.advance()
        if self.current_tokenizer.get_ind != -1:
            self.current_token = self.current_tokenizer.get_ind_token()
        else:
            print('No more tokens left')

    def start_rule(self, rule):
        """Returns xml code that represents the beginning of a rule and increments number of tabs by 1

        :param rule: (String) Rule we are parsing
        :return: (String) XML Representation
        """
        self.tab_num += 1
        out_xml = '\t' * self.tab_num
        out_xml += '<' + rule + '>\n'
        return out_xml

    def end_rule(self, rule):
        """Returns xml code that represents the end of a rule and decrements number of tabs by 1

        :param rule: (String) Rule we are parsing
        :return: (String) XML Representation
        """
        out_xml = '\t' * self.tab_num
        out_xml += '</' + rule + '>\n'
        self.tab_num -= 1
        return out_xml

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
        out_xml = self.start_rule('classVarDec')
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
        out_xml += self.end_rule('classVarDec')
        return out_xml

    def compile_var_dec(self):
        """Responsible for parsing a variable declaration

        :return: (String) XML representation
        """
        out_xml = self.start_rule('varDec')
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
        out_xml += self.end_rule('varDec')
        return out_xml

    def compile_expression(self):
        return "Incomplete method"

    def compile_statements(self):
        return "Incomplete method"

    def compile_while_statement(self):
        """Responsible for parsing a while statement

        :return: (String) XML representation
        """
        out_xml = self.start_rule('whileStatement')
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
        out_xml += self.end_rule('whileStatement')
        return out_xml










test_file_data1 = [('Data1.jack', ['class Square {', 'field int x, y;', 'constructor Square new(int Ax, int Ay, int Asize) {']), ('Data2.jack', ['field int x, y;'])]
test_file_data2 = [('Data2.jack', ['field int x, y;'])]

a = CompilationEngine(test_file_data2)
print(a.compile_class_var_dec())


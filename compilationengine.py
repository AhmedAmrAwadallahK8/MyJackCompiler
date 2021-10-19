import jacktokenizer as jt


class CompilationEngine:
    ops = ['+', '-', '*', '/', '>', '<', '=', '|', '&']
    unary_ops = ['-', '~']
    keyword_constant = ['true', 'false', 'null', 'this']
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
        if self.current_tokenizer.get_ind() != -1:
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
        self.tab_num += 1
        return out_xml

    def end_rule(self, rule):
        """Returns xml code that represents the end of a rule and decrements number of tabs by 1

        :param rule: (String) Rule we are parsing
        :return: (String) XML Representation
        """
        self.tab_num -= 1
        out_xml = '\t' * self.tab_num
        out_xml += '</' + rule + '>\n'
        self.tab_num -= 1
        return out_xml

    def xml_snippet_ll_1(self, exp_variety):
        """ Returns XML code pertaining to the current token, if the variety of the token is not expected this will
        still return XML code but the code will state that the variety is incorrect in the same line

        :param exp_variety: (String) the expected variety of token
        :return: (String) XML representation
        """
        if self.current_token.get_variety() == exp_variety:
            xml_code = '\t' * self.tab_num
            xml_code += '<' + self.current_token.get_variety() + '> '
            xml_code += self.current_token.get_val()
            xml_code += ' </' + self.current_token.get_variety() + '>\n'
        else:
            xml_code = '\t' * self.tab_num
            xml_code += 'FOUND VARIETY ' + self.current_token.get_variety() + ' AND VAL ' + self.current_token.get_val()
            xml_code += ' THIS VARIETY WAS NOT EXPECTED, THE VARIETY ' + exp_variety + ' WAS EXPECTED\n'
        self.next_token()
        return xml_code

    def compile_class_var_dec(self):
        """Responsible for parsing a class variable declaration

        :return: (String) XML representation
        """
        out_xml = self.start_rule('classVarDec')
        # Expect Keyword = static or field
        out_xml += self.xml_snippet_ll_1('keyword')
        # Expect a type
        out_xml += self.xml_snippet_ll_1('keyword')
        # Expect a variable name
        out_xml += self.xml_snippet_ll_1('identifier')
        # Expect ; or expect , and then a variable name repeating until ; is met
        while self.current_token.get_val() != ';' and self.current_token.get_val() != 'final token':
            # Expect a comma
            out_xml += self.xml_snippet_ll_1('symbol')
            # Expect a variable name
            out_xml += self.xml_snippet_ll_1('identifier')
        # Expect a ;
        out_xml += self.xml_snippet_ll_1('symbol')
        out_xml += self.end_rule('classVarDec')
        return out_xml

    def compile_var_dec(self):
        """Responsible for parsing a variable declaration

        :return: (String) XML representation
        """
        out_xml = self.start_rule('varDec')
        # Expect Keyword = var
        out_xml += self.xml_snippet_ll_1('keyword')
        # Expect a type
        out_xml += self.xml_snippet_ll_1('keyword')
        # Expect a variable name
        out_xml += self.xml_snippet_ll_1('identifier')
        # Expect ; or expect more variable names
        while self.current_token.get_val() != ';' and self.current_token.get_val() != 'final token':
            # Expect a comma
            out_xml += self.xml_snippet_ll_1('symbol')
            # Expect a variable name
            out_xml += self.xml_snippet_ll_1('identifier')
        # Expect a ;
        out_xml += self.xml_snippet_ll_1('symbol')
        out_xml += self.end_rule('varDec')
        return out_xml

    def compile_term(self): # partially implemented. Havent addressed varNames
        """Responsible for parsing a term

        :return: (String) XML representation
        """

        out_xml = self.start_rule('term')
        # We expect a term to be here but there are a variety of terms that could occur
        # Integer encountered
        if self.current_token.get_variety() == 'integerConstant':
            # Expect integer
            out_xml += self.xml_snippet_ll_1('integerConstant')
        # String encountered
        elif self.current_token.get_variety() == 'stringConstant':
            # Expect String
            out_xml += self.xml_snippet_ll_1('stringConstant')
        # Keyword constant encountered
        elif self.current_token.get_val() in self.keyword_constant:
            # Expect keyword constant
            out_xml += self.xml_snippet_ll_1('keyword')
        # Unary op term encountered
        elif self.current_token.get_val() in self.unary_ops:
            # Expect a unary op
            out_xml += self.xml_snippet_ll_1('symbol')
            # Expect a term
            out_xml += self.compile_term()
        # ( encountered
        elif self.current_token.get_val() == '(':
            # Expect (
            out_xml += self.xml_snippet_ll_1('symbol')
            # Expect expression
            out_xml += self.compile_expression()
            # Expect )
            out_xml += self.xml_snippet_ll_1('symbol')
        elif self.current_token.get_variety() == 'identifier':
            # Expect a variable name
            out_xml += self.xml_snippet_ll_1('identifier')
        # Still need more if statements for varnames LL2 scenarios but do later
        out_xml += self.end_rule('term')
        return out_xml

    def compile_expression(self):
        """ Responsible for parsing an expression

        :return: (String) XML representation
        """

        out_xml = self.start_rule('expression')
        # Expect term
        out_xml += self.compile_term()
        # Expect ; or repeating operation then term
        while self.current_token.get_val() in self.ops:
            # Expect Operation
            out_xml += self.xml_snippet_ll_1('symbol')
            # Expect term
            out_xml += self.compile_term()
        out_xml += self.end_rule('expression')
        return out_xml

    def compile_statements(self):
        pass

    def compile_while_statement(self):
        """Responsible for parsing a while statement

        :return: (String) XML representation
        """
        out_xml = self.start_rule('whileStatement')
        # Expect a While
        out_xml += self.xml_snippet_ll_1('keyword')
        # Expect a (
        out_xml += self.xml_snippet_ll_1('symbol')
        # Expect a expression
        out_xml += self.compile_expression()
        # Expect a )
        out_xml += self.xml_snippet_ll_1('symbol')
        # Expect a {
        out_xml += self.xml_snippet_ll_1('symbol')
        # Expect statements
        #out_xml += self.compile_statements()
        # Lastly expect a }
        out_xml += self.xml_snippet_ll_1('symbol')
        out_xml += self.end_rule('whileStatement')
        return out_xml

    def compile_let_statement(self):
        pass

    def compile_do_statement(self):
        pass

    def compile_if_statement(self):
        pass

    def compile_return_statement(self):
        pass










test_file_data1 = [('Data1.jack', ['class Square {', 'field int x, y;', 'constructor Square new(int Ax, int Ay, int Asize) {']), ('Data2.jack', ['field int x, y;'])]
test_file_data2 = [('Data2.jack', ['field int x, y;'])]
test_file_data3 = [('Data3.jack', ['while ( ~(x-1) ) {}'])]

a = CompilationEngine(test_file_data3)


print(a.compile_while_statement())


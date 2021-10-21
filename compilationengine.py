import jacktokenizer as jt
import filemediator as fm
import jackjanitor as jj


class CompilationEngine:
    ops = ('+', '-', '*', '/', '&gt;', '&lt;', '=', '|', '&amp;')
    unary_ops = ('-', '~')
    keyword_constant = ('true', 'false', 'null', 'this')
    jack_statements = ('let', 'do', 'while', 'if', 'return')

    def __init__(self, file_data, folder_name=''):
        self.folder_name = folder_name
        self.tokenizers = []
        self.tokenizer_ind = 0
        self.tab_num = 0
        for file in file_data:
            # First and second element of file store the file_name and the file_contents respectively
            file_contents_cleaned = jj.clean_jack_code(file[1])
            self.tokenizers.append(jt.JackTokenizer(file[0], file_contents_cleaned))
        self.current_tokenizer = self.tokenizers[self.tokenizer_ind] # Might be redundant
        self.current_token = self.current_tokenizer.get_ind_token() # Might be redundant

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
        #self.tab_num += 1
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
        #self.tab_num -= 1
        return out_xml

    def xml_snippet(self, exp_variety):
        """ Returns XML code pertaining to the current token, if the variety of the token is not expected this will
        still return XML code but the code will state that the variety is incorrect in the same line

        :param exp_variety: (String) the expected variety of token
        :return: (String) XML representation
        """
        if self.current_token.get_variety() in exp_variety:
            xml_code = '\t' * self.tab_num
            xml_code += '<' + self.current_token.get_variety() + '> '
            xml_code += self.current_token.get_val()
            xml_code += ' </' + self.current_token.get_variety() + '>\n'
        else:
            xml_code = '\t' * self.tab_num
            xml_code += 'FOUND VARIETY ' + self.current_token.get_variety() + ' AND VAL ' + self.current_token.get_val()
            xml_code += ' THIS VARIETY WAS NOT EXPECTED, THE VARIETY ' + str(exp_variety) + ' WAS EXPECTED\n'
        self.next_token()
        return xml_code

    def subroutine_call(self):
        """Responsible for handing the terminal rule, subroutineCall

        :return: (String) XML Representation
        """
        # Expect either subroutineName or a className/varName but this difference is actually resolved in the next
        # token so peek ahead and see. If the next token value is a ( then we expect subroutineName if it is a . we
        # expect a className/varName
        xml_out = ''
        if self.current_tokenizer.peek_next_token().get_val() == '(':
            # Expect subroutineName
            xml_out += self.xml_snippet(['identifier'])
            # Expect (
            xml_out += self.xml_snippet(['symbol'])
            # Expect expressionList even if its empty
            xml_out += self.compile_expression_list()
            # Expect )
            xml_out += self.xml_snippet(['symbol'])
        elif self.current_tokenizer.peek_next_token().get_val() == '.':
            # Expect className/varName
            xml_out += self.xml_snippet(['identifier'])
            # Expect a .
            xml_out += self.xml_snippet(['symbol'])
            # Expect subroutineName
            xml_out += self.xml_snippet(['identifier'])
            # Expect (
            xml_out += self.xml_snippet(['symbol'])
            # Expect expressionList
            xml_out += self.compile_expression_list()
            # Expect )
            xml_out += self.xml_snippet(['symbol'])
        return xml_out

    def compile_class_var_dec(self):
        """Responsible for parsing a class variable declaration

        :return: (String) XML representation
        """
        out_xml = self.start_rule('classVarDec')
        # Expect Keyword = static or field
        out_xml += self.xml_snippet(['keyword'])
        # Expect a type
        out_xml += self.xml_snippet(['keyword', 'identifier'])
        # Expect a variable name
        out_xml += self.xml_snippet(['identifier'])
        # Expect ; or expect , and then a variable name repeating until ; is met
        while self.current_token.get_val() != ';' and self.current_token.get_val() != 'final token':
            # Expect a comma
            out_xml += self.xml_snippet(['symbol'])
            # Expect a variable name
            out_xml += self.xml_snippet(['identifier'])
        # Expect a ;
        out_xml += self.xml_snippet(['symbol'])
        out_xml += self.end_rule('classVarDec')
        return out_xml

    def compile_var_dec(self):
        """Responsible for parsing a variable declaration

        :return: (String) XML representation
        """
        out_xml = self.start_rule('varDec')
        # Expect Keyword = var
        out_xml += self.xml_snippet(['keyword', 'identifier'])
        # Expect a type
        out_xml += self.xml_snippet(['keyword', 'identifier'])
        # Expect a variable name
        out_xml += self.xml_snippet(['identifier'])
        # Expect ; or expect more variable names
        while self.current_token.get_val() != ';' and self.current_token.get_val() != 'final token':
            # Expect a comma
            out_xml += self.xml_snippet(['symbol'])
            # Expect a variable name
            out_xml += self.xml_snippet(['identifier'])
        # Expect a ;
        out_xml += self.xml_snippet(['symbol'])
        out_xml += self.end_rule('varDec')
        return out_xml

    def compile_term(self):
        """Responsible for parsing a term

        :return: (String) XML representation
        """

        out_xml = self.start_rule('term')
        # We expect a term to be here but there are a variety of terms that could occur
        # Integer encountered
        if self.current_token.get_variety() == 'integerConstant':
            # Expect integer
            out_xml += self.xml_snippet(['integerConstant'])
        # String encountered
        elif self.current_token.get_variety() == 'StringConstant':
            # Expect String
            out_xml += self.xml_snippet(['StringConstant'])
        # Keyword constant encountered
        elif self.current_token.get_val() in self.keyword_constant:
            # Expect keyword constant
            out_xml += self.xml_snippet(['keyword'])
        # Unary op term encountered
        elif self.current_token.get_val() in self.unary_ops:
            # Expect a unary op
            out_xml += self.xml_snippet(['symbol'])
            # Expect a term
            out_xml += self.compile_term()
        # ( encountered
        elif self.current_token.get_val() == '(':
            # Expect (
            out_xml += self.xml_snippet(['symbol'])
            # Expect expression
            out_xml += self.compile_expression()
            # Expect )
            out_xml += self.xml_snippet(['symbol'])
        elif self.current_token.get_variety() == 'identifier':
            # If we have an identifier type token then there are three possibilites
            # Need to look ahead 1 token to decipher what to do with the current token (LL2)
            if self.current_tokenizer.peek_next_token().get_val() == '[':  # Arraylike variable
                # Expect variable name
                out_xml += self.xml_snippet(['identifier'])
                # Expect [
                out_xml += self.xml_snippet(['symbol'])
                # Expect expression
                out_xml += self.compile_expression()
                # Expect ]
                out_xml += self.xml_snippet(['symbol'])
            elif (self.current_tokenizer.peek_next_token().get_val() == '(' or
                  self.current_tokenizer.peek_next_token().get_val() == '.'):  # SubroutineCall
                # Expect subroutine call
                out_xml += self.subroutine_call()
            else:  # variable
                # Expect variable name
                out_xml += self.xml_snippet(['identifier'])
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
            out_xml += self.xml_snippet(['symbol'])
            # Expect term
            out_xml += self.compile_term()
        out_xml += self.end_rule('expression')
        return out_xml

    def compile_expression_list(self):
        """Responsible for parsing an expression list

        :return: (String) XML representation
        """
        xml_out = self.start_rule('expressionList')
        if self.current_token.get_val() != ')':
            # Expect expression
            xml_out += self.compile_expression()
            # If next token is , expect more expressions
            while self.current_token.get_val() == ',':
                # Expect a ,
                xml_out += self.xml_snippet(['symbol'])
                # Expect expression
                xml_out += self.compile_expression()
        xml_out += self.end_rule('expressionList')
        return xml_out

    def compile_statements(self):
        """Responsible for dealing with multiple statements and selecting the right parser for them

        :return: (String) XML representation
        """
        out_xml = self.start_rule('statements')
        # Keep looping if our current token value represents a jack statement
        while self.current_token.get_val() in self.jack_statements:
            # Find what type of statement then enter that statements method
            if self.current_token.get_val() == 'let':
                out_xml += self.compile_let_statement()
            elif self.current_token.get_val() == 'if':
                out_xml += self.compile_if_statement()
            elif self.current_token.get_val() == 'while':
                out_xml += self.compile_while_statement()
            elif self.current_token.get_val() == 'do':
                out_xml += self.compile_do_statement()
            elif self.current_token.get_val() == 'return':
                out_xml += self.compile_return_statement()
        out_xml += self.end_rule('statements')
        return out_xml

    def compile_while_statement(self):
        """Responsible for parsing a while statement

        :return: (String) XML representation
        """
        out_xml = self.start_rule('whileStatement')
        # Expect a While
        out_xml += self.xml_snippet(['keyword'])
        # Expect a (
        out_xml += self.xml_snippet(['symbol'])
        # Expect an expression
        out_xml += self.compile_expression()
        # Expect a )
        out_xml += self.xml_snippet(['symbol'])
        # Expect a {
        out_xml += self.xml_snippet(['symbol'])
        # Expect statements
        out_xml += self.compile_statements()
        # Lastly expect a }
        out_xml += self.xml_snippet(['symbol'])
        out_xml += self.end_rule('whileStatement')
        return out_xml

    def compile_let_statement(self):
        """ Responsible for parsing a let statement

        :return: (String) XML Representation
        """
        out_xml = self.start_rule('letStatement')
        # Expect let
        out_xml += self.xml_snippet(['keyword'])
        # Expect varName
        out_xml += self.xml_snippet(['identifier'])
        # Expect either a [ or =
        if self.current_token.get_val() == '[':
            # Expect a [
            out_xml += self.xml_snippet(['symbol'])
            # Expect an expression
            out_xml += self.compile_expression()
            # Expect a ]
            out_xml += self.xml_snippet(['symbol'])
        # Expect a =
        out_xml += self.xml_snippet(['symbol'])
        # Expect an expression
        out_xml += self.compile_expression()
        # Expect a ;
        out_xml += self.xml_snippet(['symbol'])
        out_xml += self.end_rule('letStatement')
        return out_xml

    def compile_do_statement(self):
        """Responsible for parsing a do statement

        :return: (String) XML representation
        """
        xml_out = self.start_rule('doStatement')
        # Expect do
        xml_out += self.xml_snippet(['keyword'])
        # Expect subroutineCall
        xml_out += self.subroutine_call()
        # Expect a ;
        xml_out += self.xml_snippet(['symbol'])
        xml_out += self.end_rule('doStatement')
        return xml_out

    def compile_if_statement(self):
        """Responsible for parsing an if statement

        :return: (String) XML Representation
        """
        out_xml = self.start_rule('ifStatement')
        # Expect an if
        out_xml += self.xml_snippet(['keyword'])
        # Expect a (
        out_xml += self.xml_snippet(['symbol'])
        # Expect an expression
        out_xml += self.compile_expression()
        # Expect a )
        out_xml += self.xml_snippet(['symbol'])
        # Expect a {
        out_xml += self.xml_snippet(['symbol'])
        # Expect statements
        out_xml += self.compile_statements()
        # Expect a }
        out_xml += self.xml_snippet(['symbol'])
        # If there is an else expect the following otherwise move on
        if self.current_token.get_val() == 'else':
            # Expect an else
            out_xml += self.xml_snippet(['keyword'])
            # Expect a {
            out_xml += self.xml_snippet(['symbol'])
            # Expect statements
            out_xml += self.compile_statements()
            # Expect a }
            out_xml += self.xml_snippet(['symbol'])
        out_xml += self.end_rule('ifStatement')
        return out_xml

    def compile_return_statement(self):
        """Responsible for parsing a return statement

        :return: (String) XML Representation
        """
        out_xml = self.start_rule('returnStatement')
        # Expect a return
        out_xml += self.xml_snippet(['keyword'])
        # Expect either an expression or ;
        if self.current_token.get_val() != ';' and self.current_token.get_val() != 'final token':
            # Expect an expression
            out_xml += self.compile_expression()
        # Expect a ;
        out_xml += self.xml_snippet(['symbol'])
        out_xml += self.end_rule('returnStatement')
        return out_xml

    def compile_parameter_list(self):
        """ Responsible for parsing a parameter list

        :return: (String) XML representation
        """
        out_xml = self.start_rule('parameterList')
        if self.current_token.get_val() != ')':
            # Expect type
            out_xml += self.xml_snippet(['keyword', 'identifier'])  # Could be an indentifier
            # Expect variable name
            out_xml += self.xml_snippet(['identifier'])
            # If a comma is encountered then repeat the following
            while self.current_token.get_val() == ',':
                # Expect a ,
                out_xml += self.xml_snippet(['symbol'])
                # Expect type
                out_xml += self.xml_snippet(['keyword', 'identifier'])  # Could be an indentifier
                # Expect variable name
                out_xml += self.xml_snippet(['identifier'])
        out_xml += self.end_rule('parameterList')
        return out_xml

    def compile_subroutine_body(self):
        """ Responsible for parsing a subroutine body

        :return: (String) XML Representation
        """
        out_xml = self.start_rule('subroutineBody')
        # Expect a {
        out_xml += self.xml_snippet(['symbol'])
        # Expect variable declaration if current token represents var
        while self.current_token.get_val() == 'var':
            out_xml += self.compile_var_dec()
        # Expect statements
        out_xml += self.compile_statements()
        # Expect }
        out_xml += self.xml_snippet(['symbol'])
        out_xml += self.end_rule('subroutineBody')
        return out_xml

    def compile_subroutine_dec(self):
        """Responsible for parsing a subroutine declaration

        :return: (String) XML representation
        """
        out_xml = self.start_rule('subroutineDec')
        # Expect constructor, function, or method
        out_xml += self.xml_snippet(['keyword'])
        # Expect void or type
        out_xml += self.xml_snippet(['keyword', 'identifier'])  # Technically this can also expect an identifier
        # Expect subroutine name
        out_xml += self.xml_snippet(['identifier'])
        # Expect a (
        out_xml += self.xml_snippet(['symbol'])
        # Expect a parameter list
        out_xml += self.compile_parameter_list()
        # Expect a )
        out_xml += self.xml_snippet(['symbol'])
        # Expect subroutine body
        out_xml += self.compile_subroutine_body()

        out_xml += self.end_rule('subroutineDec')
        return out_xml

    def compile_class(self):
        """ Responsible for parsing a class

        :return: (String) XML representation
        """
        out_xml = self.start_rule('class')
        # Expect class
        out_xml += self.xml_snippet(['keyword'])
        # Expect class name
        out_xml += self.xml_snippet(['identifier'])
        # Expect {
        out_xml += self.xml_snippet(['symbol'])
        # Possibly expect class variable declarations
        while self.current_token.get_val() in ('static', 'field'):
            # Expect a class variable declaration
            out_xml += self.compile_class_var_dec()
        # Possibly expect subroutine declarations
        while self.current_token.get_val() in ('constructor', 'function', 'method'):
            # Expect a subroutine declaration
            out_xml += self.compile_subroutine_dec()
        # Expect }
        out_xml += self.xml_snippet(['symbol'])
        out_xml += self.end_rule('class')
        return out_xml

    def start_compilation_engine(self):
        """ Responsible for directing files to be compiled. Once compilation is complete the data is loaded into a file
            named after their respective jack file.

        :return: None
        """
        for tokenizer in self.tokenizers:
            self.current_tokenizer = tokenizer
            self.current_token = self.current_tokenizer.get_ind_token()
            xml_code = self.compile_class()
            fm.load_file(self.current_tokenizer.get_file_name(), '.xml', xml_code, self.folder_name)











'''test_file_data1 = [('Data1.jack', ['class Square {', 'field int x, y;', 'constructor Square new(int Ax, int Ay, int Asize) {']), ('Data2.jack', ['field int x, y;'])]
test_file_data2 = [('Data2.jack', ['field int x, y;'])]
test_file_data3 = [('Data3', ['class Square{field int x; method void draw(int x, int y){var int z, a; var boolean b; let z = x + y; return z; } method void kill(){do draw(1,2); return;}}'])]

a = CompilationEngine(test_file_data3, 'ExpressionLessSquare')


a.start_compilation_engine()'''


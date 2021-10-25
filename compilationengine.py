import jacktokenizer as jt
import filemediator as fm
import jackjanitor as jj
import symboltable as st
import vmwriter as vmw


class CompilationEngine:
    ops = ('+', '-', '*', '/', '>', '<', '=', '|', '&')
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
        self.scope_table = None
        self.class_name = ''

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
        """Returns vm comment that represents the beginning of a rule

        :param rule: (String) Rule we are parsing
        :return: (String) XML Representation
        """

        out_vm = '//Start ' + rule
        return out_vm

    def end_rule(self, rule):
        """Returns vm comment that represents the end of a rule

        :param rule: (String) Rule we are parsing
        :return: (String) XML Representation
        """

        out_vm = '//End ' + rule
        return out_vm

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

    def xml_snippet_declare(self, name):
        """ Outputs xml code pertaining to variable declarations

        :param name: name of the variable
        :return: XML Representation
        """
        xml_code = '\t' * self.tab_num
        xml_code += '<VariableDeclaration>'
        xml_code += ' ' + name + ' ' + str(self.scope_table.table[name])
        xml_code += ' </VariableDeclaration>\n'
        return xml_code

    def xml_snippet_use_var(self, name):
        """ Outputs xml code pertaining to variable use

        :param name: (String) Name of the variable
        :return: XML Representation
        """
        xml_code = ''
        current_scope = self.scope_table
        while current_scope is not None:
            if name not in current_scope.table.keys():
                current_scope = current_scope.parent_table
            else:
                xml_code = '\t' * self.tab_num
                xml_code += '<VariableUse>'
                xml_code += ' ' + name + ' ' + str(current_scope.table[name])
                xml_code += ' </VariableUse>\n'
                break
        else:
            xml_code = '\t' * self.tab_num
            xml_code += '<ClassNameOrSubroutine>'
            xml_code += name
            xml_code += ' </ClassNameOrSubroutine>\n'

        return xml_code

    def var_info(self, name):
        """ Outputs variable information from the symbol table if it exists in any scope, otherwise outputs None

        :param name: (String) Name of the variable
        :return: (String) Jack Type, Memory Kind, Memory Index or (None)
        """
        j_t = '' # Jack Type
        k = ''  # Memory Kind
        k_i = '' # Memory Index
        current_scope = self.scope_table
        while current_scope is not None:
            if name not in current_scope.table.keys():
                current_scope = current_scope.parent_table
            else:
                return current_scope.type_of(name), current_scope.kind_of(name), current_scope.index_of(name)
        else:
            return None # This identifier is either a class name or subroutine

    def get_token(self):
        """ Returns the value stored in current token

        :return: (String) Value stored in current token
        """
        return self.current_token.get_val()

    def get_token_advance(self):
        """Gets the value stored in the current token then advances the token. The value is then returned

        :return: (String) Value stored in current token
        """
        token_val = self.current_token.get_val()
        self.next_token()
        return token_val

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
            name = self.get_token_advance()
            xml_out += self.xml_snippet_use_var(name)
            # Expect (
            xml_out += self.xml_snippet(['symbol'])
            # Expect expressionList even if its empty
            xml_out += self.compile_expression_list()
            # Expect )
            xml_out += self.xml_snippet(['symbol'])
        elif self.current_tokenizer.peek_next_token().get_val() == '.':
            # Expect className/varName
            name = self.get_token_advance()
            xml_out += self.xml_snippet_use_var(name)
            # Expect a .
            xml_out += self.xml_snippet(['symbol'])
            # Expect subroutineName
            name = self.get_token_advance()
            xml_out += self.xml_snippet_use_var(name)
            # Expect (
            xml_out += self.xml_snippet(['symbol'])
            # Expect expressionList
            xml_out += self.compile_expression_list()
            # Expect )
            xml_out += self.xml_snippet(['symbol'])
        return xml_out

    def add_symbol(self, name, j_type, kind):
        """Adds symbol to table

        :return: None
        """
        # Create a new scope variable
        self.scope_table.define(name, j_type, kind)

    def compile_class_var_dec(self):
        """Responsible for parsing a class variable declaration

        :return: (String) XML representation
        """
        out_vm = self.start_rule('classVarDec')
        # Expect Keyword = static or field
        kind = self.get_token_advance()
        # Expect a type
        j_type = self.get_token_advance()
        # Expect a variable name
        name = self.get_token_advance()
        # Update scope table
        self.add_symbol(name, j_type, kind)
        # Expect ; or expect , and then a variable name repeating until ; is met
        while self.current_token.get_val() != ';' and self.current_token.get_val() != 'final token':
            # Expect a comma
            self.next_token()
            # Expect a variable name
            name = self.get_token_advance()
            # Update scope table
            self.add_symbol(name, j_type, kind)
        # Expect a ;
        self.next_token()
        out_vm += self.end_rule('classVarDec')
        return out_vm

    def compile_var_dec(self):
        """Responsible for compiling a variable declaration

        :return: (String) VM Translation
        """
        out_vm = self.start_rule('varDec')
        # Expect Keyword = var
        kind = self.get_token_advance()
        # Expect a type
        j_type = self.get_token_advance()
        # Expect a variable name
        name = self.get_token_advance()
        self.add_symbol(name, j_type, kind)
        # Expect ; or expect more variable names
        while self.current_token.get_val() != ';' and self.current_token.get_val() != 'final token':
            # Expect a comma
            self.next_token()
            # Expect a variable name
            name = self.get_token_advance()
            self.add_symbol(name, j_type, kind)
        # Expect a ;
        self.next_token()
        out_vm += self.end_rule('varDec')
        return out_vm

    def compile_term(self): # TODO
        """Responsible for compiling a term

        :return: (String) VM Translation
        """

        out_vm = self.start_rule('term')
        # We expect a term to be here but there are a variety of terms that could occur
        # Integer encountered
        if self.current_token.get_variety() == 'integerConstant':
            # Expect integer
            integer_constant = self.get_token_advance()
            out_vm += vmw.write_push('constant', integer_constant)
        # String encountered
        elif self.current_token.get_variety() == 'stringConstant':
            # Expect String
            string_constant = self.get_token_advance() #TODO not sure how to handle strings
            out_vm += ''
        # Keyword constant encountered
        elif self.current_token.get_val() in self.keyword_constant:
            # Expect keyword constant
            kw_constant = self.get_token_advance()
            if kw_constant == 'true':
                out_vm += vmw.write_push('constant', '0')
                out_vm += vmw.write_arithmetic(unary_op='-')
            elif kw_constant == 'false':
                out_vm += vmw.write_push('constant', '0')
            elif kw_constant == 'null':
                out_vm += vmw.write_push('constant', '0')
            elif kw_constant == 'this':
                out_vm += vmw.write_push('pointer', '0')
        # Unary op term encountered
        elif self.current_token.get_val() in self.unary_ops:
            # Expect a unary op
            unary_op = self.get_token_advance()
            # Expect a term
            out_vm += self.compile_term()
            out_vm += vmw.write_arithmetic(unary_op=unary_op)
        # ( encountered
        elif self.current_token.get_val() == '(':
            # Expect (
            self.get_token_advance()
            # Expect expression
            out_vm += self.compile_expression()
            # Expect )
            self.get_token_advance()
        elif self.current_token.get_variety() == 'identifier':
            # If we have an identifier type token then there are three possibilites
            # Need to look ahead 1 token to decipher what to do with the current token (LL2)
            if self.current_tokenizer.peek_next_token().get_val() == '[':  # Arraylike variable
                # Expect variable name
                name = self.get_token_advance()
                j_type, kind, index = self.var_info(name)
                out_vm += vmw.write_push(kind, index)
                # Expect [
                self.get_token_advance()
                # Expect expression
                out_vm += self.compile_expression()
                # Expect ]
                self.get_token_advance()
                # VM code for accessing specified value in array
                out_vm += vmw.write_arithmetic(op='+')
                out_vm += vmw.write_pop('pointer', '1')
                out_vm += vmw.write_push('that', '0')
            elif (self.current_tokenizer.peek_next_token().get_val() == '(' or
                  self.current_tokenizer.peek_next_token().get_val() == '.'):  # SubroutineCall
                # Expect subroutine call
                out_vm += self.subroutine_call() # TODO
            else:  # variable
                # Expect variable name
                name = self.get_token_advance()
                j_type, kind, index = self.var_info(name)
                out_vm += vmw.write_push(kind, index)
        out_vm += self.end_rule('term')
        return out_vm

    def compile_expression(self):
        """ Responsible for compiling an expression

        :return: (String) VM Translation
        """
        op_stack = []
        out_vm = self.start_rule('expression')
        # Expect term
        out_vm += self.compile_term()
        # Expect ; or repeating operation then term
        while self.current_token.get_val() in self.ops:
            # Expect Operation
            op_stack.append(self.get_token_advance())
            # Expect term
            out_vm += self.compile_term()
        while op_stack:
            op = op_stack.pop()
            out_vm += vmw.write_arithmetic(op=op)
        out_vm += self.end_rule('expression')
        return out_vm

    def compile_expression_list(self):
        """Responsible for compiling an expression list

        :return: (String) VM translation
        """
        vm_out = self.start_rule('expressionList')
        if self.current_token.get_val() != ')':
            # Expect expression
            vm_out += self.compile_expression()
            # If next token is , expect more expressions
            while self.current_token.get_val() == ',':
                # Expect a ,
                self.get_token_advance()
                # Expect expression
                vm_out += self.compile_expression()
        vm_out += self.end_rule('expressionList')
        return vm_out

    def compile_statements(self):
        """Responsible for dealing with multiple statements and selecting the right compiler for them

        :return: (String) VM Translation
        """
        out_vm = self.start_rule('statements')
        # Keep looping if our current token value represents a jack statement
        while self.current_token.get_val() in self.jack_statements:
            # Find what type of statement then enter that statements method
            if self.current_token.get_val() == 'let':
                out_vm += self.compile_let_statement() # TODO
            elif self.current_token.get_val() == 'if':
                out_vm += self.compile_if_statement() #TODO
            elif self.current_token.get_val() == 'while':
                out_vm += self.compile_while_statement() #TODO
            elif self.current_token.get_val() == 'do':
                out_vm += self.compile_do_statement() # TODO
            elif self.current_token.get_val() == 'return':
                out_vm += self.compile_return_statement() # TODO
        out_vm += self.end_rule('statements')
        return out_vm

    def compile_while_statement(self): # TODO
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
        """ Responsible for compiling a let statement

        :return: (String) VM Translation
        """
        is_array = False
        out_vm = self.start_rule('letStatement')
        # Expect let
        self.next_token()
        # Expect varName
        var_name = self.get_token_advance()
        ## out_xml += self.xml_snippet_use_var(name)
        # Expect either a [ or =
        if self.current_token.get_val() == '[':
            is_array = True
            j_type, kind, index = self.var_info(var_name)
            # Expect a [
            self.next_token()
            # Put array memory location on to stack
            out_vm += vmw.write_push(kind, index)
            # Expect an expression: This expression is used for the array index
            out_vm += self.compile_expression() # TODO ARRAYS
            # Expect a ]
            self.next_token()
            # Add base array index and selected index together
            out_vm += vmw.write_arithmetic(op='+')
        # Expect a =
        self.next_token()
        # Expect an expression: This expression is what we set the variable equal to
        out_vm += self.compile_expression() # TODO
        # Pop this value into temp 0
        out_vm += vmw.write_pop('temp', '0')
        # Expect a ;
        self.next_token()
        # Let statement is now complete, store expression value in variable memory
        if is_array:
            # Pop array memory index into THAT
            out_vm += vmw.write_pop('pointer', '1')
            # Push the expression we are assinging the variable to back on stack
            out_vm += vmw.write_push('temp', '0')
            # Pop this value into the array index memory location
            out_vm += vmw.write_pop('that', '0')
        else:
            j_type, kind, index = self.var_info(var_name)
            out_vm += vmw.write_pop(kind, index)
            out_vm += self.end_rule('letStatement')
        return out_vm

    def compile_do_statement(self): # TODO
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

    def compile_if_statement(self): # TODO
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

    def compile_return_statement(self): # TODO
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

    def compile_parameter_list(self, is_method):
        """ Responsible for compiling a parameter list

        :return: (String) VM Translation
        """
        out_vm = self.start_rule('parameterList')
        # Since this is a method param list the kind is implicit
        kind = 'argument'
        if is_method:
            out_vm += self.add_symbol('this', self.class_name, kind)
        if self.current_token.get_val() != ')':
            # Expect type
            j_type = self.get_token_advance()
            # Expect a variable name
            name = self.get_token_advance()
            # Add symbol to table
            self.add_symbol(name, j_type, kind)
            # If a comma is encountered then repeat the following
            while self.current_token.get_val() == ',':
                # Expect a ,
                self.next_token()
                # Expect type
                j_type = self.get_token_advance()
                # Expect a variable name
                name = self.get_token_advance()
                # Add symbol to table and output xml code
                self.add_symbol(name, j_type, kind)
        out_vm += self.end_rule('parameterList')
        return out_vm

    def compile_subroutine_body(self, is_constructor): # TODO
        """ Responsible for compiling a subroutine body

        :return: (String) VM Translation
        """
        out_vm = self.start_rule('subroutineBody')
        # Expect a {
        self.next_token()
        # Expect variable declaration if current token represents var
        while self.current_token.get_val() == 'var':
            self.compile_var_dec()
        if is_constructor:
            # Constructor vm code
            out_vm += vmw.write_push('constant', self.scope_table.var_count('field'))
            out_vm += vmw.write_call('Memory', 'alloc', '1')
            out_vm += vmw.write_pop('pointer', '0')
        # Expect statements
        out_vm += self.compile_statements() # TODO
        # Expect }
        self.next_token()
        out_vm += self.end_rule('subroutineBody')
        return out_vm

    def compile_subroutine_dec(self):
        """Responsible for compiling a subroutine declaration

        :return: (String) VM Translation
        """
        out_vm = self.start_rule('subroutineDec')
        # Expect constructor, function, or method
        method = False
        constructor = False
        function = False
        void = False
        if self.get_token() == 'method':
            method = True
        elif self.get_token() == 'constructor':
            constructor = True
        elif self.get_token() == 'function':
            function = True
        self.next_token()
        # Expect void or type
        if self.get_token() == 'void':
            void = True
        self.next_token()
        # Expect subroutine name
        self.next_token()
        # Expect a (
        self.next_token()
        # Expect a parameter list
        self.compile_parameter_list(method)
        # Expect a )
        self.next_token()
        # Expect subroutine body
        out_vm += self.compile_subroutine_body(constructor) # TODO check if this returns useful information
        out_vm += self.end_rule('subroutineDec')
        return out_vm

    def compile_class(self):
        """ Responsible for compiling a class

        :return: (String) VM Translation
        """
        out_vm = self.start_rule('class')
        # Expect class
        self.next_token()  # Do Nothing
        # Expect class name
        self.class_name = self.get_token_advance()
        # Expect {
        self.next_token()  # Do Nothing
        # Possibly expect class variable declarations
        while self.current_token.get_val() in ('static', 'field'):
            # Expect a class variable declaration
            self.compile_class_var_dec()  # This process outputs no code
        # Possibly expect subroutine declarations
        while self.current_token.get_val() in ('constructor', 'function', 'method'):
            # Check if table has a parent, if it does then increment scope
            if self.scope_table.parent_table is not None:
                self.scope_table = self.scope_table.parent_table
            # Create a new sub scope table and set the current scope to this table
            self.scope_table = self.scope_table.start_subroutine()
            # Expect a subroutine declaration
            out_vm += self.compile_subroutine_dec()  # TODO check if useful code is returned
        # Expect }
        self.next_token()  # Do Nothing
        out_vm += self.end_rule('class')
        return out_vm

    def start_compilation_engine(self):
        """ Responsible for directing files to be compiled. Once compilation is complete the data is loaded into a file
            named after their respective jack file.

        :return: None
        """
        for tokenizer in self.tokenizers:
            self.scope_table = st.SymbolTable()
            self.current_tokenizer = tokenizer
            self.current_token = self.current_tokenizer.get_ind_token()
            xml_code = self.compile_class()
            # TODO Eventaully change .xml to .vm
            fm.load_file(self.current_tokenizer.get_file_name(), '.vm', xml_code, self.folder_name)











'''test_file_data1 = [('Data1.jack', ['class Square {', 'field int x, y;', 'constructor Square new(int Ax, int Ay, int Asize) {']), ('Data2.jack', ['field int x, y;'])]
test_file_data2 = [('Data2.jack', ['field int x, y;'])]
test_file_data3 = [('Data3', ['class Square{field int x; method void draw(int x, int y){var int z, a; var boolean b; let z = x + y; return z; } method void kill(){do draw(1,2); return;}}'])]
test_file_data4 = [('Data4', ['class Square { field int x; }'])]
a = CompilationEngine(test_file_data4)


a.start_compilation_engine()'''


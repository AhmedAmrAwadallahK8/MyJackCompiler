import jacktokenizer as jt


class CompilationEngine:
    def __init__(self, file_data):
        self.tokenizers = []
        for file in file_data:
            # First and second element of file store the file_name and the file_contents respectively
            self.tokenizers.append(jt.JackTokenizer(file[0], file[1]))

    def compile_class_var_dec(self):
        pass


'''test_file_data1 = [('Data1.jack', ['class Square {', 'field int x, y;', 'constructor Square new(int Ax, int Ay, int Asize) {']), ('Data2.jack', ['field int x, y;'])]
test_file_data2 = [('Data2.jack', ['field int x, y;'])]

a = CompilationEngine(test_file_data1)
token_field = a.tokenizers
for tok in token_field:
    print(tok.get_ind_token().get_variety())
    print(tok.get_ind_token().get_val())'''
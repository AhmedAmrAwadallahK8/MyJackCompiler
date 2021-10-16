class JackToken:
    def __init__(self, variety, val):
        self.variety = variety
        self.val = val

    def get_data(self):
        '''Getter

        :return: (Dictionary) Dictionary of the field names of a JackToken and their associated values
        '''
        data = vars(self)
        return data

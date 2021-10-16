class JackToken:
    def __init__(self, variety, val):
        self.variety = variety
        self.val = val

    def get_data(self):
        data = vars(self)
        return data

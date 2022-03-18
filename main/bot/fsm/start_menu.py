class FirstMenuState:
    def __init__(self):
        self.category = None
        self.dictionary = None

    def reset_state(self):
        self.category = None
        self.dictionary = None

    def __str__(self):
        return f"{self.category} - {self.dictionary}"

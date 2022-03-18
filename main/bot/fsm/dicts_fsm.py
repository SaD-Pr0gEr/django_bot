class DictsState:
    def __init__(self):
        self.dict_title = None
        self.create_dict = None
        self.del_dict = None

    def reset_state(self):
        self.dict_title = None
        self.create_dict = None
        self.del_dict = None

    def __str__(self):
        return f"{self.dict_title} - {self.create_dict}"

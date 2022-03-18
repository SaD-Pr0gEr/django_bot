class AddWordDict:
    def __init__(self):
        self.get_dict = None
        self.get_word = None

        self.dict_id_data = None

    def reset_state(self):
        self.get_dict = None
        self.get_word = None

    def reset_data(self):
        self.dict_id_data = None

    def __str__(self):
        return f"{self.get_dict}"

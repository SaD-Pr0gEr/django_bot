class TranslateCategoryState:
    def __init__(self):
        self.from_language = None
        self.to_language = None
        self.word = True

        self.from_language_data = None
        self.to_language_data = None

    def reset_data(self) -> None:
        self.from_language = None
        self.to_language = None
        self.word = True

        self.from_language_data = None
        self.to_language_data = None

class SearchKeyboard:
    def __init__(self):
        self.search_type = None
        self.by_first = None
        self.icontains = None
        self.iexact = None

    def reset_state(self):
        self.search_type = None
        self.by_first = None
        self.icontains = None
        self.iexact = None

    def __str__(self):
        return f"{self.search_type}"

class DatabaseConnectionError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        
class DatabaseQueryError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
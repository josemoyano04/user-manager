class TestingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        
class FixtureError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
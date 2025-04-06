class SendEmailError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
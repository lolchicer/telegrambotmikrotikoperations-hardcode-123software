class SentException(Exception):
    sentMessage: str
    
    def __init__(self, sentMessage: str) -> None:
        super().__init__()

        self.sentMessage = sentMessage

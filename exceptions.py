class SentException(Exception):
    sentMessage: str
    
    def __init__(self, sentMessage: str, *args: object) -> None:
        super().__init__(*args)

        self.sentMessage = sentMessage

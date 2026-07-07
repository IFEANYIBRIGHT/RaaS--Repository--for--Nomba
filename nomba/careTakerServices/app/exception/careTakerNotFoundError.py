class CareTakerNotFoundError(Exception):
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Care taker not found: {identifier}")

class ApplicationNotInitializedError(Exception):
    def __init__(self):
        super().__init__("Djing application is not initialized.")

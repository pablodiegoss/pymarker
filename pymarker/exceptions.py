class BlackBorderSizeError(Exception):
    """Exception raised for errors in the black border size."""

    def __init__(self, message="Black border size must be between 1% and 49%."):
        self.message = message
        super().__init__(self.message)


class WhiteBorderSizeError(Exception):
    """Exception raised for errors in the white border size."""

    def __init__(self, message="White border size must be between 1% and 49%."):
        self.message = message
        super().__init__(self.message)

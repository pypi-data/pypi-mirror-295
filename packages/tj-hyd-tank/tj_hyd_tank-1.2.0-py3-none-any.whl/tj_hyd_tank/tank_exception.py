class InvalidBasinFileException(Exception):
    def __init__(self):
        super().__init__(f"Invalid basin file.")


class FileNotFoundException(Exception):
    def __init__(self, file: str):
        super().__init__(f"{file} not found.")


class MissingColumnsException(Exception):
    def __init__(self, col: str):
        super().__init__(f"Missing columns, please provide the following column: '{col}'.")


class ColumnContainsEmptyDataException(Exception):
    def __init__(self, col: str):
        super().__init__(f"Column '{col}' contains empty data.")


class InvalidDatetimeException(Exception):
    def __init__(self):
        super().__init__(f"Invalid datetime.")


class InvalidDatetimeIntervalException(Exception):
    def __init__(self):
        super().__init__(f"Invalid datetime interval.")


class InvalidStartDateException(Exception):
    pass


class InvalidEndDateException(Exception):
    pass


class InvalidDateRangeException(Exception):
    def __init__(self, msg: str = ""):
        super().__init__(msg)

class InquirerError(Exception):
    pass


class ValidationError(InquirerError):
    def __init__(self, value, *args, **kwargs):
        super(ValidationError, self).__init__(*args, **kwargs)
        self.value = value


class UnknownQuestionTypeError(InquirerError):
    pass


class Aborted(InquirerError):
    pass


class EndOfInput(InquirerError):
    def __init__(self, selection, *args, **kwargs):
        super(EndOfInput, self).__init__(*args, **kwargs)
        self.selection = selection


class ThemeError(AttributeError):
    pass

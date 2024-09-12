from cat_year_calculator.lib.common.errors import CatYearCalculatorLibError


class CatYearCalculatorArgumentError(CatYearCalculatorLibError):
    pass


class CatYearCalculatorArgumentParserError(CatYearCalculatorArgumentError):
    pass


class NoQueueToProcessError(CatYearCalculatorArgumentError):
    """
    Raised when there is no queue to process.
    """

    def __init__(self, secondary_message=None):
        self._additional_info = 'No queue to process'

        if secondary_message:
            self._additional_info += f'\n{secondary_message}'

        self._line_number = self.get_line_number()
        self._file_raised = self.get_file_raised()

        super().__init__(self._additional_info)

    @property
    def line_number(self):
        return self._line_number

    @property
    def file_raised(self):
        return self._file_raised

    def __str__(self):
        return f'NoQueueToProcessError: {self._additional_info}'

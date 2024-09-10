from doogat.core.domain.interfaces.zettel_formatter import ZettelFormatter
from doogat.core.domain.value_objects.zettel_data import ZettelData


class PrintZettelUseCase:
    """
    A use case class for printing zettel data that has been formatted according to a specified format.

    This class is responsible for taking data encapsulated in a ZettelData object, formatting it using
    a provided formatter that complies with the ZettelFormatter interface, and then printing the formatted output.

    :param formatter: An instance of a class that implements the ZettelFormatter interface,
                      used to format the data before printing.
    :type formatter: ZettelFormatter
    """

    def __init__(self: "PrintZettelUseCase", formatter: ZettelFormatter) -> None:
        """
        Initializes a new instance of the PrintDoogatUseCase class.

        :param formatter: An instance of a class that implements the ZettelFormatter interface,
                          which will be used to format the data.
        :type formatter: ZettelFormatter
        """
        self.formatter = formatter

    def execute(
        self: "PrintZettelUseCase",
        zettel_data: ZettelData,
    ) -> None:
        """
        Executes the use case of printing the formatted data.

        This method takes an instance of ZettelData, formats it using the formatter provided at initialization,
        and prints the resulting string to the standard output.

        :param zettel_data: The data to be formatted and printed.
        :type zettel_data: ZettelData
        """
        print(self.formatter.format(zettel_data))

class ZettelRepositoryZettelNotFoundError(Exception):
    """
    Custom exception raised when a Zettel is not found in the ZettelRepository.

    This exception inherits from the built-in Exception class and provides a specific error
    for situations where a requested Zettel cannot be located within the repository.

    :param message: A descriptive message explaining the error.
                    Defaults to "Zettel not found in repository."
    :type message: str
    """

    def __init__(
        self: "ZettelRepositoryZettelNotFoundError",
        message: str = "Zettel not found in repository.",
    ) -> None:
        """
        Initializes the ZettelRepositoryZettelNotFoundError instance.

        :param message: An optional custom error message.
                        If not provided, defaults to "Zettel not found in repository."
        :type message: str
        :return: None
        """
        super().__init__(message)

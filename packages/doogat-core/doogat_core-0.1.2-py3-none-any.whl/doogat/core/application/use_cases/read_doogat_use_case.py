import doogat.core.domain.entities as doogat_entities
from doogat.core.domain.interfaces.zettel_repository import ZettelRepository
from doogat.core.domain.interfaces.zettel_repository_exceptions import (
    ZettelRepositoryZettelNotFoundError,
)
from doogat.core.domain.services.doogat_factory import DoogatFactory


class ReadDoogatUseCase:
    """
    A use case class for reading zettel from repository by location and downcasting it to doogat.

    This class is responsible for taking location of a zettel within a ZettelRepository, and downcasting
    it using DoogatFactory service to specific doogat according to zettel type.

    :param repository: An instance of a class that implements the ZettelRepository interface,
                      used to data access in persistence layer.
    :type repository: ZettelRepository
    """

    def __init__(self: "ReadDoogatUseCase", repository: ZettelRepository) -> None:
        """
        Initializes a new instance of the ReadDoogatUseCase class.

        :param reposiroty: An instance of a class that implements the ZettelRepository interface,
                          which will be used to retrieve the data.
        :type repository: ZettelRepository
        """

        self.repository = repository

    def execute(
        self: "ReadDoogatUseCase",
        repository_location: str,
    ) -> doogat_entities.Zettel:
        """
        Executes the use case of reading from repository by location and downcasting to doogat.

        This method takes repository location, attempts to retrieve the corresponding zettel from the repository,
        downcasts it into a doogat, and returns it. It handles potential exceptions during the retrieval process.

        :param repository_location: Unique identifier of location within repository containing zettel data.
        :type repository_location: str
        :raises ZettelRepositoryZettelNotFoundError: If the zettel is not found in the repository.
        :return: A Doogat object created from the retrieved zettel.
        :rtype: doogat.core.domain.entities.Zettel or its subclass
        """
        try:
            zettel = self.repository.find_by_location(repository_location)
        except ZettelRepositoryZettelNotFoundError as e:
            raise ZettelRepositoryZettelNotFoundError(
                e
            ) from ZettelRepositoryZettelNotFoundError
        if zettel is None:
            raise ZettelRepositoryZettelNotFoundError
        return DoogatFactory.create(zettel)

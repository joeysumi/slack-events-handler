from abc import ABC, abstractmethod


class FileNavigatorBase(ABC):
    """ Abstract base class designed to make sure new File Navigator classes coincide with
        the existing event handler.
    """

    @abstractmethod
    def is_file_in_directory(self, directory_path: str, file_name: str) -> bool:
        """ Abstract method checking if the file already exists in the desired location """
        pass

    @abstractmethod
    def save_file_to_directory(self, file_data: bytes, file_path: str) -> None:
        """ Abstract method saving file to location """
        pass

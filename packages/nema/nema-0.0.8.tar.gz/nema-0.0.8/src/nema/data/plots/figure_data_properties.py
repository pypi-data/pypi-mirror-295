from dataclasses import dataclass

from nema.data.data_properties import DataProperties, FileDataProperties


@dataclass
class FigureDataProperties(DataProperties):
    pass


@dataclass
class Image(FigureDataProperties, FileDataProperties):

    @staticmethod
    def get_default_file_extension():
        return "png"

    @property
    def data_type(self):
        return "IMAGE.V0"

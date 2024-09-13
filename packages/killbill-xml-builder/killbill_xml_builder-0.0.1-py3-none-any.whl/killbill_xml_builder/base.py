import abc
from xml.etree import ElementTree as ET


class Base:
    def __init__(self):
        self.element = None
        self.to_xml()

    @abc.abstractmethod
    def to_xml(self):
        """Create the XML representation of the object"""
        pass

    def __str__(self):
        return ET.tostring(self.element, encoding="unicode")

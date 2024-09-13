from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base


class Currency(Base):

    def __init__(self, code: str) -> None:
        """Create the XML representation of the currency

        Args:
            code (str): USD , EUR , GBP
        """

        self.code = code.upper()
        self.to_xml()

    def to_xml(self):

        currency = ET.Element("currency")
        currency.text = self.code

        self.element = currency


class Currencies(Base):
    def __init__(self, currencies: list) -> None:
        """Create the XML representation of the currency
        Args:
            currencies (list):[USD , EUR , GBP]
        """
        self.currencies = currencies
        self.to_xml()

    def to_xml(self):

        currencies_element = ET.Element("currencies")

        for currency in self.currencies:
            currencies_element.append(Currency(currency).element)

        self.element = currencies_element

from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base


class Price(Base):

    def __init__(self, currency: str, value: float) -> None:
        """Create the XML representation of the price


        Args:
            currency (str): USD , EUR , GBP
            value (float): 10.00
        """

        self.currency = currency
        self.value = value
        self.to_xml()

    def to_xml(self):

        price = ET.Element("price")

        currency = ET.SubElement(price, "currency")
        currency.text = self.currency

        value = ET.SubElement(price, "value")
        value.text = str(self.value)

        self.element = price

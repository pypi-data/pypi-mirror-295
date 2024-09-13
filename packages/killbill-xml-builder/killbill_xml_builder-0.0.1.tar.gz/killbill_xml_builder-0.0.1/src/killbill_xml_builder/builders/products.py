from typing import List
from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base
from killbill_xml_builder.enums import ProductCategory


class Product(Base):

    def __init__(
        self,
        name: str,
        category: ProductCategory = ProductCategory.BASE,
        available: list = None,
        included: List = None,
    ) -> None:
        """Create the XML representation of the product"""

        self.name = name
        self.category = category
        self.available = available
        self.included = included
        self.to_xml()

    def to_xml(self):

        product_element = ET.Element("product")
        product_element.set("name", self.name)

        category_element = ET.SubElement(product_element, "category")
        category_element.text = str(self.category)

        if self.included:
            included_element = ET.SubElement(product_element, "included")
            for ie in self.included:
                addon_product = ET.SubElement(included_element, "addonProduct")
                addon_product.text = ie.name

        if self.available:
            available_element = ET.SubElement(product_element, "available")
            for ae in self.available:
                addon_product = ET.SubElement(available_element, "addonProduct")
                addon_product.text = ae.name

        self.element = product_element

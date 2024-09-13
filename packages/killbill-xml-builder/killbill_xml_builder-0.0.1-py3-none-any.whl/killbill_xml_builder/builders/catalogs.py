from typing import List
from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base
from killbill_xml_builder.enums import BillingMode
from killbill_xml_builder.builders.currencies import Currencies
from killbill_xml_builder.builders.products import Product
from killbill_xml_builder.builders.plans import Plan


class Catalog(Base):

    def __init__(
        self,
        effective_date: str,
        name: str,
        billing_mode: BillingMode,
        currencies: Currencies,
        products: List[Product],
        plans: List[Plan],
    ) -> None:
        """Create the XML representation of the catalog"""

        self.effective_date = f"{effective_date}T00:00:00+00:00"
        self.name = name
        self.billing_mode = billing_mode
        self.currencies = currencies
        self.products = products
        self.plans = plans
        self.to_xml()

    def to_xml(self):

        catalog = ET.Element("catalog")

        effective_date_element = ET.SubElement(catalog, "effectiveDate")
        effective_date_element.text = self.effective_date

        catalog_name_element = ET.SubElement(catalog, "catalogName")
        catalog_name_element.text = self.name

        recurring_billing_mode = ET.SubElement(catalog, "recurringBillingMode")
        recurring_billing_mode.text = str(self.billing_mode)

        catalog.append(self.currencies.element)

        products_element = ET.SubElement(catalog, "products")
        for product in self.products:
            products_element.append(product.element)

        plans_element = ET.SubElement(catalog, "plans")
        for plan in self.plans:
            plans_element.append(plan.element)

        self.element = catalog

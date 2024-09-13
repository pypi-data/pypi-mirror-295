from typing import List
from xml.etree import ElementTree as ET
from killbill_xml_builder.base import Base
from killbill_xml_builder.enums import TimeUnit, BillingPeriod, PhaseType
from killbill_xml_builder.builders.prices import Price


class Duration(Base):

    def __init__(self, length: int = 0, time_unit: TimeUnit = TimeUnit.DAYS) -> None:
        """Create the XML representation of the duration"""
        self.length = str(length)
        self.time_unit = time_unit
        self.to_xml()

    def to_xml(self):

        duration_element = ET.Element("duration")

        unit_element = ET.SubElement(duration_element, "unit")
        unit_element.text = str(self.time_unit)

        if self.time_unit != TimeUnit.UNLIMITED:

            number_element = ET.SubElement(duration_element, "number")
            number_element.text = self.length

        self.element = duration_element


class RecurringPrice(Base):
    def __init__(self, prices: List[Price], billing_period: BillingPeriod) -> None:
        """Create the XML representation of the recurring price"""
        self.prices = prices
        self.billing_period = billing_period
        self.to_xml()

    def to_xml(self):

        recurring_element = ET.Element("recurring")

        billing_period_element = ET.SubElement(recurring_element, "billingPeriod")
        billing_period_element.text = str(self.billing_period)

        recurring_price_element = ET.SubElement(recurring_element, "recurringPrice")
        for price in self.prices:
            recurring_price_element.append(price.element)

        self.element = recurring_element


class FixedPrice(Base):
    def __init__(self, prices: List[Price] = []) -> None:
        """Create the XML representation of the fixed price"""
        self.prices = prices
        self.to_xml()

    def to_xml(self):

        fixed_element = ET.Element("fixed")

        fixed_price_element = ET.SubElement(fixed_element, "fixedPrice")
        for price in self.prices:
            fixed_price_element.append(price.element)

        self.element = fixed_element


class Phase(Base):
    def __init__(
        self,
        type: PhaseType,
        duration: Duration,
        recurring_price: RecurringPrice = None,
        fixed_price: FixedPrice = None,
    ) -> None:
        """Create the XML representation of the phase"""

        self.type = type
        self.duration = duration
        self.recurring_price = recurring_price
        self.fixed_price = fixed_price
        self.to_xml()

    def to_xml(self):

        phase_element = ET.Element("phase")
        phase_element.set("type", str(self.type))

        phase_element.append(self.duration.element)

        if self.fixed_price:
            phase_element.append(self.fixed_price.element)

        if self.recurring_price:
            phase_element.append(self.recurring_price.element)

        self.element = phase_element

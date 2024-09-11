from abc import ABC, abstractmethod
from typing import Union, List
from decimal import Decimal, Context, setcontext

import pint

from ..errors.backend import (
    IncompatibleConversionUnitError,
    EmptyArrayError,
    InvalidUnitError
)

from ..defaults import multiplier_symbols

class BackendInterface(ABC):
    """
    Abstract Interface between units backend and ScientificWidget

    Requires the implementation of methods for creating quantities,
    verifying units and converting units.
    """
    @property
    @abstractmethod
    def unitSystem():
        """str: Unit System to be used."""
        pass

    @property
    @abstractmethod
    def unitRegistry():
        """object: Unit Registry object."""
        pass

    @abstractmethod
    def quantityFromText(self, text: str):
        """
        Creates a new quantity object based on its text representation.

        Args:
            text (str): text representation of the new quantity.

        Returns:
            object: quantity object created from text.
        """
        pass

    @abstractmethod
    def isUnitRegistered(self, unit) -> bool:
        """Verifies if a unit is registered on the Unit Registry.
        
        Args:
            unit (str): unit representation in text.

        Returns:
            bool: True if it is registered, False otherwise.
        """
        pass
    
    @abstractmethod
    def getQuantityValueFloat(self, quantity):
        """Returns the numeric part of a quantity object as a float.
        
        Args:
            quantity (object): quantity object.
        
        Returns:
            float: numeric part of the quantity.
        """
        pass

    @abstractmethod
    def getQuantityValueStr(self, quantity) -> str:
        """Returns the numeric part of a quantity object as a string.
        
        Args:
            quantity (object): quantity object.
        
        Returns:
            str: numeric part of the quantity.
        """
        pass
    
    @abstractmethod
    def getQuantityUnit(self, quantity) -> str:
        """
        Returns the text representation of the unit part of a
        quantity object.
        
        Args:
            quantity (object): quantity object.
        
        Returns:
            str: text representation of unit part.
        """
        pass
    
    @abstractmethod
    def quantityTextRepr(self, quantity) -> str:
        """
        Returns the text representation of a quantity object.
        
        Args:
            quantity (object): quantity object.
        
        Returns:
            str: text representation of the quantity.
        """
        pass

    @abstractmethod
    def isQuantityCompatibleWithUnit(self, quantity, unit) -> bool:
        """Verifies if a quantity is compatible with an unit.
        
        Args:
            quantity (object): quantity object.
            unit (Union[object, str]): unit object or its text representation.

        Returns:
            bool: True if it is compatible, False otherwise.
        """
        pass
    
    @abstractmethod
    def isUnitsCompatible(self, unit1, unit2) -> bool:
        """Verifies if two units are compatible.

        Args:
            unit1 (Union[object, str]): unit object 1 or its text representation.
            unit2 (Union[object, str]): unit object 2 or its text representation.

        Returns:
            bool: True if they are compatible, False otherwise.
        """
        pass

    @abstractmethod
    def isQuantitiesCompatible(self, q1, q2) -> bool:
        """
        Verifies if two quantities are compatible.

        Args:
            q1 (object): quantity object 1.
            q2 (object): quantity object 2.

        Returns:
            bool: True if the quantities are compatible, False otherwise.
        """
        pass

    @abstractmethod
    def changeQuantityUnit(self, quantity, new_unit):
        """Returns a new quantity object with the new unit.
        
        Takes in a quantity object with numeric and unit parts,
        and returns a new quantity object with the numeric and
        unit parts converted to the new unit.

        Args:
            quantity (object): quantity object.
            new_unit (Union[object, str]): unit object or its text representation.
        
        Returns:
            object: new quantity object with the new unit and numeric parts.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Returns a string representation of the interface."""
        pass

class PintInterface(BackendInterface):
    """
    Interface between pint and ScientificWidget

    Implements required methods for creating quantities,
    verifying units and converting units.
    """

    def __init__(self, unit_system: str = 'SI', precision=30):
        """
        Args:
            unit_system (str): unit system to use on the pint.UnitRegistry.
                Defaults to 'SI'.
            precision (int): precision to use for Decimal. Defaults to 30.
        """
        self._unitSystem = unit_system
        self._unitRegistry = pint.UnitRegistry(
            system=self._unitSystem,
            case_sensitive=True,
            autoconvert_offset_to_baseunit=False,
        )
        self._unitRegistry.formatter.default_format = '~'
        self._precision = 30

        # Sets Decimal context
        self._decimalsContext = Context(
            prec=self._precision,       # maximum precision
            capitals=1,                 # prints exponential in uppercase
        )
        setcontext(self._decimalsContext)

    QuantityType = pint.Quantity
    ValueType = Decimal

    @property
    def decimalsContext(self):
        return self._decimalsContext

    @property
    def precision(self):
        return self._precision

    @property
    def unitSystem(self):
        return self._unitSystem

    @property
    def unitRegistry(self):
        return self._unitRegistry

    def quantityFromText(self, text: str, unit: str):
        return self.unitRegistry.Quantity(Decimal(text), unit)
    
    def quantityFromDecimal(self, value: Decimal, unit: str):
        return self.unitRegistry.Quantity(value, unit)

    def isUnitRegistered(self, unit: str) -> bool:
        try:
            _ = self.unitRegistry.Unit(unit)
            return True
        except Exception:
            return False
        
    def unitFromText(self, text: str):
        if not self.isUnitRegistered(text):
            raise InvalidUnitError(text)
        return self.unitRegistry.Unit(text)
        
    def unitToText(self, unit: pint.Unit):
        return f"{unit:~}"
        
    def getQuantityValueFloat(self, quantity: pint.Quantity):
        return quantity.m

    def getQuantityValueStr(self, quantity: pint.Quantity) -> str:
        return f'{quantity.m}'
    
    def getQuantityUnitStr(self, quantity: pint.Quantity) -> str:
        unit = f'{quantity.u:~}'
        unit_splitted = list(unit)

        # Algorithm to replace possible multiplier symbols e.g. greek characters
        # to preferred characters.
        for symbol in multiplier_symbols.keys():
            item = multiplier_symbols[symbol]
            preferred = item["preferred"]
            for possible in item["possibles"]:
                if possible in unit_splitted:
                    unit = unit.replace(possible, preferred)
        return unit
    
    def getQuantityUnit(self, quantity: pint.Quantity) -> pint.Unit:
        return quantity.u
    
    def quantityTextRepr(self, quantity: pint.Quantity, unit_separator: str, normalize: bool = False, formatter = lambda x: f"{x:f}") -> str:
        if normalize:
            if formatter:
                return f'{formatter(quantity.m.normalize())}{unit_separator}{self.getQuantityUnitStr(quantity)}'
            else:
                return f'{quantity.m.normalize()}{unit_separator}{self.getQuantityUnitStr(quantity)}'
        else:
            if formatter:
                return f'{formatter(quantity.m)}{unit_separator}{self.getQuantityUnitStr(quantity)}'
            else:
                return f'{quantity.m}{unit_separator}{self.getQuantityUnitStr(quantity)}'

    def isQuantityCompatibleWithUnit(self, quantity: pint.Quantity, unit: Union[pint.Unit, str]) -> bool:
        if isinstance(unit, str) and not self.isUnitRegistered(unit):
            return False
        try:
            is_compatible = quantity.is_compatible_with(unit)
            return is_compatible
        except Exception:
            return False
            
    def isUnitsCompatible(self, unit1: str, unit2: str) -> bool:
        try:
            u1 = self.unitRegistry.Unit(unit1)
            u2 = self.unitRegistry.Unit(unit2)
            return u1.is_compatible_with(u2)
        except Exception:
            return False

    def isQuantitiesCompatible(self, q1: pint.Quantity, q2: pint.Quantity) -> bool:
        try:
            is_compatible = q1.is_compatible_with(q2)
            return is_compatible
        except Exception:
            return False
        
    def isArrayOfSameDimension(self, array: List[str]):
        if len(array) < 1:
            raise EmptyArrayError()
        
        for item in array:
            if not self.isUnitRegistered(item):
                return False
            if not self.isUnitsCompatible(array[0], item):
                return False
        return True
    
    def isQuantitiesUnitsEqual(self, q1, q2):
        if f"{self.getQuantityUnitStr(q1)}" == f"{self.getQuantityUnitStr(q2)}":
            return True
        else:
            return False
        
    def isUnitsEqual(self, u1, u2):
        if f"{u1:~}" == f"{u2:~}":
            return True
        else:
            return False

    def changeQuantityUnit(self, quantity: pint.Quantity, new_unit: Union[str, pint.Unit], formatter=None):
        try:
            new_quantity = quantity.to(new_unit)
            if formatter:
                return formatter(quantity, new_quantity)
            else:
                return new_quantity
        except pint.DimensionalityError:
            raise IncompatibleConversionUnitError()

    def __repr__(self):
        return f"PintInterface(unit_system=`{self.unitSystem}`)"
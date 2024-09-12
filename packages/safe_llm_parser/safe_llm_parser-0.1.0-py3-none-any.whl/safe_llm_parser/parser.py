import re
import xml.etree.ElementTree as ET
import xml.sax
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, Union

from bs4 import BeautifulSoup


class Parser(ABC):
    """Abstract class for implementing methods for data extraction."""

    def __init__(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def parse(data: str) -> Dict[str, Any]:
        """Abstract method to extract data from a given string.

        This method should be implemented in subclasses to provide specific
        extraction functionality.

        Args:
        ----
            data (str): The string to extract data from.

        Returns:
        -------
            dict: The extracted data. The type of the data depends on the
                implementation in the subclass.

        """


class XMLParser(Parser):
    """Parser to extract data from XML-like formatted strings."""

    @classmethod
    def parse(cls, data: str, strict: bool = False) -> Dict[str, Any]:
        """Extract and parse XML-like data from a string.

        Args:
            data (str): String containing XML-like data.
            strict (bool): Enforce strict XML structure. Default is False.

        Raises:
            ValueError: If the data is not a valid or well-formed XML string.

        Returns:
            dict: Parsed XML data as a dictionary.
        """
        # Clean up input data using BeautifulSoup
        cleaned_data = BeautifulSoup(data, "html.parser").prettify()

        try:
            if strict:
                cls._validate_well_formedness(cleaned_data)
                root = ET.fromstring(cleaned_data)
            else:
                xml_string, tag_name = cls._extract_xml_fragment(cleaned_data)
                cls._validate_well_formedness(xml_string)
                root = ET.fromstring(xml_string)

            return {tag_name: cls._xml_to_dict(root)}

        except ET.ParseError as exc:
            raise ValueError(
                f"The provided data is not a well-formed XML: {exc}"
            ) from exc

    @staticmethod
    def _extract_xml_fragment(data: str) -> Tuple[str, str]:
        """Extract the first matching XML fragment from the input string."""
        pattern = r"(<(\w+)>[\s\S]*?<\/\2>)"
        match = re.search(pattern, data)

        if not match:
            raise ValueError("No valid XML structure found in the data.")

        xml_string = match.group(0)
        tag_name = match.group(2)
        return xml_string, tag_name

    @classmethod
    def _xml_to_dict(cls, element: ET.Element) -> Union[str, Dict[str, Any]]:
        """Convert an XML element recursively into a dictionary.

        Args:
            element (ET.Element): Root XML element to convert.

        Returns:
            Union[str, dict]: Dictionary representation of the XML element.
        """
        children = list(element)
        if not children:  # No child elements, return the text content
            return element.text.strip() if element.text else ""

        result: Dict[str, Any] = {}
        for child in children:
            child_result = cls._xml_to_dict(child)
            if child.tag in result:
                if isinstance(result[child.tag], list):
                    result[child.tag].append(child_result)
                else:
                    result[child.tag] = [result[child.tag], child_result]
            else:
                result[child.tag] = child_result

        return result

    @staticmethod
    def _validate_well_formedness(xml_string: str) -> None:
        """Validate that the XML string is well-formed.

        Args:
            xml_string (str): XML string to validate.

        Raises:
            ET.ParseError: If the XML is not well-formed.
        """
        handler = xml.sax.handler.ContentHandler()

        try:
            xml.sax.parseString(xml_string, handler)
        except xml.sax.SAXParseException as e:
            raise ET.ParseError(f"XML well-formedness error: {e}") from e

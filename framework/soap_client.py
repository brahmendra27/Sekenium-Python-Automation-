# framework/soap_client.py

"""
SOAP/XML Client for Boomi and legacy integration testing.

Supports:
  - SOAP envelope construction
  - WSDL-free requests (raw XML)
  - XML response parsing
  - Namespace handling
  - Basic and WS-Security authentication
  - Allure step integration

Usage:
    client = SOAPClient("https://api.example.com/soap")
    response = client.call("GetOrder", {"OrderId": "12345"})
    value = client.extract(response, "//OrderStatus")
"""

import logging
from typing import Dict, Any, Optional, List
from xml.etree import ElementTree as ET
import requests
import allure

logger = logging.getLogger(__name__)


class SOAPClient:
    """SOAP/XML API client for middleware integration testing."""

    DEFAULT_NS = {
        "soap": "http://schemas.xmlsoap.org/soap/envelope/",
        "soap12": "http://www.w3.org/2003/05/soap-envelope",
    }

    def __init__(self, endpoint: str, namespace: str = "",
                 soap_version: str = "1.1", timeout: int = 30):
        """Initialize SOAP client.

        Args:
            endpoint: SOAP service endpoint URL
            namespace: Target namespace for the service
            soap_version: SOAP version ('1.1' or '1.2')
            timeout: Request timeout in seconds
        """
        self.endpoint = endpoint
        self.namespace = namespace
        self.soap_version = soap_version
        self.timeout = timeout
        self.session = requests.Session()

        # Set content type based on SOAP version
        if soap_version == "1.2":
            self.session.headers["Content-Type"] = "application/soap+xml; charset=utf-8"
        else:
            self.session.headers["Content-Type"] = "text/xml; charset=utf-8"

    def set_basic_auth(self, username: str, password: str):
        """Set HTTP Basic authentication."""
        self.session.auth = (username, password)

    def set_header(self, key: str, value: str):
        """Set a custom HTTP header."""
        self.session.headers[key] = value

    @allure.step("SOAP Call: {operation}")
    def call(self, operation: str, params: Optional[Dict] = None,
             raw_body: Optional[str] = None,
             soap_headers: Optional[Dict] = None) -> ET.Element:
        """Execute a SOAP operation.

        Args:
            operation: SOAP operation/method name
            params: Operation parameters as dict (auto-builds XML)
            raw_body: Raw XML body string (overrides params)
            soap_headers: SOAP header elements as dict

        Returns:
            Parsed XML Element of the SOAP Body content
        """
        if raw_body:
            envelope = raw_body
        else:
            envelope = self._build_envelope(operation, params, soap_headers)

        logger.info(f"SOAP call: {operation} → {self.endpoint}")
        logger.debug(f"Envelope: {envelope[:500]}")

        # Set SOAPAction header for SOAP 1.1
        if self.soap_version == "1.1":
            action = f"{self.namespace}/{operation}" if self.namespace else operation
            self.session.headers["SOAPAction"] = f'"{action}"'

        resp = self.session.post(
            self.endpoint, data=envelope.encode("utf-8"),
            timeout=self.timeout
        )

        # Attach to Allure
        allure.attach(envelope, name="soap_request",
                      attachment_type=allure.attachment_type.XML)
        allure.attach(resp.text, name="soap_response",
                      attachment_type=allure.attachment_type.XML)

        resp.raise_for_status()
        return self._parse_response(resp.text)

    def _build_envelope(self, operation: str,
                        params: Optional[Dict] = None,
                        soap_headers: Optional[Dict] = None) -> str:
        """Build SOAP envelope XML.

        Args:
            operation: Operation name
            params: Parameters dict
            soap_headers: SOAP header elements

        Returns:
            SOAP envelope XML string
        """
        ns_prefix = "soap" if self.soap_version == "1.1" else "soap12"
        ns_uri = self.DEFAULT_NS[ns_prefix]

        # Build header section
        header_xml = ""
        if soap_headers:
            header_elements = ""
            for key, value in soap_headers.items():
                header_elements += f"    <{key}>{value}</{key}>\n"
            header_xml = f"  <{ns_prefix}:Header>\n{header_elements}  </{ns_prefix}:Header>\n"

        # Build body parameters
        params_xml = ""
        if params:
            for key, value in params.items():
                params_xml += f"      <{key}>{value}</{key}>\n"

        # Build namespace attribute
        ns_attr = f' xmlns:ns="{self.namespace}"' if self.namespace else ""

        envelope = (
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<{ns_prefix}:Envelope xmlns:{ns_prefix}="{ns_uri}"{ns_attr}>\n'
            f'{header_xml}'
            f'  <{ns_prefix}:Body>\n'
            f'    <ns:{operation}>\n'
            f'{params_xml}'
            f'    </ns:{operation}>\n'
            f'  </{ns_prefix}:Body>\n'
            f'</{ns_prefix}:Envelope>'
        )
        return envelope

    def _parse_response(self, xml_text: str) -> ET.Element:
        """Parse SOAP response and extract Body content.

        Args:
            xml_text: Raw XML response string

        Returns:
            XML Element of the SOAP Body content
        """
        root = ET.fromstring(xml_text)

        # Find Body element (handle both SOAP 1.1 and 1.2 namespaces)
        for ns_uri in self.DEFAULT_NS.values():
            body = root.find(f"{{{ns_uri}}}Body")
            if body is not None:
                # Check for SOAP Fault
                fault = body.find(f"{{{ns_uri}}}Fault")
                if fault is not None:
                    fault_string = fault.findtext("faultstring", "Unknown SOAP Fault")
                    raise SOAPFault(fault_string, fault)
                return body

        # If no namespace match, try without namespace
        return root

    # ==================== EXTRACTION ====================

    def extract(self, element: ET.Element, xpath: str,
                namespaces: Optional[Dict] = None) -> Optional[str]:
        """Extract text value from XML element using XPath.

        Args:
            element: XML Element to search
            xpath: XPath expression
            namespaces: Namespace mapping for XPath

        Returns:
            Text content or None
        """
        found = element.find(xpath, namespaces or {})
        if found is not None:
            return found.text
        return None

    def extract_all(self, element: ET.Element, xpath: str,
                    namespaces: Optional[Dict] = None) -> List[str]:
        """Extract all matching text values from XML.

        Args:
            element: XML Element to search
            xpath: XPath expression
            namespaces: Namespace mapping

        Returns:
            List of text values
        """
        found = element.findall(xpath, namespaces or {})
        return [el.text for el in found if el.text]

    # ==================== ASSERTIONS ====================

    @staticmethod
    def assert_element_exists(element: ET.Element, xpath: str,
                              namespaces: Optional[Dict] = None):
        """Assert an XML element exists at the given XPath."""
        found = element.find(xpath, namespaces or {})
        assert found is not None, f"Element not found at XPath: {xpath}"

    @staticmethod
    def assert_element_value(element: ET.Element, xpath: str,
                             expected: str,
                             namespaces: Optional[Dict] = None):
        """Assert an XML element has the expected text value."""
        found = element.find(xpath, namespaces or {})
        assert found is not None, f"Element not found at XPath: {xpath}"
        assert found.text == expected, (
            f"Expected '{expected}' at {xpath}, got '{found.text}'"
        )

    def close(self):
        """Close the HTTP session."""
        self.session.close()


class SOAPFault(Exception):
    """Exception raised for SOAP Fault responses."""

    def __init__(self, message: str, fault_element: ET.Element = None):
        self.fault_element = fault_element
        super().__init__(f"SOAP Fault: {message}")

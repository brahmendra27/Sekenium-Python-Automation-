"""
Self-Healing Element Locator Module

This module provides AI-assisted self-healing capabilities for element locators
when they fail. It uses multiple strategies to find elements and can learn from
failures to suggest better locators.
"""

from typing import Optional, List, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging

logger = logging.getLogger(__name__)


class SelfHealingLocator:
    """
    Self-healing locator that tries multiple strategies when an element is not found.
    
    Strategies:
    1. Original locator
    2. Fuzzy matching (partial text, contains)
    3. Alternative attributes (data-*, aria-*, role)
    4. XPath alternatives
    5. CSS selector alternatives
    """
    
    def __init__(self, driver: WebDriver, enable_logging: bool = True):
        self.driver = driver
        self.enable_logging = enable_logging
        self.healing_history = []
    
    def find_element_with_healing(
        self, 
        by: By, 
        value: str,
        timeout: int = 10
    ) -> Optional[any]:
        """
        Find element with self-healing capabilities.
        
        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Maximum time to wait for element
            
        Returns:
            WebElement if found, None otherwise
        """
        # Try original locator first
        try:
            element = self.driver.find_element(by, value)
            if self.enable_logging:
                logger.info(f"✅ Element found with original locator: {by}={value}")
            return element
        except NoSuchElementException:
            if self.enable_logging:
                logger.warning(f"⚠️ Original locator failed: {by}={value}")
        
        # Try healing strategies
        healing_strategies = self._get_healing_strategies(by, value)
        
        for strategy_name, strategy_by, strategy_value in healing_strategies:
            try:
                element = self.driver.find_element(strategy_by, strategy_value)
                if self.enable_logging:
                    logger.info(f"✅ Element found using healing strategy '{strategy_name}': {strategy_by}={strategy_value}")
                
                # Record successful healing
                self.healing_history.append({
                    'original': (by, value),
                    'healed': (strategy_by, strategy_value),
                    'strategy': strategy_name
                })
                
                return element
            except NoSuchElementException:
                if self.enable_logging:
                    logger.debug(f"❌ Healing strategy '{strategy_name}' failed: {strategy_by}={strategy_value}")
                continue
        
        # All strategies failed
        if self.enable_logging:
            logger.error(f"❌ All healing strategies failed for: {by}={value}")
        
        return None
    
    def _get_healing_strategies(self, by: By, value: str) -> List[Tuple[str, By, str]]:
        """
        Generate alternative locator strategies based on the original locator.
        
        Returns:
            List of (strategy_name, by, value) tuples
        """
        strategies = []
        
        if by == By.ID:
            # Try name attribute
            strategies.append(("name_attribute", By.NAME, value))
            # Try CSS selector with ID
            strategies.append(("css_id", By.CSS_SELECTOR, f"#{value}"))
            # Try XPath with ID
            strategies.append(("xpath_id", By.XPATH, f"//*[@id='{value}']"))
            # Try partial ID match
            strategies.append(("partial_id", By.XPATH, f"//*[contains(@id, '{value}')]"))
        
        elif by == By.NAME:
            # Try ID attribute
            strategies.append(("id_attribute", By.ID, value))
            # Try CSS selector with name
            strategies.append(("css_name", By.CSS_SELECTOR, f"[name='{value}']"))
            # Try XPath with name
            strategies.append(("xpath_name", By.XPATH, f"//*[@name='{value}']"))
        
        elif by == By.CLASS_NAME:
            # Try CSS selector
            strategies.append(("css_class", By.CSS_SELECTOR, f".{value}"))
            # Try XPath with class
            strategies.append(("xpath_class", By.XPATH, f"//*[contains(@class, '{value}')]"))
        
        elif by == By.CSS_SELECTOR:
            # Try converting CSS to XPath (basic conversion)
            if value.startswith('#'):
                # ID selector
                id_value = value[1:]
                strategies.append(("xpath_from_css_id", By.XPATH, f"//*[@id='{id_value}']"))
            elif value.startswith('.'):
                # Class selector
                class_value = value[1:]
                strategies.append(("xpath_from_css_class", By.XPATH, f"//*[contains(@class, '{class_value}')]"))
        
        elif by == By.XPATH:
            # Try alternative XPath strategies
            # If XPath contains text(), try partial text match
            if "text()=" in value:
                text_value = value.split("text()='")[1].split("'")[0] if "text()='" in value else None
                if text_value:
                    strategies.append(("partial_text", By.XPATH, f"//*[contains(text(), '{text_value}')]"))
            
            # Try data-testid if XPath looks like it's targeting an ID
            if "@id=" in value:
                id_value = value.split("@id='")[1].split("'")[0] if "@id='" in value else None
                if id_value:
                    strategies.append(("data_testid", By.CSS_SELECTOR, f"[data-testid='{id_value}']"))
        
        # Universal fallback strategies
        # Try data-testid attribute (common in modern apps)
        strategies.append(("data_testid_universal", By.CSS_SELECTOR, f"[data-testid*='{value}']"))
        
        # Try aria-label (accessibility attribute)
        strategies.append(("aria_label", By.CSS_SELECTOR, f"[aria-label*='{value}']"))
        
        # Try role attribute
        strategies.append(("role", By.CSS_SELECTOR, f"[role*='{value}']"))
        
        return strategies
    
    def get_healing_report(self) -> str:
        """
        Generate a report of all successful healing operations.
        
        Returns:
            Formatted string report
        """
        if not self.healing_history:
            return "No healing operations performed."
        
        report = "Self-Healing Report\n"
        report += "=" * 50 + "\n\n"
        
        for i, healing in enumerate(self.healing_history, 1):
            original_by, original_value = healing['original']
            healed_by, healed_value = healing['healed']
            strategy = healing['strategy']
            
            report += f"{i}. Healing Strategy: {strategy}\n"
            report += f"   Original: {original_by}={original_value}\n"
            report += f"   Healed:   {healed_by}={healed_value}\n"
            report += f"   ✅ Success\n\n"
        
        return report
    
    def suggest_locator_improvements(self) -> List[str]:
        """
        Analyze healing history and suggest permanent locator improvements.
        
        Returns:
            List of suggestions
        """
        suggestions = []
        
        for healing in self.healing_history:
            original_by, original_value = healing['original']
            healed_by, healed_value = healing['healed']
            strategy = healing['strategy']
            
            suggestion = (
                f"Consider updating locator:\n"
                f"  From: {original_by}='{original_value}'\n"
                f"  To:   {healed_by}='{healed_value}'\n"
                f"  Reason: Healed using '{strategy}' strategy"
            )
            suggestions.append(suggestion)
        
        return suggestions


# Pytest fixture for self-healing
def pytest_configure(config):
    """Register self-healing marker."""
    config.addinivalue_line(
        "markers", "self_healing: Enable self-healing for element locators"
    )


# Example usage in conftest.py:
"""
from framework.self_healing import SelfHealingLocator

@pytest.fixture
def self_healing_driver(selenium_driver):
    '''Selenium driver with self-healing capabilities.'''
    healer = SelfHealingLocator(selenium_driver)
    
    # Monkey-patch find_element to use self-healing
    original_find_element = selenium_driver.find_element
    
    def find_element_with_healing(by, value):
        element = healer.find_element_with_healing(by, value)
        if element is None:
            # Fall back to original (will raise exception)
            return original_find_element(by, value)
        return element
    
    selenium_driver.find_element = find_element_with_healing
    selenium_driver.healer = healer
    
    yield selenium_driver
    
    # Print healing report after test
    if healer.healing_history:
        print("\n" + healer.get_healing_report())
        print("\nSuggested Improvements:")
        for suggestion in healer.suggest_locator_improvements():
            print(suggestion)
"""

"""
    Module: basemanager
    Author: Neethukrishnan P
    
    Description:
    
    License:
    
    Created on: 08-17-2024
"""
from abc import ABC, abstractmethod


class BaseTestManager(ABC):
    @abstractmethod
    def run_test(self):
        pass

    @abstractmethod
    def _make_request(self):
        pass

    @abstractmethod
    def _validate_response(self, response):
        pass

from data import XmlData
from soap import SoapWebService
from assertion import XmlAssertion

__version__ = '0.1'
__author__ = 'Mykhailo Poliaruh'

class WebServicesLibrary(XmlData, SoapWebService, XmlAssertion):
    """
    WebService Library to manage testing thru soap protocol 
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
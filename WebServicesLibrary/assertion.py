from lxml import etree
from robot.api import logger

class Assertion(object):
    def __init__(self):
        self._xml = None
        
    def load_data_for_assertion(self, xml=""):
        '''
        Load xml data into internal object so then assertion method can be applied.
        '''
        try:
            self._xml = etree.fromstring(xml)
            logger.debug("Loading xml for assertion \n %s" % etree.tostring(self._xml))
        except etree.XMLSyntaxError as e:
            logger.debug("Can't load text for assertion because of error:\n %s" % e)
        
            
    def _get_xpath(self, xpath):
        try:
            nodes = self._xml.xpath(xpath)
        except:
            raise AssertionError("Failed at getting xpath %s for xml\n%s" % (xpath,self._xml.tostring()))
        return nodes
    
    def _fail_if_empty_result_in_xpath(self, xpath, nodes):
        if (len(nodes) == 0):
            raise AssertionError("Can't find xpath %s in xml" % xpath)

    def _get_xpath_and_fail_if_empty(self, xpath):
        nodes = self._get_xpath(xpath)
        self._fail_if_empty_result_in_xpath(xpath, nodes)
        return nodes    
    
    def get_value_by_xpath(self, xpath):
        '''
        Get value of xml element by xpath
        '''
        try:
            nodes = self._xml.xpath(xpath)
            if len(nodes) == 0:
                raise Exception("No element found by %s" % xpath)
        except Exception, e:
            raise Exception("Can't find element by xpath "+xpath)
        return nodes[0].text if len(nodes) <= 1 else [node.text for node in nodes]
    
class XmlAssertion(Assertion):
    def element_should_exist(self, xpath):
        '''
        Assert if element exists by passed xpath expression otherwise throw exception
        '''
        self._get_xpath_and_fail_if_empty(xpath)

    def element_should_not_exist(self, xpath):
        '''
        Assert if element doesn't exist by passed xpath expression otherwise throw exception
        '''
        nodes = self._get_xpath(xpath)
        if (len(nodes) > 0):
            raise AssertionError("Found xpath %s in xml" % xpath)
    
    def element_value_should_be_equal_to(self, xpath, expected):
        '''
        Assert one or more nodes' value for correct values that passed as arguments
        '''
        nodes = self._get_xpath_and_fail_if_empty(xpath)
        for node in nodes:
            if node.text != expected: 
                raise AssertionError("Value(%s) in xml by xpath %s didn't match to %s" 
                                     % (node.text,xpath,expected))

    def element_value_should_contain(self,xpath,expected):
        '''
        Assert one or more nodes' value contain value that passed as arguments
        '''
        nodes = self._get_xpath_and_fail_if_empty(xpath)
        for node in nodes:
            if not expected in node.text: 
                raise AssertionError("Can't find %s in %s by xpath %s" 
                                     % (expected, node.text, xpath))

    def element_value_should_be_empty(self, xpath):
        '''
        Assert one or more element's value is empty by xpath
        '''
        self.element_value_should_be_equal_to(xpath, None)

    def element_value_should_not_be_empty(self, xpath):
        '''
        Assert one or more element's value is not empty by xpath
        '''
        nodes = self._get_xpath_and_fail_if_empty(xpath)
        for node in nodes:
            if node.text is None: 
                raise AssertionError("Xpath's value(%s) for %s is empty" 
                                     % (node.text,xpath))
from robot.api import logger
from lxml import etree
import random 

class Data:
    def _read_file(self, file_path):
        try:
            self._file_content = open(file_path).read()
        except:
            raise Exception("Can't read file by path %s" % file_path)
        return self._file_content

    def _read_content(self, text):
        self._file_content = text
        return self._file_content
    
class XmlData(Data):
    '''
    Handle xml document and execute get/replace operation
    with xml document
    '''
    def __init__(self):
        self._xml = None

    def read_xml_data_from_file(self, path):
        '''
        Read xml file from file into test case
        '''
        self._xml = etree.fromstring(self._read_file(path))
        logger.debug("read xml file with content %s" % (self._read_file(path)))

    def read_xml_data_from_variable(self, text):
        '''
        Read xml file from text into test case
        '''
        self._xml = etree.fromstring(self._read_content(text))
        logger.debug("read xml from variable with content %s" % (self._read_content(text)))


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
    
    def replace_value_by_xpath(self, xpath, value):
        '''
        Replace value by xpath. If xpath returns more than 1 node than all nodes will be replaced
        @param xpath: xpath to find element in xml document
        @param value: value to substitute by xpath expression
        '''
        try:
            nodes = self._xml.xpath(xpath)
        except:
            raise Exception("Can't find elements by xpath %s" % xpath)
        for node in nodes:
            node.text = value
        return self.get_xml_data()
        
    def replace_value_by_xpath_to_random(self, xpath, prefix="", digit_count=10, suffix=""):
        '''
        Replace xpath by random value
        @param xpath: xpath to find element in xml document
        @param digit_count: how many digits to generate, 10 by defaults
        '''
        try:
            nodes = self._xml.xpath(xpath)
        except:
            raise Exception("Can't find elements by xpath %s" % xpath)
        for node in nodes:
            node.text = "".join([str(prefix),
                                 str(random.randint(10**(digit_count-1),(10**digit_count)-1)),
                                 str(suffix)])
        return self.get_xml_data()
    
    def replace_by_xslt(self, path):
        '''
        Replace data in xml thru XSLT transformation
        '''
        try:
            xslt = etree.XSLT(etree.XML(self._read_file(path)))
        except:
            raise Exception("Can't read xslt file %s" % path)
        self._xml = xslt(self._xml)
        return self.get_xml_data()
        
    def get_xml_data(self, declarion=False, encoding='UTF-8', cdata=True):
        '''
        Get corrected xml in string format. By default all xml is wrapper in CDATA section.
        As CDATA section is often used
        @param declarion:True or False. To put xml declaration for output xml.
        @param encoding: String that define encoding in xml declaration. For example, UTF-8
        @param cdata:True or False. Xml can't returned wrapped in CDATA section or without it. By default, it's True.
        '''
        output = etree.tostring(self._xml, pretty_print=True, xml_declaration=declarion, encoding=encoding)
        if cdata is True:
            return "<![CDATA[%s]]>" % output
        return etree.tostring(self._xml, pretty_print=True, xml_declaration=declarion, encoding=encoding)
    
class TextData(Data):
    def __init__(self, path):
        self.text = self.read_file(path)

    def _find_regular_expression(self, exp):
        pass

    def convert_by_regular_expression(self, re):
        pass

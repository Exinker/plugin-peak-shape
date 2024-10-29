from src.exceptions import PluginError


class DataManagerError(PluginError):
    pass


class ParseFilepathXMLError(DataManagerError):
    pass


class LoadDataXMLError(DataManagerError):
    pass


class ParseDataXMLError(DataManagerError):
    pass


class ParseMetaXMLError(ParseDataXMLError):
    pass


class ParseSpectraXMLError(ParseDataXMLError):
    pass

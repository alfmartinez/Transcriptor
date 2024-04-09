
class MappingError(Exception):
    pass

class CircularNodeLinkError(MappingError):
    pass

class MissingLabelError(MappingError):
    pass

class LineDoesntMatchAnyRuleError(MappingError):
    pass
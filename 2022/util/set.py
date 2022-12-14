class set(object):
    def __init__(self, elts):
        self.underlyingData = {}
        for elt in elts:
            self.underlyingData[elt] = True
    def add(self, elt):
        self.underlyingData[elt] = True
    def count(self):
        return len(self.underlyingData)
    def has(self, elt):
        return self.underlyingData.get(elt) is not None
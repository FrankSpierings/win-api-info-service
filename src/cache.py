class Cache:
    def __init__(self):
        self._cache = {}
    
    def add(self, name, signatures):
        if signatures:
            self._cache[name] = signatures

    def get(self, name):
        return self._cache.get(name, None)
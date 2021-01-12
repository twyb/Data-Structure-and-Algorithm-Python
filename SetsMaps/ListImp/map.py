class Map:

    # Instantiate the Map
    def __init__(self):
        self.map = list()

    # Return the length of the map
    def __len__(self):
        return len(self.map)

    # Check if key is in length
    def __contain__(self, key):
        if self.getKey(key):
            return True
        return False

    # Add new key
    def add(self, key, value):

        index = self.getKey(key)
        if index is not None:
            self.map[index].key = key
            self.map[index].value = value
            return False
        else:
            KV = _MapKV(key, value)
            self.map.append(KV)
            return True

    # Remove key
    def remove(self, key):

        index = self.getKey(key)
        if index is not None:
            self.map.pop(index)
        else:
            raise KeyError('Key is not found in mapping')
    
    # Value Of
    def valueOf(self, key):

        index = self.getKey(key)
        if index is not None:
            return self.map[index].value
        else:
            raise KeyError('Key is not found in mapping')

    # Get key
    def getKey(self, key):
        
        # Iterate through the map and find the key
        for i in range(len(self.map)):
            if self.map[i].key == key:
                return i

        return None

    # Iterator
    def __iter__(self):
        return _MapIterator(self.map)

class _MapIterator:
    # Construction of iterator of set
    def __init__(self, theMap):
        self.mapRef = theMap
        self.curIndex = 0

    # Return the ArrayIterator Object
    def output(self):
        return self

    # Show next value
    def __next__(self):
        if self.curIndex < len(self.mapRef):
            entry = self.mapRef[self.curIndex]
            self.curIndex += 1
            return entry
        else:
            raise StopIteration

class _MapKV:
    def __init__(self, key, value):
        self.key = key
        self.value = value 
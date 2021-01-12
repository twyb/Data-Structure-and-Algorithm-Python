import sys, os
sys.path.insert(0, os.path.join(sys.path[0],'Utilities'))
import error_util as e

class Set:
    
    ### List implementation
    # Instantiate a set
    def __init__(self):
        self.set = list()

    # Return the length
    def __len__(self):
        return len(self.set)

    # Check if contains
    def __contains__(self, element):
        return (element in self.set)

    # Add elements
    def add(self,element):

        # Add if it is not in set else skip
        if element not in self.set:
            self.set.append(element)

    # Remove Element
    def remove(self, element):

        # Remove if element is found in set else return error
        if element in self.set:
            self.set.remove(element)
        else:
            raise e.ElementNotInSet("Element not found in set")

    # Check if equals to
    def equals(self, setB):

        # Check if length are different
        if len(self.set) != len(setB):
            return e.SetDifferentLength("Sets are different in length")
        return self.isSubsetOf(setB)
        
    # Check if subset
    def isSubsetOf(self, setB):

        # Iterate through all to check if each element is in the other set
        for elem in self:
            if elem not in setB:
                return False
        return True

    # Set Iterator
    def __iter__(self):
        return _SetIterator(self.set)

    # Union
    def union(self, setB):

        # Instantiate new set
        newSet = Set()
        
        # Combine both set
        setB.set.extend(self.set)

        # Go through each
        for elem in setB:
            newSet.add(elem)

        return newSet.set

    # Intersect
    def intersect(self, setB):

        # Instantiate new set
        newSet = Set()

        # Get elements that are in another set
        for elem in self:
            if elem in setB:
                newSet.add(elem)

        return newSet.set

    # Difference
    def diff(self,setB):

        # Instantiate new set
        newSet = Set()

        # Get elements that are not in another set
        for elem in self:
            if elem not in setB:
                newSet.add(elem)

        for elem in setB:
            if elem not in self:
                newSet.add(elem)

        return newSet.set

class _SetIterator:

    # Construction of iterator of set
    def __init__(self, theSet):
        self.setRef = theSet
        self.curIndex = 0

    # Return the ArrayIterator Object
    def output(self):
        return self

    # Show next value
    def __next__(self):
        if self.curIndex < len(self.setRef):
            entry = self.setRef[self.curIndex]
            self.curIndex += 1
            return entry
        else:
            raise StopIteration
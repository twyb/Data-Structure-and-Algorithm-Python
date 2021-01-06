import sys, os
sys.path.insert(0, os.path.join(sys.path[0],'Utilities'))
import error_util as e
import ctypes

class Array:
    
    '''
    Arrays:
    Slightly different from Python's List counter part.
    Size of an array doesn't change and only has a few limited operations.
    Good to use when the number of elements are known, thus ensuring space used is kept to a minimal
    '''

    # Constructor Class:
    def __init__(self, size):

        if size > 0:
            
            # Use ctypes object to create our array. We then fill up the array with None to ensure that we can assign values to it
            pythonArray = ctypes.py_object * size
            self.array = pythonArray()
            self.size = size
            self.clear(None)

        elif size <= 0 or type(size) != 'int':
            raise e.ArrayConstructionError('Size of array has to be more than 0 or is not a integer')

    # Return length
    def __len__(self):
        return self.size

    # Return element at position
    def getItem(self, index):

        if index > self.size or index < 0:
            raise e.IndexError('Index exceeds the length of the array')
        else:
            return self.array[index]

    # Setting Item at position
    def setItem(self, index, value):

        if index > self.size or index < 0:
            raise e.IndexError('Index exceeds the length of the array')
        else:
            self.array[index] = value

    # Set value for all positions inside array
    def clear(self, value):

        for i in range(len(self)):
            self.array[i] = value

    # Iterate through array
    def iterate(self):
        return _ArrayIterator(self.array)

# Create an iterator function (With Reference to Data Structures and Algorithm Using Python)
class _ArrayIterator:

    # Construction of iterator of array
    def __init__(self, theArray):
        self.arrayRef = theArray
        self.curIndex = 0

    # Return the ArrayIterator Object
    def output(self):
        return self

    # Show next value
    def next(self):
        if self.curIndex < len(self.arrayRef):
            entry = self.arrayRef[self.curIndex]
            self.curIndex += 1
            return entry
        else:
            raise StopIteration


'''
Extra Note: We can't use length() to get the length for the Array class because this
would mean that when we are referring to it in the ArrayIterator, we can't get the length
of the array as this would be pointing towards the attribute which doesn't have the length()
value indicated.
'''

class Array2D:

    # 2D Constructor Array
    def __init__(self, nrows, ncols):
        if nrows > 0 and ncols > 0:

            # Create the Rows
            self.Rows = Array(nrows)

            # Iterate through the values
            for i in range(len(self.Rows)):
                self.Rows.setItem(i, Array(ncols))
            self.clear(None)
            self.nrows = nrows
            self.ncols = ncols
        else:
            raise e.ArrayConstructionError('Columns or Rows are not greater than 0, or they are not integers')

    # Return number of rows
    def numRows(self):
        return self.nrows

    # Return number of cols
    def numCols(self):
        return self.ncols

    # Clearing value
    def clear(self, value):
        
        # Iterate through the columns and give the values
        for i in range(len(self.Rows)):
            self.Rows.getItem(i).clear(None)

    # Getting item
    def getItem(self, positionTuple):

        queryRow = positionTuple[0]
        queryCol = positionTuple[1]
        return self.Rows.getItem(queryRow).getItem(queryCol)

    # Setting Item
    def setItem(self, positionTuple, value):
        queryRow = positionTuple[0]
        queryCol = positionTuple[1]
        return self.Rows.getItem(queryRow).setItem(queryCol, value)

'''
Extra Note: For consistency usage, we will be employing the Array
data structure that we have employed previously. Furthermore,
for further consistency, we ensure that we call the indexes
to retrieve or modify via a tuple format. To represent a[r,c] where
r=rows and c=columns. Conventionally, with a 2D list, a simple a[r][c]
would suffice
'''       


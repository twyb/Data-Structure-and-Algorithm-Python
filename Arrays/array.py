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
    def __iter__(self):
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
    def __next__(self):
        if self.curIndex < len(self.arrayRef):
            entry = self.arrayRef[self.curIndex]
            self.curIndex += 1
            return entry
        else:
            raise StopIteration

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
        if 0 <= queryRow < self.numRows() and 0 <= queryCol < self.numCols():
            return self.Rows.getItem(queryRow).getItem(queryCol)
        else:
            raise IndexError('Rows and Columns are not within the range or not an integer')

    # Setting Item
    def setItem(self, positionTuple, value):
        queryRow = positionTuple[0]
        queryCol = positionTuple[1]
        if 0 <= queryRow < self.numRows() and 0 <= queryCol < self.numCols():
            self.Rows.getItem(queryRow).setItem(queryCol, value)
        else:
            raise IndexError('Rows and Columns are not within the range or not an integer')

'''
Extra Note: For consistency usage, we will be employing the Array
data structure that we have employed previously. Furthermore,
for further consistency, we ensure that we call the indexes
to retrieve or modify via a tuple format. To represent a[r,c] where
r=rows and c=columns. Conventionally, with a 2D list, a simple a[r][c]
would suffice
'''

class Matrix:

    # Constructing a Matrix
    def __init__(self, nrows, ncols):
        if nrows > 0 and ncols > 0:

            # Create the Rows
            self.matrix = Array2D(nrows, ncols)
            self.matrix.clear(0)
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

    # Getting item
    def getItem(self, positionTuple):
        return self.matrix.getItem(positionTuple)

    # Setting Item
    def setItem(self, positionTuple, value):
        self.matrix.setItem(positionTuple, value)

    # Scaling By
    def scale(self, scalar):

        # Iterate through each element and times the scalar value to it
        for i in range(self.numRows()):
            for j in range(self.numCols()):
                val = self.getItem((i,j))
                self.matrix.setItem((i,j), val*scalar)

        return self.matrix

    # Transpose
    def transpose(self):

        # Generate a new array to place the number to it
        transposeArray = Array2D(self.numCols(), self.numRows())
        transposeArray.clear(0)

        # Iterate through original array
        for i in range(self.numRows()):
            for j in range(self.numCols()):
                val = self.getItem((i,j))
                transposeArray.setItem((j,i), val)

        return transposeArray

    # Addition
    def add(self, rhsmatrix):
        if self.numCols() == rhsmatrix.numCols() and self.numRows() == rhsmatrix.numRows():
            newMatrix = Matrix(self.numRows(), self.numCols())
            for i in range(self.numRows()):
                for j in range(self.numCols()):
                    current_val = self.getItem((i,j))
                    incoming_val = rhsmatrix.getItem((i,j))
                    newMatrix.setItem((i,j), current_val + incoming_val)
            return newMatrix
        else:
            raise e.MatrixOperationError('The columns or rows of the given matrix is not the same')

    # Subtraction
    def subtract(self, rhsmatrix):
        if self.numCols() == rhsmatrix.numCols() and self.numRows() == rhsmatrix.numRows():
            newMatrix = Matrix(self.numRows(), self.numCols())
            for i in range(self.numRows()):
                for j in range(self.numCols()):
                    current_val = self.getItem((i,j))
                    incoming_val = rhsmatrix.getItem((i,j))
                    newMatrix.setItem((i,j), current_val - incoming_val)
            return newMatrix
        else:
            raise e.MatrixOperationError('The columns or rows of the given matrix is not the same')

    # Multiplication
    def multiply(self, rhsmatrix):

        # Generate a new array to place the number to it
        multiplyArray = Array2D(self.numRows(), rhsmatrix.numCols())
        multiplyArray.clear(0)

        if self.numCols() == rhsmatrix.numRows():
            for i in range(self.numRows()):
                for j in range(rhsmatrix.numCols()):
                    tmp = 0
                    for k in range(self.numCols()):
                        current_val = self.getItem((i, k))
                        incoming_val = rhsmatrix.getItem((k,j))
                        tmp += current_val * incoming_val
                    multiplyArray.setItem((i, j), tmp)
            return multiplyArray        

        else:
            raise e.MatrixOperationError('The columns or rows of the given matrix is not the same')
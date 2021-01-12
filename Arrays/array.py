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
    def __getitem__(self, index):

        if index > self.size or index < 0:
            raise e.IndexError('Index exceeds the length of the array')
        else:
            return self.array[index]

    # Setting Item at position
    def __setitem__(self, index, value):

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


    '''
    Extra Note: The magic phrases such as __len__, __getitem__ and __setitem__
    will be called internally when certain syntax flavours of python are used.
    Therefore when constructing our data structures, these have to be taken
    into account for the heavylifting.
    '''

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
                self.Rows[i] = Array(ncols)
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
            self.Rows[i].clear(None)

    # Getting item
    def __getitem__(self, positionTuple):
        queryRow = positionTuple[0]
        queryCol = positionTuple[1]
        if 0 <= queryRow < self.numRows() and 0 <= queryCol < self.numCols():
            return self.Rows[queryRow][queryCol]
        else:
            raise IndexError('Rows and Columns are not within the range or not an integer')

    # Setting Item
    def __setitem__(self, positionTuple, value):
        queryRow = positionTuple[0]
        queryCol = positionTuple[1]
        if 0 <= queryRow < self.numRows() and 0 <= queryCol < self.numCols():
            self.Rows[queryRow][queryCol] = value
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
    def __getitem__(self, positionTuple):
        return self.matrix[positionTuple]

    # Setting Item
    def __setitem__(self, positionTuple, value):
        self.matrix[positionTuple] = value

    # Scaling By
    def scale(self, scalar):

        # Iterate through each element and times the scalar value to it
        for i in range(self.numRows()):
            for j in range(self.numCols()):
                val = self[(i,j)]
                self[(i,j)] =  val*scalar

        return self.matrix

    # Transpose
    def transpose(self):

        # Generate a new array to place the number to it
        transposeArray = Array2D(self.numCols(), self.numRows())
        transposeArray.clear(0)

        # Iterate through original array
        for i in range(self.numRows()):
            for j in range(self.numCols()):
                val = self[(i,j)]
                transposeArray[(j,i)] = val

        return transposeArray

    # Addition
    def add(self, rhsmatrix):
        if self.numCols() == rhsmatrix.numCols() and self.numRows() == rhsmatrix.numRows():
            newMatrix = Matrix(self.numRows(), self.numCols())
            for i in range(self.numRows()):
                for j in range(self.numCols()):
                    current_val = self[(i,j)]
                    incoming_val = rhsmatrix[(i,j)]
                    newMatrix[(i,j)] = current_val + incoming_val
            return newMatrix
        else:
            raise e.MatrixOperationError('The columns or rows of the given matrix is not the same')

    # Subtraction
    def subtract(self, rhsmatrix):
        if self.numCols() == rhsmatrix.numCols() and self.numRows() == rhsmatrix.numRows():
            newMatrix = Matrix(self.numRows(), self.numCols())
            for i in range(self.numRows()):
                for j in range(self.numCols()):
                    current_val = self[(i,j)]
                    incoming_val = rhsmatrix[(i,j)]
                    newMatrix[(i,j)] =  current_val - incoming_val
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
                        current_val = self[(i, k)]
                        incoming_val = rhsmatrix[(k,j)]
                        tmp += current_val * incoming_val
                    multiplyArray[(i, j)] = tmp
            return multiplyArray        

        else:
            raise e.MatrixOperationError('The columns or rows of the given matrix is not the same')


class MultiArray:

    # Constructing the multi array
    def __init__(self, *args):

        multiArrayLength = 1

        if len(args) < 2:
            raise e.ArrayConstructionError('Must have two or more dimensions')

        for val in args:
            if val < 1:
                raise e.ArrayConstructionError('Must have more than 1 features in each array')
            multiArrayLength *= val
        self.mArray = Array(multiArrayLength)
        self._dims = args
        self.getFactors(self._dims)

    # Get the dimensions
    def dims(self):
        return len(self._dims)

    # Get the length in dimension
    def length(self, dim):
        try:
            return self._dims[dim - 1]
        except:
            raise e.IndexError('Out of range for dimensions')

    # Clear value
    def clear(self, value):
        self.mArray.clear(value)

    # Get Item
    def __getitem__(self, positionTuple):
        index = self.getIndex(positionTuple)
        if index is None:
            raise e.IndexError('Index out of range')
        return self.mArray[index]

    # Set Item
    def __setitem__(self, positionTuple, value):
        index = self.getIndex(positionTuple)
        if index is None:
            raise e.IndexError('Index out of range')
        self.mArray[index] = value


    # Index:
    def getIndex(self, positionTuple):
        index = 0
        if len(positionTuple) != len(self._dims):
            raise e.IndexError('Position tuple is different dimension compared to the dimensions of multi array')
        for i in range(len(positionTuple)):
            if positionTuple[i] < 0 or positionTuple[i] >= self._dims[i]:
                return None
            else:
                index += positionTuple[i] * self.factors[i]
        return index
                
    # Get Factors
    def getFactors(self, dims):
        self.factors = []
        for i in range(len(dims)):
            tmp = 1
            for j in range(i+1, len(dims)):
                tmp *= dims[j]
            self.factors.append(tmp)
        
'''
Extra Notes: For MultiArray, the key idea is to decompose the
multi-dimensional array into a 1D array. This can be done via
getting each row of values or each column of values and combining
it into the 1D array. To access the data, we get the index for the
1D array through the use of a formula, i1 * f1 + .. i(n) * 1,
where f(j) = Product(d[j+1] ... d[n]) and f(n) = 1.
'''
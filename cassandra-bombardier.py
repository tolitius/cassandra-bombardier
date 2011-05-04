import pycassa
import sys

if len( sys.argv ) < 3:
    sys.exit( " Usage: %s 'number of rows' 'number of columns in a single row'" % sys.argv[0] )

NUMBER_OF_ROWS = int ( sys.argv[1] )
NUMBER_OF_COLUMNS = int ( sys.argv[2] )

# Connect to Cassandra
pool = pycassa.connect( 'Keyspace1' )
pool = pycassa.connect( 'Keyspace1', ['localhost:9160'] )

col_fam = pycassa.ColumnFamily( pool, 'ColumnFamily1' )

# Create a single row With 'numberOfColumns' columns 
def createRow( numberOfColumns ):
    row = {}

    for num in xrange( numberOfColumns ):
        row['key' + `num`] = 'value' + `num`

    return row

# Create a multi row dataset => 'howHuge' = number of rows
def createHugeDataset( howHuge ):
    dataset = {}
    dumbRow = createRow( NUMBER_OF_COLUMNS )

    for num in xrange( howHuge ):
        dataset['row'+`num`] = dumbRow

    return dataset

# Batch insert a dataset
col_fam.batch_insert( createHugeDataset( NUMBER_OF_ROWS ) )

#print createHugeDataset( NUMBER_OF_ROWS )
#print createRow( NUMBER_OF_COLUMNS )

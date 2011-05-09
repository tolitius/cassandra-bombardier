import pycassa
import sys
import pprint
from datetime import datetime 

from multiprocessing import Pool

if len( sys.argv ) < 3:
    sys.exit( " Usage: %s <number of rows> <number of columns in a single row> [<number of processes>]" % sys.argv[0] )

NUMBER_OF_ROWS = int ( sys.argv[1] )
NUMBER_OF_COLUMNS = int ( sys.argv[2] )
NUMBER_OF_PROCESSES = 1

KEY_SPACE = 'Keyspace1'
HOST = 'localhost:9160'
COLUMN_FAMILY = 'ColumnFamily1'

if len( sys.argv ) > 3:
    NUMBER_OF_PROCESSES = int ( sys.argv[3] )

# create a single row With 'numberOfColumns' columns 
def createRow( numberOfColumns ):

    row = {}
    for num in xrange( numberOfColumns ):
        row['key' + `num`] = 'value' + `num`

    return row

# create a multi row dataset => 'howHuge' = number of rows
def createHugeDataset( how_huge ):

    dataset = {}
    dumb_row = createRow( NUMBER_OF_COLUMNS )

    for num in xrange( how_huge ):
        dataset['row'+`num`] = dumb_row

    return dataset

    
# create a partitioned data set as a list of dictionaries,
# where each list item can be used as a separate partition
def createPartitionedDataset( num_of_rows, num_of_partitions ):

    dataset = []
    next_partition = {}
    single_row = createRow( NUMBER_OF_COLUMNS )

    partition_size = num_of_rows / num_of_partitions

    if ( partition_size == 0 ):
        partition_size = 1

    for row_num in xrange( num_of_rows ):

        next_partition['row'+`row_num`] = single_row

        if ( ( row_num + 1 ) % partition_size == 0 ):
            dataset.append( next_partition )
            next_partition = {}
    
    # in case there are more rows in next_partition..
    if ( num_of_rows % num_of_partitions != 0 ):
        dataset.append( next_partition )   

    #print num_of_rows, "rows in", len( dataset ), "chunks" 
    return dataset
    

# need this method, so it can be 'pickled' by the multiprocessing.Pool
# connecting to Cassandra here not to block on col_family in case of many processes
def insertDataset( dataset ):

    # connect to Cassandra
    cpool = pycassa.connect( KEY_SPACE, [HOST] )
    # finding Nemo => navigating to the family
    col_family = pycassa.ColumnFamily( cpool, COLUMN_FAMILY )
    col_family.batch_insert( dataset )


if ( NUMBER_OF_PROCESSES < 2 ):
    dataset = createHugeDataset( NUMBER_OF_ROWS )

    # batch insert a dataset
    start = datetime.now()
    insertDataset( dataset )
    stop = datetime.now()

else:
    dataset = createPartitionedDataset( NUMBER_OF_ROWS, NUMBER_OF_PROCESSES )
    #pprint.pprint( dataset )
    pool = Pool( processes = NUMBER_OF_PROCESSES )                
    start = datetime.now()
    pool.map( insertDataset, dataset )
    stop = datetime.now()

took = stop - start
print "inserting", NUMBER_OF_ROWS, "rows", NUMBER_OF_COLUMNS, "columns each took", took.seconds + took.microseconds / 1E6, "seconds"   

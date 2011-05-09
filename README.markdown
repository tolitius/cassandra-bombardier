## What is Cassandra Bombardier?

A Python bombardier based on [Pycassa](http://pycassa.github.com/pycassa/index.html "Pycassa"), that batch inserts:

  + a custom defined number of rows
  + with a custom defined number of columns
  + with a custom defined number of processes

into Cassandra
  
### The goal is to: 
  
  + optimize Cassandra setup / config to get the best write performance
  + learn Cassandra and Pycassa
  + go to sleep with geeky pride and digital satisfaction

# Here is How to Play

## Start Bombardiering

```bash
$ python cassandra-bombardier.py
 Usage: cassandra-bombardier.py <number of rows> <number of columns in a single row> [<number of processes>]
```

As you can see from the usage, you need to provide a number of rows and a number of columns to be created for each row.
[ Optionally you can also add a number of processes to insert rows to Cassandra in paralleal. By default, if number of processes is not provided, a single process will be used ]

### Single Process

Let's start from inserting 100,000 rows where each row has 7 columns:

```bash
$ python cassandra-bombardier.py 100000 7
inserting 100000 rows 7 columns each took 11.048162 seconds
```

### Multiple Processes

Cassandra was designed with parallelism in mind, so let's make it happy and use 8 processes to inserting 100,000 rows ( 7 columns each ) in parallel:

```bash
$ python cassandra-bombardier.py 100000 7 8
inserting 100000 rows 7 columns each took 6.310905 seconds
```

# Here is How to Setup / Configure

## If you have PIP / VirtualEnv installed

'cd' to the cassandra-bombardier root, and do

```bash
$ pip install -r requirements
```

### OR Install Pycassa Manually

[http://pycassa.github.com/pycassa/index.html](http://pycassa.github.com/pycassa/index.html "How to install Pycassa")
_( follow the pycassa instructions: you'd also need to install "thrift05")_

## Start Cassandra ( may need 'sudo' )

```bash
$ /usr/local/bin/cassandra -f
```

## Start Cassandra CLI

```bash
$ /usr/local/bin/cassandra-cli
```

### Enter these four to create a test keyspace / column family

```bash
[default@unknown]   connect localhost/9160;
[default@unknown]   create keyspace Keyspace1;
[default@unknown]   use Keyspace1;
[default@Keyspace1] create column family ColumnFamily1;
```

Whenever you need to delete all the data inserted previously, truncate the family ( sounds cruel, but.. gotta do it ):

```bash
[default@Keyspace1] truncate ColumnFamily1;
```


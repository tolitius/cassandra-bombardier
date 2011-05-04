## What is Cassandra Bombardier?

A simple python bombardier based on [Pycassa](http://pycassa.github.com/pycassa/index.html "Pycassa"), that batch inserts:

  + a custom defined number of rows with 
  + a custome defined number of columns

into Cassandra
  
### The goal is to: 
  
  + optimize Cassandra setup / config to get the best performance
  + learn Cassandra and Pycassa
  + go to sleep with geeky pride and digital satisfaction

# Here is How to Play

### Install Pycassa

[http://pycassa.github.com/pycassa/index.html](http://pycassa.github.com/pycassa/index.html "How to install Pycassa")

### Start Cassandra ( may need 'sudo' )

```bash
$ /usr/local/bin/cassandra -f
```

### Start Cassandra CLI

```bash
$ /usr/local/bin/cassandra-cli
```

#### Enter these four to create a test keyspace / column family

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
### Start Bombardiering

```bash
$ time python cassandra-bombardier.py
 Usage: cassandra-bombardier.py 'number of rows' 'number of columns in a single row'

real    0m0.132s
user    0m0.087s
sys     0m0.041s
```

As you can see from the usage, you need to provide a number of rows and a number of columns to be created for each row
e.g. Let's shoot 100,000 rows where each row has 7 columns:

```bash
$ time python cassandra-bombardier.py 100000 7

real    0m11.601s
user    0m8.622s
sys     0m0.138s
```


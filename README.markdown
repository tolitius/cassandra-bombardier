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

#### If you have PIP / VirtualEnv installed

'cd' to the cassandra-bombardier root, and do

```python
pip install -r requirements
```

#### OR Install Pycassa Manually

[http://pycassa.github.com/pycassa/index.html](http://pycassa.github.com/pycassa/index.html "How to install Pycassa")
_( follow the pycassa instructions: you'd also need to install "thrift05")_

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

### How do I read this output from 'time'?

#### Real 
is wall clock time - time from start to finish of the call. This is all elapsed time including time slices used by other processes and time the process spends blocked (for example if it is waiting for I/O to complete).

#### User 
is the amount of CPU time spent in user-mode code (outside the kernel) within the process. This is only actual CPU time used in executing the process. Other processes and time the process spends blocked do not count towards this figure.

#### Sys 
is the amount of CPU time spent in the kernel within the process. This means executing CPU time spent in system calls within the kernel, as opposed to library code, which is still running in user-space. Like 'user', this is only CPU time used by the process. See below for a brief description of kernel mode (also known as 'supervisor' mode) and the system call mechanism.

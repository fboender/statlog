# StatLog

Log statistics about CPU, I/O and Memory usage in a plain text file for later
analysis.

# Usage

    $ ./statlog.py > stats.log

To show a graph of Free Memory:

    $ gnuplog
    gnuplot> plot "stats.log" using 7 with lines

To show a graph with 1, 5 and 15 minute load averages:

    gnuplot> plot "stats.log" using 2 with lines, \
                           "" using 3 with lines, \
                           "" using 4 with lines

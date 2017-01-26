# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We need to scan all the horizontal and vertical neighbors of each box
   to find neighbors whos values have a length of two. When the values
   are equal, we can start to process them. It is important to distinguish
   the vertical and horizontal peers from each other. If a match occurs
   with a horizontal peer, then no vertical peer must be touched and vice
   versa. My implementation is not tuned to efficiency, and the code is
   no nice to look at as I am not used to Python due to a break of several
   years.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: I evaluated two ideas. First I tried to evaluate if the sum of every diagonal
   is exactly 45 (based on (n(n+1))/2 ). This can however only be done when the
   solution candidate is already solved completely. This means that even when
   it is clear at the beginning that the sudoku hurts the diagonal constraint,
   it must be processed until the end before it can be excluded as a viable
   solution. My tests with this method finished after ~337 seconds and failed.

   My second approach was to provide a procedure that is executed whenever
   reduce_puzzle() within search() returns a result. The values with length 1
   are evaluated for uniqueness within the two diagonals. When the uniqueness
   constraint is hurt the candidate is skipped. This implementation took
   ~185 seconds on my computer with naked_twins() disabled and finished
   successfully. With naked_twins() enabled the runtime was ~203 seconds
   and finished successfully. As the solution without naked_twins() is faster
   I disabled it for the first commit.

   After adding an improvement to the eliminate() method, the runtime
   improved to ~120 seconds.

### Additional information

The local test runs as expected.

(aind) C:\Users\me\PycharmProjects\AIND-Sudoku>python solution_test.py
...
----------------------------------------------------------------------
Ran 3 tests in 121.019s

OK

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
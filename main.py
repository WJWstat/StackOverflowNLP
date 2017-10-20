"""
StackOverflowNLP 
=====================================================

Run this code with an argument 1, 2, 3, 4 or 5 to run the tasks 3.1, 3.2, 3.3, 3.4 or 3.5. The codes are available in the subdirectories and are invoked when run with the argument.

Example: python main.py 1
"""
import sys

if __name__=='__main__':
    if (sys.argv[1] is not None):
        task = sys.argv[1]
    else:
        print (__doc__)
        sys.exit(0)

    if task == '1':
        import dataset_collection.data
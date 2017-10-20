"""
StackOverflowNLP 
=====================================================

Run this code with an argument 1, 2, 3, 4 or 5 to run the tasks 3.1, 3.2, 3.3, 3.4 or 3.5. The codes are available in the subdirectories and are invoked when run with the argument.

Example: python main.py 1
"""
import sys

if __name__=='__main__':
    if (len(sys.argv) > 1):
        task = sys.argv[1]
    else:
        print (__doc__)
        sys.exit(0)

    if task == '1':
        subtask = 'retrieve_threads'
        if (len(sys.argv) > 2):
            subtask = sys.argv[2]

        if (subtask == 'retrieve_threads'):
            print ('Running Task 1 - Retrieve Threads')
            from dataset_collection.retrieve_threads import retrieve_threads
            retrieve_threads()
        elif (subtask == 'print_thread'):
            print ('Running Task 1 - Print Thread')
            from dataset_collection.data import print_thread
            print_thread()
# MY_CODE
# I WAS AFRAID OF GARBAGE COLLECTION MESSING UP MY MULTITHREADING AND I
# DIDNT CARE ABOUT REALLY FINISHING THIS SO I BAILED


from threading import Thread
from time import time
import random
from my_alpha_beta_algos import alpha_beta_iterative_w_root, \
    get_alpha_beta_root, AB_node
from lab3 import better_evaluate
from connectfour import ConnectFourBoard
from basicplayer import get_all_next_moves

NEXT_MOVES = get_all_next_moves


class MyThread(Thread):
    def __init__(self, init_root: AB_node, target=None, group=None, name=None,
                 args=(),
                 kwargs={}):
        """
        Store the various values that we use from the constructor args,
        then let the superclass's constructor do its thing
        """
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._most_recent_val = 0
        self.root = init_root
        Thread.__init__(self, args=args, kwargs=kwargs, group=group,
                        target=target, name=name)

    def run(self):
        depth = 1
        choices = [0, 1, 2, 3, 4, 5, 6]

        children = []
        child = self.root.next_child(NEXT_MOVES)
        while child is not None:
            children.append(child)
            child = self.root.next_child(NEXT_MOVES)
        while self.has_no_update:
            random.shuffle(choices)
            for choice in choices:
                child = children[choice]

                self._target(child, depth)
            depth += 1


    def get_most_recent_val(self):
        """ Return the most-recent return value of the thread function """
        try:
            return self._most_recent_val
        except AttributeError:
            print("Error: You ran the search function for so short a time that it couldn't even come up with any answer at all!  Returning a random column choice...")
            import random
            return random.randint(0, 6)


my_func = lambda root, depth: alpha_beta_iterative_w_root(root, depth,
        eval_fn=better_evaluate, get_next_moves_fn=NEXT_MOVES)
root = get_alpha_beta_root(ConnectFourBoard(), NEXT_MOVES)
eval_t = MyThread(target=my_func, init_root=root)




eval_t.setDaemon(True)
eval_t.start()

eval_t.join(1)
print(eval_t.get_most_recent_val())
eval_t.join(1)  # 2
print(eval_t.get_most_recent_val())
eval_t.join(3)  # 5
print(eval_t.get_most_recent_val())
eval_t.join(2)  # 7
print(eval_t.get_most_recent_val())
eval_t.join(3)  # 10
print(eval_t.get_most_recent_val())
eval_t.join(7)  # 17
print(eval_t.get_most_recent_val())
eval_t.join(100)  # Overly long
print(eval_t.get_most_recent_val())

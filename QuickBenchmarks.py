from collections import namedtuple
import timeit

class ClassA(object):
    def __init__(self):
        self.A = 1
        self.B = 1

def TupleA():
    return [1,1]
def get_a(tup):
    return tup[0]

NamedTupleA = namedtuple("NamedTupleA", ["A"])

def do_class(count):
    obj = ClassA()
    total = 0
    for i in range(count):
        total += obj.A
    return total

def do_tuple(count):
    obj = TupleA()
    total = 0
    for i in range(count):
        total += obj[0]
    return total

def do_tuple_func(count):
    obj = TupleA()
    total = 0
    for i in range(count):
        total += get_a(obj)
    return total

def do_named_tuple_by_key(count):
    obj = NamedTupleA(A = 1)
    total = 0
    for i in range(count):
        total += obj.A
    return total

def do_named_tuple_by_ix(count):
    obj = NamedTupleA(A = 1)
    total = 0
    for i in range(count):
        total += obj[0]
    return total

print "Class", timeit.timeit( stmt = "do_class(100000)", setup="from __main__ import *", number = 10)
print "Tuple", timeit.timeit( stmt = "do_tuple(100000)", setup="from __main__ import *", number = 10)
print "Named", timeit.timeit( stmt = "do_named_tuple_by_key(100000)", setup="from __main__ import *", number = 10)
print "NmeIx", timeit.timeit( stmt = "do_named_tuple_by_ix(100000)", setup="from __main__ import *", number = 10)
print "tGetA", timeit.timeit( stmt = "do_tuple_func(100000)", setup="from __main__ import *", number = 10)


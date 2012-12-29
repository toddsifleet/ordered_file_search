import file_search

def create_test_file(path, size, unique):
    from random import randint
    with open(path, 'w') as test_file:
        key = 0
        for i in xrange(size):
            key += randint(1, 10)
            count = 1 if unique else randint(1, 10)
            for i in range(count):
                value = str(key) + 'ABC' * randint(1, 10)
                test_file.write("%d:%s\n" % (key, value) )

def unique_test(path):
    control_data = {}   #used to store the controlled data
    s = file_search.Search(path, key_type = int, unique = True)
    with open(path) as test_file:
        for line in test_file:
            key, value = line.split(':')
            control_data[int(key)] = value

    #test standard search
    test_standard_search(s, control_data)

    #test between search
    test_between_search(
        [s.find(i) for i in control_data], 
        [control_data[i] for i in control_data]
    )

def non_unique_test(path):
    from collections import defaultdict
    control_data = defaultdict(list)    #used to store the controlled data
    s = file_search.Search(path, key_type = int, unique = False)
    with open(path) as test_file:
        for line in test_file:
            key, value = line.split(':')
            control_data[int(key)].append( (int(key), value) )

    #test standard search
    test_standard_search(s, control_data)

    #test between search
    between_control_data = []
    test_data = []

    count = len(control_data)
    step = count / 100
    for i in range(0, count, step):
        test_data += s.between(i, i + step)
        for i in range(i, i + step + 1):
            if i in control_data:
                between_control_data += control_data[i]

    test_between_search(test_data, between_control_data)

def test_standard_search(searcher, control_data):
    error = False
    for key in control_data:
        value = searcher.find(key)
        if value != control_data[key]:
            print 'Test Data: ', key, value
            print 'Conrol Data: ', key, control_data[key]
            error = True
            
    if not error:
        print "Standard Search Succesful"

def test_between_search(test_data, control_data):
    if test_data != control_data:
        for a, b in zip(test_data, control_data):
            if a != b:
                print 'Test Data: ', a
                print 'Conrol Data: ', b
    else:
        print "Between Search Succesful" 



if __name__ == '__main__':
    import os
    file_search_test_unique = 'file_search_test_unique.txt'
    if not os.path.exists(file_search_test_unique):
        create_test_file(file_search_test_unique, 100, True)

    print "Testing Without Duplicates"
    unique_test(file_search_test_unique)

    file_search_test_non_unique = 'file_search_test_non_unique.txt'
    if not os.path.exists(file_search_test_non_unique):
        create_test_file(file_search_test_non_unique, 100, True)
    
    print "\nTesting With Duplicates"
    non_unique_test(file_search_test_non_unique)
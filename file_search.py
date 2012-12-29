class Search(object):
    '''
        Description:
            A class to search an ORDERED list of key value pairs in a text file.  With one
            key value pair per line.  A suitable file would look like:
                10:This is the data for key=10
                20:This is the data for key=20
                ...
            This uses binary search and it is significantly faster than just reading and checking each line.

            Methods you may want to overwrite:
                key_transform:
                    Convert the string to the data type you want for comparison
                    ie. if your keys are dates or integers you can use those.
                data_transform:
                    Convert the string of data into another data type.
                parser:
                    This splits a line of data into a key and value string and then calls
                    key_transform and data_transform respectively.
                _key_not_found:
                    When we can't find the element we are looking for we call this function.
                    You can overwrite it to return default data or to raise an exception.

            Arguments:
                file_path [required]:
                    A path to the file we are searching
                parser [optional]: 
                    A function used to parse each line of the file
                key_type [optional (default: int)]: 
                    the type of data your key is, e.g. float, int
                data_type [optional (default: str)]: 
                    the type of data your key is, e.g. float, int
                key_value_seperator [optional (default: ':')]: 
                    the delimeter between the key and the data
                unique_keys  [optional (default: True)]: 
                    True: if each key only appears once
                    False: keys can be duplicated  -- Only use this if you must because it slows
                        down the search process, it requires back tracking through the file.
    '''
    def __init__(self, file_path, parser = None, key_type = int, value_type = str, key_value_seperator = ':', unique = True):
        self.key_value_seperator = key_value_seperator
        self.unique = unique
        self.key_type = key_type
        self.value_type = value_type
        if parser:
            self.parser = parser
        self.fh = open(file_path)
        self.set_bounds()

    def key_transform(self, key):
        '''Transform a key string into the specified type'''
        key = key.strip()
        return self.key_type(key) if self.key_type else key

    def data_transform(self, data):
        '''Transform a data string into the specified type'''
        value = data.strip()
        return self.value_type(data) if self.value_type else value

    def parser(self, line):
        '''Parse line into key and value

            Description:
                Parse a line in the file, we split the line into
                a key and the data.  We then transform each piece
                using key_transform and data_transform respectively
            Parameters:
                line: the data to be parsed
            Return:
                key: the key portion of the line
                data: the data portion of the line
        '''
        
        key, data = line.split(self.key_value_seperator, 1)

        return self.key_transform(key), self.data_transform(data)

    def set_bounds(self):
        '''Find the bounds of the file

            Description:
                Set the minimum and maximum value of the file
                These values can then be used to determine if a
                query falls within the range of the file.
            Parameters:
                None
            Return:
                Nothing
        '''
        self.fh.seek(0)

        self.min_key, self.min_value = self.parser(self.fh.readline())

        #check for the max value
        self.fh.seek(-3, 2)
        #ignore trailing new lines
        while self.fh.read(1) == '\n':
            self.fh.seek(-2, 1)

        #walk backwards until we find the beginning of the line
        self.fh.seek(-2, 1)
        while self.fh.read(1) != '\n':
            self.fh.seek(-2, 1)

        self.max_key, self.max_value = self.parser(self.fh.readline())
        self.file_size = self.fh.tell()

    def find(self, key):
        if self.min_key > key > self.max_key:
            return self._key_not_found(key)

        if key == self.min_key:
            value = self.min_value
            position = 0
        elif key == self.max_key:
            value = self.max_value
            position = self.file_size
        else:
            value = self._search(key, 0, self.file_size)
            position = self.fh.tell()

        if self.unique:
            return value
        else:
            return self.between(key, key, position)


    def _search(self, target_key, min_position, max_position):
        '''
            Description:
                Performs a standard recursive binary search on the file
                if we can't find the specified key, we call and return
                _key_not_found.
            Parameters:
                target_key: the key we are looking for
                min_position: the minimum position in the file to look
                max_position: the maximum position in the file to look
            Return:
                value: the value of the key we were looking for
        '''
        mid = (max_position - min_position ) / 2 + min_position
        self.fh.seek(mid)
        if max_position <= self.fh.tell():
            return self._key_not_found(target_key)
        
        key, value = self.parser(self.next_full_line())

        #we need to make sure these change to avoid an endless loop
        new_min, new_max = min_position, max_position
        if key == target_key:
            return value

        elif key > target_key:
            new_max = mid + 1

        elif key < target_key:
            new_min = mid - 1

        if ( new_min >= new_max 
                or new_min == min_position 
                    and new_max == max_position ):
            return self._key_not_found(target_key)

        return self._search(target_key, new_min, new_max)

    def next_full_line(self):
        '''Get the next complete line

            Discard the current line (it could be incomplete) and
            return the complete next line

        '''
        self.fh.readline()
        return self.fh.readline()

    def __del__(self):
        '''Make sure we close the fh when we are done.'''
        self.fh.close()

    def _key_not_found(self, key = ''):
        '''
            Description:
                Allows the user to define how we behave if we 
                cannot find the key they are looking for.
        '''
        return self.value_type
    
    def between(self, min_key, max_key, start = None):
        '''Find all lines with the given key

            Back track from the given starting point untill we find a key less
            than the target key.  Then run through the file returning each line
            until we find a line with a key greater than the target key.

            Parameters:
                min_key
                max_key
                start [optional]: Where in the file to start looking
            Return:
                A list of key value pair tuples [(key, value), ...]


        '''

        if min_key > self.max_key or max_key < self.min_key:
            return []

        if start is None:
            self._search(min_key, 0, self.file_size)
            start = self.fh.tell()

        step_size = 20
        for i in xrange(start - step_size, 0, -1 * step_size):
            self.fh.seek(i)
            line = self.next_full_line()
            #if we start near the end of the file and our step size is smaller than 1
            #line we hit the end of the file, we don't want to give up we just want
            #to move farther back
            if not line:
                continue

            key, value = self.parser(line)
            if key < min_key:
                break
        else:
            #we didn't find a key smaller than the target
            self.fh.seek(0)
            key, value = self.parser(self.fh.readline())

        while key < min_key:
            key, value = self.parser(self.fh.readline())

        results = []
        while key <= max_key:
            results.append((key, value))
            line = self.fh.readline()
            if not line:
                break
            key, value = self.parser(line)

        return results

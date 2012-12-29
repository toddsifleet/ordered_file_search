Binary File Search Util
=============

A binary searcher to search large ordered files (think logs).  We implement a standard binary search by splitting the line into a key value pair, allowing you to search by key.  You can define your own line parser and key parser, allowing you to sort by: int, datetime, string etc.  The sorter can be used as is, but I built more to be subclassed for a custom usage.

A suitable file would look like:

    10:This is the data for key=10
    20:This is the data for key=20
    ...
                
The searcher is much quicker if you can guarantee unique keys, however without unique keys the searcher outpaces a standard scan search.

<<<<<<< HEAD
=======
Usage
-------

    import file_search
    searcher = file_search.Search(path, key_type = int, unique = False)

    for i in search.find(12):
        print i

    #see test.py for more usage examples
    
>>>>>>> Fix Test / Update Readme
Methods you may want to overwrite:
-------

    key_transform:
        Convert the string to the data type you want for comparison
        ie. if your keys are dates or integers you can use those.
                
    data_transform:
        Convert the string of data into another data type.

    parser:
        This splits a line of data into a key and value string and then calls key_transform 
        and data_transform respectively.

    _key_not_found:
        When we can't find the element we are looking for we call this function.  You can overwrite 
        it to return default data or to raise an exception.

Arguments:
-------

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

Testing
-------

To test you can use your own test files or we can create some dummy files.  Testing consists of using the binary search and comparing the results to the standard "read the entire file into memory" approach:

    python test.py


License:
-------

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

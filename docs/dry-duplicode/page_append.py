'''
This method extracts the raw data from each file with its file path in the 
only_paths list, appends all the data from each file as a list element in
the data_all list, and returns a list of all the data from each file.
'''

def page_append(only_paths):

    data_all = []  #  Create an empty list

    for file in only_paths:  #  Iterate through the only_paths list
        with open(file, 'r') as file_open:  #  Open the file with the current path
            data = file_open.read()  #  read/extract the data in the current file
            data_all.append(data)  #  Append all the data from the current file to the data_all list
    return data_all  #  After iterating through all the file paths, return the list containing the data from all the files


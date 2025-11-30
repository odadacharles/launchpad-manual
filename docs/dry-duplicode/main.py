#  Import required methods and packages
import glob
import os
from page_append import page_append  
from duplichecker import duplichecker
from variables import scan_dir, file_types

counter = 0

#  Perform recursive search in selected folder and create a list of all file paths of specified type(s)
only_paths = []
for file_type in file_types:
    type_files = glob.glob(scan_dir+ "/**/" + file_type, recursive=True)
    only_paths+=type_files
    
#  Store acquired file paths in a file for reference
open("dry-files/all-paths.txt","w")
for path in only_paths:
    with open("dry-files/all-paths.txt", "a") as all_paths:
        all_paths.write(path + '\n')

#  Create/open a txt files to store file paths with duplicated content
open("dry-files/duplifiles.txt", "w")

#  Use the page_append method to extract the data from all file paths as a list
all_pages = page_append(only_paths) 

#  Use the duplichecker to identify file paths with duplicated content. Repeat until only one file path remains in list of only_paths
while len(only_paths) > 1: #  This loop ensures that each file will be compared against the rest
    if duplichecker(all_pages,only_paths) == "Duplicode":  #  If duplicode is found in the current iteration
        counter += 1
        print (counter)
    all_pages.pop(0)  #  Remove the page at index 0 from the list of page data
    only_paths.pop(0) # Remove the file path at index 0 in the only_paths list



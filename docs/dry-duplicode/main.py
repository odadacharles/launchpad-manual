import glob
import os
from import_page import import_page
from duplicheck import duplicheck

rst_files = glob.glob("/home/charles.odada@canonical.com/Documents/Work Repos/launchpad-manual/docs/**/*.rst", recursive=True)
file_paths = []

open("dry-files/all-paths.txt","w")

for path in rst_files:
    with open("dry-files/all-paths.txt", "a") as all_paths:
        all_paths.write(path + '\n')
    file_paths.append(path)

open("dry-files/duplifiles.txt", "w")

while len(file_paths) > 1:
    phrases = import_page(file_paths)  #Create phrases to be compared from two files
    duplichecker = duplicheck(phrases) 
    if duplichecker[0] == True:  #Compare two phrases
        print ('duplicode')
        path1 = file_paths[0].split('/docs')
        path2 = file_paths[1].split('/docs')
        with open("dry-files/duplifiles.txt", "a") as duplifiles:
            duplifiles.write(path1[1] + '       >>>>>>           ' + path2[1] + '     ' + duplichecker[2] + '\n')

    file_paths.pop(0)

# dfs = [pd.read_rst(file) for file in rst_files]
# combined_data = pd.concat(dfs, ignore_index=True)

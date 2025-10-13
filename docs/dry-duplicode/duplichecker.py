'''
This method checks for duplicated phrases/paragraphs between files. The 
first file/page is selected as the target that all other pages will be 
iteratively compared against.  

To avoid false positives caused by "includes" at the start of most pages in the
test repository, the first 140 characters in the target page are not checked by
default. You can change this value in the variables.py file.
'''
from variables import init_start, phrase_length, kill_length, shift_val

def duplichecker(all_pages, file_paths):

    target_page = all_pages[0]  #  Assign the first page data in the all_pages list as the target
    comparison_pages = all_pages[1:]  #  Create a list of comparison pages comprising all but the target page's data

    for comp_page in comparison_pages:  #  Iterate through each comparison page

        target_start = init_start  #  Assign the index of the first character in the initial scan 
        target_end = target_start+phrase_length  #  Assign the last character in the inital scan to be the start target character plus phrase_length value

        duplicode = False  #  Set the duplicode condition checker as False

        while target_start<len(target_page)-kill_length and duplicode == False:  #  Iterate until there are only 100 characters left to scan or until the duplicode condition checker is set to True
            target_phrase = target_page[target_start:target_end]  #  Select the target phrase to be compared from the target page
            check_target = target_phrase in comp_page  #  Return True of False whether the target phrase appears in the current comparison page
            if check_target == True:  #  If target phrase is in the comparison page set duplicode condition checker to True, store current target phrase, save the relevant portion of the file paths and the copy phrase in the duplifiles.txt file.
                duplicode = True
                copy_phrase = target_phrase
                print ('duplicode')
                path1 = file_paths[0].split('/docs')
                path2 = file_paths[comparison_pages.index(comp_page)].split('/docs')  #  Set for Canonical Sphinx starterpack files. Remember to change in other applications
                with open("dry-files/duplifiles.txt", "a") as duplifiles:
                    duplifiles.write(path1[1] + '       >>>>>>           ' + path2[1] + '           ' + copy_phrase + '\n')
                return  #  Escape from loop
            
            else:  #shift the start and the end of the target phrase forward by the 'shift_val' number of characters
                target_start+=shift_val 
                target_end+=shift_val

    return


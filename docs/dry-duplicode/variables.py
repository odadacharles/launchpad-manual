'''
Variables
---------
This configuration file is used to set certain searching and scanning 
parameters that may need to be varied. This is because different repositories 
have different scanning requirements. 

For example, most of the test repository's files have an 'includes' statement 
at the start that would lead to numerous false positives. Therefore, when 
scanning that particular repository, the initial target phrase must be set to 
avoid those statements.

WARNING: Negative values or values longer than total number of characters to be
scanned in a page will most certainly cause errors. A shift value of 0 will 
cause an infinite loop. 

'''
scan_dir = "/home/charles.odada@canonical.com/Documents/Work Repos/launchpad-manual/docs/"  #  Directory to be scanned for specified file types
file_types = ['*.rst']  #  File extensions for file types to be added to comparison list. Seperate file types with comma
init_start = 140  #  Number of characters to skip before selecting the first character for scanning in each page
phrase_length = 200 #  Length of phrase to compare. Long phrases will cause false negatives and short phrases will cause false positives 
kill_length = 100  #  Scanning stops when the number of unscanned characters is less than this value
shift_val = 1  #  Number of characters by which to shift the scanning window. A scan window of 1 is the slowest but most thorough. 
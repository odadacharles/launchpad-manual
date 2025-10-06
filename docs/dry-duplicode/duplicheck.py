#  DRY-Duplicode - Don't repeat yourself, Duplicode

def duplicheck(all_pages, file_paths):

    target_page = all_pages[0]
    comparison_pages = all_pages[1:]

    for comp_page in comparison_pages:

        target_start = 140
        target_high = target_start+200

        duplicode = False

        while target_start<len(target_page)-100 and duplicode == False:
            target_phrase = target_page[target_start:target_high]
            check_target = target_phrase in comp_page
            if check_target == True:
                duplicode = True
                copy_phrase = target_page[target_start:target_high]
                print ('duplicode')
                path1 = file_paths[0].split('/docs')
                path2 = file_paths[comparison_pages.index(comp_page)].split('/docs')
                with open("dry-files/duplifiles.txt", "a") as duplifiles:
                    duplifiles.write(path1[1] + '       >>>>>>           ' + path2[1] + '           ' + copy_phrase + '\n')
                return
            
            else:
                target_start+=1
                target_high+=1

    return


        



    # page1 = phrases[0]
    # page2 = phrases[1]

    # target_start = 140
    # target_high = target_start+200

    # duplicode = False

    # while target_start<len(page1)-100:
    #     check_target = page1[target_start:target_high] in page2
    #     if check_target == True:
    #         duplicode = True
    #         copy_phrase = page1[target_start:target_high]
    #         return duplicode,target_high,copy_phrase
    #     else:
    #         target_start+=1
    #         target_high+=1
    # if duplicode == False:
    #     return duplicode,target_high,None


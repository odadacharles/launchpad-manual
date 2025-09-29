#  DRY-Duplicode - Don't repeat yourself, Duplicode

def duplicheck(phrases):
    page1 = phrases[0]
    page2 = phrases[1]

    target_low = 140
    target_high = target_low+200

    duplicode = False

    while target_low<len(page1)-100:
        check_target = page1[target_low:target_high] in page2
        if check_target == True:
            duplicode = True
            copy_phrase = page1[target_low:target_high]
            return duplicode,target_high,copy_phrase
        else:
            target_low+=1
            target_high+=1
    if duplicode == False:
        return duplicode,target_high,None


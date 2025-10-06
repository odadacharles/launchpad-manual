def import_page(file_paths):

    file_paths = file_paths
    data_all = []
    for file in file_paths:
        with open(file, 'r') as file_open:
            data = file_open.read()
            words = data.split()
            data_all.append(" ".join(words))
    return data_all


    # file1 = file_paths[0]
    # file2 = file_paths[1]

    # with open(file1, 'r') as file1_open:
    #     data1 = file1_open.read()
    #     words1 = data1.split()
    #     phrase1 = " ".join(words1)

    # with open(file2, 'r') as file2_open:
    #     data2 = file2_open.read()
    #     words2 = data2.split()
    #     phrase2 = " ".join(words2)

    # return phrase1, phrase2


    # for file in rst_files:
    #     print (file)
    #     with open(file, 'r') as f:
    #         data = f.read()
    #         words = data.split()
    #         phrase1= " ".join(words[10:21])
    #         phrase2= " ".join(words[0:20])
    #         if phrase1 in phrase2:
    #             print ("Tuko within")
    #         else:
    #             print ("nope")


    # dfs = [pd.read_rst(file) for file in rst_files]
    # combined_data = pd.concat(dfs, ignore_index=True)


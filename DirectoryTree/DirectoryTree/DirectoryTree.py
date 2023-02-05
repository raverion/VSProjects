
def is_cmd(item):
    return(item[0]=='$')

def step_into(item):
    return(item[0:4]=='$ cd' and item[5:] != '..')

def get_dir_name(item):
    return(item[4:])

def get_cd_name(item):
    return(item[5:])

def is_dir(item):
    return(item[0:3]=='dir')

def is_file(item):
    return(not is_dir(item) and not is_cmd(item))

def get_file_size(item):
    if not is_cmd(item) and not is_dir(item):
        return(int(item[0:item.index(" ")]))

def get_file_name(item):
    return(item[item.index(" ")+1:])


# optional methods >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def count_layers(inputlist):
    max_layers = 0
    current_layer = 0
    for item in inputlist:
            
        if item[0:4] == '$ cd' and item != '$ cd ..':
            current_layer += 1
            print(item, current_layer, max_layers)
        elif item == '$ cd ..':
            current_layer -= 1
            print(item, current_layer, max_layers)
        elif item == '$ ls':
            continue
            
        if current_layer > max_layers:
            max_layers += 1

    return(max_layers)
# optional functions >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def list_directories(working_dict, list_of_directories=None):
    if list_of_directories is None:
        list_of_directories = []
    for key in working_dict.keys():
        #if type(working_dict[key]) is not int:
        if type(working_dict[key]) is dict:
            list_of_directories.append(key)
            list_directories(working_dict[key], list_of_directories)

    #list_of_directories = []
    #for item in input_list:
    #    if item[0:3]=='dir' and item[3:] not in list_of_directories:
    #        list_of_directories.append(item[4:])

    return(list_of_directories)

    
def build_dir(position, _input):
    
    global inputs
    global tree #call the entire tree dictionary into this function's local scope
    dir_contents = {} # this dictionary gets assigned as a value to the key represented by "working_dir"
    #position = inputs.index(_input)

    i = position + 2
    while i!=len(inputs) and not is_cmd(inputs[i]): # iterate thru items until a '$' is reached
        if is_dir(inputs[i]):
            dir_name = get_dir_name(inputs[i])
            dir_contents[dir_name]='' # add the subdir as a key in the dictionary
        elif is_file(inputs[i]):
            file_name = get_file_name(inputs[i])
            file_size = get_file_size(inputs[i])
            dir_contents[file_name]=file_size # add the file name as key in a dictionary and the file size as the value
        i += 1
     
    if tree:
        working_dir = get_cd_name(_input)
        fill_dir(tree,working_dir,dir_contents)

    return(dir_contents)

def fill_dir(working_dict, sub_dir, dir_contents): # learned this from ChatGPT
    if sub_dir in working_dict and working_dict[sub_dir]=='':# check if sub_dir is present as a key in working_dict but is not yet built ('')
        working_dict[sub_dir] = dir_contents
        return
    for value in working_dict.values():
        if isinstance(value, dict):
            fill_dir(value, sub_dir, dir_contents)

def get_dir_size(working_dict, sub_dir):
    total_size = 0
    
    if sub_dir in working_dict: # if the specificed sub-directory is present as a key in the working directory
        for value in working_dict[sub_dir].values(): # iterate thru the contents of the sub-directory
            if isinstance(value, int): # if file (the value is a number representing file size)
                total_size += value
            if isinstance(value, dict): # if sub-directory (the value is another dictionary on its own)
                total_size += get_dir_size(tree, list(working_dict[sub_dir].keys())[list(working_dict[sub_dir].values()).index(value)]) #the second argument simply returns the key that corresponds to the specified value
    else: # otherwise, the sub-directory must be further down the tree
        for value in working_dict.values():
            if isinstance(value, dict):
                total_size = get_dir_size(value, sub_dir)
                if total_size:
                    break
    
    return(total_size)

def change_dir_name(working_dict, sub_dir, new_name):
    if sub_dir in working_dict:
        working_dict[new_name] = working_dict.pop(sub_dir)
        return
    else:
        for value in working_dict.values():
            change_dir_name(value, sub_dir, new_name)
    

if __name__ == '__main__':
    

    inputs = open("aoc_day7_part1_inputs.txt").read().splitlines()
    #inputs = open("aoc_day7_part1_example.txt").read().splitlines()
    #inputs = open("aoc_day7_part1_example2.txt").read().splitlines()
    #inputs = ['$ cd /','$ ls','dir a','14848514 b.txt','8504156 c.dat','dir d','$ cd a','$ ls','dir e','29116 f','2557 g','62596 h.lst','$ cd e','$ ls','584 i','$ cd ..','$ cd ..','$ cd d','$ ls','4060174 j','8033020 d.log','5626152 d.ext','7214296 k']
    #inputs = ['$ cd /','$ ls','dir a','14848514 b.txt','8504156 c.dat','dir d','$ cd a','$ ls','dir e','29116 f','2557 g','62596 h.lst','dir x','$ cd e','$ ls','584 i','$ cd ..','$ cd x','$ ls','1000 op.txt','$ cd ..','$ cd ..','$ cd d','$ ls','4060174 j','8033020 d.log','5626152 d.ext','7214296 k']
    tree = {} # the directory tree in the form of a nested dictionary
    
    tree['/'] = build_dir(0, inputs[0]) # build level 1 of directory, i.e. the '/' folder

    # build the rest of directory tree
    #for idx in range(len(inputs[1:])):
    idx = 1
    for _input in inputs[1:]:
        #_input = inputs[idx+2]
        if step_into(_input):
            build_dir(idx, _input)
        idx += 1

    #dir_size = get_dir_size(tree,'dcvzbqf')
    #change_dir_name(tree, 'dcvzbqf', 'dcvzbqf'+str(1))
    #dir_size = get_dir_size(tree,'dcvzbqf')

    list_of_directories = list_directories(tree)
    list_of_directories.sort()
    for directory in list_of_directories:
        print(directory)
    
        '''
    sum_of_dir_sizes_below_100k = 0
    for directory in list_of_directories:
        print(directory, end=' ')
        dir_size = get_dir_size(tree,directory)
        print(dir_size)
        if dir_size < 100000:
            sum_of_dir_sizes_below_100k += dir_size

    print(sum_of_dir_sizes_below_100k)'''

            
    

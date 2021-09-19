# orgToDict:
# Takes in a path to an org file, returns a hierarchical dictionary structured identical to the org file.
# Org headings are used as string keys in the dictionary
# -------------------------------------------------------------------------------------------------------
def orgToDict(filename, string=None, level=1, newlines=True):
    if not string == None:
        data = string
    else:
        with open(filename) as f:
            data = '\n' + f.read()
    full_dict = {}
    first_layer = data.split('\n'+('*' * level)+' ')[1:]
    for item in first_layer:
        if item == '':
            continue
        # process first line
        split_item = item.split('\n')
        base_value_index = 1
        if not split_item[1].startswith('*'):
            # base case reached
            full_dict[split_item[0].strip()] = ''
            while base_value_index < len(split_item) and not split_item[base_value_index].startswith('*'):
                # source code block
                if split_item[base_value_index].startswith('+BEGIN_SRC'):
                    #pick it up
                    full_dict[split_item[0].strip()] = []
                    base_value_index += 1
                    while not split_item[base_value_index].startswith('+END_SRC'):
                       full_dict[split_item[0].strip()].append(split_item[base_value_index][:-1])
                       base_value_index += 1
                    base_value_index += 1
                    if base_value_index >= len(split_item):
                        # end of block or file
                        break
                    continue
                # if first time iterating through this while loop
                if full_dict[split_item[0].strip()] == '':
                    if not newlines:
                        full_dict[split_item[0].strip()] += split_item[base_value_index].strip()
                    else:
                        full_dict[split_item[0].strip()] += split_item[base_value_index]
                else:
                    if not newlines:
                        full_dict[split_item[0].strip()] += ' ' + split_item[base_value_index].strip()
                    else:
                        full_dict[split_item[0].strip()] += ' ' + split_item[base_value_index]
                base_value_index += 1
            continue
        full_dict[split_item[0].strip()] = orgToDict(filename=filename,
                                                     string='\n'+'\n'.join(split_item[base_value_index:]),
                                                     level=level+1,
                                                     newlines=newlines)
    return full_dict




# dictToOrg:
# Takes in a python dictionary and a file path. Outputs the contents of the dictionary into an org file with
# a matching hierarchy
# -------------------------------------------------------------------------------------------------------
def dictToOrg(org_data, output_filename, level=1):
    # Open the file in the appropriate mode based on the current level
    if level == 1:
        f = open(output_filename, 'w')
    else:
        f = open(output_filename, 'a')
    # Check for base case
    if isinstance(org_data, dict):
        for key in org_data.keys():
            if f == None:
                f = open(output_filename, 'a')
            f.write(('*' * level) + ' ' + str(key) + '\n')
            f.close()
            f = None
            dictToOrg(org_data[key],
                      output_filename,
                      level+1)
    else:
        # Base case reached
        f.write(str(org_data) + '\n')
        f.close()

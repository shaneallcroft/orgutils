
# orgToDict:
# takes in a path to an org file, returns a hierarchical dictionary structured identical to the org file.
# Org headings are used as string keys in the dictionary
# -------------------------------------------------------------------------------------------------------
def orgToDict(filename, string=None, level=1):
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
                full_dict[split_item[0].strip()] += split_item[base_value_index].strip()
                base_value_index += 1
            continue
        full_dict[split_item[0].strip()] = orgToDict(filename=filename,
                                             string='\n'+'\n'.join(split_item[base_value_index:]),
                                             level=level+1)
    return full_dict

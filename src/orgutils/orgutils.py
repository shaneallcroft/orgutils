import os
import argparse

# orgToDict:
# Takes in a path to an org file, returns a hierarchical dictionary structured identical to the org file.
# Org headings are used as string keys in the dictionary
# ################################################################################
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
                if split_item[base_value_index].startswith('#+BEGIN_SRC'):
                    #pick it up
                    full_dict[split_item[0].strip()] = []
                    base_value_index += 1
                    while not split_item[base_value_index].startswith('#+END_SRC'):
                       full_dict[split_item[0].strip()].append(split_item[base_value_index])
                       base_value_index += 1
                    base_value_index += 1
                    if base_value_index >= len(split_item):
                        # end of block or file
                        break
                    continue
                # if first time iterating through this while loop
                if full_dict[split_item[0].strip()] == '':
                    full_dict[split_item[0].strip()] += split_item[base_value_index].strip()
                else:
                    if not newlines:
                        full_dict[split_item[0].strip()] += ' ' + split_item[base_value_index].strip()
                    else:
                        full_dict[split_item[0].strip()] += '\n' + split_item[base_value_index].strip()
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
# #######################################################################################################
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


    
    


def orgToOrgNode(filename, string=None, level=1, newlines=True):
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
                if split_item[base_value_index].startswith('#+BEGIN_SRC'):
                    #pick it up
                    full_dict[split_item[0].strip()] = []
                    base_value_index += 1
                    while not split_item[base_value_index].startswith('#+END_SRC'):
                       full_dict[split_item[0].strip()].append(split_item[base_value_index])
                       base_value_index += 1
                    base_value_index += 1
                    if base_value_index >= len(split_item):
                        # end of block or file
                        break
                    continue
                # if first time iterating through this while loop
                if full_dict[split_item[0].strip()] == '':
                    full_dict[split_item[0].strip()] += split_item[base_value_index].strip()
                else:
                    if not newlines:
                        full_dict[split_item[0].strip()] += ' ' + split_item[base_value_index].strip()
                    else:
                        full_dict[split_item[0].strip()] += '\n' + split_item[base_value_index].strip()
                base_value_index += 1
            continue
        full_dict[split_item[0].strip()] = orgToDict(filename=filename,
                                                     string='\n'+'\n'.join(split_item[base_value_index:]),
                                                     level=level+1,
                                                     newlines=newlines)
    return full_dict




#def formatPythonCode()


####################################
#         OrgUtils object
####################################

class OrgNode:
    counter = 0
    def __init__(self, key, content, level=1):  # TODO maybe make defaults, especially a universal spear
        self.level = level            
        self.key = key.lower()
        self.tags = []
        self.isLeaf = False
        self.content = dict()
        self.content['\n* '] = '' # in order to not limit what actual content org files can include
        self.isTranslator = False
        self.tab = '    '
        self.separator = '\n'
        self.translationCode = ''
        lines = content.split('\n')
        self.rawContent = content
        line_count = 0
        
        while line_count < len(lines) and (not lines[line_count].startswith('*')):#lines[line_count].startswith('#+') or lines[line_count].strip() == '':
            if lines[line_count].strip().startswith('#+'):
                # tag
                self.tags.append(lines[line_count].strip()[2:])
            elif lines[line_count].strip() == '':
                garbage_variable = True
            else:
                if (line_count == len(lines) - 1) or lines[line_count + 1].startswith('*') or lines[line_count + 1].startswith('#+'):
                    self.content['\n* '] += lines[line_count]
                else:
                    self.content['\n* '] += lines[line_count] + '\n'
            line_count += 1
        subnodes_raw = ('\n' + '\n'.join(lines[line_count:])).split('\n' + ('*' * self.level) + ' ')
        #print(subnodes_raw)
        if len(subnodes_raw) == 1:
            # split did nothing ie pattern not found ie base case
            self.isLeaf = True
            if 'translator' in self.tags or 'TRANSLATOR' in self.tags:
                self.isTranslator = True
        else:
            while lines[0] == '':
                lines = lines[1:]
            
            self.contentOrdered = [] # notably the 'value' of the node is not captured in the ordered version 
            for node_raw in subnodes_raw:
                node_key = node_raw.split('\n')[0].strip()
                if node_key == '':
                    continue
                node_content_raw = '\n'.join(node_raw.split('\n')[1:]) # TODO really not great efficiency wise here, fix
                self.content[node_key] = OrgNode(node_key, node_content_raw, level + 1)
                if self.content[node_key].isTranslator:
                    self.isTranslator = True
                self.contentOrdered.append(self.content[node_key])

    def __str__(self):
        ret_str = ('*' * self.level) + ' ' + str(self.key) + '\n'
        if len(self.tags) > 0:
            ret_str += '#+'
            ret_str += '\n#+'.join(self.tags) + '\n'
        if not str(self.getValue()) == '':
            ret_str += str(self.getValue()) + '\n'
        if self.isLeaf:
            return ret_str
        
        for node in self.contentOrdered:
            if node.level <= self.level:
                node.level = self.level + 1
            ret_str += str(node)
        return ret_str

    def searchByTag(self, tag):
        # takes in a tag as input
        # returns a list of tuples of nodes that
        print('TODO implement searchByTag')

    def translate(self, node_to_translate):
        # TODO implement functionality for non default recipe
        # this would probably be pretty straightforward, just a
        # matter of reordering the self.contentOrdered variable?
        # so how it'll happen is kind of node searched will have a different function,
        # and the functions can be called from the match statements in other functions seach level
        if self.translationCode == '':
            self.generateTranslationCode()
        specific_code = 'from orgutils import OrgNode\n\n\n' + self.translationCode
        specific_code += "\n\n\nif __name__ == '__main__':\n"
        specific_code += self.tab + 'node_to_translate = OrgNode(key=\'root\',content="""'+ str(node_to_translate) +'""")\n'
        specific_code += self.tab + 'print(func0(node_to_translate))\n'
        #system_ret = os.system("python -c '" + specific_code.replace("'","\'") + "'")
        system_ret = os.popen("python -c \"" + specific_code.replace('"','\\"') + '\"').read()
        #print(system_ret)
        return system_ret


            
    def addChild(self, child, index=-1):
        self.content[chlid.key] = child
        child.level = self.level + 1
        if index != -1:
            self.contentOrdered = self.contentOrdered[:index] + [child]  + self.contentOrdered[index:]
        else:
            self.contentOrdered = self.contentOrdered + [child]




    def getValue(self):
        return self.content['\n* ']


    def generateTranslationCode(self):
        # it is marked whether each node is a leaf and or a
        # translator, this information should be sufficient to generate the source code
        if 'comment' in self.tags:
            self.translationCode = ''
            return self.translationCode
        # comment nodes for documentation should be ignored
        
        if self.isLeaf and not self.isTranslator:
            self.translationCode = '\ndef func'+str(OrgNode.counter)+'(node_to_translate):\n' + self.tab + 'ret_str = \'\'\n'
            self.translationCode += self.tab + "ret_str += \"\"\"" + self.getValue() + "\"\"\"\n"
            self.translationCode += self.tab + 'return ret_str\n'

        elif self.isLeaf and self.isTranslator:
            self.translationCode = '\ndef func'+str(OrgNode.counter)+'(node_to_translate):\n'+self.tab+'ret_str = \'\'\n'
            self.translationCode += self.getValue().replace('o---R->', 'func' + str(OrgNode.counter))
            self.translationCode += '\n' + self.tab + 'return ret_str\n'

        # an idea for solving some of the potential ambiguity / functionality pitfalls are tags that apply to the whole of the node
        # like disjoint or conjunction
        else:
            current_function_string = '\ndef func'+str(OrgNode.counter)+'(node_to_translate):\n' +self.tab+'ret_str = \'\'\n'
            if self.isTranslator:
                current_function_string += self.tab + "ret_str += \"\"\"" + self.getValue() + "\"\"\"\n"
            else:
                current_function_string += self.getValue().replace('o---R->', 'func' + str(OrgNode.counter))
            number_before = OrgNode.counter
            difference_count = 0
            self.translationCode  = ''
            
            match_added = False
            if 'o-a-ntt-descend-iterate-over-all-children-->' in self.tags:
                current_function_string += self.tab + 'for child_node in node_to_translate.contentOrdered:\n'
                self.tab += '    '
            for org_node in self.contentOrdered:
                if 'o--//->' in org_node.tags:
                    continue
                if 'o--t-mi->' in org_node.tags:
                    print('TODO implement tag MATCH node inclusive')
                if 'o--t-mr->' in org_node.tags:
                    print('TODO implement tag MATCH node required')
                if 'o--p-mi->' in org_node.tags:
                    print('TODO implement pattern MATCH node inclusive')
                if 'o--p-me->' in org_node.tags:
                    print('TODO implement pattern MATCH node exclusive')
                else:
                    isUniversal = 'o---u->' in org_node.key
                    if isUniversal or not org_node.isTranslator:
                        OrgNode.counter += 1
                        current_function_string += (self.tab) + 'ret_str += func'+ str(OrgNode.counter)
                        current_function_string += '(node_to_translate)\n'
                    self.translationCode += org_node.generateTranslationCode()
                    # TODO add code for other cases like match or simple key matching
                    
            if 'o--node-descend-iterate-over-all-children-->' in self.tags:
            current_function_string += self.tab + 'return ret_str'
            self.translationCode += current_function_string
            
        return self.translationCode
        

    

    def getLeaves(self):
        print('TODO implement getLeaves')
        
    #def export(self, keyword):
    #    print('TODO implement export')
    # think about this more ^^^
    
    def execute(self):
        if not 'BEGIN_SRC' in self.tags:
            print('org node')
            






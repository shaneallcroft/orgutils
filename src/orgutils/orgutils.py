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


    
    



def orgToGAPOFTO(filename, string=None, level=1, newlines=True):
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

####################################
#         OrgUtils object
####################################

class SAPOFTO: # SHANE's ALL PUPOSE ORG FILE TREE OBJECT (org is at the center)
    counter = 0
    def __init__(self, key, content='', filename='', level=1):  # TODO maybe make defaults, especially a universal spear
        self.level = level            
        self.key = key.upper()
        self.tags = set()
        self.isLeaf = False
        self.content = dict()
        self.content['\n* '] = '' # in order to not limit what actual content org files can include
        self.isTranslator = False
        self.tab = '    '
        self.separator = '\n'
        self.translationCode = ''
        self.value_is_str = True
        self.priority_value = 0
        #self.degreesOfConstraint = 0
        
        if not filename == '':
            with open(filename, 'r') as f:
                 content = f.read()

        
        self.rawContent = content
        self.contentOrdered = [] # notably the 'value' of the node is not captured in the ordered version w
        
        if (content == '' or content is None):
            return 
            
        line_count = 0
    
        lines = content.split('\n')
        while line_count < len(lines) and (not lines[line_count].startswith('*')):#lines[line_count].startswith('#+') or lines[line_count].strip() == '':
            if lines[line_count].strip().startswith('#+'):
                # tag
                self.tags.add(lines[line_count].strip()[2:])
            elif lines[line_count].strip() == '':
                garbage_variable = True
            else:
                if (line_count == len(lines) - 1) or lines[line_count + 1].startswith('*') or lines[line_count + 1].startswith('#+'):
                    self.content['\n* '] += lines[line_count]
                else:
                    self.content['\n* '] += lines[line_count] + '\n'
            line_count += 1
        subnodes_raw = ('\n' + '\n'.join(lines[line_count:])).split('\n' + ('*' * self.level) + ' ')

        if len(subnodes_raw) == 1:
            # split did nothing ie pattern not found ie base case
            self.isLeaf = True
            #self.content['\n* '] += content
            if 'translator' in self.tags or 'TRANSLATOR' in self.tags:
                self.isTranslator = True
        else:
            while lines[0] == '':
                lines = lines[1:]
            for node_raw in subnodes_raw:
                node_key = node_raw.split('\n')[0].strip()
                if node_key == '':
                    continue
                
                # EXPERIMENTAL AREA BEGIN
                while node_key.startswith('*'):
                    node_key = node_key[1:]
                    node_key = node_key.strip()
                # EXPERIMENTAL AREA END
                    
                node_content_raw = '\n'.join(node_raw.split('\n')[1:]) # TODO really not great efficiency wise here, fix
                self.content[node_key] = SAPOFTO(node_key, node_content_raw, level=(level + 1))
                if self.content[node_key].isTranslator:
                    self.isTranslator = True
                self.contentOrdered.append(self.content[node_key])

    def __str__(self):
        ret_str = ('*' * self.level) + ' ' + str(self.key) + '\n'
        end_tags = []

        begin_tag = ''
        end_tag = ''
        if len(self.tags) > 0:
            tags_cpy = self.tags.copy()
            for tag in self.tags:
                if tag.startswith('END_SRC'):
                    end_tag = tag
                    tags_cpy.remove(tag)
                    continue
                elif tag.startswith('BEGIN_SRC'):
                    begin_tag = tag
                    tags_cpy.remove(tag)
                    continue
            ret_str += '#+' + '\n#+'.join(tags_cpy) + '\n'
            if ret_str.endswith('\n\n'):
                ret_str = ret_str[:-1]
            if begin_tag != '':
                ret_str += '#+' + begin_tag + '\n'
        if not str(self.getValue()) == '':
            ret_str += str(self.content['\n* ']) + '\n'
        if end_tag != '':
            ret_str += '#+' + end_tag + '\n'
        
        for node in self.contentOrdered:
            if node.level <= self.level:
                node.level = self.level + 1
            ret_str += str(node)
        return ret_str
        
    def __getitem__(self, key):
#        if key == '\n* ':
#            return self.getValue()
#        if self.content[key].isLeaf:
#            return self.content[key].getValue()
        # probably can't do shit like this damn
        #ret_val = None TODO this would be cool when i'm less tired
        #if isinstance(key, SAPOFTO):
        #    for child_key in key.keys():
        #        if child_key in self.keys():
        #            ret_val = self[key]
            

        if key not in self.keys():
            key = key.upper()
        return self.content[key]

    def __setitem__(self, subscript, item):
#        if key == '\n* ':
#            return self.getValue()
#        if self.content[key].isLeaf:
#            return self.content[key].getValue()
        # probably can't do shit like this damn
        
        #if isinstance(item, SAPOFTO) and not item is self.content[subscript]:
        #    item.
        
        self.content[subscript] = item
        return

    def append(self, data):
        value = str(self.getValue())
        self.setValue(str(value) + str(data))

    def keys(self):
        ret_list = list(self.content.keys())
        ret_list.remove('\n* ')
        return ret_list

    def pop(self, key, default_ret_val=None):
        if key == '\n* ' or not key in self.keys():
            return default_ret_val
        self.contentOrdered.remove(self.content[key])
        return self.content.pop(key,default_ret_val)


    def writeToFile(self,folder_path='./',filename=''):
        if filename=='':
            filename = self.key.lower() + '.org'
        with open(folder_path + filename, 'w') as f:
            f.write(self.castOrgLiteral())
            
    
    
    def getContentOrdered(self):
        return self.contentOrdered
        
    def addTag(self, new_tag):
        self.tags.add(new_tag)

    def quote(self):
        self.addTag('quote')
        return self
    
    def unquote(self):
        self.removeTag('quote')
        return self

    def appendLine(self, line, tab_count=0):
        self.content['\n* '] += (self.tab * tab_count) + line + '\n'

    def prependLine(self, line, tab_count=0):
        self.content['\n* '] = (self.tab * tab_count) + line + '\n' + self.content['\n* ']


    def tagAsSourceCode(self,language_name='python'):
        self.addTag('BEGIN_SRC ' + str(language_name))
        self.addTag('END_SRC ')
    
    
    def hasTag(self, tag_to_check):
        return (tag_to_check in self.tags)

    def searchTagByStartsWith(self, tag_start):
        for singular_tag in self.tags:
            if singular_tag.startswith(tag_start):
                return singular_tag
        return ''

    def searchTagByEndsWith(self, tag_end):
        for singular_tag in self.tags:
            if singular_tag.endswith(tag_end):
                return singular_tag
        return ''

    def getPriorityValue(self):
        #
        # Due to the restricted namespace inside this function, priority number is not cast
        # to in int just in case contextually it should be evaluated instead.
        priority_tag = self.searchTagByStartsWith('priority')
        if priority_tag == '':
            return '0'
        priority_number = priority_tag.split(':')[-1].strip()
        return priority_number
        

    def removeTag(self, tag_to_remove):
        self.tags.remove(tag_to_remove)


    def treeSearchByTag(self, search_tag):
        matching_nodes = []
        for child_node in self.contentOrdered:
            if child_node.searchTagByStartsWith(search_tag) != '':                
                matching_nodes.append(child_node)
            mamtching_nodes.extend(child_node.treeSearchByTag(search_tag))
        return matching_nodes

    def treeSearchByKey(self, search_key):
        matching_nodes = []
        for child_node in self.contentOrdered:
            if child_node.getHeadKey() == search_key:
                matching_nodes.append(child_node)
            mamtching_nodes.extend(child_node.treeSearchByKey(search_tag))
        return matching_nodes


        
    def addChild(self, child, index=-1):
        self.content[child.key] = child
        child.promote(self.level + 1)
        self.isLeaf = False
        if index != -1:
            self.contentOrdered = self.contentOrdered[:index] + [child]  + self.contentOrdered[index:]
        else:
            self.contentOrdered = self.contentOrdered + [child]



    def constructAndAddChild(self, key, index=-1):
        child = SAPOFTO(key)
        self.content[child.key] = child
        child.promote(self.level + 1)
        self.isLeaf = False
        if index != -1:
            self.contentOrdered = self.contentOrdered[:index] + [child]  + self.contentOrdered[index:]
        else:
            self.contentOrdered = self.contentOrdered + [child]
        return child




    def promote(self, newLevel):
        self.level = newLevel
        if not self.isLeaf:
            for child_node in self.contentOrdered:
                child_node.promote(newLevel+1)


    def promoteKeyUpper(self):
        self.key = self.key.upper()
        if not self.isLeaf:
            for child_node_key in self.keys():
                self.content[child_node_key.upper()] = self.content.pop(child_node_key)
                self.content[child_node_key.upper()].promoteKeyUpper()


        
    def removeAllChildren(self):
        value = self.getValue()
        self.content = {}
        self.content['\n* '] = value
        
    def getValue(self):
        if self.hasTag('quote'):
            return self.content['\n* ']
        elif self.value_is_str:
            ret_str = self.content['\n* '].strip()
        else:
            return self.content['\n* ']
        datatype_tag = self.searchTagByStartsWith('datatype_literal : ')
        if 'org_literal' in self.tags:
            for child_node in self.contentOrdered:
                child_node.promote(1)
                ret_str += str(child_node)
                child_node.promote(self.level+1)
        elif not datatype_tag == '':
            datatype = datatype_tag.split(':')[1].strip()
            return eval(datatype + '("' + ret_str.replace('"', '\\"') + '")')
        return ret_str

    def castOrgLiteral(self):
        # TODO maybe include the tags here??
        
        ret_str = self.content['\n* '].strip() + '\n'
        for child_node in self.contentOrdered:
            child_node.promote(1)
            ret_str += str(child_node)
            child_node.promote(self.level+1)
        return ret_str

    def addDatatypeLiteralTag(self, datatype):
        # marking something already with a 'datatype_literal' tag would
        # TODO add a check for this
        self.addTag('datatype_literal : ' + str(datatype))

    def markDatatypeString(self):
        self.addTag('datatype_literal : str')

    def isMarkedForStringLiteral(self): # meaning that this nodes value is marked to be returned as a string literal
        return 'datatype_literal : str' in self.tags
    
    def setValue(self, new_value, store_as_string=True):
        #                          ^^^^^^ it probably should be "convert_to_string" instead since new_val can be str
        if store_as_string:
            self.content['\n* '] = str(new_value)
        else:
            self.content['\n* '] = new_value
            self.value_is_str = False
            # then again it only really applies when its not a string, any issues that could arise
            # i dont see being too problematic

    def decrementValue(self, decrement_amount=1):
        # this assumes the unit is tagged
        if str(self.getValue()).isnumeric():
            if "float" in self.tags:
                self.setValue(float(self.getValue()) - float(decrement_amount))
                return float(self.getValue())
            else:
                self.setValue(int(self.getValue()) - int(decrement_amount))
                return int(self.getValue())
        else:
            print("tried to decrement a non numeric value, this isnt like catastrophic, but it probably shouldn't happen")
            return -1
        
    
    
    def setHeadKey(self, new_key):
        self.key = new_key

    def getHeadKey(self):
        return self.key

    def flatten(self):
        leaves = []
        for child in self.contentOrdered:
            if child.isLeaf:
                leaves.append(child)
            else:
                leaves.extend(child.flatten())
        return leaves


    def asLambdaFunction(self, variable_declaration_csv):
        return eval('lambda ' + variable_declaraction_csv + ' : ' + self.content['\n* '].strip())
        
        
    def lineList(self, conditional=True):
        lines = self.getValue().split('\n')
        ret_val = []
        if not conditional:
            return ret_val
        for line in lines:
            if line == '':
                continue
            ret_val.append(line.strip())
        return ret_val



    # Right now it isn't possible to have an await statement inside a conditional or loop, this should be possible
    # but requires probably a markup added while parsing and requires a tweak to the code that executes the blocks.
    #
    def getValueAsPythonBlockList(self, conditional=True): 
        if not 'BEGIN_SRC python' in self.tags:
            print('WARNING pythonStatementList function being called on non code node')
        lines = self.getValue().split('\n')
        ret_val = []
        if not conditional:
            return ret_val
        current_block = ''
        
        for line in lines:
            if line == '':
                continue
            if line.startswith('  '):
                line = line.strip()
            if line.startswith('await '):
                if not current_block == '':
                    ret_val.append(current_block)
                    current_block = ''
                ret_val.append(line)
            else:
                current_block += line + '\n'
        if not current_block == '':
            ret_val.append(current_block)
        return ret_val

    #def export(self, keyword):
    #    print('TODO implement export')
    # think about this more ^^^

    def populatePrototype(self, prototype_parameters): # parameters should be another SAPOFTO
        # returns the nubmer of vacancies filled by prototype_parameters
        
        # example of vacancy label in the prototype %-%-%SESSION_ARCHETYPE%-%-%
        # vvvv find all vacancies        
        value_list = self.getValue().split('%-%-%')
        parameter_key_list = list(prototype_parameters.keys())
        vacancies_filled_count = 0

        new_val = ''
        for i in range(0,len(value_list)+1):
            if not (i % 2):
                parameter_key = value_list[i]
                if parameter_key in prototype_parameters.keys():
                    vacancies_filled_count += 1
                    new_val += str(prototype_parameters[parameter_key].getValue())
                else:
                    new_val += '%-%-%'
                    new_val += parameter_key
                    new_val += '%-%-%'

            else:
                new_val += value_lisit[i]
        if vacancies_filled_count == 0:
            return 0
        self.setValue(new_val)
        return vacancies_filled_count
        
        
    
    def getAST(self): # chnage to be default false if memory issues,  might have weird interaction with deleting/ changing code or funcitons that change 
        
        code_str = self.content['\n* ']
        lines = code_str.split('\n')
        code_str_corrected = ''
        for line in lines:
            if line == '':
                continue
            if line.startswith('  '):
                line = line.strip()
            code_str_corrected += line + '\n'
            #                    ^^^^^^^^^^^^^^compiled python is supposed to have a 0 offset so we're subtracting 1
        SAPOFTO.counter += 1
        self.content['\n* AST'] = compile(code_str_corrected, str(self.key.lower()) + str(SAPOFTO.counter), 'exec')
        return self.content['\n* AST']

    
    def getChildByIndex(self, index):
        return self.contentOrdered[int(index)]
    
    def execute(self):
        exec(self.getAST())


    # -------------------------------------------------------
    #  TRANSLATION STUFF (PROBS NOT RELEVANT TIL LATER)
    # -------------------------------------------------------
    def translate(self, node_to_translate):
        # TODO implement functionality for non default recipe
        # this would probably be pretty straightforward, just a
        # matter of reordering the self.contentOrdered variable?
        # so how it'll happen is kind of node searched will have a different function,
        # and the functions can be called from the match statements in other functions seach level
        if self.translationCode == '':
            self.generateTranslationCode()
        specific_code = 'from orgutils import SAPOFTO\n\n\n' + self.translationCode
        specific_code += "\n\n\nif __name__ == '__main__':\n"
        specific_code += self.tab + 'node_to_translate = SAPOFTO(key=\'root\',content="""'+ str(node_to_translate) +'""")\n'
        specific_code += self.tab + 'print(func0(node_to_translate))\n'
        #system_ret = os.system("python -c '" + specific_code.replace("'","\'") + "'")
        system_ret = os.popen("python -c \"" + specific_code.replace('"','\\"') + '\"').read()
        #print(system_ret)
        return system_ret


    def generateTranslationCode(self):
        # it is marked whether each node is a leaf and or a
        # translator, this information should be sufficient to generate the source code
        if 'comment' in self.tags:
            self.translationCode = ''
            return self.translationCode
        # comment nodes for documentation should be ignored
        
        if self.isLeaf and not self.isTranslator:
            self.translationCode = '\ndef func'+str(SAPOFTO.counter)+'(node_to_translate):\n' + self.tab + 'ret_str = \'\'\n'
            self.translationCode += self.tab + "ret_str += \"\"\"" + self.getValue() + "\"\"\"\n"
            self.translationCode += self.tab + 'return ret_str\n'

        elif self.isLeaf and self.isTranslator:
            self.translationCode = '\ndef func'+str(SAPOFTO.counter)+'(node_to_translate):\n'+self.tab+'ret_str = \'\'\n'
            self.translationCode += self.getValue().replace('>---R->', 'func' + str(SAPOFTO.counter))
            self.translationCode += '\n' + self.tab + 'return ret_str\n'

        # an idea for solving some of the potential ambiguity / functionality pitfalls are tags that apply to the whole of the node
        # like disjoint or conjunction
        else:
            current_function_string = '\ndef func'+str(SAPOFTO.counter)+'(node_to_translate):\n' +self.tab+'ret_str = \'\'\n'
            if self.isTranslator:
                current_function_string += self.tab + "ret_str += \"\"\"" + self.getValue() + "\"\"\"\n"
            else:
                current_function_string += self.getValue().replace('>---R->', 'func' + str(SAPOFTO.counter))
            number_before = SAPOFTO.counter
            difference_count = 0
            self.translationCode  = ''
            
            match_added = False
            if '>-a-ntt-descend-iterate-over-all-children-->' in self.tags:
                current_function_string += self.tab + 'for child_node in node_to_translate.contentOrdered:\n'
                self.tab += '    '
            for org_node in self.contentOrdered:
                if '>--//->' in org_node.tags:
                    continue
                if '>--t-mi->' in org_node.tags:
                    print('TODO implement tag MATCH node inclusive')
                if '>--t-mr->' in org_node.tags:
                    print('TODO implement tag MATCH node required')
                if '>--p-mi->' in org_node.tags:
                    print('TODO implement pattern MATCH node inclusive')
                if '>--p-me->' in org_node.tags:
                    print('TODO implement pattern MATCH node exclusive')
                else:
                    isUniversal = '>---u->' in org_node.key
                    if isUniversal or not org_node.isTranslator:
                        SAPOFTO.counter += 1
                        current_function_string += (self.tab) + 'ret_str += func'+ str(SAPOFTO.counter)
                        current_function_string += '(node_to_translate)\n'
                    self.translationCode += org_node.generateTranslationCode()
                    # TODO add code for other cases like match or simple key matching
                    
            #if '>--node-descend-iterate-over-all-children-->' in self.tags:
            current_function_string += self.tab + 'return ret_str'
            self.translationCode += current_function_string
            
        return self.translationCode




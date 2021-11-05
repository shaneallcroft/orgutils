
####################################
#         OrgUtils object
####################################

class OrgNode:
    
    def __init__(self, key, content, level=1):
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
            if lines[line_count].startswith('#+'):
                # tag
                self.tags.append(lines[line_count][2:])
            elif lines[line_count].strip() == '':
                garbage_variable = True
            else:
                self.content['\n* '] += lines[line_count]
            line_count += 1
        subnodes_raw = ('\n' + '\n'.join(lines[line_count:])).split('\n' + ('*' * self.level) + ' ')
        print(subnodes_raw)
        if len(subnodes_raw) == 1:
            # split did nothing ie pattern not found ie base case
            self.isLeaf = True
            if 'translator' in self.tags:
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

            
    def addChild(self, child, index=-1):
        self.content[chlid.key] = child
        child.level = self.level + 1
        if index != -1:
            self.contentOrdered = self.contentOrdered[:index] + [child]  + self.contentOrdered[index:]
        else:
            self.contentOrdered = self.contentOrdered + [child]

    def getValue(self):
        return self.content['\n* ']

        
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
        
        translation_result = ''
        for translator_node in self.contentOrdered:
            # TODO check for over ridable tag
            if not translator_node.isTranslator:
                continue
        # pick it up, append the whole of thhe node to translate, then call a separate ypthon proccess

    def generateTranslationCode(self, counter=0):
        # it is marked whether each node is a leaf and or a
        # translator, this information should be sufficient to generate the source code
        if self.isLeaf and not self.isTranslator:
            self.translationCode = 'def func'+str(counter)+'(node_to_translate):\n' 
            self.translationCode += self.tab + "ret_str += \"\"\"" + self.content + "\"\"\""
            self.translationCode += self.tab + 'return ret_str'

        elif self.isLeaf and self.isTranslator:
            self.translationCode = 'def func'+str(counter)+'(node_to_translate):\n'
            self.translationCode += self.content
            self.translationCode += self.tab + 'return ret_str'

        # an idea for solving some of the potential ambiguity / functionality pitfalls are tags that apply to the whole of the node
        # like disjoint or conjunction
        else:
            current_function_string = 'def func'+str(counter)+'(node_to_translate):\n'
            number_before = counter
            self.translationCode  = ''
            
            match_added = False
            for org_node in self.contentOrdered:
                counter += 1                
                self.translationCode += org_node.generateTranslationCode(counter)
                current_function_string += "if '--u->' in node_to_translate.key:\n"
                current_function_string += (self.tab * 2) + 'func'+ str(counter) + '(node_to_translate)\n'
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
            

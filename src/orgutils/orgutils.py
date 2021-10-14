
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




def dictToHtml(dict_data, title='', level=1, full_document=False):
    html_string = ''
    if level == 1 and full_document:
        html_string = '<!DOCTYPE html>\n<html>\n<head>\n<script>'
        # credit to https://github.com/maqboolkhan/Collapsible-list/blob/master/ul.js for the js embedded in this script
        # vvvvvvvvvvvvvvvvvv
        html_string += 'window.onload = function  () {\n'
        html_string += '	var li_ul = document.querySelectorAll(".col_ul li  ul");\n'
        html_string += '    for (var i = 0; i < li_ul.length; i++) {\n'
        html_string += '        li_ul[i].style.display = "none"\n'
        html_string += '    };\n'
        html_string += '\n'
        html_string += '    var exp_li = document.querySelectorAll(".col_ul li > span");\n'
        html_string += '    for (var i = 0; i < exp_li.length; i++) {\n'
        html_string += '        exp_li[i].style.cursor = "pointer";\n'
        html_string += '        exp_li[i].onclick = showul;\n'
        html_string += '    };\n'
        html_string += '    function showul () {\n'
        html_string += '        nextul = this.nextElementSibling;\n'
        html_string += '        if(nextul.style.display == "block")\n'
        html_string += '            nextul.style.display = "none";\n'
        html_string += '        else\n'
        html_string += '            nextul.style.display = "block";\n'
        html_string += '    }\n'
        html_string += '}\n'
        html_string += '\n</script>'
        
        html_string += '<meta name="orghtml" content="width=device-width, initial-scale=1">\n'
        #html_string += '.collapsible {\n'
        #html_string += 'background-color: #777;color: white; cursor: pointer;'
        #html_string += 'padding: 18px; width: 100%; width: 100%; border: none;'
        #html_string += 'text-align: left; outline: none; font-size: 15px;}\n'
        #html_string += '.active, .collapsible:hover{ background-color: #555;}\n'
        #html_string += '.content {padding: 0 18px; max-height:0; overflow:hidden; transition: max-height 0.2s ease-out;'
        html_string += '</head>\n<body>\n<style>\n'
        html_string += '            body {\n'
        html_string += '            font-family: "Roboto", sans-serif;\n'
        html_string += '            font-size: 17px;\n'
        html_string += '            background-color: #fdfdfd;\n'
        html_string += '        }\n'
        html_string += '        .shadow {\n'
        html_string += '            box-shadow: 0 4px 2px -2px rgba(0, 0, 0, 0.1);\n'
        html_string += '        }\n'
        html_string += '        .btn-danger {\n'
        html_string += '            color: #fff;\n'
        html_string += '            background-color: #f00000;\n'
        html_string += '            border-color: #dc281e;\n'
        html_string += '        }\n'
        html_string += '        .masthead {\n'
        html_string += '            background: #3398E1;\n'
        html_string += '            height: auto;\n'
        html_string += '            padding-bottom: 15px;\n'
        html_string += '            box-shadow: 0 16px 48px #E3E7EB;\n'
        html_string += '            padding-top: 10px;\n'
        html_string += '        }\n'
        html_string += '    </style>\n'
        html_string += '<ul class="col_ul">\n'

        
    #if not title == '':
    #    html_string += '<h2>' + title + '</h2>\n'
    
    # Check for base case
    if isinstance(dict_data, dict):
        for key in dict_data.keys():
            html_string += '<li> <span>' + str(key) + '</span>\n<ul>'
            html_string += dictToHtml(dict_data[key],
                               title,
                               level+1,
                               full_document)
            html_string += '</ul>\n </li>\n' 
    else:
        # Base case reached
        html_string += '<li>' + str(dict_data) + '</li>\n'

    
    html_string += '</body>'
    #u
    return html_string
    
    
    
    
    
####################################
#         OrgUtils object
####################################


#class Org:
    
#    def __init__(self, in_dict={}):
#        self.dictionary = in_dict




#import argparse
#from orgutils import orgutils
#from src.orgutils.orgutils import orgutils

# manual tests for orgutils
#def main():
#    parser = argparse.ArgumentParser('takes in parameters testing orgutils')
#    parser.add_argument('--org-file', help='the org file to turn into a dictionary')
#    args = parser.parse_args()
#
#    org_dict = orgToDict(filename=args.org_file) #orgutils.orgToDict(filename=args.org_file)
#    #print(org_dict)
#    #dictToOrg(org_data=org_dict, output_filename='test2.org')#orgutils.dictToOrg(org_data=org_dict, output_filename='test2.org')
#    
#    print(dictToHtml(dict_data=org_dict,full_document=True))#orgutils.dictToHtml(dict_data=org_dict)

## automatic tests
    
#if __name__ == '__main__':
#    main()

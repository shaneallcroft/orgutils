import argparse
from orgutils import OrgNode
#from src.orgutils.orgutils import orgutils



def main():
    
    parser = argparse.ArgumentParser('Takes in parameters for skelorg to run')
    parser.add_argument('command',default='translate')
    parser.add_argument('--translator')
    parser.add_argument('--translatee')
    parser.add_argument('--debug', type=int, required=False, default=0)
    args = parser.parse_args()
    with open(args.translatee) as f:
        org_str_content = str(f.read())
    with open(args.translator) as f:
        org_str_translator = str(f.read())
    #print(dictToHtml(orgutils.orgToDict(filename='test.org'), full_document=True))
    try:
        translator = OrgNode(key='root translator', content=org_str_translator)
        translatee = OrgNode(key=args.translatee, content=org_str_content)
        translation = translator.translate(node_to_translate=translatee)
        print(translation)
        if args.debug == 1:
            print('debug mode on, printing translation:\n')
            print(translator.translationCode)            
    except BaseException as e:
        print(e)
        print('\n\nan error occured, printing translation code for troubleshooting')
        print('##################################################')
        print(translator.translationCode)


    
    

if __name__ == '__main__':
    main()

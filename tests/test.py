import argparse
from orgutils import orgutils




# manual tests for orgutils
def main():
    parser = argparse.ArgumentParser('takes in parameters testing orgutils')
    parser.add_argument('--org-file', help='the org file to turn into a dictionary')
    args = parser.parse_args()

    org_dict = orgutils.orgToDict(filename=args.org_file)
    print(org_dict)
    orgutils.dictToOrg(org_data=org_dict, output_filename='test2.org')
    


# automatic tests
    
if __name__ == '__main__':
    main()

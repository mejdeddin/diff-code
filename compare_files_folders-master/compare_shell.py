#import lib
import os, difflib, argparse


__auth__ = 'si majdi'
__date__ = '01/02/2021'


def compare_files(file1, file2, report):
    """
    def : compare two file
    return report file

    """

    # read file and 


    text1 = open(file1).readlines()
    text2 = open(file2).readlines()
    create_report_file(report)
    with open(report, 'a') as f:
        for line in difflib.unified_diff(text1, text2, fromfile=file1, tofile=file2,n=0):
            
            
            f.write('{}\n'.format(line))


def create_report_file(report_path):
    """
    def: create report file if it dosn't exit
    return : empty txt file
    """
    with open(report_path, 'w') as f:
        f.write("empty for the moment !!")

#######################################################


def compare_files_in_folder(file1, file2, report):
    """
    def : compare two file
    return report file

    """
    text1 = open(file1).readlines()
    text2 = open(file2).readlines()

    with open(report, 'a') as f:
        for line in difflib.unified_diff(text1, text2, fromfile=file1, tofile=file2,n=0):   
            if '@@' not in line:
                f.write('{}\n'.format(line))
    

def list_all_file(root):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(root):
        for file in f:
                files.append(os.path.join(r, file))
    # create a list of dict
    files = [{i.split('\\')[-1]:i} for i in files]
    return files


def Intersection(list_file_path, report, root,inter): 

    only_in_f1= []
    for i in list_file_path:
        if i not in inter:
            only_in_f1.append(i)
    with open(report, 'a') as f:
        f.write('file exist only in {} : {}\n'.format(root,only_in_f1))


def inter(lst1, lst2): 
    return set(lst1).intersection(lst2)


def recursive_comp_files(root1, root2, report):
    try :
        os.remove(report)
    except : 
        pass
    
    with open(report, 'a') as f:
        f.write('##### full scan report of {} folder and {} folder #####\n\nreport content : \n\n'.format(root1, root2))

    files_root1 = list_all_file(root1)
    files_root2 = list_all_file(root2)

    # empty lists
    list_file_path1, list_file_path2 = [], []

    for f1 in files_root1:
        for f2 in files_root2:
            
            # list of path 
            list_file_path1.append(list(f1.keys())[0]) 
            list_file_path2.append(list(f2.keys())[0]) 

            # check if file from folder 1 exist in folder 2
            if list(f1.keys())[0] == list(f2.keys())[0]:
                with open(report, 'a') as f:
                    print(f1, ' : ',f2)
                    f.write('##########################################################################\n')
                compare_files_in_folder(list(f1.values())[0],list(f2.values())[0],report)
                
    
    list_file_path1 = list(set(list_file_path1))
    list_file_path2 = list(set(list_file_path2))

    inter_ = inter(list_file_path1, list_file_path2)

    with open(report, 'a') as f:
        f.write('\n\n##### result of comparing folders  ##### \n\nfiles exist in both folders {}\n'.format(inter_))

    Intersection(list_file_path1,report,root1,inter_)
    Intersection(list_file_path2,report,root2,inter_)

def run(file1, file2, report, genre):
    if genre in ['f', 'F']:
        compare_files(file1, file2, report)
    if genre in ['D', 'd']:
        recursive_comp_files(file1, file2, report)
    if genre not in ['D', 'd', 'f', 'F']:
        print("genre most be one of [D, d, f, F], f for file and d for directory or check the help command.")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--first", required=True, type=str, help='first folder')
    parser.add_argument("--second", required=True, type=str, help="second folder")
    parser.add_argument("--report", required=True, type=str, help="report path")
    parser.add_argument("--genre", required=True, type=str, help="file or directory")
    
    args = parser.parse_args()
    
    file1 = args.first
    file2 = args.second
    report = args.report
    genre = args.genre
    run(file1, file2, report, genre)

        
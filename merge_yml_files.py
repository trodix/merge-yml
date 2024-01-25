#!/usr/bin/python3

import sys, getopt
import subprocess
import sys
import shutil
from os import path, listdir
from datetime import datetime

PKG_DIR_PATH = './pkg'

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def merge_config(source1, source2, dest):

    import ruamel.yaml
    yaml = ruamel.yaml.YAML()

    # Load yaml files
    with open(source1) as fp:
        tpl_conf_file = yaml.load(fp)
    with open(source2) as fp:
        conf_file = yaml.load(fp)

    # Merge source1.yml dans source2.yml
    for i in tpl_conf_file:
        if i not in conf_file:
            print(f"Ajout de la propriété {i}: {tpl_conf_file[i]}")
            conf_file.update({i: tpl_conf_file[i]})

    # Backup dest file
    if path.isfile(dest):
        shutil.copy(dest, dest + '-' + datetime.today().strftime('%Y%m%d-%H%M%S'))

    # Ecrit le resultat
    f = open(dest, 'w')
    yaml.dump(conf_file, f)
    f.close()

def show_help():
    print ('merge_yml_files.py -i <source1> -j <source2> -o <dest>')

def main(argv):
    source1 = ''
    source2 = ''
    dest = ''
    try:
        opts, args = getopt.getopt(argv,"hi:j:o:",["ifile=","jfile=","ofile="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            show_help()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            source1 = arg
        elif opt in ("-j", "--jfile"):
            source2 = arg
        elif opt in ("-o", "--ofile"):
            dest = arg
    if source1 == '' or source2 == '' or dest == '':
        show_help()
        exit(2)
    print('Fichier source 1: ', source1)
    print('Fichier source 2: ', source2)
    print('Fichier destination: ', dest)
    print('\n------------------------\n')
    merge_config(source1, source2, dest)

if __name__ == "__main__":
    for p in listdir(PKG_DIR_PATH):
        dep_path = path.join(PKG_DIR_PATH, p)
        print("Installation de la dépendance pip " + dep_path)
        print('\n------------------------\n')
        install(dep_path)
    main(sys.argv[1:])

#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import os
import platform

import importlib.metadata
__version__ = importlib.metadata.version("list-ppa")

from shutil import which
import subprocess

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.application.current import get_app
import filecmp

import argparse
import argcomplete

import requests

import re

from bs4 import BeautifulSoup

check_av=False

def prompt_autocomplete():
    app = get_app()
    b = app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)

def get_ppas_and_archive(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    ppas = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('/~'):
            user = str(href.split('/')[1]).replace('~', '') 
            pack = str(href.split('/ubuntu')[1]) 
            if which('add-apt-repository') is not None and check_av == True:
                codename=subprocess.check_output(["lsb_release", "-sc"])
                codename=str(codename).replace('b', '').replace('\\n','').replace("'","",2) 
                url="http://ppa.launchpad.net/" + str(user) + str(pack) + "/ubuntu/dists/" + str(codename) + "/"
                response = requests.get(url)
                if response.status_code == 200:
                    ppas.append(user+pack)
                else:
                    continue
            else:
                ppas.append(user+pack)
    return ppas

def main():
    def_path = os.path.expanduser('~/.config/ppas')
    
    choices = argcomplete.completers.ChoicesCompleter
    parser = argparse.ArgumentParser(description="List available ppas from 'https://launchpad.net' and add results to a file (if not in file already)",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-o", "--only-list", action='store_true', required=False, help="Only list configuration")
    parser.add_argument("-v",'--version', action='version', version='%(prog)s {version}'.format(version=__version__)) 
    
    parser.add_argument("-f","--file", required=False, help="Output file (default: " + def_path + ")", metavar="Output file")

    if which('add-apt-repository') is not None:
        parser.add_argument("-n","--not-check-available", action='store_false', required=False, help="Dont check if available for Ubuntu version")
         
    output_stream = None
    if "_ARGCOMPLETE_POWERSHELL" in os.environ:
        output_stream = codecs.getwriter("utf-8")(sys.stdout.buffer)

    argcomplete.autocomplete(parser, output_stream=output_stream)
    
    args = parser.parse_args()
    
    path=def_path
     
    res='n' 
    
    if hasattr(args, 'not_check_available'): 
        check_av=args.not_check_available 

    if not args.file and args.only_list == False: 
        res = prompt("Save results to file or output only? [Y/n]: ", pre_run=prompt_autocomplete, completer=WordCompleter(["y", "n"]))
    elif args.file:
        res='y'
    elif args.only_list == True:
        res='n'

    if res == 'y' or not res:
        if not args.file: 
            res1 = prompt("Filepath: (can be nonexistant - Empty: " + str(def_path) + "): ", pre_run=prompt_autocomplete, completer=PathCompleter())
        else:
            res1=os.path.expandvars(os.path.expanduser(args.file))
         
        if res1 == '':
            os.makedirs(os.path.dirname(def_path), exist_ok=True)
            if not os.path.exists(def_path): 
                with open(def_path, 'w'): pass 
        else:
            if os.path.isdir(res1):
                print(str(res1) + "is a directory that already exists") 
                raise SystemExit              
            if os.path.dirname(res1): 
                os.makedirs(os.path.dirname(res1), exist_ok=True) 
            if not os.path.exists(res1): 
                with open(res1, 'w'): pass
            path= os.path.abspath(os.path.abspath(res1)) 

    url = 'https://launchpad.net/ubuntu/+ppas?name_filter='            
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    last='' 
    for link in soup.find_all('a'):
        href = link.get('href')
        clas_s = link.get('class')
        if not last and clas_s == ['last']:
            last=href.split('start=')[1] 
    
    for start in range(0, int(last), 300): 
        url = 'https://launchpad.net/ubuntu/+ppas?name_filter=&batch=300'
        if start > 0:
            url = url + '&memo=' + str(start) + "&start=" + str(start)  
        ppas = get_ppas_and_archive(url)
        for ppa in ppas: 
            if res == 'y':
                non_uniq=False 
                with open(path,"r+") as file:
                    for line in file:
                        if ppa in line:
                            non_uniq = True 
                            break
                    if non_uniq == True:
                        continue
                    file.write(ppa + '\n')
                    print(str(ppa) + " added to " + str(path)) 
            else: 
                print(ppa)

if __name__ == '__main__':
#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
    main()

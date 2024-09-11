## List-ppa

Fetch and list all available ppas from https://launchpad.net/ubuntu/+ppas?name_filter=  

Available on with pip/pipx: https://pypi.org/project/list-ppa/  
Very simple script, but it does check whether the ppa is available for your specific version of Ubuntu.  
It does take a while for it to look up all the possible ppas, therefor it is not adviced to run it constantly but rather to keep the output of the script in a file which you can regenerate every so often.
Running it without any argument will trigger a prompt that asks you wheter you want to save it to a file or not.  

Checking repo availability can be disabled with `--not-check-available`

Depends on:  
    [bs4](https://pypi.org/project/bs4/),  
    [requests](https://pypi.org/project/requests/)  

## Installation:  

```
sudo apt install pipx 
pipx ensurepath
pipx install list-ppa
```  

## Options:  

```usage: list-ppa [-h] [-o] [-v] [-f Output file]  

List available ppas from 'https://launchpad.net' and add results to a file (if not in file already)

options:
  -h, --help            show this help message and exit
  -o, --only-list       Only list configuration (default: False)
  -v, --version         show program's version number and exit
  -f Output file, --file Output file
                        Output file (default: /home/user/.config/ppas) (default: None)
```

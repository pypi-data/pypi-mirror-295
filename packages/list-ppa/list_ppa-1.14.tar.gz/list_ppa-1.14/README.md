## List-ppa

Fetch and list all available ppas from https://launchpad.net/ubuntu/+ppas  

Available on with pip/pipx: https://pypi.org/project/list-ppa/  
Very simple script that doesn't use any parameters.  
It does take a while for it to look up all the possible ppas, therefor it is not adviced to run it constantly but rather to keep the output of the script in a file which you can regenerate every so often.  

Depends on:  
    [bs4](https://pypi.org/project/bs4/),  
    [requests](https://pypi.org/project/requests/)  

## Installation:  

```
sudo apt install pipx 
pipx ensurepath
pipx install list-ppa
```  


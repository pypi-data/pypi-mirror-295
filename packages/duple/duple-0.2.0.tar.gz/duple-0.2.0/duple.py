import click
from pathlib import Path
import os
import hashlib
from tqdm import tqdm
import humanize
import json
from collections import Counter
from send2trash import send2trash

# from concurrent.futures import ProcessPoolExecutor

@click.group()
@click.version_option()
def cli() -> None:
    '''
    A simple program to find and remove duplciate files.
    '''
    pass

@cli.command()
@click.argument('path', type = click.STRING)
@click.argument('hash', type = click.STRING)
@click.option('--depth_lowest', '-d', is_flag = True, help = 'keep the file with the lowest pathway depth')
@click.option('--depth_highest', '-D', is_flag = True, help = 'keep the file with the highest pathway depth')
@click.option('--shortest_name', '-s', is_flag = True, help = 'keep the file with the shortest name')
@click.option('--longest_name', '-S', is_flag = True, help = 'keep the file with the longest name')
@click.option('--created_oldest', '-c', is_flag = True, help = 'keep the file with the oldest creation date')
@click.option('--created_newest', '-C', is_flag = True, help = 'keep the file with the newest creation date')
@click.option('--modified_oldest', '-m', is_flag = True, help = 'keep the file with the oldest modification date')
@click.option('--modified_newest', '-M', is_flag = True, help = 'keep the file with the newest modification date')
def scan(path: str, hash: str, depth_lowest: bool, 
                               depth_highest: bool,
                               shortest_name: bool,
                               longest_name: bool,
                               created_oldest: bool,
                               created_newest: bool,
                               modified_oldest: bool,
                               modified_newest: bool) -> None:
    '''
    Scan recursively computes a hash of each file to put into a
    dictionary.  The keys are the hashes of the files, and the values
    are the files (path and metadata).  If an entry has more than 1 file
    associated, they are duplicates.  The original is determined by the
    flags or options (ex: -d).  The duplicates are added to a file called
    duple.delete.
    '''
    
    if hash not in hashlib.algorithms_available:
        click.secho(f'Hash must be one of the following: {hashlib.algorithms_available}')
        return
    
    flags = [depth_lowest,
            depth_highest,
            shortest_name,
            longest_name,
            created_oldest,
            created_newest,
            modified_oldest,
            modified_newest]

    c = Counter(flags)
    if c[True] > 1:
        click.secho('Only one flag can be chosen at a time.')
        return
    
    filelist = list()
    for root, dirs, files in os.walk(path, followlinks=False):
        for file in files:
            if Path(f'{root}/{file}').exists():
                filelist.append(f'{root}/{file}')

#################################################
#   opportunity to speed this up with concurrent futures
#################################################

    p_dict: dict = dict()
    for p in tqdm(filelist):
        with open(p, 'rb') as f:
            digest = hashlib.file_digest(f, hash)
        
        hex = digest.hexdigest()
        if hex not in p_dict.keys():
            p_dict[hex] = list()
        p_dict[hex].append(p)

#################################################
#################################################

    result = dict()
    for k, v in p_dict.items():
        if len(v) > 1:
            result[k] = v

    for k, v in result.items():
        stats = dict()
        for file in v:
            stat = Path(file).stat()
            stats[file] = stat
        result[k] = stats    
    
    # compute some statistics and create outputs

    total_size = 0
    file_count = 0
    for k, stats in result.items():
        for file, stat in stats.items():
            file_count += 1
            total_size += stat.st_size
        total_size -= stat.st_size
        file_count -= 1

    with open('duple.json', 'w') as f:
        json.dump(result, f, indent = 4)

    delete_list = create_remove_list(*flags)
    with open('duple.delete', 'w') as f:
        for file in delete_list:
            f.write(f'{file}\n')

    click.secho()
    click.secho(f'In total {len(filelist)} files, whereof {file_count} are duplicates in {len(result.keys())} groups')
    click.secho(f'Duplicates which can be removed: {humanize.naturalsize(total_size)}')
    click.secho()
    click.secho("Wrote 'duple.json' with results.")
    click.secho("Wrote 'duple.delete' with files to be deleted")

def create_remove_list(depth_lowest: bool, 
           depth_highest: bool,
           shortest_name: bool,
           longest_name: bool,
           created_oldest: bool,
           created_newest: bool,
           modified_oldest: bool,
           modified_newest: bool) -> list:

    # define test functions
    def path_depth(path: str) -> int:
        return len(Path(path).parents)
    
    def name_length(path: str) -> int:
        return len(Path(path).name)
    
    def created_date(path: str) -> int:
        return Path(path).stat().st_birthtime
    
    def modified_date(path: str) -> int: 
        return Path(path).stat().st_mtime

    # select the test function based on flag
    options = [(depth_lowest , path_depth, 1),
               (depth_highest , path_depth, -1),
               (shortest_name , name_length, 1),
               (longest_name , name_length, -1),
               (created_oldest ,  created_date, 1),
               (created_newest , created_date, -1),
               (modified_oldest , modified_date, 1),
               (modified_newest , modified_date, -1)]
    
    for flag, function, option in options:
        if flag:
            test_fun = function
            negate = option
    
    delete_files = list()

    with open('duple.json', 'r') as f:
        scan: dict = json.load(f)

    for item in scan.values():
        keys = list(item.keys())
        seed = test_fun(keys[0])
        result = keys[0]
        for path in item.keys():
            if negate * seed > negate * test_fun(path):
                seed = test_fun(path)
                result = path
        
        keys.remove(result)
        delete_files.extend(keys)
    
    return delete_files

@cli.command()
def rm() -> None:
    with open('duple.delete', 'r') as f:
        paths = f.read().splitlines()
    
    for path in tqdm(paths):
        send2trash(path)

    dirs = list()
    for root, folders, files in os.walk(os.getcwd()):
        if f'.DS_Store' in files:
            send2trash(f'{root}/.DS_Store')
    
    for root, folders, files in os.walk(os.getcwd()):
        if not files and not folders:
            dirs.append(root)

    dirs = sorted(dirs, key = lambda x: -1 * len(Path(x).parents))
    for dir in dirs:
        send2trash(dir)
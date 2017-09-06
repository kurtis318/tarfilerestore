#!/usr/bin/python

import sys
import os
import argparse
from RunCmdPy import RunCmd
from pip.utils import untar_file

cmd_runner = RunCmd()

NORMAL_MODE = "normal"
TEST_MODE = "test"
BLANKS16=' '*16
BLANKS20=' '*20

def parse_parms(cmd_parms):
    """

    :param cmd_parms: Command-line parameters
    :type cmd_parms:  array of strings
    :return: command parameters
    :rtype: list
    """

    # Here are options with values after the option
    parser = argparse.ArgumentParser()
   
    parser.add_argument('-s', '--src_dir', 
                        help="Path to directory of tar files.", 
                        required=True, 
                        dest="src_dir") 
    parser.add_argument('-t', '--target', 
                        help="Target of untar output.", 
                        required=True, 
                        dest="to_dir")
    parser.add_argument('-m', '--mode', 
                        help="Mode to run.", 
                        required=False, 
                        choices=[NORMAL_MODE,TEST_MODE],
                        default=NORMAL_MODE, 
                        dest="mode")

    # Perform parsing and issue messages.
    args = parser.parse_args()

    print(">>> Parameters are correct.")
    print("<args1={}>".format(args))
    
    return args     # parse_parms()

def verify_dir(dir_path, mode):
    
    ecnt = 0
    if not os.path.isdir(dir_path):
        ecnt+=1
        print(">>> ERROR: directory of tar files not found <dir_path={}".format(dir_path))
        return ecnt
    
    cmd = "ls -l {}/*.tar|wc -l".format(dir_path)
    cmd_runner.run(cmd, mode)
    if cmd_runner.get_rc != 0:
        ecnt+=1
        print(">>> ERROR: Bad return code from ls command. rc=".format(cmd_runner.get_rc))
        return ecnt
    
    tfcnt = int(cmd_runner.get_stdout[0])
    print("<tfcnt={}> <stdout[0]={}> <cmd={}>".format(tfcnt, cmd_runner.get_stdout[0], cmd))
    if tfcnt == 0:
        print(">>> ERROR: Directory {} has NO tar files.  Terminating script.".format(dir_path))
        exit(100)
    
    # OK, lets untar the tar files!
    cmd = "ls {}/*.tar".format(dir_path)
    
    cmd_runner.run(cmd, mode)
    
    if cmd_runner.get_rc != 0:
        print(">>> ERROR: Error with <cmd={}> <rc={}>.  Terminating script.".format(cmd, cmd_runner.get_rc))
        exit(101)
        
    return cmd_runner.get_stdout    # verify_dir()

def untar_files(tar_files, to_dir, mode):
    """
    Untar a list of files into a specify directory.
    """
    
    for tar_file in tar_files:
        
        cmd = "tar -xf {} {}".format(tar_file, to_dir)
        print(">>> INFO: <tar_file={} {}".format(tar_file, to_dir))
        
        print("{}<mode={}> <cmd={}>".format(BLANKS16, mode, cmd,))
        msecs = cmd_runner.elaspe_time_run(cmd, mode)
        print("{}<rc={}> Elapased time={}".format(BLANKS16,
                                                  cmd_runner.get_rc,
                                                  cmd_runner.ms_2_human_readable(msecs)))
    
    return      # verify_dir()

def main():
    
    args = parse_parms(sys.argv)
    print("<src_dir={}> <to_dir={}> <mode={}>".format(args.src_dir, args.to_dir, args.mode))
    
    files = verify_dir(args.src_dir, args.mode)
    
    # Adjust the value of run mode to mathc RunCmd object
    if args.mode == NORMAL_MODE:
        args.mode = RunCmd.NORMAL_MODE
    else:
        args.mode = RunCmd.DEBUG_MODE
        
    print("<files={}>".format(files))
    untar_files(files, args.to_dir, args.mode)
    
    return          # main()

if __name__ == "__main__":
    # execute only if run as a script
    main()
    exit(0)
    
"""<short function description>

          <longer function description>

          Args:
              big_table: An open Bigtable Table instance.
              keys: A sequence of strings representing the key of each table row
                  to fetch.
              other_silly_variable: Another optional variable, that has a much
                  longer name than the other args, and which does nothing.

          Returns:
              A dict mapping keys to the corresponding table row data
              fetched. Each row is represented as a tuple of strings. For
              example:

              {'Serak': ('Rigel VII', 'Preparer'),
               'Zim': ('Irk', 'Invader'),
               'Lrrr': ('Omicron Persei 8', 'Emperor')}

              If a key from the keys argument is missing from the dictionary,
              then that row was not found in the table.

          Raises:
              IOError: An error occurred accessing the bigtable.Table object.
          """

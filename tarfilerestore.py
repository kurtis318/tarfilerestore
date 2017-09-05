#!/usr/bin/python

import sys
import os
import argparse
from RunCmdPy import RunCmd

cmd_runner = RunCmd()

NORMAL_MODE = "normal"
TEST_MODE = "test"

def parse_parms(cmd_parms):
    """

    :param cmd_parms: Command-line parameters
    :type cmd_parms:  array of strings
    :return: command parameters
    :rtype: list
    """

    # Here are options with values after the option
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-d', '--dir', 
                        help="Path to directory of tar files", 
                        required=True, 
                        dest="dir")
    parser.add_argument('-m', '--mode', 
                        help="Mode to run", 
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
    
    cmd = "ls -l {}/*.tar|wc -l"
    cmd_runner.run(cmd, mode)
    if cmd_runner.get_rc != 0:
        ecnt+=1
        print(">>> ERROR: Bad return code from ls command. rc=".format(cmd_runner.get_rc))
        return ecnt
    
    tfcnt = int(cmd_runner.get_stdout[0])
    if tfcnt == 0:
        print(">>> ERROR: Directory {} has NO tar files.  Terminating script.".format(dir_path))
        exit(100)
    
    
        
    return      # verify_dir()

def main():
    
    args = parse_parms(sys.argv)
    print("<dir={}> <mode={}>".format(args.dir, args.mode))
    
    verify_dir(args.dir, args.mode)
    
    return          # main()

if __name__ == "__main__":
    # execute only if run as a script
    main()
    exit(0)

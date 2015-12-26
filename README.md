#logcat v1

A tool to execute command at remote hosts.

C:\\\{PROJECT_DIR\}\\> python main\.py  
Usage: main.py APP\_ID\(Default|your\_app\_id\) WORKING\_DIRECTORY COMMAND \[OUTPUT\(Console|FILE\_PATH\) LINE\_SIZE\]

Examples:  
> 1. Output to console  
        python main.py "Default" "/" "ls -lrt"  
        python main.py "Default" "/" "ls -lrt" Console  
> 2. Output to text file  
        python main.py "Default" "/" "ls -lrt" "res/sysout.txt"  
> 3. Limit the line size  
        python main.py "Default" "/" "ls -lrt" Console 20  

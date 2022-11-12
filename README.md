# NeatSeq-Flow-GUI

A Graphical User Interface for the High Throughput Sequencing Workflow Platform **"NeatSeq-Flow"**.

For more information about **"NeatSeq-Flow"** see the full documentation on **[Read The Docs](http://neatseq-flow.readthedocs.io/en/latest/)**

<img align="right" src="https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/doc/NeatSeq-Flow-GUI.gif" width="650">

### Table of Contents    
- [Dependencies](#dependencies)
- [Installing](#installing)
  - [Using Conda](#using-conda)
  - [No Conda](#no-conda)
- [Tutorial](#tutorial)
- [Contact](#contact)

&nbsp;  
&nbsp;
&nbsp;  
&nbsp;
&nbsp;  
&nbsp;
&nbsp;  
&nbsp;
&nbsp;  
&nbsp;
&nbsp;  
&nbsp;
&nbsp;  
&nbsp;

***

## Dependencies
**For NeatSeq-Flow-GUI to work you will need:**
- python = 3.6.5
- wxpython
- pyyaml
- munch
- pandas
- [Flexx](https://github.com/flexxui/flexx)
- A web-browser (Preferably firefox)

## Installing

  ### Using Conda
  Installing Using Conda will install NeatSeq-Flow-GUI with all its dependencies* in one go: 
  - First if you don't have **Conda**, [install it!](https://conda.io/miniconda.html) 
  - Then in the terminal:
    1. Create the **NeatSeq_Flow** conda environment:
    ```Bash
      conda env create levinl/neatseq_flow
    ```  
    2. Activate the **NeatSeq_Flow** conda environment:
    ```Bash
      bash
      source activate NeatSeq_Flow
    ```
    3. Run **NeatSeq_Flow_GUI**:
    ```Bash 
      NeatSeq_Flow_GUI.py
    ```
    4. For more option:
    ```Bash 
        NeatSeq_Flow_GUI.py -h
        usage: NeatSeq_Flow_GUI.py [-h] [--Server] [--PORT CHAR] [--HOST CHAR] [--SSL]
                           [--SSH_HOST CHAR] [--SSH_PORT CHAR] [--USER CHAR]
                           [--PASSW CHAR] [--USERSFILE CHAR]
                           [--UNLOCK_USER_DIR] [--WOKFLOW_DIR CHAR]
                           [--CONDA_BIN CHAR] [--LOG_DIR CHAR]

        NeatSeq-Flow GUI By Liron Levin

        optional arguments:
          -h, --help          show this help message and exit
          --Server            Run as Server
          --PORT CHAR         Use this port in which to run the app, If not set will
                              search for open port (Works only When --Server is set)
          --HOST CHAR         The host name/ip to serve the app, If not set, will try
                              to identify automatically (Works only When --Server is
                              set)
          --SSL               Use SSL (Only When --Server is set)
          --SSH_HOST CHAR     Connect using SSH to a remote host, NeatSeq-Flow needs
                              to be installed on the remote host (Works only When
                              --Server is set)
          --SSH_PORT CHAR     When --SSH_HOST is set use this ssh port to connect to a
                              remote host.
          --USER CHAR         User Name For This Serve (Works only When --Server is
                              set)
          --PASSW CHAR        Password For This Serve (Works only When --Server is
                              set)
          --USERSFILE CHAR    The location of a Users file in which a list of users,
                              E-mails addresses and Users directories are separated by
                              one space (as:USER user@example.com /USER/DIR). The
                              login password will be send to the user e-mail after
                              filling its user name and the password generated at the
                              beginning of the run (Works only When --Server is set).
                              You will need a Gmail account to send the password to
                              the users (you will be prompt to type in your Gmail
                              address and password)
          --UNLOCK_USER_DIR   Don't Lock Users to their Directory Or to the Current
                              Working Directory
          --WOKFLOW_DIR CHAR  A Path to a Directory containing work-flow files to
                              choose from at log-in. Works only When --Server is set.
                              If --SSH_HOST is set, the Path needs to be in the remote
                              host.
          --CONDA_BIN CHAR    A path to a the CONDA bin location. If --SSH_HOST is
                              set, the Path needs to be in the remote host.
          --LOG_DIR CHAR      A path to a directory to save log files about users
                              statistics. Only woks If --Server is set. In any way the
                              path needs to be at the local host.
    ```
  *Not including the web-browser

  ### No Conda
  If all the dependencies are satisfied:
  - Just clone the github repository:
    ```Bash 
      git clone https://github.com/bioinfo-core-BGU/NeatSeq-Flow-GUI.git
    ```
  - NOTE: If not installed using CONDA you need to clone the NeatSeq-Flow repository as well as the NeatSeq-Flow Modules repository
  
  [NeatSeq-Flow repository](https://github.com/bioinfo-core-BGU/neatseq-flow) 
  
  [NeatSeq-Flow Modules repository](https://github.com/bioinfo-core-BGU/neatseq-flow-modules) 

# Tutorial
Detailed [Tutorial](https://github.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/blob/master/Tutorial.md) to learn and experience NeatSeq-Flow-GUI.


# Contact
Please contact Liron Levin at: [levinl@post.bgu.ac.il](mailto:levinl@post.bgu.ac.il)
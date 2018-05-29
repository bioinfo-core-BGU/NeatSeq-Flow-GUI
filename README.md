# NeatSeq-Flow-GUI

A Graphical User Interface for the High Throughput Sequencing Workflow Platform **"NeatSeq-Flow"**.

For more information about **"NeatSeq-Flow"** see the full documentation on **[Read The Docs](http://neatseq-flow.readthedocs.io/en/latest/)**

<img align="right" src="https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/doc/NeatSeq-Flow-GUI.PNG" width="650">

### Table of Contents    
- [Dependencies](#dependencies)
- [Installing](#installing)
  - [Using Conda](#using-conda)
  - [No Conda](#no-conda)
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
- python >= 3.6
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
    1. Download the conda installer file:
    ```Bash
      wget https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/NeatSeq_Flow_GUI_installer.yaml
    ```
    2. Create the **NeatSeq_Flow_GUI** conda environment:
    ```Bash
      conda env create -f NeatSeq_Flow_GUI_installer.yaml
    ```  
    3. Activate the **NeatSeq_Flow_GUI** conda environment:
    ```Bash
      bash
      source activate NeatSeq_Flow_GUI
    ```
    4. Run **NeatSeq_Flow_GUI**:
    ```Bash 
      NeatSeq_Flow_GUI.py
    ```
  *Not including the web-browser

  ### No Conda
  If all the dependencies are satisfied:
  - Just clone the github repository:
    ```Bash 
      git clone https://github.com/bioinfo-core-BGU/neatseq-flow.git
    ```
# Contact
Please contact Liron Levin at: [levinl@post.bgu.ac.il](mailto:levinl@post.bgu.ac.il)
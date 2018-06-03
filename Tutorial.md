# NeatSeq-Flow-GUI Tutorial

## In this Tutorial we will:
 - [Install Conda](#install-conda)
 - [Install NeatSeq-Flow](#install-neatseq-flow)
 - [Install NeatSeq-Flow-GUI](#install-neatseq-flow-gui)
 - [Learn How to Create a Work-Flow](#learn-how-to-create-a-work-flow)
 - [Create a Sample file](#create-a-sample-file)
 - [Configure the Used Variables in the Work-Flow](#configure-the-used-variables-in-the-work-flow)
 - [Configure the Cluster information ](#configure-the-cluster-information)
 - [Run the Work-Flow](#run-the-work-flow)




***


## Install Conda

  - For Linux 64bit, in the terminal:
    ```Bash
      wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
      sh Miniconda2-latest-Linux-x86_64.sh
    ```
    **During conda's installation: type yes to add conda to the PATH**
    
    For different operating system go to [Conda](https://conda.io/miniconda.html) 
    
## Install NeatSeq-Flow 
    1. Create New Directory for the Tutorial
       ``Bash
         mkdir Tutorial
         cd Tutorial
       ```
    2. Download the **NeatSeq Flow Tutorial** installer file:
        ``Bash
          wget http://neatseq-flow.readthedocs.io/en/latest/_downloads/NeatSeq_Flow_Tutorial_Install.yaml
        ```
    3. Create the **NeatSeq_Flow_Tutorial** conda environment:
        ```Bash
          conda env create -f NeatSeq_Flow_Tutorial_Install.yaml
        ```  


## Install NeatSeq-Flow-GUI
   1. Download the **NeatSeq-Flow-GUI** installer file:
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
    
## Learn How to Create a Work-Flow
    1. Add New Step:
        In the Work-Flow Tab choose a module template and click on the 'Create New Step' button.
        <img align="right" src="https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/doc/Add_Step.gif" width="650">
    2. You can change the new step name by clicking on the step name and edit the key field and then click the 'Edit' button to set the change. 
        <img align="right" src="https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/doc/Change_Step_Name.gif" width="650">
    3. To determine the position of the new step in the work-flow:
        <img align="right" src="https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/doc/Set_base.gif" width="650">    
        - Click on the step button to see the step options 
        - Click on the base option
        - Click on the 'Value options' drop-down menu
        - Choose a previous step and click the 'Add' button. This can be repeated to choose several previous steps.
        - Click the 'Edit' button to set the changes.
    4. Add new step option:
        <img align="right" src="https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/doc/New_step_option.gif" width="650">    
        - Click on the step's name (or a step option to create a new sub option)
        - Click on the 'New' button.
        - It is possible to edit the new option name and value by editing the 'Key' field and the 'Value' field, it is also possible to choose from the 'Value options' drop-down menu.
        - Click the 'Edit' button to set the changes.
    5. Edit step's options:
        <img align="right" src="https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/doc/Edit_step_option.gif" width="650">    
        - Click on the step's option name and change the 'Key' field and/or the 'Value' field, it is also possible to choose from the 'Value options' drop-down menu.
        - When using the 'Value options' drop-down menu, in some cases it is possible to choose variables that are defined in the 'Vars' Tab.
          They will appear in the form of {Vars.some_field.some_sub_field} to indicate the value found in the 'Vars' Tab in the some_sub_field field ( which is a sub field of 'some_field' ).  
        - It is possible to choose file location as a value to the 'Value' field by clicking on the 'Browse' button. 
        - Click the 'Edit' button to set the changes.        
    6. Remove field or step:
        <img align="right" src="https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/doc/Remove_field_or_step.gif" width="650">    
        - Click on the step's name (to remove the step) or on a step's option name (to remove the option and it's sub fields) 
        - Click the 'Remove' button
        
# Contact
Please contact Liron Levin at: [levinl@post.bgu.ac.il](mailto:levinl@post.bgu.ac.il)
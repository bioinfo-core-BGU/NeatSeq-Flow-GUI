
from flexx import flx
from flexx import app, event, ui
import pandas as pd
import sys, time, os ,re
from datetime import datetime
import socket
import asyncio
import argparse
from multiprocessing import Process, Queue

__author__   = "Liron Levin"
jid_name_sep = '..'
LOCAL_HOST   = socket.gethostname()

Text_COLORS  = ['black','green','red','orange','magenta','cyan','blue']

class Table(flx.GroupWidget):
    items            = event.DictProp({}, settable=True)
    rowmode          = event.ListProp([], settable=True)
    active           = event.BoolProp(True, settable=True)
    choice           = event.IntProp(-1, settable=True)
    Current_Highlite = event.IntProp(-1, settable=True)
    def init(self,Highlite=0,Heder_Backgroun_Color='SeaShell'):
        self.Rows                  = {}
        self.Highlite              = Highlite
        self.num_of_rows           = 0
        self.num_of_col            = 0
        self.ROWMODE               = []
        self.Heder_Backgroun_Color = Heder_Backgroun_Color
        self.MaxRows               = 30
        self.Show_MaxRows          = 5
        with flx.Layout(style='overflow-x:scroll;') as self.table:
            self.Drow_window()
        self.set_Current_Highlite(self.Highlite)

    def Drow_window(self):
        with ui.VFix(spacing=1,style='background: white; border: 0px solid gray;') as self.content  :
            col_num=-1
            self.num_of_col  = len(self.items.keys())
            if self.num_of_col>0:
                self.num_of_rows = len(self.items[self.items.keys()[0]])

                self.Rows['heder']={}
                self.Rows['heder']['handle'] = flx.HFix(padding=3,spacing=3,style='overflow-y:scroll; ')
                with self.Rows['heder']['handle']:
                    for col in self.items.keys():
                        col_num = col_num+1
                        count=0
                        self.Rows['heder'][col_num] = flx.LineEdit(text=str(col),
                                                                    disabled=True,
                                                                    style='font-size: 120%; background: ' + self.Heder_Backgroun_Color  +'  ;color: blue;border-radius: 0px;max-height:35px;')

                    # flx.LineEdit(text='',
                    #             disabled=True,
                    #             style=' background: SeaShell ;color: blue;border-radius: 0px; max-height: 35px; max-width: 15px;')

                if self.num_of_rows>0:
                    if len(self.ROWMODE)!=self.num_of_rows:
                        self.ROWMODE=[0]*self.num_of_rows
                    if self.num_of_rows > self.MaxRows:
                        num_of_rows = self.Show_MaxRows
                    else:
                        num_of_rows = self.num_of_rows
                        
                    with flx.Layout(style='overflow-y:scroll; ') as self.ROW_LAYOUT:
                        for row_num in range(num_of_rows):
                            self.Rows[row_num]={}
                            self.Rows[row_num]['handle'] = flx.HFix(padding=3,spacing=3)
                            with self.Rows[row_num]['handle']:
                                col_num = -1
                                for col in self.items.keys():
                                    col_num = col_num+1
                                    if row_num!=self.Highlite:
                                        self.Rows[row_num][col_num] = flx.LineEdit(text=str(self.items[col][row_num]),
                                                                                      disabled=True,
                                                                                      style='background:white; color: ' +Text_COLORS[self.ROWMODE[row_num]]+ '; border-radius: 0px;max-height:30px;')
                                    else:
                                        self.Rows[row_num][col_num] = flx.LineEdit(text=str(self.items[col][row_num]),
                                                                                      disabled=True,
                                                                                      style='background: yellow;color: '+Text_COLORS[self.ROWMODE[row_num]]+ ';border-radius: 0px;max-height:30px;')
    @event.reaction('items','rowmode')
    def update_Data(self):
        self.ROWMODE  = self.rowmode
        if len(self.items.keys())>0:
            if (self.num_of_col !=len(self.items.keys())) or (self.num_of_rows !=len(self.items[self.items.keys()[0]])) :
                self.content.dispose()
                with self.table:
                    self.Drow_window()
            else:
                #self.Highlite=0
                self.Re_Drow_window()
        else:
            self.content.dispose()

    def Re_Drow_window(self):
        
        count=0
        if len(self.items[self.items.keys()[0]])> self.MaxRows:
            Extra = int(int(self.Highlite)/self.Show_MaxRows) * self.Show_MaxRows
        else:
            Extra = 0
        for row in self.Rows.keys():
            if row!='heder':
                if (int(row)+Extra)!=int(self.Highlite):
                    if (int(row)+Extra) >= self.num_of_rows:
                        for col in self.Rows[row].keys():
                            if col!='handle':
                                self.Rows[row][col].apply_style('background:white;')
                                self.Rows[row][col].set_text('')
                    else:
                        for col in self.Rows[row].keys():
                            if col!='handle':
                                self.Rows[row][col].apply_style('background:white; color: ' +Text_COLORS[self.ROWMODE[int(row)+Extra]]+ '; border-radius: 0px;max-height:30px;')
                                self.Rows[row][col].set_text(str(self.items[self.items.keys()[int(col)]][int(row)+Extra]) )
                        count=count+1
                else:
                    for col in self.Rows[row].keys():
                        if col!='handle':
                            self.Rows[row][col].apply_style('background: yellow;color:' +Text_COLORS[self.ROWMODE[int(row)+Extra]]+ ';border-radius: 0px;')
                            self.Rows[row][col].set_text(str(self.items[self.items.keys()[int(col)]][int(row)+Extra]))
                    count=count+1
    @flx.emitter
    def key_down(self, e):
        """Overload key_down emitter to prevent browser scroll."""
        ev = self._create_key_event(e)
        # print(ev.key)
        # if ev.key.startswith('Arrow'):
        #     e.preventDefault()
        return ev
    @flx.reaction('key_down')
    def _handle_highlighting(self, *events):
        for ev in events:
            # if ev.modifiers:
            #     continue
            if ev.key == 'ArrowDown':
                if (self.Highlite+1) < self.num_of_rows:
                    self.Highlite=self.Highlite+1
                    self.ROW_LAYOUT.node.scrollTop=self.ROW_LAYOUT.node.scrollTop+32
                    self.Re_Drow_window()
                    self.set_Current_Highlite(self.Highlite)
            elif ev.key == 'ArrowUp':
                if (self.Highlite-1) >= 0:
                    self.Highlite=self.Highlite-1
                    self.ROW_LAYOUT.node.scrollTop=self.ROW_LAYOUT.node.scrollTop-32
                    self.Re_Drow_window()
                    self.set_Current_Highlite(self.Highlite)
            elif ev.key == 'Enter':
                self.set_choice(self.Highlite)
                self.set_Current_Highlite(self.Highlite)
                return self.Highlite
            elif ev.key == 'Escape':
                return -2
    @flx.reaction('Current_Highlite')
    def update_Highlite(self):
        if self.Current_Highlite!=self.Highlite:
            self.Highlite=self.Current_Highlite

class nsfgm(flx.PyComponent):
    #  Main class for neatseq-flow Log file parser
    #Function for setting the main directory [the pipeline run location]
    Dir = event.StringProp('', settable=True)
    
    def init(self,directory,
                  Regular,        
                  Bar_Marker,     
                  Bar_Spacer ,    
                  Bar_len):

        # Store input parameters
        
        self.Regular         = Regular
        self.Bar_Marker      = Bar_Marker
        self.Bar_Spacer      = Bar_Spacer
        self.Bar_len         = Bar_len
        self.set_Dir(os.path.join(directory ,"logs"))

    #Function for gathering information about the available log files as Data-Frame
    def file_browser(self,Regular,q=None):
        try:
            file_sys=pd.DataFrame()
            # get the available log files names
            file_sys["Name"]=[x for x in os.listdir(self.Dir) if len(re.findall(Regular,x))]
            # get the available log files created times
            file_sys["Created"]=[datetime.fromtimestamp(os.path.getctime(os.path.join(self.Dir,x))).strftime('%d/%m/%Y %H:%M:%S') for x in file_sys["Name"]]
            # get the available log files last modified times
            file_sys["Last Modified"]=[os.path.getmtime(os.path.join(self.Dir,x)) for x in file_sys["Name"]]
            file_sys=file_sys.sort_values(by="Last Modified",ascending=False).reset_index(drop=True).copy()
            file_sys["Last Modified"]=[datetime.fromtimestamp(x).strftime('%d/%m/%Y %H:%M:%S') for x in file_sys["Last Modified"]]
            # get the available log files sizes
            file_sys["Size"]=[os.path.getsize(os.path.join(self.Dir,x)) for x in file_sys["Name"]]

        except :
            file_sys=pd.DataFrame(columns=["Name","Created","Last Modified","Size"])
        if q!=None:
           q.put({'items':file_sys.to_dict('list'),'rowmode': len(file_sys)})
        return {'items':file_sys.to_dict('list'),'rowmode': len(file_sys)}

    #Function for getting information from qstat
    def get_qstat(self):
        import subprocess
        qstat=pd.DataFrame()
        # run qstat and get running information in xml format
        if subprocess.call('type qstat', shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
            #xml = os.popen('qstat -xml -u $USER').read()
            xml = os.popen('qstat -xml ').read()
            # extract the jobs names
            qstat["Job name"]=[re.sub("[</]+JB_name>","",x) for x in re.findall('[</]+JB_name>\S+',xml)]
            # extract the jobs status
            qstat["State"]=[x.strip('job_list state="') for x in re.findall('job_list state="\w+',xml)]
        return qstat

    #Function for getting PID information
    def get_PID(self):
        PID=pd.DataFrame()
        PID["Job ID"]   = list(map(lambda x: str(int(x.strip('\n'))),os.popen('ps -ae -o pid=').readlines()))
        PID["PID_State"] = 'running'
        return PID

    # function for generating the progress bar
    def gen_bar(self,Bar_len,Bar_Marker,Bar_Spacer):
        char_value=float(self.logpiv["Finished"].max().total_seconds())/Bar_len
        if char_value==0:
            char_value=1.0/Bar_len
        return [char_value,list(map(lambda x,y: (int(x.total_seconds()/char_value)*Bar_Spacer + ((int(-(-(y.total_seconds()-x.total_seconds())/char_value))+1)*Bar_Marker)).ljust(Bar_len,Bar_Spacer)  ,self.logpiv["Started"],self.logpiv["Finished"]))]

    # main function for parsing log file
    def read_run_log(self,runlog_file,Bar_len,Bar_Marker,Bar_Spacer,q=None,Instance=True,read_from_disk=True):

        try:
            # read log file to a Data-Frame
            if read_from_disk:
                runlog_Data=pd.read_table(runlog_file,header =4,dtype={'Job ID':str})
                self.LogData=runlog_Data.copy()
            else:
                runlog_Data=self.LogData.copy()
            # If there is a level column: Remove information about high level scripts runs
            if "Level" in runlog_Data.columns:
                runlog_Data=runlog_Data.loc[runlog_Data["Level"]=="low",]
            # If there is a Status column: Convert to OK or ERROR
            if "Status" in runlog_Data.columns:
                runlog_Data['Status']=['OK' if 'OK' in x else 'ERROR' for x in runlog_Data['Status']]
            # Format the Timestamp column
            runlog_Data.Timestamp = [datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in runlog_Data.Timestamp]
            runlog_Data['Timestamp2'] = [int(time.mktime(x.timetuple())) for x in runlog_Data.Timestamp]
            # sort the Data-Frame according to the Timestamp column
            runlog_Data=runlog_Data.sort_values(by="Timestamp2",ascending=True).reset_index(drop=True).copy()
            # remove old runs [duplicated jobs names events]
            runlog_Data.drop_duplicates(keep="last",subset=["Job name","Event"],inplace=True)
            # if after the remove duplicated there are old finished jobs of new runs: remove the finished time of these jobs
            args_pivot=['Job name','Event','Timestamp']
            pre_logpiv = runlog_Data.pivot(index=args_pivot[0], columns=args_pivot[1], values=args_pivot[2])

            if "Finished" in pre_logpiv.columns:
                pre_logpiv=pre_logpiv.loc[~pre_logpiv["Finished"].isnull(),]
                log=list(map( lambda x,y: (x in pre_logpiv[pre_logpiv["Finished"]<pre_logpiv["Started"]].index)&(y=="Finished")==False , runlog_Data["Job name"],runlog_Data["Event"] ))
                runlog_Data=runlog_Data[log].copy()

            # for the main window information:
            if Instance==True:
                args_pivot=['Instance','Event','Timestamp']
            # for the sample window information:
            else:
                # get the running information from qstat
                qstat=self.get_qstat()
                if len(qstat)>0:
                    runlog_Data=runlog_Data.merge(qstat,how='left')
                    runlog_Data.loc[runlog_Data["State"].isnull(),"State"]=''
                else:
                    runlog_Data["State"]=''

                if 'Job ID' in runlog_Data.columns:
                    if len(set(runlog_Data["Host"]))==1:
                        if list(set(runlog_Data["Host"]))[0]==LOCAL_HOST+"-LOCAL_RUN":
                            PID = self.get_PID()
                            if len(PID)>0:
                                runlog_Data = runlog_Data.merge(PID,how='left',on='Job ID')
                                runlog_Data.loc[~runlog_Data["PID_State"].isnull(),"State"]='running'
                                runlog_Data = runlog_Data.drop('PID_State',axis=1)

                # get only the data for the chosen step
                runlog_Data=runlog_Data.loc[runlog_Data["Instance"]==Instance,].copy()
                # change the names of the jobs to the samples names
                runlog_Data['Job name']=list(map(lambda x,y,z: re.sub("^"+y+jid_name_sep+z+jid_name_sep,"",re.sub(jid_name_sep+"[0-9]+$","",x)) ,runlog_Data['Job name'],runlog_Data['Module'],runlog_Data['Instance'] ))
                args_pivot=['Job name','Event','Timestamp']

                # generate a pivot table
                logpiv = runlog_Data.pivot(index=args_pivot[0], columns=args_pivot[1], values=args_pivot[2])
                # make sure the Finished column exist
                if "Finished" not in logpiv.columns:
                      logpiv["Finished"]=''
                # convert Nan to empty sring
                #logpiv[logpiv.isnull()]=''
                logpiv=logpiv.sort_values("Finished")

                # generate the items Data-Frame
                self.items=pd.DataFrame()
                self.items['Samples']=[str(x) for x in logpiv.index.values]
                self.items['Started']=[str(x) for x in logpiv['Started']]
                self.items['Finished']=[str(x) if str(x)!="NaT" else '' for x in logpiv['Finished']]
                self.items['Host']=[str(list(runlog_Data.loc[runlog_Data['Job name']==x,'Host'])[0]) for x in logpiv.index.values]
                #self.items['Memory']=[str(max(list(runlog_Data.loc[runlog_Data['Job name']==x,'Max mem']))) for x in logpiv.index.values]
                self.items['Running?']=[str(list(runlog_Data.loc[runlog_Data['Job name']==x,'State'])[0]) for x in logpiv.index.values]

                #mark un-Finished samples
                self.rowmode=[2 if x =='' else 1 for x in self.items['Finished']]
                self.rowmode=list(map(lambda x,y: 3 if len(y)>0  else x,self.rowmode,self.items['Running?']))
                self.items['Running?']=[x  if len(x)>0  else "No" for x in self.items['Running?']]

                # If there is a Status column: Display the samples status
                if "Status" in runlog_Data.columns:
                    self.items['Status']=[str(list(runlog_Data.loc[(runlog_Data['Job name']==x)&(runlog_Data['Event']=='Finished'),'Status'])).replace('[','').replace(']','').replace("'",'') for x in logpiv.index.values]
                    #mark samples with ERRORs
                    self.rowmode=list(map(lambda x,y: 2 if 'ERROR' in x else y, self.items['Status'],self.rowmode))

                if q!=None:
                    q.put({'items':self.items.to_dict('list'),'rowmode': self.rowmode})
                return {'items':self.items.to_dict('list'),'rowmode': self.rowmode}
            # group all jobs by Instance and event to lists of Timestamps
            logpiv=runlog_Data.groupby([args_pivot[0],args_pivot[1]])[args_pivot[2]].apply(list).reset_index()
            # generate a pivot table
            logpiv = logpiv.pivot(index=args_pivot[0], columns=args_pivot[1], values=args_pivot[2])
            # make sure the Finished column exist
            if "Finished" not in logpiv.columns:
                logpiv["Finished"]=''
            # convert Nan to empty sring
            logpiv[logpiv.isnull()]=''
            # make a copy of the Finished column
            logpiv["temp_Finished"]=logpiv["Finished"]
            # count how many jobs started
            N_Started=logpiv.applymap(lambda x:len(x))["Started"]
            # count how many jobs Finished
            N_Finished=logpiv.applymap(lambda x:len(x))["Finished"]

            # get the running information from qstat and add the information to the Data-Frame
            qstat=self.get_qstat()
            if len(qstat)>0:
                runlog_Data=runlog_Data.merge(qstat,how='left')
                runlog_Data.loc[runlog_Data["State"].isnull(),"State"]=''
            else:
                runlog_Data["State"]=''


            if 'Job ID' in runlog_Data.columns:
                if len(set(runlog_Data["Host"]))==1:
                    if list(set(runlog_Data["Host"]))[0]==LOCAL_HOST+"-LOCAL_RUN":
                        PID = self.get_PID()
                        if len(PID)>0:
                            runlog_Data = runlog_Data.merge(PID,how='left',on='Job ID')
                            runlog_Data.loc[~runlog_Data["PID_State"].isnull(),"State"]='running'
                            runlog_Data = runlog_Data.drop('PID_State',axis=1)

            logpiv=logpiv.join(runlog_Data.groupby("Instance")["State"].apply(lambda x:list(x).count("running")),how="left", rsuffix='running')

            # set the Timestamps of instances with no Finished jobs and are still running to the current time [for calculating the progress bar]
            logpiv["Finished"]=list(map(lambda x,y,z: {datetime.strptime(str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')), '%d/%m/%Y %H:%M:%S')} if (x=='')&(y>0) else z if (x=='') else x ,logpiv["Finished"],logpiv["State"].values,logpiv["Started"] ))
            #logpiv.loc[logpiv["Finished"]=='',"Finished"]={datetime.strptime(str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')), '%d/%m/%Y %H:%M:%S')}
            # find the earliest Timestamps of every instances
            Started=[min(x) for x in logpiv["Started"]]
            # find the latest Timestamps of every instances
            Finished=[max(x) for x in logpiv["Finished"]]
            # Add the new information in the pivot table
            logpiv["Started"]=Started
            logpiv["Finished"]=Finished
            logpiv["#Started"]=N_Started
            logpiv["#Finished"]=N_Finished
            # sort the pivot table by the earliest Timestamps
            logpiv=logpiv.sort_values("Started")
            # calculate the total time for each instances
            logpiv_diff=pd.DataFrame()
            logpiv_diff["Started"]=logpiv["Started"]-logpiv["Started"].min()
            logpiv_diff["Finished"]=logpiv["Finished"]-logpiv["Started"].min()
            self.logpiv=logpiv_diff
            # generate the progress bar column
            [char_value,bar]=self.gen_bar(Bar_len,Bar_Marker,Bar_Spacer)
            Runs_str="Progress #=" + str(char_value)+"seconds"
            # generate the items Data-Frame to show in the window
            self.items =pd.DataFrame()
            # # Make sure the instances names are no longer then 20 chars
            # self.items["Steps"]=map(lambda x:x[:20],logpiv.index.values)
            self.items["Steps"]=[x for x in logpiv.index.values]
            self.items[Runs_str]=bar
            self.items["Started"]=[str(x) for x in logpiv["Started"]]
            # Show the finished Timestamps for only instances with finished jobs
            self.items["Finished"]=list(map(lambda x,y: str(x) if y!='' else '',logpiv["Finished"],logpiv["temp_Finished"]))
            self.items["#Started"]=[str(x) for x in logpiv["#Started"]]
            self.items["#Finished"]=[str(x) for x in logpiv["#Finished"]]
            self.items["#Running"]=logpiv["State"].values

            # Set the lines colour mode
            self.rowmode=logpiv["#Started"]-logpiv["#Finished"]
            self.rowmode=[5 if x > 0 else 1 for x in self.rowmode]
            self.rowmode=list(map(lambda x,y: 3 if (y >0)&(x>=2) else x,self.rowmode, self.items["#Running"]))

            # If there is a Status column: Display the steps status error count
            if "Status" in runlog_Data.columns:
                logpiv=logpiv.join(runlog_Data.groupby("Instance")["Status"].apply(lambda x:list(x).count("ERROR")),how="left", rsuffix='ERROR')
                self.items["#ERRORs"]=logpiv["Status"].values
                self.rowmode=list(map(lambda x,y: 2 if x>0 else y, self.items["#ERRORs"],self.rowmode))

        except :# ValueError: #IOError:
            if Instance==True:
                self.items=pd.DataFrame(columns=["Steps","Progress","Started","Finished","#Started","#Finished","#Running"])
            else:
                self.items=pd.DataFrame(columns=["Samples","Started","Finished","Host","Memory","Running?"])

            self.rowmode=[]

        # if this function is running in a sub-process store the results in the queue
        if q!=None:
           q.put({'items':self.items.to_dict('list'),'rowmode': self.rowmode})
        return {'items':self.items.to_dict('list'),'rowmode': self.rowmode}

class Relay_log_files(flx.PyComponent):

    def init(self,mynsfgm,Table_H,refreshrate=1):
        self.q           = Queue()
        self.running     = False
        self.mynsfgm     = mynsfgm
        self.Table_H     = Table_H
        self.refreshrate = refreshrate
        self.Refresh_log_files()

    def Refresh_log_files(self):
        if not self.running:
            self.Process = Process(target=self.mynsfgm.file_browser, args=(self.mynsfgm.Regular,self.q))
            self.Process.start()
            self.running=True
        elif self.q.empty()==False:
            log=self.q.get(True)
            self.Process.join()
            self.running=False
            self.Table_H.set_items(log['items'])
            self.Table_H.set_rowmode([1]*log['rowmode'])
        if self.session.status:
            asyncio.get_event_loop().call_later(self.refreshrate, self.Refresh_log_files)
        else:
            if self.Process.is_alive():
                self.q.get(True)
                self.Process.join()

class Relay_main_menu(flx.PyComponent):
    runlog_file   = event.StringProp('', settable=True)

    def init(self,mynsfgm,Table_H,refreshrate=1):
        self.q           = Queue()
        self.running     = False
        self.mynsfgm     = mynsfgm
        self.Table_H     = Table_H
        self.refreshrate = refreshrate
        self.Refresh_main_menu()

    def Refresh_main_menu(self):
        if not self.running:
            self.Process = Process(target=self.mynsfgm.read_run_log, args=(self.runlog_file,
                                                                           self.mynsfgm.Bar_len,
                                                                           self.mynsfgm.Bar_Marker,
                                                                           self.mynsfgm.Bar_Spacer,
                                                                           self.q))
            self.Process.start()
            self.running=True
        elif self.q.empty()==False:
            steps=self.q.get(True)
            self.Process.join()
            self.running=False
            self.Table_H.set_items(steps['items'])
            self.Table_H.set_rowmode(steps['rowmode'])
        if self.session.status:
            asyncio.get_event_loop().call_later(self.refreshrate, self.Refresh_main_menu)
        else:
            if self.Process.is_alive():
                self.q.get(True)
                self.Process.join()
            
class Relay_sample_menu(flx.PyComponent):
    instances   = event.StringProp('', settable=True)
    runlog_file = event.StringProp('', settable=True)

    def init(self,mynsfgm,Table_H,refreshrate=1):
        self.q           = Queue()
        self.running     = False
        self.mynsfgm     = mynsfgm
        self.Table_H     = Table_H
        self.refreshrate = refreshrate
        self.Refresh_sample_menu()

    def Refresh_sample_menu(self):
        if not self.running:
            self.Process = Process(target=self.mynsfgm.read_run_log, args=(self.runlog_file,
                                                                           self.mynsfgm.Bar_len,
                                                                           self.mynsfgm.Bar_Marker,
                                                                           self.mynsfgm.Bar_Spacer,
                                                                           self.q,
                                                                           self.instances))
            self.Process.start()
            self.running=True
        elif self.q.empty()==False:
            steps=self.q.get(True)
            self.Process.join()
            self.running=False
            self.Table_H.set_items(steps['items'])
            self.Table_H.set_rowmode(steps['rowmode'])
        if self.session.status:
            asyncio.get_event_loop().call_later(self.refreshrate, self.Refresh_sample_menu)
        else:
            if self.Process.is_alive():
                self.q.get(True)
                self.Process.join()

class Monitor_GUI(flx.PyComponent):
    Dir = event.StringProp('', settable=True)
    #main program
    def init(self,directory         = os.getcwd(),
                  Regular           = "log_[0-9]+.txt$",
                  Monitor_RF        = 1,
                  File_browser_RF   = 2,
                  Sample_RF         = 3,
                  Bar_Marker        = '#',
                  Bar_Spacer        = ' ',
                  Bar_len           = 40 ):
                  
        sample_menu_flag=-1
        sample_menu_active=False
        #initializing the main monitor/qstat log file parser module
        self.mynsfgm = nsfgm(directory,
                             Regular,           
                             Bar_Marker,        
                             Bar_Spacer ,       
                             Bar_len)

        #initializing file browser window
        with flx.VSplit(padding=20,spacing=20,style='background: white;'):
            self.file_menu   = Table(0,title='Log File Menu',style='font-size: 70%;')
            self.main_menu   = Table(0,'LightSteelBlue',title='Steps Menu',style='font-size: 70%;')
            self.sample_menu = Table(0,'NavajoWhite',title='Samples Menu',style='font-size: 70%;')
        #get list of log files and information about them
        #with self:
        self.Relay_log    = Relay_log_files(self.mynsfgm,
                                            self.file_menu,
                                            File_browser_RF)
        self.Relay_main   = Relay_main_menu(self.mynsfgm,
                                            self.main_menu,
                                            Monitor_RF)
        self.Relay_sample = Relay_sample_menu(self.mynsfgm,
                                              self.sample_menu,
                                              Sample_RF)


    @event.reaction('Dir')
    def Update_Dir(self, *events):
        for ev in events:
            if ev.new_value!='':
                self.mynsfgm.set_Dir(os.path.join(ev.new_value,"logs"))
        
    @event.reaction('file_menu.Current_Highlite','file_menu.choice')
    def choose_log_file(self, *events):
        for ev in events:
            try:
                if 'Name' in ev.source.items.keys():
                    runlog_file = os.path.join(self.mynsfgm.Dir,ev.source.items['Name'][ev.new_value])
                else:
                    runlog_file = ''
            except :
                    runlog_file = ''
            self.Relay_main.set_runlog_file(runlog_file)
            self.main_menu.set_Current_Highlite(0)
            self.Relay_sample.set_runlog_file('')

    # @event.reaction('file_menu.Current_Highlite')
    # def choose_log_file_control(self, *events):
    #     for ev in events:
    #         if ev.new_value!=self.file_menu.choice:
    #             self.Relay_main.set_runlog_file('None')

    @event.reaction('main_menu.Current_Highlite','main_menu.choice')
    def choose_step_file(self, *events):
        for ev in events:
            try:
                if 'Steps' in ev.source.items.keys():
                    instances=ev.source.items['Steps'][ev.new_value]
                else:
                    instances = ''
            except :
                    instances = ''
            self.Relay_sample.set_instances(instances)
            self.Relay_sample.set_runlog_file(self.Relay_main.runlog_file)

    # @event.reaction('main_menu.Current_Highlite')
    # def choose_step_file_control(self, *events):
    #     for ev in events:
    #         if ev.new_value!=self.main_menu.choice:
    #             self.Relay_sample.set_instances('None')
    #             self.Relay_sample.set_runlog_file('None')

if __name__ == '__main__':
    #getting arguments from the user
    parser = argparse.ArgumentParser(description='Neatseq-flow Monitor By Liron Levin ')
    parser.add_argument('-D', dest='directory',metavar="STR", type=str,default=os.getcwd(),
                        help='Neatseq-flow project directory [default=cwd]')
    parser.add_argument('-R', dest='Regular',metavar="STR" , type=str,default="log_[0-9]+.txt$",
                        help='Log file Regular Expression [in ./logs/ ] [default=log_[0-9]+.txt$]')
    parser.add_argument('--Monitor_RF',metavar="FLOAT", type=float,dest='Monitor_RF',default=1,
                        help='Steps Monitor Refresh rate [default=1]')
    parser.add_argument('--File_browser_RF',metavar="FLOAT", type=float,dest='File_browser_RF',default=2,
                        help='File Browser Refresh rate [default=2]')
    parser.add_argument('--Sample_RF',metavar="FLOAT", type=float,dest='Sample_RF',default=3,
                        help='Samples Browser Refresh rate [default=3]')
    parser.add_argument('--Bar_Marker',metavar="CHAR",type=str,dest='Bar_Marker',default="#",
                        help='Progress Bar Marker [default=#]')
    parser.add_argument('--Bar_Spacer',metavar="CHAR",type=str,dest='Bar_Spacer',default=" ",
                        help='Progress Bar Spacer [default=Space]')
    parser.add_argument('--Bar_len',metavar="INT",type=int,dest='Bar_len',default=40,
                        help='Progress Bar Total Length [in chars] [default=40]')
    parser.add_argument('--Server',dest='Server',action='store_true',
                        help='Run as Server')
    args = parser.parse_args()
    if args.Server:
        import socket
        m = app.App(Monitor_GUI,
                    args.directory,
                    args.Regular,
                    args.Monitor_RF,
                    args.File_browser_RF,
                    args.Sample_RF,
                    args.Bar_Marker,
                    args.Bar_Spacer,
                    args.Bar_len)
        app.create_server(host=socket.gethostbyname(socket.gethostname()))
        m.serve('')
        flx.start()
    else:
        m = app.App(Monitor_GUI)
        app.run()
    

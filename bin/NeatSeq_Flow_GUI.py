#!/usr/bin/env python

__author__ = "Liron Levin"
__version__ = "3.0"


__affiliation__ = "Bioinformatics Core Unit, NIBN, Ben Gurion University"



from flexx import app, event, ui, flx 
from pscript import RawJS
import os,sys,dialite
from collections import OrderedDict
import asyncio
import signal
from multiprocessing import Process, Queue

sys.path.append(os.path.realpath(os.path.expanduser(os.path.dirname(os.path.abspath(__file__))+os.sep+"..")))

keep_runing            = True

Title                  = 'NeatSeq-Flow'

ICON                   = ''

NeatSeq_Flow_Conda_env = 'NeatSeq_Flow'

CONDA_BIN              = ''

Base_Help_URL          = 'https://neatseq-flow.readthedocs.io/projects/neatseq-flow-modules/en/latest/'

MODULES_TEMPLATES_FILE = 'https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/neatseq_flow_gui/TEMPLATES/MODULES_TEMPLATES.yaml'

SERVE                  = False

LOCK_USER_DIR          = True

STEPS                  = {'Import': {'module': 'Import', 'script_path': None  },

                        }

COLORS                 = ('#EF9A9A','#B2EBF2','#FFECB3',
                          '#E1BEE7','#C5CAE9','#C8E6C9',
                          '#B3E5FC','#F8BBD0','#4DD0E1',
                          '#B2DFDB','#DCEDC8','#F0F4C3',
                          '#FFF9C4','#D1C4E9','#FFE0B2',
                          '#FFCCBC','#BBDEFB','#F06292'
                                                  
                   
                         )

COLOR_BY               = ['module','tag','scope']

CLUSTER                = {'Executor': 'SGE',
           'Default_wait': '10',
           'Qsub_opts': '-cwd',
           'Qsub_path': '/storage/SGE6U8/bin/lx24-amd64',
           'Qsub_q': 'fairshare.q,intel_all.q',
           'module_path': '/path/to/modules',
           'conda': {'path': '{Vars.conda.base}', 'env': '{Vars.conda.env}' }
           }

VARS                   = {'Programs': {},
        'Genome': {},
        'conda': {'base': None, 'env': 'base' }
        }

Executor               = ['SGE', 'SLURM','PBS', 'Local']

MODULES_TEMPLATES      = {'Basic': {'Basic_New_Step': {'base': None, 'module': None, 'script_path': None, }}

                     }

MODULE_INFO            = {}

DEFAULT_HELP_BOX_TEXT  = '''This is the Help Box!
======================
Information about modules and module's options will be displayed here.
-
'''

FILE_TYPES             = ['Single', 'Forward', 'Reverse', 'Nucleotide', 'Protein', 'SAM', 'BAM', 'REFERENCE', 'VCF', 'G.VCF','genes.counts','HTSeq.counts','results']

FILE_TYPES_SLOTS       = ['fastq.S', 'fastq.F', 'fastq.R', 'fasta.nucl', 'fasta.prot', 'sam', 'bam', 'reference', 'vcf', 'g.vcf']

FIELDS2SPLIT           = ['base']

Documentation          = '''
WorkFlow's Documentation
=========================
Here you can document your workflow and add notes.
---------------------------------------------------
* **important:**

    1.  **DON'T** use the hash **#** symbol!!!
        2. Don't forget to **save** the workflow at the Design tab!!!
'''

html_cite              = '''
    <p class=MsoNormal dir=LTR style='color:CadetBlue;margin-top:0cm;margin-bottom:0cm;margin-bottom:.0000pt;
    text-align:left;line-height:normal;direction:ltr;unicode-bidi:embed'><b>NeatSeq-Flow
    was Created by the Bioinformatics Core Facility at the Ben Gurion University, Israel</b><br>
    <span style='font-size:10.0pt'>If you are using NeatSeq-Flow, please cite:</span></p>

    <p class=MsoNormal dir=LTR style='margin-top:0cm;margin-right:0cm;margin-bottom:
    0cm;margin-left:36.0pt;margin-bottom:.0001pt;text-align:left;line-height:normal;
    direction:ltr;unicode-bidi:embed'><b><span style='font-size:10.0pt'>NeatSeq-Flow:
    A Lightweight High Throughput Sequencing Workflow Platform for Non-Programmers
    and Programmers alike. </span></b></p>

    <p class=MsoNormal dir=LTR style='margin-top:0cm;margin-right:0cm;margin-bottom:
    0cm;margin-left:36.0pt;margin-bottom:.0001pt;text-align:left;line-height:normal;
    direction:ltr;unicode-bidi:embed'><span style='font-size:9.0pt'>Menachem Y.
    Sklarz, Liron Levin, Michal Gordon, Vered Chalifa-Caspi<br>
    doi: https://doi.org/10.1101/173005</span></p>
      '''

TOOLTIP                = True

HELP                   = {'login'             :'Click to Log-in',
                          
                          'order_steps'       :'Click to Re-Order the Steps in the Steps Tree to their Hierarchical Order at the Work-Flow',
                          'step_dropdown'     :'Choose a Step Template to be Added to the Work-Flow.',
                          'about'             :'Select a Template Step at the Drop-Down Menu on the Left and Click Here to See Information About it',
                          'add_step'          :'Select a Template Step at the Drop-Down Menu on the Left and Click Here to Add it to the Work-Flow',
                          'load_step'         :'Click to Choose a Step File to be Added to the Work-Flow',
                          'color_steps_by'    :'Choose How to Color the Steps in the Work-Flow',
                          'load_workflow'     :'Click to Choose a Work-Flow Parameter File to be Loaded',
                          'save_workflow'     :'Click to Choose a Location and a File Name to Save The Work-Flow as a Parameter File',
                          'apply'             :'Click to Set the Values Entered/Changed in the Step Editing Panel',
                          'new'               :'Click to Create a New Sub Option. Make Sure You select a Field in the Tree Options Below',
                          'browse'            :'Click to Choose a File Path to Add to the Value Field',
                          'duplicate'         :'Click to Duplicate the Selected Field in the Tree Options Below. It is Possible to Duplicate a Step by Selecting the Step`s Name',
                          'remove'            :'Click to Remove the Selected Field in the Tree Options Below. It is Possible to Remove a Step by Selecting the Step`s Name',
                          'export'            :'Click to Export a Selected Step to a File. Select the Step`s Name You Want to Export in the Tree Options Below',
                          'options_dropdown'  :'Choose an Option that can be Added to the Option Value Field. The Options Depend on the Selected Field in the Tree Options Below',
                          'add'               :'Click to Add the Option Selected at the Above Drop-Down Menu to the Value Field',
                          
                          'load_sample_file'  :'Click to Choose a Sample File to be Loaded',
                          'save_sample_file'  :'Click to Choose a Location and a File Name to Save The Sample File',
                          'select_s_files'    :'Click to Choose and Add Sample Level Files',
                          'select_p_files'    :'Click to Choose and Add Project Level Files',
                          
                          'cite'              :'Click to See How to Cite NeatSeq-Flow'
                         }

Download_FileName      = 'Download_File'

Download_Size_Limit    = 150 # in MB

Download_TimeOut       = 30

Preview_Buffer         = 10000

COMMAND_TIME_OUT       = 10000

Process_Runing = {}

def tracefunc(frame, event, arg, indent=[0]):
    if os.path.basename(__file__) != os.path.basename(frame.f_code.co_filename):
        if event == "call":
          indent[0] += 2
          print("-" * indent[0] + "> call function", frame.f_code.co_name)
        elif event == "return":
          print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
          indent[0] -= 2
        return tracefunc

# Associate CodeMirror's assets with this module so that Flexx will load
# them when (things from) this module is used.

try:
    base_url =  os.path.join(os.path.realpath(os.path.expanduser(os.path.dirname(os.path.abspath(__file__))+os.sep+"..")),'neatseq_flow_gui','Codemirror')
    flx.assets.associate_asset(__name__,'codemirror.css'    ,open(os.path.join(base_url ,'codemirror.css'), encoding="utf-8").read())
    flx.assets.associate_asset(__name__,'codemirror.js'     ,open(os.path.join(base_url ,'codemirror.js'), encoding="utf-8").read())
    flx.assets.associate_asset(__name__,'markdown.js'       ,open(os.path.join(base_url ,'mode/markdown/markdown.js'), encoding="utf-8").read())
    flx.assets.associate_asset(__name__,'yaml.js'           ,open(os.path.join(base_url ,'mode/yaml/yaml.js'), encoding="utf-8").read())
    flx.assets.associate_asset(__name__,'solarized.css'     ,open(os.path.join(base_url ,'theme/solarized.css'), encoding="utf-8").read())
    flx.assets.associate_asset(__name__,'active-line.js'    ,open(os.path.join(base_url ,'addon/selection/active-line.js'), encoding="utf-8").read())
    flx.assets.associate_asset(__name__,'matchbrackets.js'  ,open(os.path.join(base_url ,'addon/edit/matchbrackets.js'), encoding="utf-8").read())
    flx.assets.associate_asset(__name__,'continuelist.js'   ,open(os.path.join(base_url ,'addon/edit/continuelist.js'), encoding="utf-8").read())
except :
    base_url = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.46.0/'
    flx.assets.associate_asset(__name__, base_url + 'codemirror.css')
    flx.assets.associate_asset(__name__, base_url + 'codemirror.js')
    flx.assets.associate_asset(__name__, base_url + 'mode/markdown/markdown.js')
    flx.assets.associate_asset(__name__, base_url + 'mode/yaml/yaml.js')
    flx.assets.associate_asset(__name__, base_url + 'theme/solarized.css')
    flx.assets.associate_asset(__name__, base_url + 'addon/selection/active-line.js')
    flx.assets.associate_asset(__name__, base_url + 'addon/edit/matchbrackets.js')
    flx.assets.associate_asset(__name__, base_url + 'addon/edit/continuelist.js')

try:
    base_url =  os.path.join(os.path.realpath(os.path.expanduser(os.path.dirname(os.path.abspath(__file__))+os.sep+"..")),'neatseq_flow_gui','ToolTip')
    flx.assets.associate_asset(__name__,'jquery.min.js'     ,open(os.path.join(base_url ,'jquery.min.js'), encoding="utf-8").read())
    flx.assets.associate_asset(__name__,'bootstrap.min.js'  ,open(os.path.join(base_url ,'bootstrap.min.js'), encoding="utf-8").read())
    #flx.assets.associate_asset(__name__,"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css")
except:
    TOOLTIP = False

class Add_Tooltip(app.JsComponent):
    CSS = '''
                 
    .tooltip{position:absolute;
            z-index:1070;
            display:block;
            font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;
            font-style:normal;
            font-weight:400;
            line-height:1.42857143;
            line-break:auto;
            text-align:left;
            text-align:start;
            text-decoration:none;
            text-shadow:none;
            text-transform:none;
            letter-spacing:normal;
            word-break:normal;
            word-spacing:normal;
            word-wrap:normal;
            white-space:normal;
            font-size:18px;
            filter:alpha(opacity=0);
            opacity:0}.tooltip.in{
            filter:alpha(opacity=90);
            opacity:.9
            }
    .tooltip.top{
            padding:5px 0;
            margin-top:-3px
            }
    .tooltip.right{
            padding:0 5px;
            margin-left:3px
            }
    .tooltip.bottom{
            padding:5px 0;
            margin-top:3px
            }
    .tooltip.left{
            padding:0 5px;
            margin-left:-3px
            }
    .tooltip.top .tooltip-arrow{
            bottom:0;
            left:50%;
            margin-left:-5px;
            border-width:5px 5px 0;
            border-top-color:#000
            }
    .tooltip.top-left .tooltip-arrow{
            right:5px;
            bottom:0;
            margin-bottom:-5px;
            border-width:5px 5px 0;
            border-top-color:#000
            }
    .tooltip.top-right .tooltip-arrow{
            bottom:0;
            left:5px;
            margin-bottom:-5px;
            border-width:5px 5px 0;
            border-top-color:#000
            }
    .tooltip.right .tooltip-arrow{
            top:50%;
            left:0;
            margin-top:-5px;
            border-width:5px 5px 5px 0;
            border-right-color:#000
            }
    .tooltip.left .tooltip-arrow{
            top:50%;
            right:0;
            margin-top:-5px;
            border-width:5px 0 5px 5px;
            border-left-color:#000
            }
    .tooltip.bottom .tooltip-arrow{
            top:0;
            left:50%;
            margin-left:-5px;
            border-width:0 5px 5px;
            border-bottom-color:#000
            }
    .tooltip.bottom-left .tooltip-arrow{
            top:0;
            right:5px;
            margin-top:-5px;
            border-width:0 5px 5px;
            border-bottom-color:#000
            }
    .tooltip.bottom-right .tooltip-arrow{
            top:0;
            left:5px;
            margin-top:-5px;
            border-width:0 5px 5px;
            border-bottom-color:#000
            }
    .tooltip-inner{
            max-width:200px;
            padding:3px 8px;
            color:#fff;
            text-align:center;
            background-color:#000;
            border: 2px solid orange;
            border-radius:4px;
            opacity:1
            }
    .tooltip-arrow{
            position:absolute;
            width:0;
            height:0;
            border-color:transparent;
            border-style:solid
            }
        
    '''
    def init(self,element,help,placement='auto'):
        if TOOLTIP:
            # global window
            RawJS('''
                    $(document).ready(function(){
                    $('[data-toggle="tooltip"]').tooltip({html: true});
                    });
                    ''')
            node  = element.node
            node.setAttribute('data-container',"body")
            node.setAttribute('data-toggle',"tooltip")
            node.setAttribute('data-placement',placement)
            node.setAttribute('title',help)
        else:
            pass

class Graphical_panel(ui.CanvasWidget):
    Selected_step    = event.StringProp('', settable=True)
    Steps_Data       = event.DictProp(STEPS, settable=True)
    refresh_flag     = event.BoolProp(False, settable=True)
    Step_Colors      = event.DictProp({}, settable=True)
    color_by_option  = event.StringProp('', settable=True)
    Steps_Order      = event.DictProp({},settable=True)

    def init(self):
        super().init()
        self.new_size = None
        self.ctx = self.node.getContext('2d')
        # Set mouse capturing mode
        self.set_capture_mouse(2)
        self.set_Step_Colors({})
        self.Button_list = []
        self.Button_count = 0
        self.steps = self.Steps_Data
        self.calculate_steps_conections()
        if len(self.steps.keys()) > 0:
            for step in self.steps.keys():
                if 'SKIP' in self.steps[step].keys():
                    self.create_Button(step, self, [50, 50],'gray')
                else:
                    if self.color_by_option in self.steps[step].keys():
                        if self.steps[step][self.color_by_option]!=None:
                            if self.steps[step][self.color_by_option] not in self.Step_Colors.keys():
                                 self.Step_Colors[self.steps[step][self.color_by_option]] = COLORS[len(self.Step_Colors.keys())]
                            self.create_Button(step, self, [50, 50],self.Step_Colors[self.steps[step][self.color_by_option]])
                        else:
                            self.create_Button(step, self, [50, 50])
                    else:
                        self.create_Button(step, self, [50, 50])

    @event.reaction('color_by_option')
    def change_step_colors(self, *events):
        for Button_id in self.Button_list:
            getattr(self, Button_id).dispose()
        if len(self.steps.keys()) > 0:
            self.init()
            self.set_refresh_flag(True)
        else:
            self.Button_list = []
            self.Button_count = 0

    def get_Button_by_name(self, name):
        Button = None
        for Button_id in self.Button_list:
            Button = getattr(self, Button_id)
            if Button.text == name:
                break
        return Button

    @event.reaction('Steps_Data')
    def if_step_chaned(self, *events):
        for ev in events:
            if ev.new_value:
                # self.steps = self.Steps_Data
                for Button_id in self.Button_list:
                    getattr(self, Button_id).dispose()
                if len(self.steps.keys()) > 0:
                    self.init()
                    self.set_refresh_flag(True)
                else:
                    self.Button_list = []
                    self.Button_count = 0

    @event.reaction('refresh_flag')
    def do_updeate(self, *events):
        for ev in events:
            self.order_Buttons()
            self.update()
            self.set_refresh_flag(False)

    @event.reaction
    def order_Buttons(self):
        if len(self.steps.keys()) > 0:
            self.calculate_steps_conections()
            levels = max(self.step_order.keys()) + 1
            height = 0
            height_pedding = 60
            width = {}
            width_pedding = 30
            num_in_level = {}
            if len(self.step_order.keys()) > 0:
                for level in range(levels):
                    height_by_level = []
                    width_by_level = 0
                    num_in_level[level] = len(self.step_order[level])
                    for step in self.step_order[level]:
                        Button = self.get_Button_by_name(step)
                        height_by_level.append(Button.size[1])
                        width_by_level = width_by_level + Button.size[0]
                    width[level] = width_by_level
                    height = height + max(height_by_level)

                y = height + (height_pedding * (levels - 1))

                y = (self.size[1] - y) / 2
                if y < 0:
                    y = 20
                for level in range(levels):
                    x = width[level] + (width_pedding * (num_in_level[level] - 1))
                    x = (self.size[0] - x) / 2
                    for step in self.step_order[level]:
                        Button = self.get_Button_by_name(step)
                        new_pos = [x, y - (Button.size[1] / 2)]
                        Button._last_pos = new_pos
                        style = 'position:absolute;left:' + Button._last_pos[0] + 'px; top:' + Button._last_pos[
                            1] + 'px;'
                        Button.apply_style(style)
                        x = x + Button.size[0] + width_pedding
                    y = y + Button.size[1] + height_pedding

            if x > self.size[0]:
                self.node.width = x
                self.node.style.width = str(x) + 'px'
            if y > self.size[1]:
                self.node.height = y
                self.node.style.height = str(y) + 'px'

            self.update()

    def calculate_steps_order(self, steps_conections, corrent_step, count, step_order):
        if count == 0:
            step_order[corrent_step] = 0
        count = count + 1
        for corrent in steps_conections[corrent_step]:
            if corrent in step_order.keys():
                if step_order[corrent] < count:
                    step_order[corrent] = count
            else:
                step_order[corrent] = count
            self.calculate_steps_order(steps_conections, corrent, count, step_order)

        t_step_order = {}
        for step in step_order.keys():
            if step_order[step] not in t_step_order.keys():
                t_step_order[step_order[step]] = []
            t_step_order[step_order[step]].append(step)

        return t_step_order

    def calculate_steps_conections(self):
        first = None
        steps = self.steps
        steps_conections = {}
        if len(steps.keys()) > 0:
            for step in steps.keys():

                if isinstance(steps[step], dict) == False:
                    steps[step] = {}
                if step not in steps_conections.keys():
                    steps_conections[step] = []
                if steps[step]['base'] != None:
                    for base in steps[step]['base']:
                        if base in steps_conections.keys():
                            steps_conections[base].append(step)
                        else:
                            steps_conections[base] = [step]
                elif first == None:
                    first = step

        step_order = {}
        self.step_order = self.calculate_steps_order(steps_conections, first, 0, step_order)
        self.steps_conections = steps_conections
        self.first_step = first
        self.set_Steps_Order(self.step_order)

    def create_Button(self, Button_name, parent, pos, color='white'):
        Button_id = 'Button' + str(self.Button_count)
        self.Button_count = self.Button_count + 1
        setattr(self, Button_id, ui.Button(text=Button_name, parent=parent))
        getattr(self, Button_id)._last_pos = pos
        getattr(self, Button_id).Button_id = Button_id
        style = 'position:absolute;left:' + \
                getattr(self, Button_id)._last_pos[0] + \
                'px; top:' + \
                getattr(self, Button_id)._last_pos[1] + \
                'px;'
        if color!='white':
            style = style + 'background-color:' + color + ';'
        getattr(self, Button_id).apply_style(style)
        self.Button_list.append(Button_id)

    @event.action
    def update(self):
        if len(self.steps.keys()) > 0:
            ctx = self.ctx

            w = self.node.width
            h = self.node.height

            ctx.clearRect(0, 0, w, h)

            # Draw grid
            ctx.strokeStyle = '#eee'
            ctx.lineWidth = 1
            for y in range(0, h, 20):
                ctx.beginPath()
                ctx.moveTo(0, y)
                ctx.lineTo(w, y)
                ctx.stroke()
            for x in range(0, w, 20):
                ctx.beginPath()
                ctx.moveTo(x, 0)
                ctx.lineTo(x, h)
                ctx.stroke()

            self.calculate_steps_conections()

            # Draw lines
            color_count = 5
            for from_step in self.steps_conections.keys():
                from_Button = self.get_Button_by_name(from_step)
                for to_step in self.steps_conections[from_step]:
                    to_Button = self.get_Button_by_name(to_step)
                    ctx.lineCap = "round"
                    ctx.strokeStyle = COLORS[color_count]
                    ctx.lineWidth = 5
                    color_count = color_count + 1
                    if color_count >= len(COLORS):
                        color_count = 5
                    # Interpolate
                    ctx.beginPath()
                    ctx.moveTo(from_Button._last_pos[0] + (from_Button.size[0] / 2),
                               from_Button._last_pos[1] + (from_Button.size[1] / 2))
                    ctx.lineTo(to_Button._last_pos[0] + (to_Button.size[0] / 2),
                               to_Button._last_pos[1] + (to_Button.size[1] / 2))
                    ctx.stroke()

    @event.reaction('!children**.pointer_click')
    def on_button_click(self, *events):
        for ev in events:
            if 'Shift' in ev.modifiers:
                self.Button_list.remove(ev.source.Button_id)
                ev.source.dispose()
            else:
                self.set_Selected_step(ev.source.text)

    @event.reaction('pointer_down')
    def on_click(self, *events):
        self.order_Buttons()
        self.update()

    @event.reaction('!children**.pointer_move', '!children**.pointer_down')
    def on_button_move(self, *events):
        rect = self.node.getBoundingClientRect()
        offset = rect.left, rect.top
        ev = events[-1]
        new_pos = [ev.page_pos[0] - offset[0] - (ev.source.size[0] / 2),
                   ev.page_pos[1] - offset[1] - (ev.source.size[1] / 2)]

        size_limit = [self.node.width - ev.source.size[0], self.node.height - ev.source.size[1]]
        if (new_pos[0] < size_limit[0]) & (new_pos[1] < size_limit[1]) & (new_pos[0] > 0) & (new_pos[1] > 0):
            ev.source._last_pos[0] = new_pos[0]
            ev.source._last_pos[1] = new_pos[1]
            style = 'position:absolute;left:' + ev.source._last_pos[0] + 'px; top:' + ev.source._last_pos[1] + 'px;'
            ev.source.apply_style(style)
            self.update()

class Step_Tree_Class(ui.Widget):
    flag               = event.BoolProp(False, settable=True)
    open_filepicker    = event.StringProp('', settable=True)
    file_path          = event.ListProp([], settable=True)
    workflow_file      = event.ListProp([], settable=True)
    save_workflow_file = event.ListProp([], settable=True)
    Steps_Data_update  = event.BoolProp(False, settable=True)
    Steps_Data         = event.DictProp({}, settable=True)
    Data               = event.DictProp({}, settable=True)
    converter          = event.DictProp({}, settable=True)
    options            = event.ListProp([], settable=True)
    Vars_data          = event.DictProp({}, settable=True)
    Go2Help            = event.StringProp('', settable=True)
    step2export        = event.DictProp({}, settable=True)
    step_export_file   = event.ListProp([], settable=True)
    Load_step_file     = event.ListProp([], settable=True)
    step2load          = event.DictProp({}, settable=True)
    step_converter     = event.DictProp({}, settable=True)
    
    def init(self):
        self.current_selected = None
        
        with ui.HSplit() as self.main_lay:
            with ui.VSplit(flex=0.25) as self.tree_lay:
                with ui.GroupWidget(flex=0.05,title='Step Editing Panel'):
                    with ui.HSplit(spacing=2,padding=0):
                        with ui.VSplit(spacing=2,padding=1) as self.form:
                            with ui.HSplit(spacing=0,padding=1,style='max-height: 30px; min-height: 30px;'):
                                ui.Label(text='Key:',style='min-width: 110px; max-width: 110px;')
                                self.tree_key_b       = ui.LineEdit(title='Key:', text='')
                            with ui.HSplit(spacing=0,padding=1):
                                ui.Label(text='Value:',style='min-width: 110px; max-width: 110px;')
                                self.tree_value_b     = Documentation_Editor('',False,False,True,style='border: 1px solid gray; min-height: 50px;min-width: 100px;overflow-y: auto; ')
                            with ui.HSplit(spacing=0,padding=1,style='max-height: 30px; min-height: 30px;'):
                                ui.Label(text='Value options: ',style='min-width: 110px; max-width: 110px;align-content: stretch;')
                                self.tree_value_options_b = ui.ComboBox(title='Value options:',
                                                                        style='max-height: 30px; min-height: 30px;border: 1px solid gray;',
                                                                        editable=False,
                                                                        text='',
                                                                        placeholder_text='Value options:')
                                Add_Tooltip(self.tree_value_options_b,HELP['options_dropdown'],'right')
                            with ui.HSplit(spacing=0,padding=1,style='max-height: 30px; min-height: 30px;'):
                                ui.Label(text='',style='min-width: 110px; max-width: 110px;align-content: stretch;')
                                self.tree_add_option_b = ui.Button(text='Add',style='max-height: 25px; min-height: 25px;')
                                Add_Tooltip(self.tree_add_option_b,HELP['add'],'right')
                        with ui.VSplit(spacing=2,padding=0,flex=0.0035,style='min-width: 100px; max-width: 100px;'):
                            self.tree_submit_b      = ui.Button(text='Apply')
                            self.tree_new_b         = ui.Button(text='New')
                            self.file_path_b        = ui.Button(text='Browse')
                            self.tree_duplicate_b   = ui.Button(text='Duplicate')
                            self.tree_remove_b      = ui.Button(text='Remove')
                            self.tree_export_b      = ui.Button(text='Export Step')
                            Add_Tooltip(self.tree_submit_b,HELP['apply'],'right')
                            Add_Tooltip(self.tree_new_b,HELP['new'],'right')
                            Add_Tooltip(self.file_path_b,HELP['browse'],'right')
                            Add_Tooltip(self.tree_duplicate_b,HELP['duplicate'],'right')
                            Add_Tooltip(self.tree_remove_b,HELP['remove'],'right')
                            Add_Tooltip(self.tree_export_b,HELP['export'],'right')
                self.tree           = ui.TreeWidget(flex=0.1, max_selected=1)
                self.tree.text      = 'Top_level'
                self.Order_Steps_b  = ui.Button(text='Order Steps',style='font-size: 80%;')
                self.info_lable     = ui.Label(text='Help box:',style='max-height: 20px; min-height: 20px;')
                self.info           = Documentation_Editor(DEFAULT_HELP_BOX_TEXT,True,False,True,flex=0.01,style='border: 1px solid red;min-height: 50px;min-width: 100px; ')
                Add_Tooltip(self.Order_Steps_b,HELP['order_steps'],'right')
                self.info_lable.set_capture_mouse(2)
                self.info.set_capture_mouse(2)
                self.main_lay.set_capture_mouse(2)
                
            with ui.VSplit(flex=0.6) as self.canvas_lay:
                with ui.Layout(flex=0.03, style='min-height: 70px; max-height: 75px;'):
                    with ui.HSplit():
                        with ui.GroupWidget(title='Add New Step',style='min-width: 400px;border: 2px solid purple;'):
                            with ui.HSplit(spacing=2):
                                self.tree_module_b = ui.ComboBox(title='Use Module:', editable=True,
                                                                 style='min-width: 280px;border: 1px solid red;',
                                                                 placeholder_text='Choose a Step Template',
                                                                 options=MODULES_TEMPLATES.keys())
                                Add_Tooltip(self.tree_module_b,HELP['step_dropdown'],'top')
                                self.Help_b = ui.Button(text='About',style=' min-width: 80px;max-width: 80px;font-size: 100% ;')
                                Add_Tooltip(self.Help_b,HELP['about'],'bottom')
                                self.tree_create_new_step_b = ui.Button(text='Add',style=' min-width: 80px;max-width: 80px;')
                                Add_Tooltip(self.tree_create_new_step_b,HELP['add_step'],'bottom')
                                self.tree_Load_step_from_file_b = ui.Button(text='Load Step From File',style=' min-width: 160px;max-width: 160px;')
                                Add_Tooltip(self.tree_Load_step_from_file_b,HELP['load_step'],'bottom')
                        with ui.GroupWidget(title='Color Steps By',style='border: 2px solid pink;'):
                            with ui.HSplit():
                                self.Color_by_b = ui.ComboBox(title='Color by:', editable=False,
                                                                 style='max-width: 150px; border: 1px solid pink;',
                                                                 placeholder_text='Color by:',
                                                                 selected_index=0,
                                                                 options=list(map(lambda x: x.capitalize(),COLOR_BY)) )
                                Add_Tooltip(self.Color_by_b,HELP['color_steps_by'],'top')
                        with ui.VSplit(spacing=2):
                            self.tree_Load_WorkFlow_b = ui.Button(text='Load WorkFlow',style='max-height: 30px; max-width: 150px;')
                            self.tree_save_WorkFlow_b = ui.Button(text='Save WorkFlow',style='max-height: 30px; max-width: 150px;')
                            Add_Tooltip(self.tree_Load_WorkFlow_b,HELP['load_workflow'],'left')
                            Add_Tooltip(self.tree_save_WorkFlow_b,HELP['save_workflow'],'left')
                self.Graphical_panel = Graphical_panel(flex=0.5, style='min-height:600px; overflow-y: auto; overflow-x: auto;')
                with self.tree:
                    self.create_tree(self.Graphical_panel.Steps_Data)
                    self.collapse_all_not_selectd(self.tree)

    # @event.reaction('info_lable.pointer_move','info.pointer_move')
    # def on_info_move(self, *events):
        
        # for ev in events:
            # w_border = float(ev.source.size[0])*0.15
            # h_border = float(ev.source.size[1])*0.15
            # if (ev.pos[0]>ev.source.size[0]-w_border) or (ev.pos[0]<w_border)  or (ev.pos[1]>ev.source.size[1]-h_border) or (ev.pos[1]<h_border) :
                # self.info.set_flex(0.05)
            # else:
                # self.info.set_flex(0.2)
            
    @event.reaction('Order_Steps_b.pointer_click')
    def change_order(self):
        order=list()
        new_Dict={}
        if len(self.Graphical_panel.Steps_Order.keys())>0:
            data=self.tree2dict_for_export(self.tree)
            for key in self.Graphical_panel.Steps_Order.keys():
                order.extend(self.Graphical_panel.Steps_Order[key])
            for key in order:
                if isinstance(data[key], dict):
                    new_Dict[key]=dict(data[key])
                else:
                    new_Dict[key]=data[key]
                
            self.clean_steps_tree_info_Widget()
            with self.tree:
                self.create_tree(new_Dict)
                self.collapse_all_not_selectd(self.tree)

    @event.reaction('Color_by_b.selected_index')
    def Color_Steps_by(self, *events):
        if self.Color_by_b.selected_index!=-1:
            self.Graphical_panel.set_color_by_option(COLOR_BY[self.Color_by_b.selected_index])

    def uncorrect_dict(self, dic, converer):
        if isinstance(dic, dict):
            dic_keys = list(dic.keys())
            for key in dic_keys:
                temp = dic.pop(key)
                dic[converer[key]] = self.uncorrect_dict(temp, converer)
        return dic

    def clean_steps_tree_info_Widget(self):
        for tree in self.tree.children:
            tree.dispose()

    def recreate_steps_tree_info_Widget(self):
        with self.tree:
            self.create_tree(self.Steps_Data)
            self.collapse_all_not_selectd(self.tree)

    def Fix_Steps_Data(self, Steps_Data):
        self.uncorrect_dict(Steps_Data, self.converter)
        self.set_Steps_Data(Steps_Data)

    @event.reaction
    def update_step_data(self, *events):
        if self.Steps_Data_update:
            if len(self.workflow_file) > 0:
                self.Fix_Steps_Data(self.Steps_Data)
                self.clean_steps_tree_info_Widget()
                self.recreate_steps_tree_info_Widget(self.samples_data)
                self.set_workflow_file([])
                self.set_Steps_Data_update(False)
        else:
            self.Graphical_panel.set_Steps_Data(self.tree2dict(self.tree))
            self.set_Data(self.tree2dict_for_export(self.tree))

    @event.reaction('Help_b.pointer_click')
    def on_Help_click(self, *events):
        for ev in events:
            if self.tree_module_b.selected_index != -1:
                step = MODULES_TEMPLATES[self.tree_module_b.selected_key]
                if 'module' in step[step.keys()[0]].keys():
                    self.set_Go2Help(step[step.keys()[0]]['module'])
                    self.set_Go2Help('')

    @event.reaction('tree_Load_WorkFlow_b.pointer_click')
    def on_load_workflow_click(self, *events):
        for ev in events:
            self.set_open_filepicker('workflow_file')

    @event.reaction('tree_save_WorkFlow_b.pointer_click')
    def on_save_workflow_click(self, *events):
        for ev in events:
            self.set_open_filepicker('save_workflow_file')

    @event.reaction('file_path_b.pointer_click')
    def on_file_path_click(self, *events):
        for ev in events:
            self.set_open_filepicker('file_path')

    @event.reaction('file_path')
    def on_file_path_value_change(self, *events):
        for ev in events:
            if len(self.file_path) > 0:
                self.tree_value_b.set_value(self.file_path[0][0])
                #self.tree_value_b2.set_text(self.file_path[0][0])
                self.tree_value_b.set_load_flag(True)
                self.set_file_path([])

    @event.reaction('Graphical_panel.Selected_step')
    def if_step_selected(self, *events):
        for tree in self.tree.children:
            if self.Graphical_panel.Selected_step == tree.text:
                tree.set_selected(True)
                self.tree.highlight_show_item(tree)
                self.current_selected = tree
            else:
                tree.set_selected(False)
        self.collapse_all_not_selectd(self.tree)

    @event.reaction('tree_create_new_step_b.pointer_click')
    def tree_create_new_step_button_click(self, *events):
        for ev in events:
            if self.tree_module_b.selected_index != -1:
                if MODULES_TEMPLATES[
                    self.tree_module_b.selected_key].keys() not in self.Graphical_panel.Steps_Data.keys():
                    self.set_Vars_data(MODULES_TEMPLATES[self.tree_module_b.selected_key])
                    with self.tree:
                        self.create_tree(MODULES_TEMPLATES[self.tree_module_b.selected_key])

    @event.reaction('tree_module_b.text')
    def search_tree_module_b(self, *events):
        if (self.tree_module_b.selected_index == -1) and (len(self.tree_module_b.text)>0) and (self.tree_module_b.text!= self.tree_module_b.placeholder_text):
            self.tree_module_b.set_options(list(
                                                filter(
                                                       lambda x: len(x.lower().split(self.tree_module_b.text.lower()))>1,
                                                       MODULES_TEMPLATES.keys()
                                                       )))

            self.set_flag(True)
        elif (self.flag):
            self.tree_module_b.set_options(MODULES_TEMPLATES.keys())
            self.set_flag(False)

    def create_tree(self, current_level):
        for level in current_level.keys():
            if isinstance(current_level[level], dict):
                with ui.TreeItem(text=level, checked=None):
                    self.create_tree(current_level[level])
            else:
                if current_level[level] == None:
                    ui.TreeItem(text=level, checked=None)
                elif ((len(str(current_level[level]).split(',')) > 1) and isinstance(current_level[level], list)):
                    ui.TreeItem(title=level, text='['+str(current_level[level])+']', checked=None)
                else:
                    ui.TreeItem(title=level, text=str(current_level[level]), checked=None)

    def tree2dict_for_export(self, current_tree):
        steps = {}
        for tree in current_tree.children:
            if len(tree.children) > 0:
                steps[tree.text] = dict(self.tree2dict_for_export(tree))
            else:
                if len(tree.title) > 0:
                    if (len(tree.text.split(',')) > 1):
                        if (tree.text.startswith('[') and tree.text.endswith(']') ):
                            steps[tree.title] = tree.text.lstrip('[').rstrip(']').split(',')
                            steps[tree.title] = map(lambda x: int(x) if x.isnumeric() else x , steps[tree.title])
                        else:
                            if tree.text.isnumeric():
                                steps[tree.title] = int(tree.text)
                            else:
                                steps[tree.title] = tree.text
                    else:
                        if (tree.text.startswith('[') and tree.text.endswith(']') ):
                            steps[tree.title] = tree.text.lstrip('[').rstrip(']')
                        # elif (tree.text.startswith('[') or tree.text.endswith(']') ):
                            # steps[tree.title] = '"'+tree.text+'"'
                        else:
                            steps[tree.title] = tree.text
                        if steps[tree.title].isnumeric():
                            steps[tree.title] = int(steps[tree.title])
                else:
                    steps[tree.text] = None
        return steps

    def tree2dict(self, current_tree):
        steps = {}
        for tree in current_tree.children:
            if len(tree.children) > 0:
                steps[tree.text] = dict(self.tree2dict(tree))
            else:
                if len(tree.title) > 0:
                    if (len(tree.text.split(',')) > 1):
                        if (tree.text.startswith('[') and tree.text.endswith(']') ):
                            steps[tree.title] = tree.text.lstrip('[').rstrip(']').split(',')
                        else:
                            steps[tree.title] = [tree.text]
                    else:
                        if (tree.text.startswith('[') and tree.text.endswith(']') ):
                            steps[tree.title] = [tree.text.lstrip('[').rstrip(']')]
                        elif (tree.text.startswith('[') or tree.text.endswith(']') ):
                            steps[tree.title] = ['"'+tree.text+'"']
                        else:
                            steps[tree.title] = [tree.text]
                else:
                    steps[tree.text] = None
        return steps

    @event.action
    def collapse_all_not_selectd(self, current_tree):
        for tree in current_tree.children:
            if tree.selected == True:
                tree.set_collapsed(False)
            else:
                tree.set_collapsed(True)

    def get_options(self, key):
        module=''
        flag=True
        options = {'base': lambda: filter(lambda x: x != self.current_selected.parent.text,
                                          self.Graphical_panel.Steps_Data.keys()),
                   'scope': lambda: ['sample', 'project'],
                   'File_Type' : lambda:  self.get_file_type_options(self.Graphical_panel.Steps_Data,FILE_TYPES_SLOTS)

                   }

        temp = self.current_selected
        while temp.parent.text!='Top_level':
            temp = temp.parent
        for tree in temp.children:
            if tree.title == 'module':
                module = tree.text
        if module in MODULE_INFO.keys():
            if key in MODULE_INFO[module].keys():
                if 'info' in MODULE_INFO[module][key].keys():
                    if isinstance(MODULE_INFO[module][key]['info'],str):
                        self.info.set_value(MODULE_INFO[module][key]['info'])
                        self.info.set_load_flag(True)
                        flag = False
                    else:
                        self.info.set_value(DEFAULT_HELP_BOX_TEXT)
                        self.info.set_load_flag(True)
                else:
                    self.info.set_value(DEFAULT_HELP_BOX_TEXT)
                    self.info.set_load_flag(True)
                if 'options' in MODULE_INFO[module][key].keys():
                    if isinstance(MODULE_INFO[module][key]['options'],list):
                        return(MODULE_INFO[module][key]['options'])
        if flag:
            self.info.set_value(DEFAULT_HELP_BOX_TEXT)
            self.info.set_load_flag(True)
        if key in options.keys():
            return options[key]()
        else:
            return None

    def get_file_type_options(self,dic,options):
        if isinstance(dic,dict):
            for key in dic.keys():
                if isinstance(dic[key],dict):
                    self.get_file_type_options(dic[key],options)
                else:
                    if (key == 'File_Type') and (dic[key] != None):
                        options.extend(str(dic[key]).strip('[').strip(']').split(','))
        unique_options=[]
        map(lambda x: False if x in unique_options else unique_options.append(x) ,options)
        return unique_options

    def update_bases(self, From, To):
        for Top_level_tree in self.tree.children:
            for tree in Top_level_tree.children:
                if tree.title == 'base':
                    newsteps = ''
                    for step in tree.text.lstrip('[').rstrip(']').split(','):
                        if step == From:
                            step = To
                        newsteps = newsteps + step + ','
                    if len(newsteps.strip(',').split(','))>1:
                        tree.set_text('['+newsteps.strip(',')+']')
                    else:
                        tree.set_text(newsteps.strip(','))

    def update_bases_for_remove(self, step):
        bases = ''
        for Top_level_tree in self.tree.children:
            if Top_level_tree.text == step:
                for tree in Top_level_tree.children:
                    if tree.title == 'base':
                        bases = tree.text
        for Top_level_tree in self.tree.children:
            for tree in Top_level_tree.children:
                if tree.title == 'base':
                    if step in tree.text.lstrip('[').rstrip(']').split(','):
                        temp_text=[]
                        for old_steps in tree.text.lstrip('[').rstrip(']').split(','):

                            if step == old_steps:
                                temp_text.extend([bases.lstrip('[').rstrip(']').split(',')])

                            else:
                                temp_text.extend([old_steps])
                        unique_temp_text=[]
                        list(map(lambda x: x  if x in unique_temp_text  else unique_temp_text.append([x]) ,temp_text ))
                        temp_text=unique_temp_text
                        if '' in temp_text:
                            temp_text.remove('')

                        if len(temp_text)==0:
                            tree.set_text('base')
                            tree.set_title('')
                        elif len(temp_text)==1:
                            tree.set_text(str(temp_text))
                        else:
                            tree.set_text('['+str(temp_text)+']')

    @event.reaction('tree_submit_b.pointer_click')
    def tree_submit_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                if not ((self.current_selected.parent.text == 'Top_level') and (
                        self.tree_key_b.text in self.Graphical_panel.Steps_Data.keys())):
                    if self.current_selected.parent.text == 'Top_level':
                        self.update_bases(self.current_selected.text, self.tree_key_b.text)
                    if self.tree_value_b.disabled != True:
                        if self.tree_value_b.value != '':
                            self.current_selected.set_text(self.tree_value_b.value)
                            self.current_selected.set_title(self.tree_key_b.text)
                        else:
                            self.current_selected.set_text(self.tree_key_b.text)
                            self.current_selected.set_title('')
                    elif self.tree_key_b.disabled != True:
                        if self.tree_key_b.text != '':
                            self.current_selected.set_text(self.tree_key_b.text)

    @event.reaction('tree_add_option_b.pointer_click')
    def tree_add_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                if self.tree_value_b.disabled != True:
                    if self.tree_value_options_b.text != '':
                        if self.tree_value_b.value.lstrip('[').rstrip(']') != '':
                            if (self.current_selected.title == 'base') or (len(self.current_selected.title) ==0 and self.current_selected.text=='base') or (self.tree_value_b.value.startswith('[') and self.tree_value_b.value.endswith(']')):
                                self.tree_value_b.set_value('['+self.tree_value_b.value.lstrip('[').rstrip(']') + ',' + self.tree_value_options_b.text+']')
                                self.tree_value_b.set_load_flag(True)

                            elif (self.current_selected.title == 'File_Type') or (len(self.current_selected.title) ==0 and self.current_selected.text=='File_Type'):
                                self.tree_value_b.set_value(self.tree_value_b.value + ',' + self.tree_value_options_b.text)
                                self.tree_value_b.set_load_flag(True)
                            else:
                                self.tree_value_b.set_value(self.tree_value_b.value + ' ' + self.tree_value_options_b.text)
                                self.tree_value_b.set_load_flag(True)

                        elif self.tree_value_b.value.startswith('[') and self.tree_value_b.value.endswith(']'):
                            self.tree_value_b.set_value('['+self.tree_value_options_b.text+']')
                            self.tree_value_b.set_load_flag(True)

                        else:
                            self.tree_value_b.set_value(self.tree_value_options_b.text)
                            self.tree_value_b.set_load_flag(True)

    @event.reaction('tree_new_b.pointer_click')
    def tree_new_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                self.current_selected.set_collapsed(False)
                if len(self.current_selected.title) > 0:
                    self.current_selected.set_text(self.current_selected.title)
                    self.current_selected.set_title('')
                with self.current_selected:
                    ui.TreeItem(text='New', checked=None)

    @event.reaction('tree_remove_b.pointer_click')
    def tree_remove_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                if self.current_selected.parent.text == 'Top_level':
                    self.update_bases_for_remove(self.current_selected.text)
                self.current_selected.set_collapsed(True)
                self.current_selected.dispose()
                self.current_selected = None

    @event.reaction('step2load')
    def tree_step_load_step_from_file(self, *events):
        for ev in events:
            if (len(self.step2load.keys())==1):
                step2load      = self.step2load
                step_converter = self.step_converter
                self.uncorrect_dict(step2load, step_converter)
                for step_name in step2load.keys():
                    if step_name in self.Graphical_panel.Steps_Data.keys():
                        new_step_name = step_name+'_Copy'
                    else:
                        new_step_name = step_name
                    if new_step_name not in self.Graphical_panel.Steps_Data.keys():
                        self.set_Vars_data({new_step_name:step2load[step_name]})
                        with self.tree:
                            self.create_tree({new_step_name:step2load[step_name]})
            self.set_step2load({})
            self.set_step_converter({})

    @event.reaction('tree_Load_step_from_file_b.pointer_click')
    def tree_step_load_button_click(self, *events):
        for ev in events:
            self.set_open_filepicker('Load_step_file')

    @event.reaction('tree_export_b.pointer_click')
    def tree_export_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                if self.current_selected.parent.text == 'Top_level':
                    if len(self.current_selected.title) == 0:
                        dict         = self.tree2dict_for_export(self.current_selected)
                        if 'base' in dict.keys():
                            dict['base'] = None
                        else:
                            temp_dict    = {'base':None}
                            temp_dict.update(dict)
                            dict         = temp_dict
                        dict         = {self.current_selected.text:dict}
                        self.set_step2export(dict)
                        self.set_open_filepicker('step_export_file')
                    
    @event.reaction('tree_duplicate_b.pointer_click')
    def tree_duplicate_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                with self.current_selected.parent:
                    if len(self.current_selected.title) > 0:
                        self.create_tree({self.current_selected.title:self.current_selected.text})
                    else:
                        #dict=self.tree2dict(self.current_selected)
                        dict=self.tree2dict_for_export(self.current_selected)

                        if self.current_selected.parent.text == 'Top_level':
                            new_name = self.current_selected.text+'_copy'
                            if new_name not in self.Graphical_panel.Steps_Data.keys():
                                self.create_tree({new_name:dict})
                        else:
                            self.create_tree({self.current_selected.text:dict})

    @event.reaction('tree.children**.checked', 'tree.children**.selected',
                    'tree.children**.collapsed')
    def on_event(self, *events):
        for ev in events:
            if (ev.type == 'selected') :#& (ev.new_value):
                self.current_selected = ev.source
                if self.current_selected.parent.text=='Top_level':
                    self.get_options('__module_info__')
                if len(self.current_selected.title) > 0:
                    self.tree_value_b.set_value(self.current_selected.text)
                    self.tree_value_b.set_load_flag(True)
                    self.tree_key_b.set_text(self.current_selected.title)
                    self.tree_value_b.set_disabled(False)
                    if self.get_options(self.current_selected.title) != None:
                        self.tree_value_options_b.set_options(self.get_options(self.current_selected.title))
                        self.tree_value_options_b.set_editable(True)
                    else:
                        if len(self.options) > 0:
                            self.tree_value_options_b.set_options(self.options)
                            self.tree_value_options_b.set_editable(True)
                        else:
                            self.tree_value_options_b.set_editable(False)
                            self.tree_value_options_b.set_options([''])
                            self.tree_value_options_b.set_selected_index(-1)
                            self.tree_value_options_b.set_text('')


                else:
                    self.tree_key_b.set_text(self.current_selected.text)
                    self.tree_value_b.set_value('')
                    self.tree_value_b.set_load_flag(True)


                    if len(self.current_selected.children) > 0:
                        self.tree_value_b.set_disabled(True)
                        self.tree_value_options_b.set_editable(False)
                        self.tree_value_options_b.set_options([''])
                        self.tree_value_options_b.set_selected_index(-1)
                        self.tree_value_options_b.set_text('')
                    else:
                        self.tree_value_b.set_disabled(False)
                        if self.get_options(self.current_selected.text) != None:
                            self.tree_value_options_b.set_options(self.get_options(self.current_selected.text))
                            self.tree_value_options_b.set_editable(True)
                        else:
                            if len(self.options) > 0:
                                self.tree_value_options_b.set_options(self.options)
                                self.tree_value_options_b.set_editable(True)
                            else:
                                self.tree_value_options_b.set_editable(False)
                                self.tree_value_options_b.set_options([''])
                                self.tree_value_options_b.set_selected_index(-1)
                                self.tree_value_options_b.set_text('')

class Only_Tree_Class(ui.Widget):
    Data_update = event.BoolProp(False, settable=True)
    Data = event.DictProp({}, settable=True)
    converter = event.DictProp({}, settable=True)
    open_filepicker = event.StringProp('', settable=True)
    file_path = event.ListProp([], settable=True)

    def init(self, DATA):
        self.current_selected = None
        with ui.HSplit() as self.main_lay:
            with ui.VSplit(flex=0.3,style='min-height: 600px; max-height: 600px;') as self.tree_lay:
                with ui.HSplit(flex=0.1):
                    with ui.FormLayout(flex=0.01, style='min-height: 190px; max-height: 190px;') as self.form:
                        self.tree_key_b = ui.LineEdit(title='Key:', text='')
                        self.tree_value_b = ui.LineEdit(title='Value:', text='')

                        self.tree_value_options_b = ui.ComboBox(title='Value options:', editable=False, text='',
                                                                placeholder_text='Value options:')
                        self.tree_add_option_b = ui.Button(text='Add')
                    with ui.VSplit(flex=0.0035):
                        self.tree_submit_b = ui.Button(text='Edit')
                        with ui.HSplit():
                            self.tree_new_sub_b = ui.Button(text='New Sub Field')
                            self.tree_new_b = ui.Button(text='New Field')
                        self.file_path_b = ui.Button(text='Browse')
                        self.tree_remove_b = ui.Button(text='Remove')
                with ui.TreeWidget(flex=0.2, max_selected=1) as self.tree:
                    self.create_tree(DATA)
                self.collapse_all_not_selectd(self.tree)

    @event.reaction('file_path_b.pointer_click')
    def on_file_path_click(self, *events):
        for ev in events:
            self.set_open_filepicker(self.title + '_file_path')

    @event.reaction('file_path')
    def on_file_path_value_change(self, *events):
        for ev in events:
            if len(self.file_path) > 0:
                self.tree_value_b.set_text(self.file_path[0][0])
                self.set_file_path([])

    def uncorrect_dict(self, dic, converer):
        if isinstance(dic, dict):
            dic_keys = list(dic.keys())
            for key in dic_keys:
                temp = dic.pop(key)
                dic[converer[key]] = self.uncorrect_dict(temp, converer)
        return dic

    def clean_tree_info_Widget(self):
        for tree in self.tree.children:
            tree.dispose()

    def recreate_tree_info_Widget(self):
        with self.tree:
            self.create_tree(self.Data)
            self.collapse_all_not_selectd(self.tree)

    def Fix_Data(self, Data):
        self.uncorrect_dict(Data, self.converter)
        self.set_Data(Data)

    @event.reaction
    def update_data(self, *events):
        if self.Data_update:
            self.Fix_Data(self.Data)
            self.clean_tree_info_Widget()
            self.recreate_tree_info_Widget()
            self.set_Data_update(False)
            self.check_real_size()
        self.set_Data(self.tree2dict_for_export(self.tree))

    def create_tree(self, current_level):
        for level in current_level.keys():
            if isinstance(current_level[level], dict):
                with ui.TreeItem(text=level, checked=None):
                    self.create_tree(current_level[level])
            else:

                if current_level[level] == None:
                    ui.TreeItem(text=level, checked=None)
                elif ((len(str(current_level[level]).split(',')) > 1) and isinstance(current_level[level], list)):
                    ui.TreeItem(title=level, text='['+str(current_level[level])+']', checked=None)
                else:
                    ui.TreeItem(title=level, text=str(current_level[level]), checked=None)


    def tree2dict_for_export(self, current_tree):
        steps = {}
        for tree in current_tree.children:
            if len(tree.children) > 0:
                steps[tree.text] = dict(self.tree2dict_for_export(tree))
            else:
                if len(tree.title) > 0:
                    if (len(tree.text.split(',')) > 1):
                        if (tree.text.startswith('[') and tree.text.endswith(']') ): #(tree.title in FIELDS2SPLIT):
                            steps[tree.title] = tree.text.lstrip('[').rstrip(']').split(',')
                        else:
                            steps[tree.title] = tree.text
                    else:
                        if (tree.text.startswith('[') and tree.text.endswith(']') ):
                            steps[tree.title] = tree.text.lstrip('[').rstrip(']')
                        # elif (tree.text.startswith('[') or tree.text.endswith(']') ):
                            # steps[tree.title] = '"'+tree.text+'"'
                        else:
                            steps[tree.title] = tree.text
                else:
                    steps[tree.text] = None
        return steps

    @event.action
    def collapse_all_not_selectd(self, current_tree):
        for tree in current_tree.children:
            if tree.selected == True:
                tree.set_collapsed(False)
            else:
                tree.set_collapsed(True)

    def get_options(self, key):
        options = {'Executor': lambda: Executor
                   }
        if key in options.keys():
            return options[key]()
        else:
            return None

    @event.reaction('tree_submit_b.pointer_click')
    def tree_submit_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                if self.tree_value_b.disabled != True:
                    if self.tree_value_b.text != '':
                        self.current_selected.set_text(self.tree_value_b.text)
                        self.current_selected.set_title("".join([ c if (c.isalnum() or c=='_') else "" for c in self.tree_key_b.text ]))
                    else:
                        self.current_selected.set_text("".join([ c if (c.isalnum() or c=='_') else "" for c in self.tree_key_b.text ]))
                        self.current_selected.set_title('')
                elif self.tree_key_b.disabled != True:
                    if self.tree_key_b.text != '':
                        self.current_selected.set_text("".join([ c if (c.isalnum() or c=='_')  else "" for c in self.tree_key_b.text ]))

    @event.reaction('tree_add_option_b.pointer_click')
    def tree_add_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                if self.tree_value_b.disabled != True:
                    if self.tree_value_options_b.text != '':
                        if self.tree_value_b.text.lstrip('[').rstrip(']') != '':
                            if (self.current_selected.title == 'base') or (len(self.current_selected.title) ==0 and self.current_selected.text=='base') or (self.tree_value_b.text.startswith('[') and self.tree_value_b.text.endswith(']')):
                                self.tree_value_b.set_text('['+self.tree_value_b.text.lstrip('[').rstrip(']') + ',' + self.tree_value_options_b.text+']')
                            elif (self.current_selected.title == 'File_Type') or (len(self.current_selected.title) ==0 and self.current_selected.text=='File_Type'):
                                self.tree_value_b.set_text(self.tree_value_b.text + ',' + self.tree_value_options_b.text)
                            else:
                                self.tree_value_b.set_text(self.tree_value_b.text + ' ' + self.tree_value_options_b.text)
                        elif self.tree_value_b.text.startswith('[') and self.tree_value_b.text.endswith(']'):
                            self.tree_value_b.set_text('['+self.tree_value_options_b.text+']')
                        else:
                            self.tree_value_b.set_text(self.tree_value_options_b.text)

    @event.reaction('tree_new_sub_b.pointer_click')
    def tree_new_sub_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                self.current_selected.set_collapsed(False)
                if len(self.current_selected.title) > 0:
                    self.current_selected.set_text(self.current_selected.title)
                    self.current_selected.set_title('')
                with self.current_selected:
                    ui.TreeItem(text='New', checked=None)

    @event.reaction('tree_new_b.pointer_click')
    def tree_new_button_click(self, *events):
        for ev in events:
            with self.tree:
                ui.TreeItem(text='New', checked=None)

    @event.reaction('tree_remove_b.pointer_click')
    def tree_remove_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                self.current_selected.set_collapsed(True)
                self.current_selected.dispose()
                self.current_selected = None

    @event.reaction('tree.children**.checked', 'tree.children**.selected',
                    'tree.children**.collapsed')
    def on_event(self, *events):

        for ev in events:
            if (ev.type == 'selected') & (ev.new_value):
                self.current_selected = ev.source
                if len(self.current_selected.title) > 0:
                    self.tree_value_b.set_text(self.current_selected.text)
                    self.tree_key_b.set_text(self.current_selected.title)
                    self.tree_value_b.set_disabled(False)
                    if self.get_options(self.current_selected.title) != None:
                        self.tree_value_options_b.set_options(self.get_options(self.current_selected.title))
                        self.tree_value_options_b.set_editable(True)
                    else:
                        self.tree_value_options_b.set_editable(False)
                        self.tree_value_options_b.set_options([''])
                        self.tree_value_options_b.set_selected_index(-1)
                        self.tree_value_options_b.set_text('')


                else:
                    self.tree_key_b.set_text(self.current_selected.text)
                    self.tree_value_b.set_text('')
                    if len(self.current_selected.children) > 0:
                        self.tree_value_b.set_disabled(True)
                        self.tree_value_options_b.set_editable(False)
                        self.tree_value_options_b.set_options([''])
                        self.tree_value_options_b.set_selected_index(-1)
                        self.tree_value_options_b.set_text('')
                    else:
                        self.tree_value_b.set_disabled(False)
                        if self.get_options(self.current_selected.text) != None:
                            self.tree_value_options_b.set_options(self.get_options(self.current_selected.text))
                            self.tree_value_options_b.set_editable(True)
                        else:
                            self.tree_value_options_b.set_editable(False)
                            self.tree_value_options_b.set_options([''])
                            self.tree_value_options_b.set_selected_index(-1)
                            self.tree_value_options_b.set_text('')

class Samples_info(ui.Widget):
    open_filepicker = event.StringProp('', settable=True)
    project_files = event.ListProp([], settable=True)
    sample_files = event.ListProp([], settable=True)
    load_samples_file = event.ListProp([], settable=True)
    save_samples_file = event.ListProp([], settable=True)
    samples_data = event.DictProp({}, settable=True)
    samples_data_update = event.BoolProp(False, settable=True)
    converter = event.DictProp({}, settable=True)

    def init(self):
        with ui.VSplit( padding=10,spacing=10) as self.layout:
            with ui.Layout( style='min-height: 95px; max-height: 95px;'):
                with ui.HSplit(style='min-height: 55px; max-height: 55px;'):
                    with ui.GroupWidget(title='Edit Project Title',style='font-size: 120%; border: 2px solid purple; max-height: 55px; min-height: 55px;' ):
                        self.tree_title_b = ui.LineEdit(text='My_Project', style = 'font-size: 80%; border: 1px solid red;min-width: 300px;',
                                                        placeholder_text='My_Project')
                    with ui.GroupWidget(title='Project Level File/s',style='border: 2px solid green;max-height: 55px; min-height: 55px; max-width: 200px;' ):
                        self.add_project_file_b = ui.Button(text='Add',style='min-width: 150px;')
                    with ui.GroupWidget(title='Sample Level File/s',style='border: 2px solid blue;max-height: 55px; min-height: 55px;max-width: 200px;' ):
                        self.add_sample_file_b  = ui.Button(text='Add',style='min-width: 150px;')
                    with ui.VSplit():
                        self.load_sample_file_b = ui.Button(text='Load Sample File',style='max-width: 200px;')
                        self.save_sample_file_b = ui.Button(text='Save Sample File',style='max-width: 200px;')
            
            #ui.Label(text='',style='min-height: 5px; max-height: 5px;')
            with ui.GroupWidget(title='Project Level',style='font-size: 120% ;padding: 10px ;border: 2px solid green; border-radius: 10px;'):
                 with ui.VSplit():
                    with ui.HFix(style='max-height:30px;'):#overflow-y:scroll;'):
                        ui.LineEdit(text='File Type',
                                    disabled=True,
                                    style='background: SeaShell  ; text-align: center;border-radius: 0px; text-decoration: max-height:30px;')
                        ui.LineEdit(text='Path',
                                    disabled=True,
                                    style='background: SeaShell  ; text-align: center;border-radius: 0px; text-decoration: max-height:30px;')
                        ui.LineEdit(text='Remove Project File',
                                    disabled=True,
                                    style='background: SeaShell  ; text-align: center;border-radius: 0px; text-decoration: max-height:30px;')
                        ui.LineEdit(text='',
                                    disabled=True,
                                    style='background: SeaShell  ; text-align: center;border-radius: 0px; text-decoration: max-height:30px; max-width:15px;')

                    
                    with ui.Layout(style='overflow-y:scroll;'):
                        self.project = ui.VFix(style='font-size: 80%;')


            with ui.GroupWidget( title='Sample Level',style='font-size: 120% ;padding: 5px ; border: 3px solid blue; border-radius: 10px;'):
                with ui.VSplit():
                    with ui.HFix(style='max-height:30px;'):#overflow-y:scroll;'):
                        ui.LineEdit(text='Sample Name',
                                    disabled=True,
                                    style='background: Lavender  ; text-align: center;border-radius: 0px; text-decoration: max-height:30px;')
                        ui.LineEdit(text='File Type',
                                    disabled=True,
                                    style='background: Lavender  ; text-align: center;border-radius: 0px; text-decoration: max-height:30px;')
                        ui.LineEdit(text='Path',
                                    disabled=True,
                                    style='background: Lavender  ; text-align: center;border-radius: 0px; text-decoration: max-height:30px;')
                        ui.LineEdit(text='Remove Sample File',
                                    disabled=True,
                                    style='background: Lavender  ; text-align: center;border-radius: 0px; text-decoration: max-height:30px;')
                        ui.LineEdit(text='',
                                    disabled=True,
                                    style='background: Lavender  ; text-align: center;border-radius: 0px; text-decoration: max-height:30px; max-width:15px;')

                    
                    with ui.Layout(style='overflow-y:scroll;'):
                        self.sample = ui.VFix(style='font-size: 80%;')

            self.project.spacer = None
            self.sample.spacer = None
            #ui.Label(flex=0.1, text='')

    def uncorrect_dict(self, dic, converer):
        if isinstance(dic, dict):
            dic_keys = list(dic.keys())
            for key in dic_keys:
                temp = dic.pop(key)
                dic[converer[key]] = self.uncorrect_dict(temp, converer)
        return dic

    def clean_samples_info_Widget(self):
        for project in self.project.children:
            project.dispose()
        for sample in self.sample.children:
            sample.dispose()

    def recreate_samples_info_Widget(self, samples_data):
        samples_data_keys = samples_data.keys()
        samples_data_keys.sort()
        if 'Title' in samples_data_keys:
            self.tree_title_b.set_text(samples_data['Title'])

        if 'project_data' in samples_data_keys:
            for project_type in samples_data['project_data'].keys():
                for project_file in samples_data['project_data'][project_type]:
                    self.add_project_file(project_file, project_type)

        for name in samples_data_keys:
            if name not in ['project_data', 'Title', 'samples']:
                for filetype in samples_data[name].keys():
                    for path in samples_data[name][filetype]:
                        self.add_sample_file(name, path, filetype)

    def update_samples_data(self, samples_data):
        self.uncorrect_dict(samples_data, self.converter)
        self.set_samples_data(samples_data)

    @event.reaction('samples_data_update')
    def on_samples_data_change(self, *events):
        if self.samples_data_update:
            for ev in events:
                if len(self.load_samples_file) > 0:
                    self.update_samples_data(self.samples_data)
                    self.clean_samples_info_Widget()
                    self.recreate_samples_info_Widget(self.samples_data)
                    self.set_load_samples_file([])
                    self.set_samples_data_update(False)

    @event.reaction
    def get_sample_data(self, *events):
        sample_data = {'Title': self.tree_title_b.text,
                       'project_data': {}}
        for project in self.project.children:
            if project.id.startswith('HFix'):
                project_file_type = project.file_type.text
                project_file_path = project.file_path.text
                if project_file_type != '':
                    if project_file_type in sample_data['project_data'].keys():
                        sample_data['project_data'][project_file_type].append(project_file_path)
                    else:
                        sample_data['project_data'][project_file_type] = [project_file_path]
        for samples in self.sample.children:
            if samples.id.startswith('HFix'):
                sample_name = samples.sample_name.text
                sample_file_type = samples.sample_file_type.text
                sample_file_path = samples.sample_file_path.text
                if (sample_name != '') & (sample_file_type != ''):
                    if sample_name in sample_data.keys():
                        if sample_file_type in sample_data[sample_name].keys():
                            sample_data[sample_name][sample_file_type].append(sample_file_path)
                        else:
                            sample_data[sample_name][sample_file_type] = [sample_file_path]
                    else:
                        sample_data[sample_name] = {}
                        sample_data[sample_name][sample_file_type] = [sample_file_path]
        self.set_samples_data(sample_data)

    def add_sample_file(self, sample_name='', file_path='', file_type=''):
        with self.sample:
            if self.sample.spacer != None:
                self.sample.spacer.dispose()
            with ui.HFix(padding=3,spacing=5) as sample:
                sample.sample_name      = ui.LineEdit(placeholder_text='Sample Name', text=sample_name)
                sample.sample_file_type = ui.ComboBox(placeholder_text='File Type', editable=True, text=file_type,
                                                      options=FILE_TYPES)
                sample.sample_file_path = ui.LineEdit(placeholder_text='File Path', text=file_path)
                ui.Button(text='Remove',style='border-radius: 0px;')
            self.sample.spacer = ui.Label(flex=0.1, text='_')

    def add_project_file(self, file_path='', file_type=''):
        with self.project:
            if self.project.spacer != None:
                self.project.spacer.dispose()
            with ui.HFix(padding=3,spacing=5) as project:
                project.file_type = ui.ComboBox(placeholder_text='File Type', editable=True, text=file_type,
                                                options=FILE_TYPES)
                project.file_path = ui.LineEdit(placeholder_text='File Path', text=file_path)
                ui.Button(text='Remove',style='border-radius: 0px;')

            self.project.spacer = ui.Label(flex=0.1, text='_')

    @event.reaction('!project.children**.pointer_click', '!sample.children**.pointer_click')
    def on_button_click(self, *events):
        for ev in events:
            if ev.source.text=='Remove':
                ev.source.parent.dispose()

    @event.reaction('add_project_file_b.pointer_click')
    def on_add_project_file_click(self, *events):
        for ev in events:
            self.set_open_filepicker('project')

    @event.reaction('add_sample_file_b.pointer_click')
    def on_add_sample_file_click(self, *events):
        for ev in events:
            self.set_open_filepicker('samples')

    @event.reaction('save_sample_file_b.pointer_click')
    def on_save_sample_file_click(self, *events):
        for ev in events:
            self.set_open_filepicker('save_samples_file')

    @event.reaction('load_sample_file_b.pointer_click')
    def on_load_sample_file_click(self, *events):
        for ev in events:
            self.set_open_filepicker('load_samples_file')

    @event.reaction('project_files')
    def on_project_files(self, *events):
        for ev in events:
            if len(self.project_files) > 0:
                for file in self.project_files:
                    self.add_project_file(file[0])

    @event.reaction('sample_files')
    def on_sample_files(self, *events):
        for ev in events:
            if len(self.sample_files) > 0:
                for file in self.sample_files:
                    self.add_sample_file(file[1], file[0])

def Load_MODULES_TEMPLATES():
    import yaml, os, inspect
    import urllib.request

    location = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda: 0)))
    location = os.path.expanduser(location+os.sep+"..")

    local_MODULES_TEMPLATES_FILE = os.path.abspath(os.path.join(location, 'neatseq_flow_gui', 'TEMPLATES', 'MODULES_TEMPLATES.yaml'))
    try:
        urllib.request.urlretrieve(MODULES_TEMPLATES_FILE,local_MODULES_TEMPLATES_FILE)
        print("Modules Templates File was Updated Successfully!")
    except:
        print("Modules Templates File could not be Updated")

    try:

        with open(local_MODULES_TEMPLATES_FILE, 'rb') as infile:
            MODULES_TEMPLATES = yaml.load(infile, yaml.SafeLoader)
            return MODULES_TEMPLATES

    except:
        return {}

def Update_Yaml_Data(remote_file,local_directory, file,Message=''):
    import yaml, os, inspect
    import urllib.request

    location = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda: 0)))
    location = os.path.expanduser(location+os.sep+"..")

    local_FILE = os.path.abspath(os.path.join(location, 'neatseq_flow_gui', local_directory, file))
    try:
        urllib.request.urlretrieve(remote_file,local_FILE)
        print( Message +" File was Updated Successfully!")
    except:
        print( Message +" File could not be Updated")

    try:

        with open(local_FILE, 'rb') as infile:
            Yaml_Data = yaml.load(infile, yaml.SafeLoader)
            return Yaml_Data

    except:
        return {}

def setup_yaml(yaml, OrderedDict):
    """ http://stackoverflow.com/a/8661021 """
    represent_dict_order = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
    yaml.add_representer(OrderedDict, represent_dict_order)
    return yaml

class Run_NeatSeq_Flow(ui.Widget):
    open_filepicker = event.StringProp('', settable=True)
    NeatSeq_bin     = event.ListProp([], settable=True)
    conda_bin       = event.ListProp([], settable=True)
    conda_env       = event.ListProp([], settable=True)
    Project_dir     = event.ListProp([], settable=True)
    sample_file     = event.ListProp([], settable=True)
    parameter_file  = event.ListProp([], settable=True)
    command         = event.ListProp([], settable=True)
    Terminal        = event.StringProp('', settable=True)
    Tags            = event.ListProp(['Run All Work-Flow'], settable=True)
    Tag_selected    = event.StringProp('', settable=True)
    jump2monitortab = event.StringProp('None', settable=True)
    
    def init(self,Server):
        self.Server = Server
        with ui.VSplit(spacing=10,padding=50):
            ui.Layout(style='max-height: 50px;')
            with ui.HSplit():
                with ui.VSplit(flex=1):
                    with ui.GroupWidget(title='Project Information', style='min-height: 230px; min-width: 250px; border: 2px solid blue; '):
                        with ui.VSplit():
                            ui.Layout()
                            with ui.Layout(title='Project Directory', style='min-height: 70px; max-height: 70px;'):
                                ui.Label(text='Project Directory:',style='padding-left: 0px; font-size: 120% ;')
                                with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                    self.Project_dir_L = ui.LineEdit(text='',disabled = (Server and LOCK_USER_DIR) )
                                    self.Project_dir_b = ui.Button(text='Browse', style='max-width: 100px; ')
                            ui.Layout()
                            with ui.Layout(title='Sample File', style='min-height: 70px; max-height: 70px;'):
                                ui.Label(text='Sample File:',style='padding-left: 0px; font-size: 120% ;')
                                with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                    self.sample_file_L = ui.LineEdit(text='',disabled = (Server and LOCK_USER_DIR))
                                    self.sample_file_b = ui.Button(text='Browse', style='max-width: 100px;')
                            ui.Layout()
                            with ui.Layout(title='Parameter File', style='min-height: 70px; max-height: 70px;'):
                                ui.Label(text='Parameter File:',style='padding-left: 0px; font-size: 120% ;')
                                with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                    self.parameter_file_L = ui.LineEdit(text='',disabled = (Server and LOCK_USER_DIR))
                                    self.parameter_file_b = ui.Button(text='Browse', style='max-width: 100px;')
                            ui.Layout()
                    ui.Label(style='padding: 0px ;min-height: 20px; max-height: 20px; ')
                    #ui.Layout()
                    with ui.GroupWidget(title='NeatSeq-Flow Information (For Advanced Users)', style='min-height: 230px; min-width: 250px; border: 2px solid green;'):
                        with ui.VSplit():
                            ui.Layout()
                            with ui.Layout(title='NeatSeq-Flow script location', style='min-height: 70px; max-height: 70px;'):
                                ui.Label(text='NeatSeq-Flow script location:',style='padding-left: 0px; font-size: 120% ;')
                                with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                    self.NeatSeq_bin_L = ui.LineEdit(text='neatseq_flow.py',disabled = (Server and LOCK_USER_DIR))
                                    self.NeatSeq_bin_b = ui.Button(text='Browse', style='max-width: 100px; ')
                            ui.Layout()
                            with ui.Layout(title='Conda bin location', style='min-height: 70px; max-height: 70px;'):
                                ui.Label(text='Conda bin location:',style='padding-left: 0px; font-size: 120% ;')
                                with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                    self.conda_bin_L = ui.LineEdit(text=CONDA_BIN,disabled = (Server and LOCK_USER_DIR))
                                    self.conda_bin_b = ui.Button(text='Browse', style='max-width: 100px; ')
                            ui.Layout()
                            with ui.Layout(title='Conda environment to use', style='min-height: 70px; max-height: 70px;'):
                                ui.Label(text='Conda environment to use:',style='padding-left: 0px; font-size: 120% ;')
                                with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                    self.conda_env_L = ui.ComboBox(editable= not (Server and LOCK_USER_DIR), text='',
                                                                   placeholder_text='Choose Conda Environment')
                                    self.conda_env_b = ui.Button(text='Search', style='max-width: 100px; ')
                            ui.Layout()
                    ui.Label(style='padding: 0px ;min-height: 5px; max-height: 5px; ')
                with ui.VSplit(flex=2):

                    with ui.HSplit():
                        self.Generate_scripts_b = ui.Button(text='Generate scripts', style='max-height: 55px; min-width: 150px; ')
                        with ui.VSplit():
                            self.Run_Tag_b      = ui.ComboBox(editable=False,
                                                              style='font-size: 90%; max-height: 20px; min-width: 150px;',
                                                              placeholder_text='Select Tag',
                                                              options=self.Tags,
                                                              selected_index=0)
                            self.Run_scripts_b  = ui.Button(text='Run scripts', style='max-height: 20px; min-width: 150px;')
                        self.Run_Monitor_b      = ui.Button(text='Run Monitor', style='max-height: 55px; min-width: 130px;')
                        self.Kill_Run_b         = ui.Button(text='Kill Run', style='max-height: 55px; min-width: 100px;')
                        with ui.VSplit():
                            self.Locate_Failures_b  = ui.Button(text='Locate Failures', style='max-height: 20px; min-width: 150px;')
                            self.Recovery_b         = ui.Button(text='Recover', style='max-height: 20px; min-width: 150px;')
                    ui.Label(text='',style='max-height: 5px; min-height: 5px;')
                    with ui.GroupWidget(title='Terminal:',style='font-size: 120% ;border: 2px solid red;'):
                        with ui.VFix():#ui.Layout( style='min-height: 460px; max-height: 460px; padding: 10px ;'):
                        #ui.Label(text='Terminal:',style='padding-left: 0px; padding-top: 10px; font-size: 120% ;max-height: 30px; min-height: 30px;')
                            self.label = ui.Label(style=' padding: 10px ; border: 0px solid gray; border-radius: 10px;   overflow-y: auto; overflow-x: auto;')
                    ui.Label(style='padding: 0px ;min-height: 5px; max-height: 5px; ')
            ui.Layout(style='max-height: 50px;')


    @event.reaction('conda_env')
    def conda_env_options(self, *events):
        for ev in events:
            if len(self.conda_env) > 0:
                self.conda_env_L.set_options(self.conda_env)
            else:
                self.conda_env_L.set_options([])

    @event.reaction('Terminal')
    def write_2_Terminal(self, *events):
        if len(self.Terminal) > 0:
            temp = []
            temp.extend(self.Terminal.split('\n'))
            temp.extend(['', ''])
            self.label.set_html('<br />'.join(temp))
            #self.set_Terminal('')

    @event.reaction('Run_Tag_b.pointer_click')
    def Select_Tag(self, *events):
        for ev in events:
            self.set_command(['Tags',self.Project_dir_L.text])

    @event.reaction('Tags')
    def set_Tags_options(self, *events):
        options = self.Tags
        options = list(options)
        options.sort(reverse=False)
        #options.insert(0,self.Run_Tag_b.options[0])
        self.Run_Tag_b.set_options(options)

    @event.reaction('Run_Tag_b.selected_index')
    def Get_Selected_Tag(self, *events):
        if self.Run_Tag_b.selected_index!=-1:
            self.set_Tag_selected(self.Run_Tag_b.options[self.Run_Tag_b.selected_index][0])
        else:
            self.set_Tag_selected('')

    @event.reaction('Generate_scripts_b.pointer_click')
    def on_Generate_scripts_b_click(self, *events):
        for ev in events:
            self.set_command(['Generate_scripts', self.NeatSeq_bin_L.text, self.conda_bin_L.text, self.conda_env_L.text,
                              self.Project_dir_L.text, self.sample_file_L.text, self.parameter_file_L.text])

    @event.reaction('Run_scripts_b.pointer_click')
    def on_Run_scripts_b_click(self, *events):
        for ev in events:
            self.set_command(['Run_scripts',self.Project_dir_L.text])

    @event.reaction('Kill_Run_b.pointer_click')
    def on_Kill_Run_b_click(self, *events):
        for ev in events:
            self.set_command(['Kill_Run',self.Project_dir_L.text])

    @event.reaction('Recovery_b.pointer_click')
    def on_Recovery_b_click(self, *events):
        for ev in events:
            self.set_command(['Recovery',self.Project_dir_L.text])

    @event.reaction('Locate_Failures_b.pointer_click')
    def on_Locate_Failures_click(self, *events):
        for ev in events:
            self.set_command(['Locate_Failures',self.Project_dir_L.text])


    @event.reaction('Run_Monitor_b.pointer_click')
    def on_Run_Monitor_b_click(self, *events):
        for ev in events:
            if self.Server:
                self.set_jump2monitortab(self.Project_dir_L.text)
            else:
                self.set_command(['Run_Monitor',self.Project_dir_L.text])

    @event.reaction('conda_env_b.pointer_click')
    def on_conda_env_b_click(self, *events):
        for ev in events:
            self.set_command(['conda_env', self.conda_bin_L.text])

    @event.reaction('NeatSeq_bin_b.pointer_click')
    def on_NeatSeq_bin_b_click(self, *events):
        for ev in events:
            self.set_open_filepicker('NeatSeq_bin')

    @event.reaction('conda_bin_b.pointer_click')
    def on_conda_bin_b_click(self, *events):
        for ev in events:
            self.set_open_filepicker('conda_bin')

    @event.reaction('Project_dir_b.pointer_click')
    def on_Project_dir_b_click(self, *events):
        for ev in events:
            self.set_open_filepicker('Project_dir')

    @event.reaction('sample_file_b.pointer_click')
    def on_sample_file_b_click(self, *events):
        for ev in events:
            self.set_open_filepicker('sample_file_to_run')

    @event.reaction('parameter_file_b.pointer_click')
    def on_parameter_file_b_click(self, *events):
        for ev in events:
            self.set_open_filepicker('parameter_file_to_run')

    @event.reaction('NeatSeq_bin')
    def on_NeatSeq_bin(self, *events):
        for ev in events:
            if len(self.NeatSeq_bin) > 0:
                self.NeatSeq_bin_L.set_text(self.NeatSeq_bin[0][0])
                self.set_NeatSeq_bin([])

    @event.reaction('conda_bin')
    def on_conda_bin(self, *events):
        for ev in events:
            if len(self.conda_bin) > 0:
                self.conda_bin_L.set_text(self.conda_bin[0][0])
                self.set_conda_bin([])

    @event.reaction('Project_dir')
    def on_Project_dir(self, *events):
        for ev in events:
            if len(self.Project_dir) > 0:
                self.Project_dir_L.set_text(self.Project_dir[0][0])
                self.set_Project_dir([])

    @event.reaction('sample_file')
    def on_sample_file(self, *events):
        for ev in events:
            if len(self.sample_file) > 0:
                self.sample_file_L.set_text(self.sample_file[0][0])
                self.set_sample_file([])

    @event.reaction('parameter_file')
    def on_parameter_file(self, *events):
        for ev in events:
            if len(self.parameter_file) > 0:
                self.parameter_file_L.set_text(self.parameter_file[0][0])
                self.set_parameter_file([])

class Documentation_Editor(flx.Widget):
    """ A CodeEditor widget based on CodeMirror.
    """

    CSS = """
    .flx-Documentation_Editor > .CodeMirror {
        width: 100%;
        height: 100%;
        font-size: 100% ;
        font-family: Calibri;

    }
    .flx-Documentation_Editor  .cm-header { font-family: Calibri; }
    .flx-Documentation_Editor  .cm-header-1 { font-size: 160%; color: purple;}
    .flx-Documentation_Editor  .cm-header-2 { font-size: 150%; color: green;}
    .flx-Documentation_Editor  .cm-header-3 { font-size: 140%; color: yellowy;}
    .flx-Documentation_Editor  .cm-header-4 { font-size: 130%; color: blue;}
    .flx-Documentation_Editor  .cm-header-5 { font-size: 120%; color: orange;}}
    .flx-Documentation_Editor  .cm-header-6 { font-size: 110%; color: brown;}
    .flx-Documentation_Editor  .cm-strong { font-size: 120%; }
    }

    """
    value     = event.StringProp('', settable=True)
    load_flag = event.BoolProp(False, settable=True)
    text      = event.StringProp('', settable=True)
    multiline = event.BoolProp(True, settable=True)
    disabled  = event.BoolProp(False, settable=True)
    readOnly  = event.BoolProp(False, settable=True)
    options   = event.ListProp([],settable=True)

    def init(self,value=Documentation,readOnly=False,lineNumbers=True,multiline=True,styleActiveLine=True):
        global window
        self.set_value(value)
        self.set_multiline(multiline)
        self.set_readOnly(readOnly)
        # https://codemirror.net/doc/manual.html
        options = dict(value=self.value,
                        mode='markdown',
                        theme='default',
                        #theme='solarized dark',
                        #highlightFormatting=True,
                        maxBlockquoteDepth=True,
                        fencedCodeBlockHighlighting=True,
                        tokenTypeOverrides=True,
                        allowAtxHeaderWithoutSpace=True,
                        autofocus=True,
                        styleActiveLine=styleActiveLine,
                        matchBrackets=True,
                        indentUnit=4,
                        smartIndent=True,
                        lineWrapping=True,
                        lineNumbers=lineNumbers,
                        firstLineNumber=1,
                        readOnly=readOnly,
                        )
        self.cm = window.CodeMirror(self.node, options)
        self.set_load_flag(True)

    @flx.reaction('size')
    def __on_size(self, *events):
        self.cm.refresh()

    @flx.reaction('key_down')
    def __update_text(self, *events):
        if self.multiline:
            self.cm.refresh()
            self.set_value(self.cm.getValue())
        else:
            if events[0].key=='Enter':
                pos=self.cm.getCursor()
                self.cm.setValue(self.value)
                self.cm.setCursor(pos)
                self.cm.refresh()
            else:
                self.cm.refresh()
                self.set_value(self.cm.getValue())

    @flx.reaction('load_flag')
    def __load_text(self, *events):
        if self.load_flag:
            self.cm.setValue(self.value)
            self.cm.refresh()
            self.set_load_flag(False)

    @flx.reaction('disabled')
    def disable(self, *events):
        if self.disabled:
            self.cm.setOption('readOnly',self.disabled)
            self.cm.setOption('theme','solarized dark')
            self.cm.setOption('styleActiveLine',False)
            self.set_value('')
            self.set_load_flag(True)
        else:
            if self.readOnly==False:
                self.cm.setOption('readOnly',self.disabled)
            self.cm.setOption('theme','default')
            self.cm.setOption('styleActiveLine',True)
    
    @flx.reaction('options')
    def SetOption(self,*events):
        for ev in events:
            if ev.new_value!='':
                for options in self.options:
                    if len(options)==2:
                        self.cm.setOption(options[0],options[1])
                self.set_options([])
                self.set_load_flag(True)

class File_Browser(flx.GroupWidget):
    Dir           = event.DictProp({}, settable=True)
    update        = event.BoolProp(False, settable=True)
    Path          = event.StringProp('', settable=True)
    Change_Dir    = event.StringProp('', settable=True)
    Browser_Type  = event.DictProp({'select_style':'Single','select_type':'Dir'}, settable=True)
    Done          = event.BoolProp(False, settable=True)
    Selected_Path = event.ListProp([],settable=True)
    New_Dir       = event.StringProp('', settable=True)
    Preview_Path  = event.ListProp([],settable=True)
    
    #main program
    def init(self,base_path,upper_panel=True,show_size=True,columns={'Name':'','Size':'max-width: 100px;','Time':'max-width: 150px;'}):
        self._legend.style.fontSize = 'xx-large'
        self.Upper_Panel       = upper_panel
        self.Show_Size         = show_size
        self.New_Directory_str = 'Create New Directory'
        self.Parent_Dir_str    = '..'
        self.Path_Label_str    = 'Enter Path'
        self.columns           = columns
        self.Sort_By           = list(self.columns.keys())[0]
        self.Sort_How          = True
        self.First_SortBy      = 'Name'
        self.page              = 1
        self.page_limit        = 20
        self.page_names        = ['Previous Page','Next Page']
        self.set_Path(base_path)
        if self.Show_Size:
            size_style = 'visibility: visible;'
        else:
            size_style = 'visibility: hidden;'
                
        with ui.VFix(spacing=10):
            if self.Upper_Panel:
                with ui.HSplit(style='max-height: 30px;'):
                    self.Parent_Dir        = ui.Button(text=self.Parent_Dir_str,style='max-width: 30px;')
                    self.Path_Label        = ui.LineEdit(text=self.Path, placeholder_text = self.Path_Label_str,disabled=LOCK_USER_DIR)
                    self.New_Dir_Button    = ui.Button(text=self.New_Directory_str,style='max-width: 200px;')
                    self.New_Dir_Name_Edit = ui.LineEdit(placeholder_text = 'Enter New Directory Name',style='max-height: 30px;max-width: 250px;',disabled=False)
            
                
            with ui.HSplit(style='max-height: 30px;') as self.Sort_Button:
                for col in list(self.columns.keys()):
                    ui.Button(text=col,disabled=not self.Show_Size,style= size_style+'color: black; background: white;border: 2px solid gray;max-height: 30px;min-height: 30px;'+self.columns[col])
            
            with flx.Layout(style='border: 0px solid gray; overflow-y:scroll;') as self.Browser:
                with ui.HSplit(style='background: white; border: 0px solid gray;') as self.Data:
                    self.set_update(True)
            
            with ui.HSplit(style='max-height: 30px;') as self.Page_Button:
                ui.Button(text=self.page_names[0],disabled=False,style= 'font-size: 80% ; color: black; background: white;border: 2px solid gray;max-height: 30px;min-height: 30px;max-width: 150px;')
                self.page_count = ui.Button(text=str(self.page),disabled= True,style= 'font-size: 80%; color: black; background: white;border: 2px solid gray;max-height: 30px;min-height: 30px;')
                ui.Button(text=self.page_names[1],disabled=False,style= 'font-size: 80%; color: black; background: white;border: 2px solid gray;max-height: 30px;min-height: 30px;max-width: 150px;')

            with ui.HSplit(style='max-height: 30px;'):
                self.File_Name_title = ui.Label(text='File Name:',style='font-size: 120%;max-width: 100px;color:red;')
                self.File_Name_Edit  = ui.LineEdit(placeholder_text = 'Enter a File Name to Save',style='border: 2px solid red;color:red;',disabled=True)
            self.File_Name_title.apply_style('visibility: hidden;')
            self.File_Name_Edit.apply_style('visibility: hidden;')
            if self.Browser_Type['select_type']=='Save':
                self.File_Name_Edit.set_disabled(False)
            with ui.HBox(style='max-height: 40px;'):
                self.Cancel   = ui.Button(text='Cancel',style='min-width: 150px;',disabled=False)
                self.Download = ui.Button(text='Download',style='min-width: 150px;',disabled=True)
                self.OK       = ui.Button(text='OK',style='min-width: 150px;',disabled=False)
                self.Download.apply_style('visibility: hidden;')
                if self.Browser_Type['select_type']=='Open':
                    if self.Browser_Type['select_style']=='Single':
                        self.OK.set_text('Open')
                    else:
                        self.OK.set_text('Select')
                elif self.Browser_Type['select_type']=='Save':
                    self.OK.set_text('Save')
                elif self.Browser_Type['select_type']=='Download':
                    self.Cancel.set_disabled(True)
                    self.Cancel.apply_style('visibility: hidden;')
                    self.OK.set_disabled(True)
                    self.OK.apply_style('visibility: hidden;')
                    self.Download.set_disabled(False)
                    self.Download.apply_style('visibility: visible;')
                    
                    
            flx.Layout(style='max-height: 10px;')
            if self.First_SortBy in self.columns:
                self.Sort_By = self.First_SortBy
                if self.Sort_How:
                    self.Sort_How = False
                else:
                    self.Sort_How = True
                self.update_Dir()
            
    @event.reaction('Download.pointer_click')
    def Download_Button_click(self):
        selected_path=[]
        for button in self.Files.children:
            if button.checked:
                selected_path.append(button.text)
                
        self.set_Selected_Path(selected_path)
        if self.Done:
            self.set_Done(False)
        else:
            self.set_Done(True)
            
    @event.reaction('!children**.checked')
    def radio_changed(self, *events):
        ev = events[-1]
        if ev.source.text!='':
            self.set_Preview_Path([self.Path,ev.source.text])
    
    @event.reaction('Path')
    def update_path_label(self):
        if self.Upper_Panel:
            self.Path_Label.set_text(self.Path)
            
    @event.reaction('!children**.pointer_click','!children**.user_done')
    def Upper_Panel_setup(self, *events):
        for ev in events:
            if ev.type=='user_done':
                if ev.source.placeholder_text ==self.Path_Label_str:
                    self.set_Path(ev.source.text)
                    self.page = 1
                    self.page_count.set_text(str(self.page))
                    if self.update:
                        self.set_update(False)
                    else:
                        self.set_update(True)
            elif ev.source.text==self.Parent_Dir_str:
                self.set_Change_Dir('..')
                self.page = 1
                self.page_count.set_text(str(self.page))
                if self.update:
                    self.set_update(False)
                else:
                    self.set_update(True)
            elif ev.source.text==self.New_Directory_str:
                if self.New_Dir_Name_Edit.text.strip().replace(' ','_')!='':
                    self.set_New_Dir(self.New_Dir_Name_Edit.text.strip().replace(' ','_'))
            
    @event.reaction('OK.pointer_click')
    def Ok_Button_click(self):
        selected_path=[]
        if self.Browser_Type['select_type']=='Save':
                selected_path.append(self.File_Name_Edit.text)
        elif self.Browser_Type['select_type']=='Open':
            for button in self.Files.children:
                if button.checked:
                    selected_path.append(button.text)
        else:
            selected_path.append(self.Path)
        self.set_Selected_Path(selected_path)
        if self.Done:
            self.set_Done(False)
        else:
            self.set_Done(True)
            
    @event.reaction('Cancel.pointer_click')
    def Cancel_Button_click(self):
        selected_path=[]
        self.set_Selected_Path(selected_path)
        if self.Done:
            self.set_Done(False)
        else:
            self.set_Done(True)
            
    @event.reaction('!Browser.children**.pointer_click')
    def update_path_in(self, *events):
        for ev in events:
            if isinstance(ev.source.text,str) and (ev.source.parent.title=='Directory'):
                self.set_Change_Dir(ev.source.text)
                self.page = 1
                self.page_count.set_text(str(self.page))
                if self.update:
                    self.set_update(False)
                else:
                    self.set_update(True)

    @event.reaction('!Sort_Button.children**.pointer_click')
    def Sort_Files(self, *events):
        for ev in events:
            if isinstance(ev.source.text,str):
                if ev.source.text in list(self.columns.keys()):
                    self.Sort_By = ev.source.text
                    if self.Sort_How:
                        self.Sort_How = False
                    else:
                        self.Sort_How = True
                    self.update_Dir()
                    
    @event.reaction('!Page_Button.children**.pointer_click')
    def Change_Files_Page(self, *events):
        for ev in events:
            if isinstance(ev.source.text,str):
                if ev.source.text ==self.page_names[0]:
                    if self.page >1:
                        self.page = self.page - 1
                        self.page_count.set_text(str(self.page))
                        self.update_Dir()
                else:
                    if (len(self.Dir['Directory'].keys())+len(self.Dir['File'].keys()) - (self.page * self.page_limit) ) > 0:
                        self.page = self.page + 1
                        self.page_count.set_text(str(self.page))
                        self.update_Dir()
                    
    @event.reaction('Dir','Browser_Type')
    def update_Dir(self, *events):
        max_pages= 0 
        self.Data.dispose()
        if self.Browser_Type['select_type']=='Download':
            self.Cancel.set_disabled(True)
            self.Cancel.apply_style('visibility: hidden;')
            self.OK.set_disabled(True)
            self.OK.apply_style('visibility: hidden;')
            self.Download.set_disabled(False)
            self.Download.apply_style('visibility: visible;')
            self.Browser_Type['select_style']='Single'
        if self.Browser_Type['select_type']=='Save':
            self.File_Name_Edit.set_disabled(False)
            self.File_Name_Edit.apply_style('visibility: visible;')
            self.File_Name_title.apply_style('visibility: visible;')
        else:
            self.File_Name_Edit.set_disabled(True)
            self.File_Name_Edit.apply_style('visibility: hidden;')
            self.File_Name_title.apply_style('visibility: hidden;')
        if self.Browser_Type['select_type']=='Open':
            if self.Browser_Type['select_style']=='Single':
                self.OK.set_text('Open')
            else:
                self.OK.set_text('Select')
        elif self.Browser_Type['select_type']=='Save':
            self.OK.set_text('Save')
            
        if self.Show_Size:
            size_style = 'visibility: visible;'
        else:
            size_style = 'visibility: hidden;'
            
        columns = list(self.columns.keys())
        
        with self.Browser:
            with ui.HFix(spacing=1,style='background: white; border: 0px solid gray;') as self.Data:
                Dir_list   = []
                files_list = []
                if 'Directory' in  self.Dir.keys():
                    Dir_list = list(self.Dir['Directory'].keys())
                    max_pages = max_pages + len(Dir_list)
                    Dir_list.sort(key=lambda x: x.upper(),reverse = self.Sort_How)
                    #Dir_list.sort(key=lambda x: self.Dir['Directory'][x]['Time'])
                    if len(Dir_list) - ((self.page-1) * self.page_limit) > 0: 
                        if len(Dir_list) - ((self.page) * self.page_limit)>0:
                            Dir_list = Dir_list[((self.page-1) * self.page_limit) : ((self.page) * self.page_limit)]
                        else:
                            Dir_list = Dir_list[((self.page-1) * self.page_limit):]
                    else:
                        Dir_list = []
                
                if 'File' in  self.Dir.keys():
                    files_list = list(self.Dir['File'].keys())
                    max_pages = max_pages + len(files_list)
                    if self.Sort_By == columns[1]:
                        files_list.sort(key=lambda x: self.Dir['File'][x][columns[1]+'_int'],reverse = self.Sort_How)
                    elif self.Sort_By == columns[2]:
                        files_list.sort(key=lambda x: self.Dir['File'][x][columns[2]],reverse = self.Sort_How)
                    else:
                        files_list.sort(key=lambda x: x.upper(),reverse = self.Sort_How)
                    
                    if len(Dir_list) < self.page_limit: 
                        page=int(len(self.Dir['Directory'].keys())/self.page_limit)
                        
                        if len(Dir_list) + len(files_list) - ((self.page - page -1 ) * self.page_limit) > 0: 
                            files_list = files_list[((self.page -1) * self.page_limit) - len(self.Dir['Directory'].keys()) + len(Dir_list) : (( self.page * self.page_limit)) - len(self.Dir['Directory'].keys())  ]
                        else:
                            files_list = files_list[((self.page -1) * self.page_limit) - len(self.Dir['Directory'].keys()) + len(Dir_list):]
                    else:
                        files_list = []
                        
                self.page_count.set_text(str(self.page)+'/'+str(int( (max_pages /self.page_limit ))+1))
                for col in columns:
                    with ui.VFix(spacing=0,style='background: white; border: 0px solid gray;'):
                        if col == columns[0]:
                            if 'Directory' in  self.Dir.keys():
                                with ui.VFix(spacing=1,title='Directory'):
                                    for files in Dir_list: 
                                        ui.Button(text=files,style='max-height: 30px;min-height: 30px;text-align:left;border: 1px solid gray;'+self.columns[col])
                            with ui.VFix(spacing=1,title='Files') as self.Files:
                                for files in files_list: 
                                    if (self.Browser_Type['select_type']=='Open') or (self.Browser_Type['select_type']=='Download'):
                                        if self.Browser_Type['select_style']=='Single':
                                            ui.RadioButton(text=files,style='color: black; max-height: 30px;min-height: 30px;border: 0px solid gray;'+self.columns[col])
                                        else:
                                            ui.CheckBox(text=files,style='color: black; max-height: 30px;min-height: 30px;border: 0px solid gray;'+self.columns[col])
                                    else:
                                        ui.Button(text=files,disabled=True,style='color: black; background: white;border: 0px solid gray;max-height: 30px;min-height: 30px;text-align:left;'+self.columns[col])
                        else:
                            if 'Directory' in  self.Dir.keys():
                                with ui.VFix(spacing=1):
                                    for files in Dir_list:
                                        ui.Button(text=self.Dir['Directory'][files][col],disabled=True,style= size_style+'color: black; background: white;border: 0px solid gray;max-height: 30px;min-height: 30px;'+self.columns[col])
                            with ui.VFix(spacing=1):
                                for files in files_list: 
                                    ui.Button(text=self.Dir['File'][files][col],disabled=True,style=size_style+'color: black; background: white;border: 0px solid gray;max-height: 30px;min-height: 30px;text-align:right;'+self.columns[col])

class Run_File_Browser(flx.PyComponent):
    Done          = event.BoolProp(False, settable=True)
    Browser_Type  = event.DictProp({'select_style':'Single','select_type':'Dir','Regular':'.+'}, settable=True)
    Selected_Path = event.ListProp([],settable=True)
    
    #main program
    def init(self,base_path,ssh_client=None,Title='File Browser',Regular = '.+',upper_panel=True,show_size=True,show_dir=True,Preview=False):
        import os,re
        import signal
        signal.signal(signal.SIGALRM, lambda x,y: 1/0 )
        self.show_dir            = show_dir
        self.timeout             = 5
        self.ssh_client          = ssh_client
        self.sftp                = None
        self.Path                = ''
        self.Preview             = Preview
        self.Download            = Download_Link()
        self.massage             = send_massage()
        self.columns             = {'Name':'','Size':'max-width: 100px;','Time':'max-width: 150px;'}
        try:
            self.Regular  = re.compile(Regular)
        except:
            self.Regular  = re.compile('.+')
        
        if self.ssh_client!=None:
            try:
                signal.alarm(self.timeout)
                self.sftp   = self.ssh_client.open_sftp()
                if 'SSHClient' not in self.session.__dict__.keys():
                    self.session.SSHClient = [self.sftp]
                else:
                    self.session.SSHClient.append(self.sftp)
                signal.alarm(0)
            except:
                Redirect('/').go()
            
        if self.sftp!=None:
            from stat import S_ISDIR, S_ISREG
            try:
                signal.alarm(self.timeout)
                self.base_path = self.sftp.normalize(base_path)
                signal.alarm(0)
            except:
                # self.sftp      = self.ssh_client.open_sftp()
                # if 'SSHClient' not in self.session.__dict__.keys():
                    # self.session.SSHClient = [self.sftp]
                # else:
                    # self.session.SSHClient.append(self.sftp)
                self.base_path = ''
            try:
                signal.alarm(self.timeout)
                if not S_ISDIR(self.sftp.stat(self.sftp.normalize(self.base_path)).st_mode):
                    self.base_path = self.sftp.getcwd()
                else:
                    self.base_path = self.sftp.normalize(self.base_path)
                signal.alarm(0)
            except:
                Redirect('/').go()
        else:
            if os.path.isdir(base_path.strip()):
                self.base_path=os.path.abspath(base_path)
            else:
                if SERVE:
                    self.base_path=os.getcwd()
                else:
                    self.base_path=''
        self.Path = self.base_path
        with ui.VSplit(spacing=10,padding=50):
            ui.Layout(style='max-height: 10px;')
            with ui.HSplit():
                if self.Preview:
                    self.File_Browser  = File_Browser(self.base_path,upper_panel,show_size,self.columns,title=Title,style='border: 4px solid purple;')
                    self.Preview_Panel = Preview_Panel(title='Preview',style='border: 4px solid purple;') 
                else:
                    ui.Layout(style='max-width: 150px;')
                    self.File_Browser = File_Browser(self.base_path,upper_panel,show_size,self.columns,title=Title,style='border: 4px solid purple;')
                    ui.Layout(style='max-width: 150px;')
            self.progress = ui.ProgressBar(min=0,
                                           max=100,
                                           text='{value}%',
                                           style='max-height: 30px')
            self.progress.apply_style('visibility: hidden;')
            ui.Layout(style='max-height: 10px;')
    
    @event.reaction('!File_Browser.Preview_Path')
    def Preview_file(self, *events):
        import os
        if self.Preview:
            if len(self.File_Browser.Preview_Path)==2:
                path = os.path.join(self.File_Browser.Preview_Path[0],self.File_Browser.Preview_Path[1])

                if self.ssh_client!=None:
                    # try:
                        # signal.alarm(self.timeout)
                        # self.sftp.normalize('')
                        # signal.alarm(0)
                    # except:
                        # self.sftp   = self.ssh_client.open_sftp()
                        # if 'SSHClient' not in self.session.__dict__.keys():
                            # self.session.SSHClient = [self.sftp]
                        # else:
                            # self.session.SSHClient.append(self.sftp)
                    try:
                        with self.sftp.file(path, mode='rb') as file:
                            file_size = Preview_Buffer
                            file.prefetch(file_size)
                            file.set_pipelined()
                            self.Preview_Panel.set_Document_STR(str(file.read(file_size).decode('utf-8')))
                            file.close()
                    except:
                        self.Preview_Panel.set_Document_STR('')
                    self.File_Browser.set_Preview_Path([])
                else:
                    try:
                        with open(path, mode='rb') as file:
                            file_size = Preview_Buffer
                            self.Preview_Panel.set_Document_STR(str(file.read(file_size).decode('utf-8')))
                            file.close()
                    except:
                        self.Preview_Panel.set_Document_STR('')
                    self.File_Browser.set_Preview_Path([])

    def Delete_Download_File(self):
        if (self.session.status!=0):
            if Download_FileName in self.session._data:
                self.session.remove_data(Download_FileName)

    @event.reaction('File_Browser.Done')
    def when_Done(self, *events):
        import os
        if len(self.File_Browser.Selected_Path)>0:
            if self.Browser_Type['select_type']=='Dir':
                self.set_Selected_Path([self.File_Browser.Selected_Path,self.File_Browser.Selected_Path])
            elif self.Browser_Type['select_type']=='Download':
                file_name = self.File_Browser.Selected_Path[-1]
                path      = os.path.join(self.File_Browser.Path,file_name)
                if self.ssh_client!=None:
                    # try:
                        # signal.alarm(self.timeout)
                        # self.sftp.normalize('')
                        # signal.alarm(0)
                    # except:
                        # self.sftp   = self.ssh_client.open_sftp()
                        # if 'SSHClient' not in self.session.__dict__.keys():
                            # self.session.SSHClient = [self.sftp]
                        # else:
                            # self.session.SSHClient.append(self.sftp)
                    try:
                        with self.sftp.file(path, mode='rb') as file:
                            file_size = file.stat().st_size
                            if round(file_size/1000000,2) <= Download_Size_Limit:
                                file.prefetch()
                                sessions    = flx.manager.get_connections(self.session._app_name)
                                names = []
                                [names.extend(list(s._data.keys())) for s in sessions]
                                if Download_FileName not in names:
                                    size = 0
                                    total_data = bytes()
                                    while True: 
                                        data = file.read(32768) 
                                        total_data += data 
                                        if len(data) == 0: 
                                          break 
                                        size += len(data)
                                        self.progress.set_value(round(size/file_size*100,1))
                                    link = self.session.add_data(Download_FileName,
                                                                 total_data)
                                    file.close()
                                    if (self.session.status!=0):
                                        asyncio.get_event_loop().call_later(Download_TimeOut,self.Delete_Download_File)
                                    self.Download.set_link([file_name,link])
                                else:
                                    self.massage.set_massage('''Another Download is in Progress\nTry Again Later.
                                                             ''' )
                            else:
                                self.massage.set_massage('''The File Exceed the {size}MB Size Limit\nUse a Dedicated SCP Programs For large Files Transfer.
                                                         '''.format(size = str(Download_Size_Limit)) )
                    except:
                        pass
                else:
                    try:
                        with open(path, mode='rb') as file:
                            file_size = os.stat(path).st_size
                            if round(file_size/1000000,2) <= Download_Size_Limit:
                                sessions    = flx.manager.get_connections(self.session._app_name)
                                names = []
                                [names.extend(list(s._data.keys())) for s in sessions]
                                if Download_FileName not in names:
                                    size = 0
                                    total_data = bytes()
                                    while True: 
                                        data = file.read(32768) 
                                        total_data += data 
                                        if len(data) == 0: 
                                          break 
                                        size += len(data)
                                        self.progress.set_value(round(size/file_size*100,1))
                                    link = self.session.add_data(Download_FileName,
                                                                 total_data)
                                    file.close()
                                    if (self.session.status!=0):
                                        asyncio.get_event_loop().call_later(Download_TimeOut,self.Delete_Download_File)
                                    self.Download.set_link([file_name,link])
                                else:
                                    self.massage.set_massage('''Another Download is in Progress\nTry Again Later.
                                                             ''' )
                            else:
                                self.massage.set_massage('''The File Exceed the {size}MB Size Limit\nUse a Dedicated SCP Programs For large Files Transfer.
                                                         '''.format(size = str(Download_Size_Limit)) )
                    except:
                        pass
            else:
                files = []
                for file in self.File_Browser.Selected_Path:
                    files.append([os.path.join(self.File_Browser.Path,file), file])
                self.set_Selected_Path(files)
        else:
            self.set_Selected_Path([])
        if self.Done:
            self.set_Done(False)
        else:
            self.set_Done(True)

    @event.reaction('File_Browser.update')
    def update_file_sys(self, *events):
        if self.File_Browser.update:
            for ev in events:
                from stat import S_ISDIR, S_ISREG
                from datetime import datetime, timezone
                
                Dir              = {}
                Dir['Directory'] = {}
                Dir['File']      = {}
                
                if self.ssh_client!=None:
                    # try:
                        # signal.alarm(self.timeout)
                        # self.sftp.normalize('')
                        # signal.alarm(0)
                    # except:
                        # self.sftp   = self.ssh_client.open_sftp()
                        # if 'SSHClient' not in self.session.__dict__.keys():
                            # self.session.SSHClient = [self.sftp]
                        # else:
                            # self.session.SSHClient.append(self.sftp)
                    try:
                        signal.alarm(self.timeout)
                        Path    = self.sftp.normalize(self.File_Browser.Path)
                        self.sftp.chdir(Path)
                        signal.alarm(0)
                    except:
                        Path        = self.Path
                        # self.sftp   = self.ssh_client.open_sftp()
                        # if 'SSHClient' not in self.session.__dict__.keys():
                            # self.session.SSHClient = [self.sftp]
                        # else:
                            # self.session.SSHClient.append(self.sftp)
                else:
                    if self.File_Browser.Path=='':
                        Path = os.getcwd()
                    else:
                        Path = os.path.abspath(self.File_Browser.Path)
                        
                if self.File_Browser.Change_Dir != '':
                    if self.File_Browser.Change_Dir == '..':
                        self.File_Browser.set_Change_Dir('')
                        if (Path != self.base_path) or (not LOCK_USER_DIR):
                            Path = os.path.split(Path)[0]
                    else:
                        Path = os.path.join(Path,self.File_Browser.Change_Dir)
                        self.File_Browser.set_Change_Dir('')
                
                try:
                    columns = list(self.columns.keys())
                    if self.ssh_client!=None:
                        # try:
                            # signal.alarm(self.timeout)
                            # self.sftp.normalize('')
                            # signal.alarm(0)
                        # except:
                            # self.sftp   = self.ssh_client.open_sftp()
                            # if 'SSHClient' not in self.session.__dict__.keys():
                                # self.session.SSHClient = [self.sftp]
                            # else:
                                # self.session.SSHClient.append(self.sftp)
                        
                        signal.alarm(self.timeout)
                        for entry in self.sftp.listdir_attr(Path):
                            if S_ISDIR(entry.st_mode):
                                if self.show_dir:
                                    Dir['Directory'][entry.filename]={}
                                    Dir['Directory'][entry.filename][columns[1]]='Directory'
                                    Dir['Directory'][entry.filename][columns[2]]=''
                            elif self.Regular.fullmatch(entry.filename):
                                Dir['File'][entry.filename]={}
                                size = entry.st_size
                                Dir['File'][entry.filename][columns[1]+'_int'] = size
                                if size>1000:
                                    if size>1000000:
                                        if size>1000000000:
                                            Dir['File'][entry.filename][columns[1]]="{0:.2f}".format(round(size/1000000000,2))+'GB'
                                        else:
                                            Dir['File'][entry.filename][columns[1]]="{0:.2f}".format(round(size/1000000,2))+'MB'
                                    else:
                                        Dir['File'][entry.filename][columns[1]]="{0:.2f}".format(round(size/1000,2))+'KB'
                                else:
                                    Dir['File'][entry.filename][columns[1]] = str(size)+'B'
                                time = entry.st_mtime
                                Dir['File'][entry.filename][columns[2]] = datetime.fromtimestamp(time).strftime('%Y-%m-%d-%H:%M')
                                
                        signal.alarm(0)
                    else:
                        with os.scandir(Path) as it:
                            for entry in it:
                                if entry.is_dir():
                                    if self.show_dir:
                                        Dir['Directory'][entry.name]={}
                                        Dir['Directory'][entry.name][columns[1]]='Directory'
                                        Dir['Directory'][entry.name][columns[2]]=''
                                elif self.Regular.fullmatch(entry.name):
                                    Dir['File'][entry.name]={}
                                    size = entry.stat().st_size
                                    Dir['File'][entry.name][columns[1]+'_int'] = size
                                    if size>1000:
                                        if size>1000000:
                                            if size>1000000000:
                                                Dir['File'][entry.name][columns[1]]="{0:.2f}".format(round(size/1000000000,2))+'GB'
                                            else:
                                                Dir['File'][entry.name][columns[1]]="{0:.2f}".format(round(size/1000000,2))+'MB'
                                        else:
                                            Dir['File'][entry.name][columns[1]]="{0:.2f}".format(round(size/1000,2))+'KB'
                                    else:
                                        Dir['File'][entry.name][columns[1]]=str(size)+'B'
                                    time = entry.stat().st_mtime
                                    Dir['File'][entry.name][columns[2]] = datetime.fromtimestamp(time).strftime('%Y-%m-%d-%H:%M')
                    self.File_Browser.set_Path(Path)
                    self.Path = Path
                    self.File_Browser.set_Dir(Dir)
                except  BaseException as e:
                    print(str(e))
                    # if self.ssh_client!=None:
                        # self.sftp   = self.ssh_client.open_sftp()
                        # if 'SSHClient' not in self.session.__dict__.keys():
                            # self.session.SSHClient = [self.sftp]
                        # else:
                            # self.session.SSHClient.append(self.sftp)
                    self.File_Browser.set_Path(self.Path)
                self.File_Browser.set_update(False)

    @event.reaction('Browser_Type')
    def update_Browser_Type(self,*events):
        import re
        if self.Browser_Type['select_type']=='Download':
            self.progress.apply_style('visibility: visible;')
        else:
            self.progress.apply_style('visibility: hidden;')
        if 'Regular' in self.Browser_Type.keys():
            try:
                self.Regular  = re.compile(self.Browser_Type['Regular'])
            except:
                self.Regular  = re.compile('.+')
        self.File_Browser.set_Browser_Type(self.Browser_Type)

    @event.reaction('File_Browser.New_Dir')
    def create_new_dir(self,*events):
        Path = os.path.abspath(self.File_Browser.Path)
        Path = os.path.join(Path,self.File_Browser.New_Dir)
        try:
            if self.sftp!=None:
                signal.alarm(self.timeout)
                self.sftp.mkdir(Path)
                signal.alarm(0)
            else:
                os.mkdir(Path)
        except :
            pass
            # if self.sftp!=None:
                # try:
                    # self.sftp.close()
                # except:
                    # pass
                # self.sftp   = self.ssh_client.open_sftp()
                # if 'SSHClient' not in self.session.__dict__.keys():
                    # self.session.SSHClient = [self.sftp]
                # else:
                    # self.session.SSHClient.append(self.sftp)

        self.File_Browser.set_update(True)

class Preview_Panel(flx.GroupWidget):
    Document_STR = event.StringProp('', settable=True)
    
    def init(self):
        with flx.Layout(style='border: 0px solid gray; '):
            self._legend.style.fontSize = 'xx-large'
            with ui.VSplit(spacing=20,padding=20):
                self.Document               = Documentation_Editor('',
                                                                 True,
                                                                 False,
                                                                 True,
                                                                 False,
                                                                 style='border: 0px solid red;')
                
                self.Document.set_options([['mode','yaml'],['lineWrapping',False]])
            #self.Document.set_disabled(True) 

    @event.reaction('Document_STR')
    def update_Document(self,*events):
        self.Document.set_value(self.Document_STR)
        self.Document.set_load_flag(True)

class Empty_class(flx.PyComponent):
    Done          = event.BoolProp(False, settable=True)
    def init(self):
        pass

class Results(flx.PyComponent):
    Done          = event.BoolProp(False, settable=True)
    def init(self,path,ssh_client):
        select_style = 'Single'
        select_type  = 'Download'
        wildcard     = '*'
        Regular = wildcard.replace('*','.+')
        with ui.Layout(title='Results'):
            self.Browser  = Run_File_Browser(path,ssh_client,'File Browser','.+',True,True,True,True)
        self.Browser.set_Browser_Type({'select_style':select_style,'select_type':select_type,'Regular':Regular})

class Option_Menu(ui.HFix):
    Done             = event.BoolProp(False, settable=True)
    Selected_Option  = event.StringProp('', settable=True)
    
    def init(self,options = ['New Work-Flow','Load Work-Flow','Choose a Work-Flow From Repository']):
        ui.Layout()
        with ui.VFix():
            ui.Layout()
            with ui.GroupWidget(title='Option Menu',style='border: 4px solid purple;'):
                with ui.VFix(padding=25):
                    for Button in options:
                        ui.RadioButton(text=Button)
                    ui.Layout()
                    self.Choose = ui.Button(text='Choose')
            ui.Layout()
        ui.Layout()

    @event.reaction('!children**.checked')
    def radio_changed(self, *events):
        ev = events[-1]
        if ev.source.text!='':
            self.set_Selected_Option(ev.source.text)
            
    @event.reaction('Choose.pointer_click')
    def Option_Selescted(self, *events):
        if  self.Selected_Option!='':
            self.set_Done(True)

def Reconnect_SSH(ssh_client):
    try:
        import paramiko
        transport  = ssh_client.get_transport()
        ssh_client_ = paramiko.SSHClient()
        ssh_client_.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
        ssh_client_.connect(transport.getpeername()[0], username=transport.get_username(), password=transport.auth_handler.password,port=transport.getpeername()[1])
    except:
        ssh_client_.close()
    return   ssh_client_

class Rainbow(flx.CanvasWidget):
    def init(self):
        global Math, window
        self.colors        = ["red", "orange", "yellow","LightSeaGreen","green","Cyan", "blue","DeepSkyBlue" ,"violet","Purple "]
        self.ctx           = self.node.getContext('2d')
        self.lineWidth     = 5
        self.ctx.lineWidth = self.lineWidth

        i=0
        self.speed = {}
        self.angle = {}
        self.direction = {}
        for color in self.colors:
            self.speed[color] = 5 + Math.random()*5
            self.angle[color] = Math.PI / 4
            self.direction[color] = 0
        self.draw()
        # window.setInterval(self.draw, 100/7 )
        
        
    def drawArc(self, radius, color, angle):
        global Math, window
        w, h = self.size
        self.ctx.beginPath()
        self.ctx.strokeStyle = color
        self.ctx.lineWidth = self.lineWidth
        self.ctx.arc(w*0.5, h*0.5, radius, angle, angle- Math.PI/2 , True)
        self.ctx.stroke();
        self.ctx.closePath()
        
        
    def makeArc(self,radius, color):
        global Math, window
        self.drawArc(radius, color, self.angle[color])
        self.direction[color] += Math.PI / 180
        self.angle[color] += Math.PI / 180 * Math.sin(self.direction[color])  * self.speed[color]  
        

    def draw(self):
        global Math, window
        w, h = self.size
        #self.ctx.clearRect(0, 0, w, h)
        self.ctx.fillStyle = 'rgba(256, 256, 256, 0.4)'
        self.ctx.fillRect(0, 0, w, h)
        i = 0
        for color in self.colors:
            i+=1
            self.makeArc(10 + i * 9, color ) # 
        window.setTimeout(self.draw, 100/7 )

def LoadingWin(string='Collecting Data'):
    with ui.HSplit():
        ui.Layout()
        with ui.VSplit():
            ui.Layout()
            with flx.GroupWidget(title=string,style='font-size: 200%; border: 0px solid purple;'):
                with ui.VBox():
                    # Rainbow(style='min-height: 200px; min-width: 200px; ')
                    ui.ImageWidget(stretch=False,
                                   source='https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/neatseq_flow_gui/Loading.gif')
                                   #source='https://i.pinimg.com/originals/0c/28/08/0c28087b5cedf7276ee6c8d81e28d328.gif')
                    ui.Widget()  # Spacing
            ui.Layout()
        ui.Layout()

class NeatSeq_Flow_GUI(app.PyComponent):
    CSS = """
        .flx-LineEdit {
            border: 2px solid #9d9;
            border-radius: 5px;
            transition: all 0.5s;
        }
        .flx-CanvasWidget > canvas {
            /* Set position to absolute so that the canvas is not going
             * to be forcing a size on the container div. */
            position: absolute;
            
        }

        .flx-TreeWidget {
            background: white;
            color: black;
            border: 5px solid white;
            overflow-y: auto;
            overflow-x: auto;
            transition: all 0.5s;
        }
        .flx-FormLayout{
            background: white;
            padding: 10px;
            border: 5px solid white;
            border-radius: 10px;
            transition: all 0.5s;
        }

        .flx-ComboBox > ul   {
                position: fixed;
                min-height: 100px;
                max-height: 200px;
                min-width: 300px;
                width:  300px;
                background: white;
                z-index: 10001;
                display: none;
                overflow-y: scroll;
                overflow-x: auto;
            }


      .flx-Button {
          border: 1px solid white;
          color: white;
          background-color: #555555;
          text-align: center;
          transition: all 0.3s;
          cursor: pointer;
        }

    .flx-Button:after {
          content: "";
          position: absolute;
          top: 0;
          right: -20px;
          transition: 0.5s;
        }

    .flx-Button:hover  {
          border: 1px solid black;
          color: black;
          background-color: white;
          padding-right: 25px;
        }

    .flx-Button:hover:after {
          right: 0;
        }


     .flx-Graphical_panel .flx-Button {
          color: black;
          border-radius: 8px;
          background-color: white;
          border: 2px solid gray;
          box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
          text-align: center;
          transition: all 0s;
          cursor: pointer;
          padding: 0.2em 0.4em;
          white-space: nowrap;
        }



    .flx-Graphical_panel .flx-Button:after {
          content: "";
          position: absolute;
          text-align: center;
          top: 0;

          transition: 0s;
        }

    .flx-Graphical_panel .flx-Button:hover  {
          text-align: center;
          transition: 0s;
          transform: scale(1.1);
          background: #e8eaff;
          margin: 2px;
        }

    .flx-Graphical_panel .flx-Button:active  {
          border: 2px solid blue;
          text-align: center;
          transition: 0s;
          transform: scale(1);
          box-shadow: 0px 0px 3px 1px rgba(0, 100, 200, 0.7);
        }

    .flx-Graphical_panel .flx-Button:hover:after {
          right: 0;
          text-align: center;
          transition: 0.3s;
        }


     .flx-TabLayout > .flx-tabbar > .flx-tab-item.flx-current {
        background: #eaecff;
        border-top: 8px solid #7bf;
        margin-top: 0;
    }

        """
    
    Running_script               = event.IntProp(0, settable=True)
    Generating_scripts           = event.IntProp(0, settable=True)
    Running_Commands             = event.DictProp({}, settable=True)
    Kill_Run                     = event.IntProp(0, settable=True)
    Recovery                     = event.IntProp(0, settable=True)
    Locate_Failures              = event.IntProp(0, settable=True)
    
    
    def init(self,path,ssh_client=None,WOKFLOW_DIR=None):
        self.send_massage = None
        self.ssh_client = ssh_client
        if self.ssh_client!=None:
            if 'SSHClient' not in self.session.__dict__.keys():
                self.session.SSHClient = [self.ssh_client]
            else:
                self.session.SSHClient.append(self.ssh_client)
            try:
                from stat import S_ISDIR, S_ISREG
                self.sftp = self.ssh_client.open_sftp()
                Test_sftp_alive(self.ssh_client)
            except:
                self.sftp = None
                
            if 'SSHClient' not in self.session.__dict__.keys():
                if self.sftp!=None:
                    self.session.SSHClient = [self.sftp]
            else:
                if self.sftp!=None:
                    self.session.SSHClient.append(self.sftp)
        else:
            self.sftp = None
        
        if SERVE:
            self.send_massage = send_massage()
        
        self.filepicker_key = ''
        with ui.StackLayout(flex=1) as self.stack:
            with ui.VSplit() as self.MainStack:
                with ui.TabLayout(flex=0.9) as self.TabLayout2:
                    with ui.TabLayout(flex=0.9,title='Work-Flow',style='color: blue;') as self.TabLayout:
                        self.step_info = Step_Tree_Class(title='Design', style='padding-top: 10px;color: black;')
                        self.vars_info = Only_Tree_Class(VARS, title='Vars', style='padding-top: 10px;color: black;')
                        self.cluster_info = Only_Tree_Class(CLUSTER, title='Cluster', style='padding-top: 10px;color: black;')
                        self.Documentation = Documentation_Editor(title='Documentation', style='padding-top: 10px;color: black;')
                    self.samples_info = Samples_info(title='Samples')
                    self.Run  = Run_NeatSeq_Flow(SERVE,title='Run')
                    if SERVE:
                        import Monitor_GUI
                        with ui.Widget(title='Monitor') as self.Monitor:
                            with ui.Layout() as self.Monitor_Widget:
                                self.monitor      = Monitor_GUI.Monitor_GUI(path)
                                self.Test_Monitor = Test_Monitor_Command(self.monitor)
                        self.Results = Results(path,self.ssh_client)
                    self.Help    = ui.IFrame(url=Base_Help_URL,
                                          title='Help')
                
                self.label = ui.Label(text='NeatSeq-Flow Graphical User Interface By Liron Levin',
                                      style='padding-left: 40px; background: #e8eaff; min-height: 15px; font-size:15px; transition: all 0.5s;')
                self.label.set_capture_mouse(2)
                self.label.set_html(html_cite)
                self.TabLayout.set_capture_mouse(2)
                self.TabLayout2.set_capture_mouse(2)
                self.Terminal_string = ''
                Add_Tooltip(self.label,HELP['cite'])
            with ui.Widget(flex=1) as self.Browser_W:
                self.Browser         = Run_File_Browser(path,self.ssh_client)
            with ui.Widget(style='background:white;') as self.LoadingWin:
                LoadingWin()
            if SERVE:
                with ui.Widget(flex=1) as self.Option_Menu_w:
                    if (WOKFLOW_DIR != None):
                        self.Option_Menu = Option_Menu(['New Work-Flow','Load Work-Flow','Choose a Work-Flow From Repository'])
                    else:
                        self.Option_Menu = Option_Menu(['New Work-Flow','Load Work-Flow'])
                    self.Option_Menu_w.apply_style('font-size:110%;')
                    self.stack.set_current(self.Option_Menu_w)
                    
                if (WOKFLOW_DIR != None):
                    with ui.Widget(flex=1) as self.workflow_select_w:
                        self.workflow_select = Run_File_Browser(WOKFLOW_DIR,self.ssh_client,'Select a Work-Flow','.+yaml$',False,False,False)
                        self.workflow_select.set_Browser_Type({'select_style':'Single','select_type':'Open'})
                        self.workflow_select_w.apply_style('font-size:140%;')
                else:
                    self.workflow_select = Empty_class()
            else:
                self.workflow_select = Empty_class()
                self.Option_Menu     = Empty_class()
                
        if not SERVE:
            self.stack.apply_style('font-size:80%;')
        self.Run_FUN = Run_function_in_thread()

    @event.reaction('!Option_Menu.Done')
    def Option_Menu_Done(self,*events):
        for ev in events:
            if ev.source.Done:
                ev.source.set_Done(False)
                if ev.source.Selected_Option=='Load Work-Flow':
                    self.step_info.set_open_filepicker('workflow_file')
                elif ev.source.Selected_Option=='Choose a Work-Flow From Repository':
                    self.filepicker_key  = 'workflow_file'
                    self.stack.set_current(self.workflow_select_w)
                else:
                    self.stack.set_current(self.MainStack)
                    self.label.set_flex(0.02)
    
    @event.reaction('Browser.Done','!workflow_select.Done')
    def when_File_Browser_Done(self,*events):
        for ev in events:
            if ev.source.Done:
                ev.source.set_Done(False)
                if self.filepicker_key  == 'workflow_file':
                    import re
                    if len(ev.source.Selected_Path)>0:
                        sample_file = ev.source.Selected_Path[0][0]
                        sample_file = re.sub('.yaml$','',sample_file)
                        if ev.source.ssh_client!=None:
                            import os,re
                            # import signal
                            # timeout = 2
                            # signal.signal(signal.SIGALRM, lambda x,y: 1/0 )
                            try:
                                sftp = ev.source.sftp
                                # signal.alarm(timeout)
                                # sftp   = ev.source.ssh_client.open_sftp()
                                # if 'SSHClient' not in self.session.__dict__.keys():
                                    # self.session.SSHClient = [sftp]
                                # else:
                                    # self.session.SSHClient.append(sftp)
                                # signal.alarm(0)
                            except:
                                sftp   = None
                            
                            if sftp!=None:
                                try:
                                    sftp.stat(sample_file)
                                    self.filepicker_key  = 'load_samples_file'
                                    self.set_filepicker_options([[sample_file],[os.path.basename(sample_file)]])
                                except:
                                    pass
                        else:
                            try:
                                os.stat(sample_file)
                                self.filepicker_key  = 'load_samples_file'
                                self.set_filepicker_options([[sample_file],[os.path.basename(sample_file)]])
                            except:
                                pass
                        self.filepicker_key  = 'workflow_file'
                        self.set_filepicker_options(ev.source.Selected_Path)
                        self.stack.set_current(self.MainStack)
                        # self.label.set_flex(0.02)
                    else:
                        self.stack.set_current(self.MainStack)
                        self.label.set_flex(0.02)
                else:
                    self.set_filepicker_options(ev.source.Selected_Path)
                    self.stack.set_current(self.MainStack)
                    # self.label.set_flex(0.02)
            
    @event.reaction('label.pointer_click')
    def on_label_click(self, *events):
        self.label.set_flex(0.2)
        asyncio.get_event_loop().call_later(5, self.label.set_flex,0.02)
    
    def select_files(self,select_style='Single', select_type='Open', wildcard='*'):
        if SERVE:
            Regular = wildcard.replace('*','.+')
            self.Browser.set_Browser_Type({'select_style':select_style,'select_type':select_type,'Regular':Regular})
            self.stack.set_current(self.Browser_W)
            self.Browser.File_Browser.set_update(True)
        else:
            try:
                import wx, os
                app = wx.App(None)
                if select_type == 'Open':
                    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
                    if select_style != 'Single':
                        style = style | wx.FD_MULTIPLE
                elif select_type == 'Dir':
                    style = wx.DD_DEFAULT_STYLE
                else:
                    style = wx.FD_SAVE
                if select_type == 'Dir':
                    dialog = wx.DirDialog(None, "Choose Directory", "", style=style)
                else:
                    dialog = wx.FileDialog(None, select_type, wildcard=wildcard, style=style)
                if dialog.ShowModal() == wx.ID_OK:
                    if select_type == 'Dir':
                        path = dialog.GetPath()
                        dialog.Destroy()
                        if len(path)>0:
                            self.Browser.set_Selected_Path([[path, path]])
                            self.Browser.set_Done(True)
                            return 
                        else:
                            self.Browser.set_Selected_Path([])
                            self.Browser.set_Done(True)
                            return 
                    else:
                        path = dialog.GetPaths()
                    files = []
                    for file in path:
                        files.append([file, os.path.basename(file)])
                    if len(files) > 0:
                        path = files
                    else:
                        path = []

                else:
                    path = []

                dialog.Destroy()
                self.Browser.set_Selected_Path(path)
                self.Browser.set_Done(True)
                return 
            except:
                import os
                from tkinter import filedialog
                from tkinter import Tk

                Tk().withdraw()
                path = []
                if select_type == 'Open':
                    if select_style == 'Single':
                        path = [filedialog.askopenfilename(title='Choose a file')]
                    else:
                        path = list(filedialog.askopenfilenames(title='Choose files'))
                elif select_type == 'Dir':
                    path = filedialog.askdirectory(title="Choose Directory")
                    if len(path)>0:
                        self.Browser.set_Selected_Path([[path, path]])
                        self.Browser.set_Done(True)
                        return 
                else:
                    path = [filedialog.asksaveasfilename(title='Save')]

                files = []
                for file in path:
                    if len(file)>0:
                        files.append([file, os.path.basename(file)])
                if len(files) > 0:
                    path = files
                else:
                    path = []
                self.Browser.set_Selected_Path(path)
                self.Browser.set_Done(True)
                return 
    
    # @event.reaction('label.pointer_move')
    # def on_label_move(self, *events):
        # self.label.set_flex(0.2)
    
    # @event.reaction('TabLayout2.pointer_move')
    # def on_label_after(self, *events):
        # self.label.set_flex(0.02)
    
    def filepicker_options(self, key):
        options = {'file_path'            : lambda: self.select_files('Single', 'Open'),
                   'NeatSeq_bin'          : lambda: self.select_files('Single', 'Open'),
                   'conda_bin'            : lambda: self.select_files('Single', 'Dir'),
                   'Project_dir'          : lambda: self.select_files('Single', 'Dir'),
                   'sample_file_to_run'   : lambda: self.select_files('Single', 'Open'),
                   'parameter_file_to_run': lambda: self.select_files('Single', 'Open'),
                   'Cluster_file_path'    : lambda: self.select_files('Single', 'Open'),
                   'Vars_file_path'       : lambda: self.select_files('Single', 'Open'),
                   'workflow_file'        : lambda: self.select_files('Single', 'Open'),
                   'save_workflow_file'   : lambda: self.select_files('Single', 'Save'),
                   'project'              : lambda: self.select_files(select_style='Multy'),
                   'samples'              : lambda: self.select_files(select_style='Multy'),
                   'load_samples_file'    : lambda: self.select_files('Single', 'Open'),
                   'save_samples_file'    : lambda: self.select_files('Single', 'Save'),
                   'step_export_file'     : lambda: self.select_files('Single', 'Save'),
                   'Load_step_file'       : lambda: self.select_files('Single', 'Open','*.step')
                   }
        if key in options.keys():
            self.filepicker_key = key
            return options[key]()
        else:
            self.filepicker_key = ''
            return None
    
    def set_filepicker_options(self,Selected_Path):
        options = {'file_path'            : lambda: self.step_info.set_file_path(Selected_Path),
                   'NeatSeq_bin'          : lambda: self.Run.set_NeatSeq_bin(Selected_Path),
                   'conda_bin'            : lambda: self.Run.set_conda_bin(Selected_Path),
                   'Project_dir'          : lambda: self.Run.set_Project_dir(Selected_Path),
                   'sample_file_to_run'   : lambda: self.Run.set_sample_file(Selected_Path),
                   'parameter_file_to_run': lambda: self.Run.set_parameter_file(Selected_Path),
                   'Cluster_file_path'    : lambda: self.cluster_info.set_file_path(Selected_Path),
                   'Vars_file_path'       : lambda: self.vars_info.set_file_path(Selected_Path),
                   'workflow_file'        : lambda: self.step_info.set_workflow_file(Selected_Path),
                   'save_workflow_file'   : lambda: self.step_info.set_save_workflow_file(Selected_Path),
                   'project'              : lambda: self.samples_info.set_project_files(Selected_Path),
                   'samples'              : lambda: self.samples_info.set_sample_files(Selected_Path),
                   'load_samples_file'    : lambda: self.samples_info.set_load_samples_file(Selected_Path),
                   'save_samples_file'    : lambda: self.samples_info.set_save_samples_file(Selected_Path),
                   'step_export_file'     : lambda: self.step_info.set_step_export_file(Selected_Path),
                   'Load_step_file'       : lambda: self.step_info.set_Load_step_file(Selected_Path)
                   }
        if self.filepicker_key in options.keys():
            return options[self.filepicker_key]()
        else:
            return None
    
    def command_pars(self, key):
        options = {'conda_env':        lambda: self.conda_env_options(key[1]),
                   'Generate_scripts': lambda: self.Generate_scripts_command(key[1], key[2], key[3], key[4], key[5],
                                                                             key[6]),
                   'Run_scripts':      lambda: self.Run_scripts_command(key[1]),
                   'Kill_Run':         lambda: self.Kill_Run_command(key[1]),
                   'Recovery':         lambda: self.Recovery_command(key[1]),
                   'Locate_Failures':  lambda: self.Locate_Failures_command(key[1]),
                   'Run_Monitor':      lambda: self.Run_Monitor_command(key[1]),
                   'Tags':             lambda: self.Search_Tags(key[1]),

                   }
        if key[0] in options.keys():
            return options[key[0]]()
        else:
            return None
    
    def conda_env_options(self, conda_bin):
        import os
        from subprocess import Popen, PIPE, STDOUT
        options      = []
        temp_command = ''
        if len(conda_bin) > 0:
            temp_command = conda_bin
        temp_command = os.path.join(temp_command, 'conda')
        temp_command = temp_command + ' info --env'
        err_flag = False
        try:
            self.Run.set_Terminal(self.Terminal_string + '[Searching for Conda Environments]: Searching...\n')
            if self.ssh_client!= None:
                SSH = Popen_SSH(self.session,self.ssh_client,temp_command)
                [outs, errs , exit_status] = SSH.output()
                SSH.kill()
                if exit_status!=0:
                    err_flag = True
            else:
                conda_proc = Popen(temp_command, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
                outs, errs = conda_proc.communicate(timeout=15)

        except :
            err_flag = True
            if self.ssh_client == None:
                conda_proc.kill()
                outs, errs = conda_proc.communicate()

        if len(errs) > 0:
            self.Terminal_string = self.Terminal_string + '[Searching for Conda Environments]: Error:\n' + errs
        if err_flag:
            self.Terminal_string = self.Terminal_string + '[Searching for Conda Environments]: Finished with Error!! \n'
        elif len(outs) > 0:
            options = list(map(lambda y: y.split(os.sep)[0].replace('*', '').replace(' ', ''),
                           filter(lambda x: len(x.split(os.sep)) > 1, outs.split('\n'))))
            self.Run.set_conda_env(options)
            if len(options) > 0:
                self.Terminal_string = self.Terminal_string +  ' [Searching for Conda Environments]: '+ str(len(options)) + ' Conda Environments were found \n'
        
        self.Run.set_Terminal(self.Terminal_string)
        return options
    
    def Generate_scripts_command(self, NeatSeq_bin, conda_bin, conda_env, Project_dir, sample_file, parameter_file):
        import os,re
        from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
        
        errs  = ''
        outs  = ''
        Error = ''
        if self.Generating_scripts==0:
            if len(Project_dir) == 0:
                Error = Error + '[Error]: No Project Directory\n'
            
            if len(conda_bin) > 0:
                if self.sftp !=None:
                    try:
                        signal.alarm(5)
                        listdir   = self.sftp.listdir(conda_bin)
                        signal.alarm(0)
                    except:
                        listdir   = []
                # if self.ssh_client != None:
                    # try:
                        # self.sftp.close()
                    # except:
                        # pass
                    # try:
                        # signal.alarm(5)
                        # self.sftp = self.ssh_client.open_sftp()
                        # if 'SSHClient' not in self.session.__dict__.keys():
                            # self.session.SSHClient = [self.sftp]
                        # else:
                            # self.session.SSHClient.append(self.sftp)
                        # listdir   = self.sftp.listdir(conda_bin)
                        # signal.alarm(0)
                    # except:
                        # listdir   = []
                else:
                    try:
                        listdir   = os.listdir(conda_bin)
                    except:
                        listdir   = []
                if not (('conda' in listdir) and ('activate' in listdir)):
                    Error = Error + '[Error]: Your Conda Bin is incorrect\n[Error]: Make Sure the Programs: "conda" and "activate" are located within the Conda Bin Directory\n'
            
            if  (len(conda_env)==0) and (len(Error))==0:
                if len(conda_bin) > 0:
                    options = self.conda_env_options(conda_bin)
                else:
                    options = self.conda_env_options('')
                if len(options)>0:
                    if NeatSeq_Flow_Conda_env in options:
                        conda_env = NeatSeq_Flow_Conda_env
                        self.Terminal_string = self.Terminal_string + '[Note]: The Conda Environment '+ NeatSeq_Flow_Conda_env+' Was Detected and will be used to Generated Scripts\n[Note]:If You want to use a different NeatSeq Flow Environment, Choose an Environment from the "Conda environment to use" Drop-Down Menu\n\n'
                        # self.Run.set_Terminal(self.Terminal_string + '[Note]: The Conda Environment '+ NeatSeq_Flow_Conda_env+' Was Detected and will be used to Generated Scripts\n[Note]:If You want to use a different NeatSeq Flow Environment, Choose an Environment from the "Conda environment to use" Drop-Down Menu\n')
                    else:
                        self.Terminal_string = self.Terminal_string + '[Note]: A NeatSeq-Flow Conda Environment Could NOT be Detected!!! \n[Note]: You Can Look for a NeatSeq Flow Environment from the "Conda environment to use" Drop-Down Menu\n\n'
                        # self.Run.set_Terminal(self.Terminal_string + '[Note]: A NeatSeq-Flow Conda Environment Could NOT be Detected!!! \n[Note]: You Can Look for a NeatSeq Flow Environment from the "Conda environment to use" Drop-Down Menu\n')
                        
            if len(NeatSeq_bin) > 0:
                temp_command = ''
                if len(conda_env) > 0:
                    # temp_command = 'bash  '
                    # temp_command = temp_command + 'source '
                    if len(conda_bin) > 0:
                        temp_command = temp_command + 'source '
                        temp_command = temp_command + os.path.join(conda_bin, 'deactivate')+';;source '
                        temp_command = temp_command + os.path.join(conda_bin, 'activate') + ' ' + conda_env + ';'
                        temp_command = temp_command + 'export CONDA_BASE=$(' + os.path.join(conda_bin,
                                                                                            'conda') + ' info --root) ;'
                    else:
                        temp_command = temp_command + 'export CONDA_BASE=$(conda  info --root); '
                        temp_command = temp_command + 'source $CONDA_BASE/bin/activate '+ conda_env + ';'
                        
                elif self.ssh_client == None:
                    if 'CONDA_PREFIX' in os.environ.keys():
                        temp_command = temp_command + 'export CONDA_BASE=$(conda  info --root); '

                if NeatSeq_bin.startswith(os.sep):
                    temp_command = temp_command + ' python ' + NeatSeq_bin
                else:
                    temp_command = temp_command + ' ' + NeatSeq_bin

                if len(sample_file) > 0:
                    temp_command = temp_command + ' -s ' + sample_file
                else:
                    Error = Error + '[Error]: No Sample File\n'

                if len(parameter_file) > 0:
                    temp_command = temp_command + ' -p ' + parameter_file
                else:
                    Error = Error + '[Error]: No Parameter File\n'

                if len(Project_dir) > 0:
                    temp_command = temp_command + ' -d ' + Project_dir
                else:
                    Error = Error + '[Error]:No Project directory \n'
                
                if self.sftp!= None:
                    try:
                        logs_files = list(filter(lambda x: len(re.findall('log_[0-9]+.txt$',x))>0,
                                          list(self.sftp.listdir(self.sftp.normalize(os.path.join(Project_dir,'logs'))))))
                    except:
                        logs_files = []
                        
                    if len(logs_files)>0:
                        temp_command = temp_command + ' -r curr '
                        
                else:
                    if os.path.exists(os.path.join(Project_dir,'logs')):
                        logs_files = list(filter(lambda x: len(re.findall('log_[0-9]+.txt$',x))>0,
                                            os.listdir(os.path.join(Project_dir,'logs') )))
                        if len(logs_files)>0:
                            temp_command = temp_command + ' -r curr '


                if len(Error) == 0:
                    err_flag = False
                    # import sys
                    # sys.setprofile(tracefunc)
                    try:
                        self.Run.set_Terminal(self.Terminal_string + '[Generating_scripts]:  Generating...\n')
                        self.Running_Commands['Generating_scripts'] =  Run_command_in_thread2(self.session,temp_command,self.ssh_client)
                        self.Running_Commands['Generating_scripts'].Run()
                        self.set_Generating_scripts(self.Generating_scripts+1)
                    except BaseException as e:
                        print(e)
                        pass
                else:
                    self.Run.set_Terminal(Error)
    
    def Search_Tags(self,Project_dir):
        import os,re
        # if len(Project_dir) != 0:
            # Project_dir=os.getcwd()
        if len(Project_dir) > 0:
            try:
                dname = os.path.join(Project_dir,'scripts', 'tags_scripts')
                if self.sftp!= None:
                    options=list(map(lambda y: re.sub('\.sh$','',y) ,list(filter(lambda x: x.endswith('.sh'),self.sftp.listdir( self.sftp.normalize(dname) )))))
                    options.insert(0,self.Run.Tags[0])
                    self.Run.set_Tags(options)
                else:
                    if os.path.isdir(dname):
                        options=list(map(lambda y: re.sub('\.sh$','',y) ,list(filter(lambda x: x.endswith('.sh'),os.listdir(dname)))))
                        options.insert(0,self.Run.Tags[0])
                        self.Run.set_Tags(options)
            except:
                self.Run.set_Tags([self.Run.Tags[0]])
    
    def Run_scripts_command(self,Project_dir):
        import os
        from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
        
        Error = ''
        temp_command = ''
            
        if len(Project_dir) > 0:
            if self.sftp!= None:
                if self.Run.Tag_selected!=self.Run.Tags[0]:
                    dname = os.path.join(Project_dir,'scripts', 'tags_scripts')
                    fname    = self.Run.Tag_selected+'.sh'
                else:
                    dname = os.path.join(Project_dir,'scripts')
                    fname    = '00.workflow.commands.sh'
                try:
                    if fname in self.sftp.listdir( self.sftp.normalize(dname) ):
                        temp_command = temp_command + 'source deactivate ;;'
                        temp_command = temp_command + 'bash ' + os.path.join(self.sftp.normalize(dname),fname)
                except:
                        Error = Error + 'Error:\n You first need to generate the scripts \n'
            else:
                if self.Run.Tag_selected!=self.Run.Tags[0]:
                    fname = os.path.join(Project_dir,'scripts', 'tags_scripts',self.Run.Tag_selected+'.sh')
                else:
                    fname = os.path.join(Project_dir,'scripts', '00.workflow.commands.sh')
                if os.path.isfile(fname):
                    temp_command = temp_command + 'bash ' + fname
                else:
                    Error = Error + 'Error:\n You first need to generate the scripts \n'
        else:
            Error = Error + 'Error:\n No Project directory \n'
        if len(Error) == 0:
            if self.Running_script == 0:
                try:
                    self.Terminal_string = self.Terminal_string + '[Running_script]:  Running scripts...\n'
                    self.Run.set_Terminal(self.Terminal_string)
                    self.Running_Commands['Running_script'] =  Run_command_in_thread2(self.session,temp_command,self.ssh_client)
                    self.Running_Commands['Running_script'].Run()
                    self.set_Running_script(self.Running_script+1)
                except :
                    pass

            # elif self.Running_Commands['Running_script'].proc.poll() is not None:
                # try:
                    # self.Running_Commands['Running_script'] =  Run_command_in_thread2(self.session,temp_command)
                    # self.Running_Commands['Running_script'].Run()
                    # self.set_Running_script(self.Running_script+1)
                # except :
                    # pass

        else:
            self.Run.set_Terminal(Error)
    
    def Kill_Run_command(self,Project_dir):
        import os
        from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

        Error = ''
        temp_command = ''
        if len(Project_dir) > 0:
            fname = '99.kill_all.sh'
            dname = os.path.join(Project_dir,'scripts')
            
            if self.sftp!= None:
                if fname in self.sftp.listdir( self.sftp.normalize(dname) ):
                    temp_command = temp_command + 'source deactivate ;;'
                    temp_command = temp_command + 'bash ' + os.path.join(self.sftp.normalize(dname),fname)
                else:
                    Error = Error + 'Error:\n You first need to generate and run the scripts \n'
            else:
                fname = os.path.join(dname,fname)
                if os.path.isfile(fname):
                    temp_command = 'bash ' + fname
                else:
                    Error = Error + 'Error:\n You first need to generate and run the scripts \n'
        else:
            Error = Error + 'Error:\n No Project directory \n'

        try:
            self.Running_Commands['Running_script'].Stop()
            self.set_Running_script(0)
            self.Run.set_Terminal('Stop Running Scripts')
        except :
            pass

        if len(Error) == 0:

            if self.Kill_Run == 0:
                try:
                    self.Running_Commands['Kill_Run'] =  Run_command_in_thread2(self.session,temp_command,self.ssh_client)
                    self.Running_Commands['Kill_Run'].Run()
                    self.set_Kill_Run(self.Kill_Run+1)
                except :
                    pass

            # elif self.Running_Commands['Kill_Run'].proc.poll() is not None:
                # try:
                    # self.Running_Commands['Kill_Run'] =  Run_command_in_thread2(self.session,temp_command)
                    # self.Running_Commands['Kill_Run'].Run()
                    # self.set_Kill_Run(self.Kill_Run+1)
                # except :
                    # pass

        else:
            self.Run.set_Terminal(Error)
    
    def Locate_Failures_command(self,Project_dir):
        import os
        from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

        Error = ''
        temp_command = ''
        if len(Project_dir) > 0:
            fname = 'DD.utilities.sh'
            dname = os.path.join(Project_dir,'scripts')
            if self.sftp!= None:
                if fname in self.sftp.listdir( self.sftp.normalize(dname) ):
                    temp_command = temp_command + 'source deactivate ;;'
                    temp_command = temp_command + '. ' + os.path.join(self.sftp.normalize(dname),fname) + ' ; recover_run '
                else:
                    Error = Error + 'Error:\n You first need to generate and run the scripts \n'
            else:
                fname = os.path.join(dname,fname)
                if os.path.isfile(fname):
                    temp_command = '. ' + fname + ' ; recover_run '
                else:
                    Error = Error + 'Error:\n You first need to generate and run the scripts \n'
        else:
            Error = Error + 'Error:\n No Project directory \n'


        if len(Error) == 0:
            if self.Locate_Failures == 0:
                try:
                    self.Running_Commands['Locate_Failures'] =  Run_command_in_thread2(self.session,temp_command,self.ssh_client)
                    self.Running_Commands['Locate_Failures'].Run()
                    self.Terminal_string = self.Terminal_string + '[Locate Failures]:   Searching for failures in the last run.. \n'
                    self.Terminal_string = self.Terminal_string + '[Locate Failures]:   Click on the Recover button if you want to re-run these steps: \n'
                    self.Run.set_Terminal(self.Terminal_string)
                    self.set_Locate_Failures(self.Locate_Failures+1)

                except :
                    pass

            # elif self.Running_Commands['Locate_Failures'].proc.poll() is not None:
                # try:
                  # self.Running_Commands['Locate_Failures'] =  Run_command_in_thread2(self.session,temp_command)
                    # self.Running_Commands['Locate_Failures'].Run()
                    # self.Terminal_string = self.Terminal_string + '[ Locate Failures ]:   Searching for failures in the last run.. \n'
                    # self.Terminal_string = self.Terminal_string + '[ Locate Failures ]:   Click on the Recover button if you want to re-run these steps: \n'
                    # self.Run.set_Terminal(self.Terminal_string)
                    # self.set_Locate_Failures(self.Locate_Failures+1)
                # except :
                    # pass

        else:
            self.Run.set_Terminal(Error)
    
    def Recovery_command(self,Project_dir):
        import os
        from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
        
        Error = ''
        temp_command = ''
        if len(Project_dir) > 0:
            fname = 'DD.utilities.sh'
            dname = os.path.join(Project_dir,'scripts')
            
            if self.sftp!= None:
                if fname in self.sftp.listdir( self.sftp.normalize(dname) ):
                    fname = 'AA.Recovery_script.sh'
                    if fname in self.sftp.listdir( self.sftp.normalize(dname) ):
                        temp_command = temp_command + 'source deactivate ;;'
                        temp_command = temp_command + 'bash ' + os.path.join(self.sftp.normalize(dname),fname)
                    else:
                        Error = Error + 'Error:\n You first need to "Locate Failures" \n'
                else:
                    Error = Error + 'Error:\n You first need to generate and run the scripts \n'
            else:
                fname = os.path.join(dname,fname)
                if os.path.isfile(fname):
                    fname = 'AA.Recovery_script.sh'
                    fname = os.path.join(dname,fname)
                    if os.path.isfile(fname):
                        temp_command = 'bash ' + fname
                    else:
                        Error = Error + 'Error:\n You first need to "Locate Failures" \n'
                else:
                    Error = Error + 'Error:\n You first need to generate and run the scripts \n'
        else:
            Error = Error + 'Error:\n No Project directory \n'


        if len(Error) == 0:

            if self.Recovery == 0:
                try:
                    self.Running_Commands['Recovery'] =  Run_command_in_thread2(self.session,temp_command,self.ssh_client)
                    self.Running_Commands['Recovery'].Run()
                    self.Terminal_string = self.Terminal_string + '[Recovery]:   Trying to Recover.. \n'
                    self.Run.set_Terminal(self.Terminal_string)
                    self.set_Recovery(self.Recovery+1)
                    self.Terminal_string = self.Terminal_string + '[Recovery]:   Click on Run Monitor to See if it Worked \n'
                    self.Run.set_Terminal(self.Terminal_string)
                except :
                    pass
        else:
            self.Run.set_Terminal(Error)
    
    def Run_Monitor_command(self,Project_dir):
        import os
        import curses, argparse
        import neatseq_flow_monitor
        import threading

        Error = ''

        parser = argparse.ArgumentParser(description='Neatseq-flow Monitor By Liron Levin ')
        parser.add_argument('-D', dest='directory',metavar="STR", type=str,default=Project_dir,
                            help='Neatseq-flow project directory ')
        parser.add_argument('-R', dest='Regular',metavar="STR" , type=str,default="log_[0-9]+.txt$",
                            help='Log file Regular Expression [in ./logs/ ] [default=log_[0-9]+.txt$]')
        parser.add_argument('--Monitor_RF',metavar="FLOAT", type=float,dest='Monitor_RF',default=1,
                            help='Monitor Refresh rate [default=1]')
        parser.add_argument('--File_browser_RF',metavar="FLOAT", type=float,dest='File_browser_RF',default=1,
                            help='File Browser Refresh rate [default=1]')
        parser.add_argument('--Bar_Marker',metavar="CHAR",type=str,dest='Bar_Marker',default="#",
                            help='Progress Bar Marker [default=#]')
        parser.add_argument('--Bar_Spacer',metavar="CHAR",type=str,dest='Bar_Spacer',default=" ",
                            help='Progress Bar Spacer [default=Space]')
        parser.add_argument('--Bar_len',metavar="INT",type=int,dest='Bar_len',default=40,
                            help='Progress Bar Total Length [in chars] [default=40]')
        parser.add_argument('--Server',dest='Server',action='store_true',
                            help='Run as Server')
        args = parser.parse_args()
        if len(Project_dir) > 0:
            self.Terminal_string = self.Terminal_string + 'Running Monitor...\n'
            self.Run.set_Terminal( self.Terminal_string  )
            try:
                threading.Thread(target=lambda : curses.wrapper(neatseq_flow_monitor.neatseq_flow_monitor,args)).start()
            except:
                Error=Error + 'Error:\n Monitor Error \n'


        else:
            Error = Error + 'Error:\n No Project directory \n'

        if len(Error) > 0:
            self.Terminal_string = self.Terminal_string +  '\n' + Error
            self.Run.set_Terminal(self.Terminal_string)
    
    def Run_ReRun_command(self,command):
        import time
        Error = ''
        if len(command) > 0:
            if  self.Kill_Run == 0 :
                while self.Recovery != 0:
                    time.sleep(0.000001)
                try:
                    time.sleep(0.00001)
                    self.Running_Commands['Recovery'] =  Run_command_in_thread2(self.session,command,self.ssh_client)
                    self.Running_Commands['Recovery'].Run()
                    self.Terminal_string = self.Terminal_string + '[Recovery]:'+ command +'\n'
                    self.Run.set_Terminal(self.Terminal_string)
                    self.set_Recovery(self.Recovery+1)
                    self.Run.set_Terminal(self.Terminal_string)
                except BaseException as e:
                    Error += "Some Unknown ERROR!! " + str(e) + '\n'
            else:
                Error += "Can't Re-Run script while Killing scripts, Try later"
        else:
            Error += 'No Script to Run'
            
        if len(Error)==0:
            self.TabLayout2.set_current(self.Run)
        else:
            if SERVE:
                self.send_massage.set_massage(Error)
            else:
                print(Error)
    
    @event.action
    def change_value(self,obj,prop_name,value):
        obj._mutate(prop_name,value)
    
    @event.reaction('Running_script','Kill_Run','Recovery','Locate_Failures','Generating_scripts')
    def update_Terminal(self, *events):
        from datetime import datetime
        for ev in events:
            if ev.new_value>0:
                Task_End = False
                Title    = ''
                stat     = True
                outs     = ''
                errs     = ''
                try:
                    if self.Running_Commands[ev.type].is_alive():
                       outs, errs = self.Running_Commands[ev.type].output()
                       #asyncio.get_event_loop().call_later(0.5, self.change_value,ev.source,ev.type,ev.new_value + 1)
                       self.change_value(ev.source,ev.type,ev.new_value + 1)
                    else:
                        self.Running_Commands[ev.type].Stop()
                        outs, errs = self.Running_Commands[ev.type].output()
                        # self.Running_Commands[ev.type].Stop()
                        self.change_value(ev.source,ev.type,0)
                        Task_End=True
                except BaseException as e:
                    print(e)
                    stat=False


                if stat:
                    if (len(outs+errs)==0) and Task_End:
                        [outs, errs] = self.Running_Commands[ev.type].output()

                    if len(outs) > 0:
                        Title = Title + outs
                    if len(errs) > 0:
                        Title = Title  + errs

                    if Task_End:
                        Title = Title + '\n<p style="color:CadetBlue;"><b>The Task has Finished [ Look for Successful Run or Possible Errors ]</b></p>\n'

                    if len(Title) > 0:
                        Time_STR = '<span  style="color:Green;">' + datetime.now().strftime("%d/%m %H:%M") + '</span >' 
                        Job_STR  = '<span  style="color:Blue;">' + ev.type.replace('_',' ') + '</span >'
                        for line in Title.split('\n'):
                            if len(line)>0:
                                self.Terminal_string = self.Terminal_string + '['+ Job_STR +'] ['+Time_STR+']: ' + line + '\n'
                        self.Run.set_Terminal(self.Terminal_string)
    
    @event.reaction('step_info.Go2Help')
    def Go2Help(self, *events):
        for ev in events:
            self.TabLayout2.set_current(self.Help)
            if ev.source.Go2Help!='':
                self.Help.set_url(Base_Help_URL)
                self.Help.set_url(Base_Help_URL+'Module_docs/AllModules.html#'+ev.source.Go2Help.lower().replace('_','-'))
    
    @event.reaction('Run.jump2monitortab')
    def jump2monitortab(self, *events):
        import Monitor_GUI
        for ev in events:
            if ev.new_value!='None':
                self.monitor.close()
                # self.monitor.dispose()
                with self.Monitor:
                    with ui.Layout() as self.Monitor_Widget:
                        self.monitor      = Monitor_GUI.Monitor_GUI(ev.new_value,self.ssh_client)
                        self.Test_Monitor.update_monitor_object(self.monitor)
                self.TabLayout2.set_current(self.Monitor)
                self.Run.set_jump2monitortab('None')
    
    @event.reaction('!Test_Monitor.RunCommand')
    def Monitor_send_command(self, *events):
        for ev in events:
            if ev.new_value!='':
                if self.Recovery == 0:
                    for line in ev.new_value.split('\n'):
                            if len(line)>0:
                                self.Run_ReRun_command(line)
                else:
                    Error = "Can't Re-Run script while other scripts are submitted, Try later"
                    if SERVE:
                        self.send_massage.set_massage(Error)
                    else:
                        print(Error)
                        
    @event.reaction('!Run.open_filepicker', 'samples_info.open_filepicker', 'step_info.open_filepicker',
                    'cluster_info.open_filepicker', 'vars_info.open_filepicker')
    def open_filepicker(self, *events):
        for ev in events:
            if ev.source.open_filepicker != '':
                self.filepicker_options(ev.source.open_filepicker)
                ev.source.set_open_filepicker('')
    
    @event.reaction('!Run.command')
    def Run_command(self, *events):
        for ev in events:
            if len(ev.source.command) > 0:
                self.command_pars(ev.source.command)
                ev.source.set_command([])
    
    @event.reaction('samples_info.save_samples_file')
    def save_sample_file(self, *events):
        for ev in events:
            if len(self.samples_info.save_samples_file) > 0:
                self.stack.set_current(self.LoadingWin)
                if len(self.samples_info.samples_data.keys()) > 0:
                    if self.samples_info.save_samples_file[0][0].endswith(os.sep):
                        if SERVE:
                            self.send_massage.set_massage('[Saving Sample file Error]: No File Name Was Identified')
                        else:
                            dialite.fail('Saving Sample file Error','No File Name Was Identified' )
                    else:
                        try:
                            if self.sftp!=None:
                                sample_file = self.sftp.open(self.samples_info.save_samples_file[0][0],mode='w')
                            else:
                                sample_file = open(self.samples_info.save_samples_file[0][0], 'w')
                            sample_file.write('Title\t' + self.samples_info.samples_data.setdefault("Title", "Untitled") + '\n')
                            sample_file.write('\n')
                            if "project_data" in self.samples_info.samples_data.keys():
                                sample_file.write('#Type\tPath' + '\n')
                                for project_types in self.samples_info.samples_data["project_data"].keys():
                                    for project_path in self.samples_info.samples_data["project_data"][project_types]:
                                        sample_file.write(project_types + '\t' + project_path + '\n')
                            sample_file.write('\n')
                            sample_file.write('#SampleID\tType\tPath' + '\n')
                            for sample_name in self.samples_info.samples_data.keys():
                                if sample_name not in ['project_data', 'Title']:
                                    for sample_types in self.samples_info.samples_data[sample_name].keys():
                                        for sample_path in self.samples_info.samples_data[sample_name][sample_types]:
                                            if sample_path=='':
                                                sample_path='""'
                                            sample_file.write(sample_name + '\t' + sample_types + '\t' + sample_path + '\n')
                            sample_file.close()
                            self.Run.set_sample_file(self.samples_info.save_samples_file)
                            self.samples_info.set_title('Samples - '+os.path.basename(self.samples_info.save_samples_file[0][0]))
                            self.samples_info.set_save_samples_file([])
                        except BaseException as e: 
                            if SERVE:
                                self.send_massage.set_massage(str(e))
                            else:
                                dialite.fail('Saving Sample file Error', str(e))
                            self.samples_info.set_save_samples_file([])
            else:
                self.stack.set_current(self.MainStack)
                self.label.set_flex(0.02)
    
    @event.reaction('samples_info.load_samples_file')
    def load_sample_file(self, *events):
        samples_data = self.samples_info.samples_data
        for ev in events:
            if len(self.samples_info.load_samples_file) > 0:
                self.stack.set_current(self.LoadingWin)
                try:
                    if self.sftp!=None:
                        from neatseq_flow_gui.modules.parse_sample_data import parse_sample_file_object
                        file_name    = self.samples_info.load_samples_file[0][0]
                        file_object  = self.sftp.open(file_name,mode='r')
                        samples_data = parse_sample_file_object(file_object,file_name,self.sftp)
                        file_object.close()
                    else:
                        from neatseq_flow_gui.modules.parse_sample_data import parse_sample_file
                        samples_data = parse_sample_file(self.samples_info.load_samples_file[0][0])
                    if len(samples_data) > 0:
                        self.update_samples_data(samples_data)
                        self.Run.set_sample_file(self.samples_info.load_samples_file)
                        self.samples_info.set_title('Samples - '+os.path.basename(self.samples_info.load_samples_file[0][0]))
                except BaseException as e: 
                    if SERVE:
                        self.send_massage.set_massage('[Loading Sample file Error]:'+str(e))
                    else:
                        dialite.fail('Loading Sample file Error', str(e))
                    samples_data = []
                    self.samples_info.set_load_samples_file([])
            else:
                self.stack.set_current(self.MainStack)
                self.label.set_flex(0.02)
    
    @event.action
    def update_samples_data(self, samples_data):
        converer = {}
        self.correct_dict(samples_data, 1, converer)
        self.samples_info.set_samples_data(samples_data)
        self.samples_info.set_converter(converer)
        self.samples_info.set_samples_data_update(True)
    
    @event.reaction('step_info.step_export_file')
    def step_export_file(self, *events):
        import yaml,re
        from collections import OrderedDict
        setup_yaml(yaml, OrderedDict)

        for ev in events:
            if len(self.step_info.step_export_file) > 0:
                if self.step_info.step_export_file[0][0].endswith(os.sep):
                    if SERVE:
                        self.send_massage.set_massage('[Saving Step file Error]:No File Name Was Identified')
                    else:
                        dialite.fail('Saving Step file Error','No File Name Was Identified' )
                    err_flag=False
                else:
                    err_flag=True
                    try:
                        if self.sftp!=None:
                            file_name   = self.step_info.step_export_file[0][0]
                            if not file_name.endswith('.step'):
                                file_name = file_name + '.step'
                            file_object = self.sftp.open(file_name,mode='w')
                        else:
                            file_name   = self.step_info.step_export_file[0][0]
                            if not file_name.endswith('.step'):
                                file_name = file_name + '.step'
                            file_object = open(file_name, 'w')
                            
                        with file_object as outfile:
                            step_data         = OrderedDict()
                            step_data['Step'] = self.fix_order_dict(self.step_info.step2export)
                            yaml.dump(step_data['Step'], outfile, default_flow_style=False,width=float("inf"), indent=4)

                    except BaseException as e: 
                        if SERVE:
                            self.send_massage.set_massage('[Saving Step file Error]:'+str(e))
                        else:
                            dialite.fail('Saving Step file Error', str(e))
                        err_flag=False
                    
                if self.sftp!=None:
                    try:
                        file_object.close()
                    except:
                        pass
                self.step_info.set_step_export_file([])
    
    @event.reaction('step_info.Load_step_file')
    def load_step_file(self, *events):
        import yaml
        for ev in events:
            if len(self.step_info.Load_step_file) > 0:
                try:
                    file_name   = self.step_info.Load_step_file[0][0]
                    if self.sftp!=None:
                        file_object = self.sftp.open(file_name)
                    else:
                        file_object = open(file_name,'r')
                    Step_data   = yaml.load(file_object, yaml.SafeLoader)
                    file_object.close()
                except BaseException as e: 
                    if SERVE:
                        self.send_massage.set_massage('[Loading Step file Error]:'+str(e))
                    else:
                        dialite.fail('Loading Step file Error', str(e))
                    Step_data = OrderedDict()
                    
                self.step_info.set_Load_step_file([])
                if len(Step_data.keys()) > 0:
                    converter = OrderedDict()
                    self.correct_dict(Step_data, 1, converter)
                    self.step_info.set_step_converter(converter)
                    self.step_info.set_step2load(Step_data)
    
    @event.reaction('step_info.workflow_file')
    def load_workflow_file(self, *events):
        for ev in events:
            if len(self.step_info.workflow_file) > 0:
                self.stack.set_current(self.LoadingWin)
                # self.Run_FUN.Run_Function(Name='sleep',FUN=Test_FUN,agrs=(50))
                try:
                    if self.sftp!=None:
                        from neatseq_flow_gui.modules.parse_param_data import parse_param_file_object
                        file_name   = self.step_info.workflow_file[0][0]
                        file_object = self.sftp.open(file_name)
                        param_data  = parse_param_file_object(file_object,file_name)
                        file_object.close()
                    else:
                        from neatseq_flow_gui.modules.parse_param_data import parse_param_file
                        param_data = parse_param_file(self.step_info.workflow_file[0][0])
                except BaseException as e: 
                    if SERVE:
                        self.send_massage.set_massage('[Load WorkFlow Error]:'+str(e))
                    else:
                        dialite.fail('Load WorkFlow Error', str(e))
                    param_data = []
                    self.step_info.set_workflow_file([])
                if len(param_data) > 0:

                    if 'Step_params' in param_data.keys():
                        if len(param_data['Step_params']) > 0:
                            self.update_steps_data(param_data['Step_params'])

                    if 'Global_params' in param_data.keys():
                        if len(param_data['Global_params']) > 0:
                            self.update_cluster_data(param_data['Global_params'])

                    if 'Vars' in param_data.keys():
                        if len(param_data['Vars']) > 0:
                            self.update_vars_data(param_data['Vars'])

                    if 'Documentation' in param_data.keys():
                        self.Documentation.set_value(param_data['Documentation'])
                        self.Documentation.set_load_flag(True)
                    
                    self.Run.set_parameter_file(self.step_info.workflow_file)
                    self.TabLayout.set_title('Work-Flow - '+os.path.basename(self.step_info.workflow_file[0][0]))
            else:
                self.stack.set_current(self.MainStack)
                self.label.set_flex(0.02)
    
    @event.reaction('step_info.save_workflow_file')
    def save_workflow_file(self, *events):
        import yaml,re
        from collections import OrderedDict
        setup_yaml(yaml, OrderedDict)
        for ev in events:
            if len(self.step_info.save_workflow_file) > 0:
                self.stack.set_current(self.LoadingWin)
                if self.step_info.save_workflow_file[0][0].endswith(os.sep):
                    if SERVE:
                        self.send_massage.set_massage('[Save WorkFlow Error]:No File Name Was Identified')
                    else:
                        dialite.fail('Save WorkFlow Error','No File Name Was Identified' )
                    err_flag=False
                else:
                    err_flag=True
                    try:
                        if self.sftp!=None:
                            file_name   = self.step_info.save_workflow_file[0][0]
                            file_object = self.sftp.open(file_name,mode='w')
                        else:
                            file_object = open(self.step_info.save_workflow_file[0][0], 'w')
                            
                        with file_object as outfile:
                            param_data = OrderedDict()
                            param_data['Documentation'] = re.sub(string=self.Documentation.value.rstrip('\t').replace('\t',"    "),
                                                                 pattern=' +\n',
                                                                 repl='\n').rstrip(' ').rstrip('\n')
                            yaml.dump(param_data, outfile,
                                      default_flow_style=False,
                                      width=float("inf"),
                                      default_style="|" ,
                                      explicit_start = False,
                                      explicit_end   = False,
                                      #version=(1,2),
                                      indent=4)

                            param_data = OrderedDict()
                            param_data['Global_params'] = self.fix_order_dict(self.cluster_info.Data)
                            yaml.dump(param_data, outfile, default_flow_style=False,width=float("inf"), indent=4)
                            param_data = OrderedDict()
                            param_data['Vars'] = self.fix_order_dict(self.vars_info.Data)
                            yaml.dump(param_data, outfile, default_flow_style=False,width=float("inf"), indent=4)
                            param_data = OrderedDict()
                            param_data['Step_params'] = self.fix_order_dict(self.step_info.Data)
                            yaml.dump(param_data, outfile, default_flow_style=False,width=float("inf"), indent=4)

                    except BaseException as e: 
                        if SERVE:
                            self.send_massage.set_massage('[Save WorkFlow Error]:'+str(e))
                        else:
                            dialite.fail('Save WorkFlow Error', str(e))
                        err_flag=False
                        
                
                if self.sftp!=None:
                    try:
                        file_object.close()
                    except:
                        pass
                if err_flag:
                    self.Run.set_parameter_file(self.step_info.save_workflow_file)
                    self.TabLayout.set_title('Work-Flow - '+os.path.basename(self.step_info.save_workflow_file[0][0]))
                self.step_info.set_save_workflow_file([])
            else:
                self.stack.set_current(self.MainStack)
                self.label.set_flex(0.02)
    
    def fix_order_dict(self, dic):
        if isinstance(dic, dict):
            dic = OrderedDict(dic)
            dic_keys = list(dic.keys())
            for key in dic_keys:
                dic[key] = self.fix_order_dict(dic[key])
        return dic
    
    @event.reaction('vars_info.Data')
    def send_Vars_options(self, *events):
        for ev in events:
            options = list()
            self.dic2list(self.vars_info.Data, options)
            self.step_info.set_options(options)
    
    @event.action
    def update_steps_data(self, Steps_Data):
        converter = OrderedDict()
        self.correct_dict(Steps_Data, 1, converter)
        self.step_info.set_Steps_Data(Steps_Data)
        self.step_info.set_converter(converter)
        self.step_info.set_Steps_Data_update(True)
    
    @event.action
    def update_cluster_data(self, Cluster_Data):
        converer = OrderedDict()
        self.correct_dict(Cluster_Data, 1, converer)
        self.cluster_info.set_Data(Cluster_Data)
        self.cluster_info.set_converter(converer)
        self.cluster_info.set_Data_update(True)
    
    @event.action
    def update_vars_data(self, Vars_Data):
        converer = OrderedDict()
        self.correct_dict(Vars_Data, 1, converer)
        self.vars_info.set_Data(Vars_Data)
        self.vars_info.set_converter(converer)
        self.vars_info.set_Data_update(True)
        
    def correct_dict(self, dic, count, converer):
        if isinstance(dic, dict):
            dic_keys = list(dic.keys())
            for key in dic_keys:
                temp = dic.pop(key)
                converer['temp_' + str(count)] = key
                dic['temp_' + str(count)], count = self.correct_dict(temp, count + 1, converer)
        return dic, count
    
    def dic2list(self, Vars, flat_list, string='Vars.'):
        for item in Vars.keys():
            if isinstance(Vars[item], dict):
                temp_string = string
                string = string + item + '.'
                self.dic2list(Vars[item], flat_list, string)
                string = temp_string
            else:
                flat_list.append('{' + string + item + '}')
    
    @event.reaction('step_info.Vars_data')
    def pars_vars_in_new_step(self, *events):
        input_list = []
        self.find_vars_in_dict(self.step_info.Vars_data, input_list)
        new_vars_data = self.Add_items_to_vars_dict(self.vars_info.Data, input_list)
        self.update_vars_data(new_vars_data)
        
    def Add_items_to_vars_dict(self, vars_data, items2add):
        for items in items2add:
            item = items.split('.')
            item.remove('Vars')
            self.list2dict(vars_data, item)
        return vars_data
    
    def list2dict(self, dic, input_list):
        if len(input_list) > 0:
            key = input_list.pop(0)
            if not isinstance(dic, dict):
                dic = {}
            if key not in dic.keys():
                dic[key] = {}
            dic[key] = self.list2dict(dic[key], input_list)
            return dic
        else:
            if isinstance(dic, dict):
                if len(dic) == 0:
                    return None
                else:
                    return dic

            if dic == None:
                return None
            else:
                return dic
    
    def find_vars_in_dict(self, input_dict, input_list):
        import re
        var_re = "\{(Vars\.[\w\.\-]+?)\}"
        for key in input_dict.keys():
            if isinstance(input_dict[key], dict):
                self.find_vars_in_dict(input_dict[key], input_list)
            elif len(re.findall(var_re, str(input_dict[key]))) > 0:
                input_list.extend(list(re.findall(var_re, input_dict[key])))
    
    # @event.reaction('Run_FUN.Loading')
    def Collect_Function_in_Thread(self, *events):
        for ev in events:
            if ev.new_value==False:
                self.stack.set_current(self.MainStack)
                self.label.set_flex(0.02)

class Popen_SSH(object):
    
    def __init__(self,session,ssh_client,command,shell=False,out_queue=None,err_queue=None,pty=True,timeout=COMMAND_TIME_OUT,nbytes = 4096):
        import time
        self.session     = session
        self.timeout     = timeout
        self.shell       = shell
        self.err_flag    = True
        self.nbytes      = nbytes
        self.stdout_data = []
        self.stderr_data = []
        self.ssh_session = None
        self.EFC         = get_random_string()
        self.Done        = True
        self.time        = time.time()
        
        try:
            if (ssh_client!= None) and (self.session.status!=0):
                import paramiko
                transport  = ssh_client.get_transport()
                ssh_client_ = paramiko.SSHClient()
                ssh_client_.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
                ssh_client_.connect(transport.getpeername()[0],
                                   username=transport.get_username(),
                                   password=transport.auth_handler.password,
                                   port=transport.getpeername()[1])
                                   
                if 'SSHClient' not in self.session.__dict__.keys():
                    self.session.SSHClient = [ssh_client_]
                else:
                    self.session.SSHClient.append(ssh_client_)
                
                if ssh_client_.get_transport().is_active():
                    self.ssh_transport     = ssh_client_.get_transport()
                    self.ssh_session       = self.ssh_transport.open_channel(kind='session')
                    if pty:
                        self.ssh_session.get_pty('vt100')
                    if self.shell:
                        self.err_flag = False
                        self.ssh_session.invoke_shell()
                        self.Done = False
                        self.ssh_session.send("stty -echo\n")
                        command = "bash;" + command + "; echo " + self.EFC
                        command = command.replace(';','\n')
                        for line in command.split('\n'):
                            self.ssh_session.send(line+'\n')
                    if not self.shell:
                        self.ssh_session.settimeout(self.timeout)
                        self.Done = False
                        self.err_flag = False
                        self.ssh_session.exec_command(command)
                    if (out_queue!=None) and (err_queue!=None):
                        self.output(out_queue,err_queue)
        except :
            self.err_flag = True
            try:
                self.ssh_session.close()
                ssh_client_.close()
            except:
                pass
            pass
            
    def output(self,out_queue=None,err_queue=None):
        import time
        import string
        printable = set(string.printable)
        
        keep_running = False
        if not self.err_flag:
            try:
                while self.session.status!=0:
                    out = ''
                    err = ''
                    if self.ssh_session.recv_ready() or keep_running:
                        out = self.ssh_session.recv(self.nbytes).decode('utf-8')
                        out = ''.join(filter(lambda x: x in printable, out))
                        self.stdout_data.extend(out)
                        if (out_queue!=None):
                            if self.shell:
                                if len(''.join(self.stdout_data).split(self.EFC))==2:
                                    if len(out.split(self.EFC))==2:
                                        if self.session.status!=0:
                                            out_queue.put(out.split(self.EFC)[1])
                                            
                                    else:
                                        if self.session.status!=0:
                                            out_queue.put(out)
                                elif len(''.join(self.stdout_data).split(self.EFC))>2:
                                    if len(out.split(self.EFC))==2:
                                        if self.session.status!=0:
                                            out_queue.put(out.split(self.EFC)[0])
                                    else:
                                        if self.session.status!=0:
                                            out_queue.put(out)
                            else:
                                if self.session.status!=0:
                                    out_queue.put(out)
                    if self.ssh_session.recv_stderr_ready() or keep_running:
                        err = self.ssh_session.recv_stderr(self.nbytes).decode('utf-8')
                        err = ''.join(filter(lambda x: x in printable, err))
                        self.stderr_data.extend(err)
                        if err_queue!=None:
                            if self.shell:
                                if self.session.status!=0:
                                    err_queue.put(err)
                    if self.shell:
                        if len(''.join(self.stdout_data).split(self.EFC))>2:
                            break
                        if (time.time() - self.time) > self.timeout:
                            if self.session.status!=0:
                                out_queue.put('\n [Error]: Time Out\n')
                            break
                    if self.ssh_session.exit_status_ready():
                        if (len(out)!=0) or (len(err)!=0) or (self.ssh_session.recv_ready()) or (self.ssh_session.recv_stderr_ready()):
                            keep_running = True
                        else:
                            break 
                    
                if not self.shell:
                    self.stdout_data = ''.join(self.stdout_data)
                    self.stderr_data = ''.join(self.stderr_data)
                    if self.ssh_session.recv_exit_status()==0:
                        self.err_flag = False
                    else:
                        self.err_flag = True
                else:
                    if len(''.join(self.stdout_data).split(self.EFC))>2:
                        self.stdout_data = ''.join(self.stdout_data).split(self.EFC)[1]
                    else:
                        self.stdout_data = ''.join(self.stdout_data)
                    self.stderr_data = ''.join(self.stderr_data)
                self.Done = True
            except BaseException as e: 
                print(str(e))
                self.err_flag = True
                self.Done = True
            if self.err_flag:
                try:
                    self.ssh_session.close()
                except:
                    pass
                return [''.join(self.stdout_data) , ''.join(self.stderr_data) , 1]
            else:
                try:
                    self.ssh_session.close()
                except:
                    pass
                return [''.join(self.stdout_data) , ''.join(self.stderr_data) , 0]
        else:
            return ['','',1]
    
    def kill(self):
        try:
            self.ssh_session.close()
            ssh_client_.close()
        except:
            pass
    
    def poll(self):
        if self.shell:
            if self.Done:
                return 1
            else:
                return None
        else:
            if not self.ssh_session.exit_status_ready():
                return None
            else:
                return self.ssh_session.recv_exit_status()

class Run_command_in_thread(object):


    def __init__(self,session,command,ssh_client=None,shell=True):

        import threading
        import multiprocessing
        import queue

        self.session      =   session
        self.stdout       =   queue.Queue()
        self.stderr       =   queue.Queue()
        self.get_std_err  =   threading.Thread(target=self.collect_err)
        self.get_std_out  =   threading.Thread(target=self.collect_out)
        self.proc         =   None
        self.Run_command  =   command
        self.ssh_client   =   ssh_client
        self.shell        =   shell
        self.refreshrate  =   1

    def collect_out(self):
        if self.ssh_client != None:
            if self.session.status!=0:
                self.proc.output(self.stdout,self.stderr)
            else:
                self.Stop()
        else:
            if self.session.status!=0:
                for stdout in iter(self.proc.stdout.readline, ''):
                    if self.session.status!=0:
                        if len(stdout)>0:
                            self.stdout.put(stdout,False)
                    else:
                        break
            else:
                self.Stop()

    def collect_err(self):
        if self.session.status!=0:
            for stderr in iter(self.proc.stderr.readline, ''):
                if self.session.status!=0:
                    if len(stderr)>0:
                        self.stderr.put(stderr,False)
                else:
                    break

    def Run(self):
        if self.ssh_client != None:
            self.proc = Popen_SSH(self.session,self.ssh_client,self.Run_command,self.shell)
            self.get_std_out.daemon = True
            self.get_std_out.start()
            # self.get_std_err.start()
            asyncio.get_event_loop().call_later(self.refreshrate, self.Test_Alive)
        else:
            from subprocess import Popen, PIPE, STDOUT
            self.proc = Popen(self.Run_command , shell=self.shell, executable='/bin/bash', stdout=PIPE, stderr=PIPE,
                                 universal_newlines=True)
            self.get_std_out.daemon = True
            self.get_std_out.start()
            self.get_std_err.daemon = True
            self.get_std_err.start()
            asyncio.get_event_loop().call_later(self.refreshrate, self.Test_Alive)

    def Stop(self):
        self.get_std_out.join()
        if self.ssh_client == None:
            self.get_std_err.join()
        self.proc.kill()
        
    def is_alive(self):
        if self.session.status==0:
            self.Stop()
        if self.proc.poll() == None:
            return False
        else:
            return True
    
    def Test_Alive(self):
        if self.session.status==0:
            self.Stop()
        else:
            asyncio.get_event_loop().call_later(self.refreshrate, self.Test_Alive)
            
    def output(self):
        import time
        all_out = ''
        all_err = ''
        while (self.stdout.empty()==False) and (self.session.status!=0):
            out = self.stdout.get()
            all_out = all_out + out
            self.stdout.task_done()
        
        out=all_out
        
        while (self.stderr.empty()==False) and (self.session.status!=0):
            err = self.stderr.get()
            all_err = all_err + err
            self.stderr.task_done()
        
        err=all_err
        time.sleep(0.000001)
        return [ out , err]

class Run_command_in_thread2(object):

    def __init__(self,session,command,ssh_client=None,shell=True):

        import threading
        import multiprocessing
        from multiprocessing import Process, Queue
        import queue

        self.session      =   session
        self.stdout       =   Queue()
        self.stderr       =   Queue()
        self.Run_command  =   command
        self.ssh_client   =   ssh_client
        self.shell        =   shell
        self.Process      =   None
        self.get_std_err  =   threading.Thread(target=self.collect_err)
        self.get_std_out  =   threading.Thread(target=self.collect_out)
        # self.get_std_err  =   None
        # self.get_std_out  =   None
        self.refreshrate  =   1
    
    def collect_out(self):
        if self.ssh_client != None:
            if self.session.status!=0:
                self.Process.output(self.stdout,self.stderr)
            else:
                self.Stop()
        else:
            while (self.session.status!=0):
                stdout = self.Process.stdout.readline()
                if self.session.status!=0:
                    if len(stdout)>0:
                        self.stdout.put(stdout)
                    else:
                        if self.Process.poll() != None:
                            break
                else:
                    self.Stop()
                    break

    def collect_err(self):
        while (self.session.status!=0):
            stderr = self.Process.stderr.readline()
            if self.session.status!=0:
                if len(stderr)>0:
                    self.stderr.put(stderr)
                else:
                    if self.Process.poll() != None:
                        break
            else:
                self.Stop()
                break


    def Run(self):
        if self.ssh_client != None:
            self.Process = Process(target=Popen_SSH,args=(self.session,
                                                       self.ssh_client,
                                                       self.Run_command,
                                                       self.shell,
                                                       self.stdout,
                                                       self.stderr,
                                                       ))
            self.Process.daemon = True
            if 'Process' not in self.session.__dict__.keys():
                self.session.Process = [self.Process]
            else:
                self.session.Process.append(self.Process)
            
            self.Process.start()
            
                
            asyncio.get_event_loop().call_later(self.refreshrate, self.Test_Alive)
        else:
            from subprocess import Popen, PIPE, STDOUT
            
            self.Process     = Popen(self.Run_command , shell=self.shell, executable='/bin/bash', stdout=PIPE, stderr=PIPE,
                                     universal_newlines=True)
            
            self.get_std_out.daemon = True
            # if 'Threads' not in self.session.__dict__.keys():
                # self.session.Threads = [self.get_std_out]
            # else:
                # self.session.Threads.append(self.get_std_out)
            self.get_std_out.start()
            
            
            
            self.get_std_err.daemon = True
            # if 'Threads' not in self.session.__dict__.keys():
                # self.session.Threads = [self.get_std_err]
            # else:
                # self.session.Threads.append(self.get_std_err)
            self.get_std_err.start()
            

            if 'Pop_Process' not in self.session.__dict__.keys():
                self.session.Pop_Process = [self.Process]
            else:
                self.session.Pop_Process.append(self.Process)

            
            asyncio.get_event_loop().call_later(self.refreshrate, self.Test_Alive)
            
    def Stop(self):
        if self.ssh_client != None:
            if self.Process!=None:
                self.Process.terminate()
                self.Process.join()
                self.Process=None
        else:
            # if self.get_std_out!=None:
                # #self.get_std_out.terminate()
                # self.get_std_out.join()
                # self.get_std_out = None
            # if self.get_std_err!=None:
                # #self.get_std_err.terminate()
                # self.get_std_err.join()
                # self.get_std_err = None
            if self.Process!=None:
                self.Process.kill()
                
    def is_alive(self):
        if self.session.status==0:
            self.Stop()
        if self.ssh_client != None:
            return self.Process.is_alive()
        else:
            if self.Process.poll() == None:
                return True
            else:
                return False
        
    def Test_Alive(self):
        if self.session.status==0:
            self.Stop()
        else:
            asyncio.get_event_loop().call_later(self.refreshrate, self.Test_Alive)
            
    def output(self):
        import time
        all_out = ''
        all_err = ''
        while (self.stdout.empty()==False) and (self.session.status!=0):
            out = self.stdout.get(True)
            all_out = all_out + out
            
        out=all_out
        
        while (self.stderr.empty()==False) and (self.session.status!=0):
            err = self.stderr.get(True)
            all_err = all_err + err
        
        if self.session.status==0:
           self.Stop()
        
        err=all_err
        time.sleep(0.000001)
        return [ out , err]

class Run_function_in_thread(flx.PyComponent):
    
    Loading = event.BoolProp(True, settable=True)
    Data    = event.DictProp({}   , settable=True)
    
    def init(self,refreshrate=1):
        self.q              = Queue()
        self.running        = False
        self.refreshrate    = refreshrate
        self.Process        = None
        self.keep_running   = True
        
    def Run_Function(self,Name,FUN,agrs):
        self.FUN  = FUN
        self.agrs = agrs
        self.Name = Name
        if (not self.running) :
            try:
                self.set_Loading(True)
                self.Process        = Process(target=self.FUN, args=(self.agrs,
                                                                       self.q,))
                self.Process.daemon = True
                
                if 'Process' not in self.session.__dict__.keys():
                    self.session.Process = [self.Process]
                else:
                    self.session.Process.append(self.Process)
                
                self.Process.start()
                self.running        = True
                self.keep_running   = True
                self.Monitor()
            except BaseException as e:
                self.Process        = None
                self.running        = False
                self.close()
                print(e)
                
                
    def Monitor(self):
        if  (self.keep_running):
            if self.q.empty()==False:
                Data=self.q.get(True)
                self.set_Loading(False)
                self.set_Data({self.Name:Data})
        if self.Process!=None:
            if not self.Process.is_alive():
                self.close()
        else:
            self.close()
        if (self.session.status!=0) and (self.keep_running):
            asyncio.get_event_loop().call_later(self.refreshrate, self.Monitor) 

    def close(self):
        self.keep_running = False
        self.set_Loading(False)
        if self.Process!=None:
            self.Process.terminate()
            self.Process.join()
            self.Process=None
        self.running=False

def Test_FUN(sleeptime,q):
    import time
    print(sleeptime)
    time.sleep(sleeptime)
    q.put('test')
    
class send_massage(ui.Widget):
    massage = event.StringProp('', settable=True)
    def init(self):
        pass
        
    @event.reaction('massage')
    def print_massage(self, *events):
        for ev in events:
            if ev.new_value!='':
                global window
                window.alert(ev.new_value)
                self.set_massage('') 
                # RawJS("""      
                        # var msg = ('{massage}');
                        # window.alert(msg);   
                                # """.format(massage=ev.new_value) )

class Test_Monitor_Command(flx.PyComponent):
    RunCommand     = event.StringProp('', settable=True)
    
    def init(self,monitor,refreshrate=1):
        self.refreshrate     = refreshrate
        self.keep_running    = True
        self.monitor         = monitor
        if self.monitor !=None:
            self.Test_Monitor()

    def Test_Monitor(self):
        if (self.keep_running):
            try:
                if self.RunCommand != self.monitor.RunCommand:
                    self.set_RunCommand(self.monitor.RunCommand)
            except:
                pass
        if (self.session.status!=0) and (self.keep_running):
            asyncio.get_event_loop().call_later(self.refreshrate, self.Test_Monitor)
        else:
            self.close_session()

    def close(self):
        self.keep_running = False

    def close_session(self):
        self.monitor.close()
    
    def update_monitor_object(self,monitor):
        self.monitor         = monitor
    
class Download_Link(ui.Widget):
    link = event.ListProp([], settable=True)
    def init(self):
        pass
        
    @event.reaction('link')
    def Download(self, *events):
        for ev in events:
            if len(ev.new_value)==2:
                global window
                link = window.document.createElement('a')
                link.download = ev.new_value[0]
                link.href = ev.new_value[1]
                link.click()
                self.set_link([]) 

class Test_sftp_alive(flx.PyComponent):
    Kill_session = event.BoolProp(False, settable=True)

    def init(self,ssh_client,refreshrate=1):
        self.redirect       = Redirect('/')
        self.refreshrate    = refreshrate
        self.ssh_client     = ssh_client
        self.keep_running   = True
        if self.ssh_client !=None:
            self.sftp_alive()

    def sftp_alive(self):
        if (self.keep_running):
            try:
                if not self.ssh_client.get_transport().is_active():
                    print('SSH disconnected')
                    self.keep_running = False
            except:
                self.keep_running = False
            if self.keep_running==False:
                self.set_Kill_session(True)
        if (self.session.status!=0) and (self.keep_running):
            asyncio.get_event_loop().call_later(self.refreshrate, self.sftp_alive)
        else:
            self.close_session()

    def close(self):
        self.keep_running = False

    def close_session(self):
        self.ssh_client.close()
        self.redirect.go()

class Redirect(flx.JsComponent):

    def init(self, dest):
        super().init()
        self.dest = dest

    @flx.action
    def go(self):
        global window
        window.location.href = self.dest

class Login(flx.PyComponent):

    def init(self):
        self.redirect = Redirect('/')
        with ui.HSplit(icon=ICON,title = Title):
            ui.Layout()
            with ui.VSplit():
                ui.Layout()
                with flx.GroupWidget(title='NeatSeq-Flow Log-In',style='font-size: 120%; border: 4px solid purple;min-width:450px;min-height:350px;'):
                    with ui.VBox():
                        ui.ImageWidget(stretch=True,
                                       source='https://neatseq-flow.readthedocs.io/en/latest/_images/NeatSeq_Flow_logo.png')
                        ui.Widget()  # Spacing
                        with flx.FormLayout():
                            self.input1 = flx.LineEdit(title='User Name')
                            self.input2 = flx.LineEdit(title='Password',password_mode=True)
                        ui.Widget()  # Spacing
                        self.b1 = flx.Button(text='Login')
                        Add_Tooltip(self.b1,HELP['login'])
                        ui.Widget()  # Spacing
                ui.Layout( )
            ui.Layout()

    @flx.reaction('input1.submit', 'b1.pointer_click')
    def login(self, *events):
        self.session.set_cookie('ARG1', self.input1.text)
        self.session.set_cookie('ARG2', self.input2.text)
        self.redirect.go()

class Run_NeatSeq_Flow_GUI(app.PyComponent):

    def init(self,arg1,arg2,USERSFILE,SMTPserver=None,sender_email=None,password=None,SSH_HOST=None,SSH_PORT=22,WOKFLOW_DIR=None):
        super().init()
        import os , datetime
        ssh_client = None
        self.UserName = ''
        Users={}
        if (SMTPserver!=None) and (SSH_HOST==None) and (USERSFILE!=None):
            try:
                for line in open(USERSFILE, 'r').readlines():
                    split_line = line.split(" ")
                    if len(split_line) ==2:
                        Users[split_line[0]]=[split_line[1].strip(),'']
                    if len(split_line) >2:
                        Users[split_line[0]]=[split_line[1].strip(),split_line[2].strip()]
            except:
                pass
        
        if SERVE:
            self.redirect = Redirect('/Login')
            try:
                ARG1  = self.session.get_cookie('ARG1')
                ARG2  = self.session.get_cookie('ARG2')
            except:
                self.session.set_cookie('ARG1', None)
                self.session.set_cookie('ARG2', None)
                self.redirect.go()
                return
            
            if SSH_HOST!=None:
                try:
                    import paramiko
                    ssh_client = paramiko.SSHClient()
                    ssh_client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
                    ssh_client.connect(SSH_HOST, username=ARG1, password=ARG2,port=SSH_PORT)
                    if ssh_client!=None:
                        if 'SSHClient' not in self.session.__dict__.keys():
                            self.session.SSHClient = [ssh_client]
                        else:
                            self.session.SSHClient.append(ssh_client)
                except:
                    self.session.set_cookie('ARG1', None)
                    self.session.set_cookie('ARG2', None)
                    ssh_client.close()
                    ssh_client = None
                    self.redirect.go()
                    return
                path = ''
                
                if SMTPserver!=None:
                    try:
                        message = "Subject: The user %s just logged in \n " % (self.session.get_cookie('ARG1'))
                        SMTPserver = SMTP_connect(sender_email,password,SMTPserver)
                        SMTPserver.sendmail(sender_email,sender_email, message)
                        #SMTPserver.quit()
                        print(str(datetime.datetime.now())+' The User '+ self.session.get_cookie('ARG1') +' just logged in ; Mail Sent to you')
                    except:
                        pass
            
            else:
            
                if ARG1 in Users.keys():
                    if ARG2 == arg2:
                        self.session.set_cookie('ARG3', ARG1)
                        self.session.set_cookie('ARG4', get_random_string(length=10))
                        try:
                            message = "Subject: Your NeatSeq-Flow login password \n" + self.session.get_cookie('ARG4')
                            SMTPserver = SMTP_connect(sender_email,password,SMTPserver)
                            SMTPserver.sendmail(sender_email,Users[ARG1][0], message)
                            #SMTPserver.quit()
                            print('Mail Sent to ' + Users[ARG1][0])
                        except:
                            pass
                        self.redirect.go()
                        return
                    else:
                        try:
                            ARG3  = self.session.get_cookie('ARG3')
                            ARG4  = self.session.get_cookie('ARG4')
                        except:
                            self.session.set_cookie('ARG1', None)
                            self.session.set_cookie('ARG2', None)
                            self.session.set_cookie('ARG3', None)
                            self.session.set_cookie('ARG4', None)
                            self.redirect.go()
                            return
                try:
                    ARG3  = self.session.get_cookie('ARG3')
                    ARG4  = self.session.get_cookie('ARG4')
                except:
                    self.session.set_cookie('ARG3', None)
                    self.session.set_cookie('ARG4', None)
                    self.redirect.go()
                    return
        
                
                if SMTPserver!=None:
                    if (ARG1 != ARG3) or (ARG1==None) or (ARG2==None) or (ARG3==None) or (ARG4==None) or (ARG2 != ARG4):
                         self.redirect.go()
                         return
                    path = Users[ARG1][1]
                    try:
                        message = "Subject: The user %s just logged in \n The user email is %s" % (self.session.get_cookie('ARG1'),Users[ARG1][0])
                        SMTPserver = SMTP_connect(sender_email,password,SMTPserver)
                        SMTPserver.sendmail(sender_email,sender_email, message)
                        #SMTPserver.quit()
                        print(str(datetime.datetime.now())+' The User '+ self.session.get_cookie('ARG1') +' just logged in ; Mail Sent to you')
                    except:
                        pass
                else:
                    if (ARG1!=arg1) or (ARG2 != arg2):
                        self.redirect.go()
                        return
                    path = ''
            self.UserName = ARG1
            self.session.set_cookie('ARG1', None)
            self.session.set_cookie('ARG2', None)
            self.session.set_cookie('ARG3', None)
            self.session.set_cookie('ARG4', None)
            with flx.Layout(icon=ICON,title = Title):
                NeatSeq_Flow_GUI(path,ssh_client,WOKFLOW_DIR)

def get_random_string(length=24, allowed_chars=None):
    import random
    """ Produce a securely generated random string.
    NOTE: secure random string generation implementation is adapted from the Django project.
    With a length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    allowed_chars = allowed_chars or ('abcdefghijklmnopqrstuvwxyz' +
                                      'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    try:
        srandom = random.SystemRandom()
    except NotImplementedError:  # pragma: no cover
        srandom = random
        logger.warning('Falling back to less secure Mersenne Twister random string.')
        bogus = "%s%s%s" % (random.getstate(), time.time(), 'sdkhfbsdkfbsdbhf')
        random.seed(hashlib.sha256(bogus.encode()).digest())

    return ''.join(srandom.choice(allowed_chars) for i in range(length))

def SMTP_connect(sender_email,password,SMTPserver=None,try_for=5):
    import smtplib, ssl,getpass,sys
    from tornado.web import decode_signed_value
    status=-1
    if SMTPserver!=None:
        try:
            status = SMTPserver.noop()[0]
        except:  # smtplib.SMTPServerDisconnected
            status = -1
        print(status)
        if status == 250:
            return SMTPserver
    count=0
    while (status!=250)  & (count < try_for):
        port           = 465  # For SSL
        smtp_server    = "smtp.gmail.com"
        context    = ssl.create_default_context()
        SMTPserver = smtplib.SMTP_SSL(smtp_server, port, context=context)
        SMTPserver.login(sender_email,
                         decode_signed_value(flx.config.cookie_secret,
                                             'email',
                                             password).decode('UTF-8') )
        try:
            status = SMTPserver.noop()[0]
        except:  # smtplib.SMTPServerDisconnected
            status = -1
        print(count)
        print(status)
        count=count+1
    return SMTPserver

def set_gmail_connection():
    import smtplib, ssl,getpass,sys
    SMTPserver   = None
    sender_email = None
    password     = None
    
    sender_email   = input('Enter your Gmail address and press enter:\n')
    
    password       = create_signed_value(flx.config.cookie_secret,
                                         'email',
                                         getpass.getpass("Type your Gmail address password and press enter:\n"))
    
    try:
        SMTPserver = SMTP_connect(sender_email,password)
    except:
        print('Error: Could not login to your Gmail account')
        print('Make sure to Turn Allow less secure apps to ON at: https://myaccount.google.com/lesssecureapps')
        sys.exit(1)
    #SMTPserver.quit()
    return [SMTPserver,password,sender_email]
    
class Manage_Participants(flx.Component):
    
    def init(self,app_name,LOG_DIR=None,max_count=30,refreshrate=0.5):
        self.app_name    = app_name
        self.refreshrate = refreshrate
        self.LOG_DIR     = LOG_DIR
        self.names       = []
        self.sessions_id = []
        self.count       = 0
        self.max_count   = max_count
        self.update_participants()
        
    def update_participants(self):
        import datetime
        import gc
        # Query the app manager to see who's Logedin 
        sessions    = flx.manager.get_connections(self.app_name)
        names       = [s.app.UserName for s in sessions]
        sessions_id = [s.id for s in sessions]
        
        for session in sessions:
            if 'Process' in session.__dict__.keys():
                for Proces in session.Process:
                    if not Proces.is_alive():
                        Proces.terminate()
                        Proces.join()
                        session.Process.remove(Proces)
            if 'Threads' in session.__dict__.keys():
                for Proces in session.Threads:
                    if not Proces.is_alive():
                        Proces.join()
                        session.Threads.remove(Proces)
            if 'Pop_Process' in session.__dict__.keys():
                for Proces in session.Pop_Process:
                    if Proces.poll() != None:
                        Proces.kill()
                        session.Pop_Process.remove(Proces)
        if self.sessions_id != sessions_id:
            self.names = names
            for closed_session in set(self.sessions_id).difference(sessions_id):
                for session in self.sessions:
                    if session.id == closed_session:
                        if 'Process' in session.__dict__.keys():
                            for Proces in session.Process:
                                Proces.terminate()
                                Proces.join()
                                session.Process.remove(Proces)
                        if 'Threads' in session.__dict__.keys():
                            for Proces in session.Threads:
                                Proces.join()
                                session.Threads.remove(Proces)
                        if 'Pop_Process' in session.__dict__.keys():
                            for Proces in session.Pop_Process:
                                Proces.kill()
                                session.Pop_Process.remove(Proces)
                        if 'SSHClient' in session.__dict__.keys():
                            for SSHClient in session.SSHClient:
                                try:
                                    SSHClient.close()
                                except:
                                    pass
                                session.SSHClient.remove(SSHClient)
                        session.close()
                        gc.collect()
                                        
            self.sessions_id = sessions_id
            self.count = self.max_count
            print(names)
        self.sessions = sessions
            
        if (self.LOG_DIR!=None) and (self.count==self.max_count):
            if (os.path.exists(self.LOG_DIR)):
                self.count = 0
                date = datetime.datetime.now()
                try:
                    with open(os.path.join(self.LOG_DIR,date.strftime("%x").replace('/','.')), 'a') as file:
                        for name in zip(names,sessions_id):
                            if name[0]!='':
                                file.write(name[0]+'\t'+name[1]+'\t'+date.strftime("%x")+'\t'+date.strftime("%X")+'\n')
                except:
                    pass
        self.count = self.count + 1
        del sessions
        asyncio.get_event_loop().call_later(self.refreshrate, self.update_participants)

class Manage_UpTime(flx.Component):
    
    def init(self,UPTIMELIMIT,refreshrate=0.5):
        import time
        self.refreshrate = refreshrate
        self.UPTIMELIMIT = UPTIMELIMIT
        self.StarTime    = time.time()
        self.UpTime()
    
    def UpTime(self):
        import time
        import sys
        global keep_runing
        
        # print((time.time()-self.StarTime)/3600)
        if ((time.time()-self.StarTime)/3600)>self.UPTIMELIMIT:
            keep_runing = False
            print('Bye Bye ..')
            exit()
        else:
            asyncio.get_event_loop().call_later(self.refreshrate, self.UpTime)
    
if __name__ == '__main__':
    #getting arguments from the user 
    import argparse
    parser = argparse.ArgumentParser(description='NeatSeq-Flow GUI By Liron Levin ')
    parser.add_argument('--Server',dest='Server',action='store_true', default=True,
                        help='Run as Server')
    parser.add_argument('--PORT',dest='PORT',metavar="CHAR",type=int,default=None,
                        help='''Use this port in which to run the app,
                                If not set will search for open port
                                (Works only When --Server is set)
                                ''')
    parser.add_argument('--UPTIMELIMIT',dest='UPTIMELIMIT',metavar="CHAR",type=float,default=None,
                        help='''ShutDown after this amount of time (H)
                                ''')
    parser.add_argument('--HOST',dest='HOST',metavar="CHAR",type=str,default=None,
                        help='''The host name/ip to serve the app,
                            If not set, will try to identify automatically
                            (Works only When --Server is set)
                            ''')
    parser.add_argument('--SSL',dest='SSL',action='store_true',
                        help='Use SSL (Only When --Server is set)')
    parser.add_argument('--SSH_HOST',dest='SSH_HOST',metavar="CHAR",type=str,default="",
                        help='''Connect using SSH to a remote host,
                                NeatSeq-Flow needs to be installed on the remote host
                                (Works only When --Server is set)''')
    parser.add_argument('--SSH_PORT',dest='SSH_PORT',metavar="CHAR",type=int,default=22,
                        help='''When --SSH_HOST is set use this ssh port to connect to a remote host.
                                ''')
    parser.add_argument('--USER',dest='USER',metavar="CHAR",type=str,default="",
                        help='User Name For This Serve (Works only When --Server is set)')
    parser.add_argument('--PASSW',dest='PASSW',metavar="CHAR",type=str,default="",
                        help='Password For This Serve (Works only When --Server is set)')
    parser.add_argument('--USERSFILE',dest='USERSFILE',metavar="CHAR",type=str,default="",
                        help='''
                                 The location of a Users file in which a list of users, E-mails addresses and Users Directorys are separated by one space (as:USER user@example.com /USER/DIR).
                                 The login password will be send to the user e-mail after filling its user name and the password generated at the beginning of the run (Works only When --Server is set).
                                 You will need a Gmail account to send the password to the users (you will be prompt to type in your Gmail address and password) 
                                 '''
                                 )
    parser.add_argument('--UNLOCK_USER_DIR',dest='UNLOCK',action='store_true',
                        help="Don't Lock Users to their Directory Or to the Current Working Directory")
    parser.add_argument('--WOKFLOW_DIR',dest='WOKFLOW_DIR',metavar="CHAR",type=str,default=None,
                        help='''A Path to a Directory containing work-flow files to choose from at log-in. 
                                Works only When --Server is set.
                                If --SSH_HOST is set, the Path needs to be in the remote host.
                        ''')
    parser.add_argument('--CONDA_BIN',dest='CONDA_BIN',metavar="CHAR",type=str,default='',
                        help='''A path to a the CONDA bin location. 
                                If --SSH_HOST is set, the Path needs to be in the remote host.
                        ''')
    parser.add_argument('--LOG_DIR',dest='LOG_DIR',metavar="CHAR",type=str,default='',
                        help='''A path to a directory to save log files about users statistics. 
                                Only woks If --Server is set.
                                In any way the path needs to be at the local host.
                        ''')
    args          = parser.parse_args()
    SERVE         = args.Server
    LOCK_USER_DIR = not args.UNLOCK
    CONDA_BIN     = args.CONDA_BIN
    #temp_MODULES_TEMPLATES = Load_MODULES_TEMPLATES()
    temp_MODULES_TEMPLATES = Update_Yaml_Data(MODULES_TEMPLATES_FILE,'TEMPLATES', 'MODULES_TEMPLATES.yaml',"Modules Templates")
    if len(temp_MODULES_TEMPLATES) > 0:
        MODULES_TEMPLATES = temp_MODULES_TEMPLATES
    icon = os.path.join(os.path.realpath(os.path.expanduser(os.path.dirname(os.path.abspath(__file__))+os.sep+"..")),'neatseq_flow_gui','NeatSeq_Flow.ico')
    #icon = app.assets.add_shared_data('ico.icon', open(icon, 'rb').read())
    ICON = app.assets.add_shared_data('ico.icon', open(icon, 'rb').read())
    if args.Server:
        import socket 
        from tornado.web import create_signed_value
        LOG_DIR = None
        if args.LOG_DIR!='':
            if (os.path.exists(args.LOG_DIR)) and (os.path.isdir(args.LOG_DIR)):
                LOG_DIR = args.LOG_DIR
            else:
                print('The LOG_DIR you entered does not exists or it is not a directory')
                sys.exit(1)
        
        flx.config.cookie_secret = get_random_string()
        if args.HOST!=None:
            Host = args.HOST
        else:
            Host = socket.gethostbyname(socket.gethostname())
        if args.SSL:
            CERTFILE = 'self-signed.crt'
            KEYFILE  = 'self-signed.key'
            SLL_COMMAND = 'openssl req  -subj /CN=%s -x509 -nodes -days 1 -batch -newkey rsa:2048 -keyout %s -out %s' % (Host,
                                                                                                        KEYFILE,
                                                                                                        CERTFILE)
            os.system(SLL_COMMAND)
            # use the self-signed certificate as if specified in normal config
            flx.config.ssl_certfile = CERTFILE
            flx.config.ssl_keyfile  = KEYFILE
        
        Login_m = flx.App(Login)
        Login_m.serve()
        
        if args.SSH_HOST!='':
            try:
                import paramiko
            except:
                print('You need to install the "paramiko" package to use the SHH options')
                sys.exit(1)
            print('Do you want to use gmail to notify you when user logs-in? (yes/no)')
            if input() == 'yes':
                [SMTPserver,password,sender_email] = set_gmail_connection()
            else:
                SMTPserver     = None
                sender_email   = None
                password       = None
            args.USERSFILE     = None
            SSH_HOST = args.SSH_HOST
        else:
            SSH_HOST = None
            if os.path.isfile(args.USERSFILE):
                
                args.USERSFILE = os.path.abspath(args.USERSFILE)
                [SMTPserver,password,sender_email] = set_gmail_connection()
                if args.PASSW=='':
                    args.PASSW = get_random_string(length=7)
                print('Password: '+ args.PASSW)
                
            else:
                SMTPserver     = None
                sender_email   = None
                password       = None
                args.USERSFILE = None
                
                if args.USER=='':
                    args.USER  = get_random_string(length=7)
                if args.PASSW=='':
                    args.PASSW = get_random_string(length=7)
                print('User Name: '+ args.USER)
                print('Password: '+ args.PASSW)
        
        m = app.App(Run_NeatSeq_Flow_GUI,
                    args.USER,
                    args.PASSW,
                    args.USERSFILE,
                    SMTPserver,
                    sender_email,
                    password,
                    SSH_HOST,
                    args.SSH_PORT,
                    args.WOKFLOW_DIR
                    )

        app.create_server(host=Host,port=args.PORT)
        m.serve('')
        Manage_Participants(m.name,LOG_DIR)
        # keep_runing = True
        import signal
        if args.UPTIMELIMIT!=None:
            Manage_UpTime(args.UPTIMELIMIT)
        
        while keep_runing:
            try:
                flx.start()
                print('Do you want to exit? (yes/no)')
                signal.signal(signal.SIGALRM, lambda x,y: 1/0 )
                signal.alarm(5)
                if input() == 'yes':
                    signal.alarm(0)
                    keep_runing = False
                    print('Bye Bye ..')
                    #sys.exit(1)
            except :
                if keep_runing:
                    print(' Keep going ')
        try:
            #flx.stop()
            sys.exit(1)
        except :
            sys.exit(1)
    else:
        m = app.App(NeatSeq_Flow_GUI,os.getcwd()).launch(runtime ='app',size=(1300, 750),title='NeatSeq-Flow GUI',icon=icon)
        app.run()


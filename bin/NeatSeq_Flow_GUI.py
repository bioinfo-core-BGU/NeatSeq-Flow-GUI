#!/usr/bin/env python



__author__ = "Liron Levin"
__version__ = "1.0"


__affiliation__ = "Bioinformatics Core Unit, NIBN, Ben Gurion University"



from flexx import app, event, ui
import os,sys

sys.path.append(os.path.realpath(os.path.expanduser(os.path.dirname(os.path.abspath(__file__))+os.sep+"..")))

MODULES_TEMPLATES_FILE= 'https://raw.githubusercontent.com/bioinfo-core-BGU/NeatSeq-Flow-GUI/master/neatseq_flow_gui/TEMPLATES/MODULES_TEMPLATES.yaml'

STEPS = {'Merge': {'module': 'merge', 'script_path': None  },

         }

COLORS = ('#eee', '#999', '#555', '#111',
          '#f00', '#0f0', '#00f', '#ff0', '#f0f', '#0ff',
          '#a44', '#4a4', '#44a', '#aa4', '#afa', '#4aa',
          )

CLUSTER = {'Executor': 'Local',
           'Default_wait': '10',
           'Qsub_opts': '-V -cwd',
           'Qsub_path': '/path/to/qstat',
           'Qsub_q': 'queue.q',
           'module_path': '/path/to/modules',
           'conda': {'path': '{Vars.conda.base}', 'env': '{Vars.conda.env}' }
           }

VARS = {'Programs': {},
        'Genome': {},
        'conda': {'base': None, 'env': None }
        }

Executor = ['SGE', 'SLURM', 'Local']

MODULES_TEMPLATES = {'Basic': {'Basic_New_Step': {'base': None, 'module': None, 'script_path': None, }}

                     }
FILE_TYPES = ['Single', 'Forward', 'Reverse', 'Nucleotide', 'Protein', 'SAM', 'BAM', 'REFERENCE', 'VCF', 'G.VCF']

FIELDS2SPLIT = ['base'] 

html_cite='''
    <p class=MsoNormal dir=LTR style='margin-top:0cm;margin-bottom:0cm;margin-bottom:.0000pt;
    text-align:left;line-height:normal;direction:ltr;unicode-bidi:embed'><b>NeatSeq-Flow
    Graphical User Interface By Liron Levin</b><br>
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


class Graphical_panel(ui.CanvasWidget):
    Selected_step = event.StringProp('', settable=True)
    Steps_Data = event.DictProp(STEPS, settable=True)
    refresh_flag = event.BoolProp(False, settable=True)

    def init(self):

        super().init()
        self.new_size = None
        self.ctx = self.node.getContext('2d')
        # Set mouse capturing mode
        self.set_capture_mouse(2)
        self.Button_list = []
        self.Button_count = 0
        self.steps = self.Steps_Data
        self.calculate_steps_conections()
        if len(self.steps.keys()) > 0:
            for step in self.steps.keys():
                if 'SKIP' in self.steps[step].keys():
                    self.create_Button(step, self, [50, 50],'gray')
                else:
                    self.create_Button(step, self, [50, 50])

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
    flag = event.BoolProp(False, settable=True)
    open_filepicker = event.StringProp('', settable=True)
    file_path = event.ListProp([], settable=True)
    workflow_file = event.ListProp([], settable=True)
    save_workflow_file = event.ListProp([], settable=True)
    Steps_Data_update = event.BoolProp(False, settable=True)
    Steps_Data = event.DictProp({}, settable=True)
    Data = event.DictProp({}, settable=True)
    converter = event.DictProp({}, settable=True)
    options = event.ListProp([], settable=True)
    Vars_data = event.DictProp({}, settable=True)

    def init(self):
        self.current_selected = None
        with ui.HSplit() as self.main_lay:
            with ui.VSplit(flex=0.25) as self.tree_lay:
                with ui.HSplit(flex=0.08, style='min-height: 190px; max-height: 190px;'):
                    with ui.FormLayout(flex=0.01) as self.form:
                        self.tree_key_b = ui.LineEdit(title='Key:', text='')
                        self.tree_value_b = ui.LineEdit(title='Value:', text='')

                        self.tree_value_options_b = ui.ComboBox(title='Value options:', editable=False, text='',
                                                                placeholder_text='Value options:')
                        self.tree_add_option_b = ui.Button(text='Add')
                    with ui.VSplit(flex=0.0035,style='min-width: 90px; max-width: 90px;'):
                        self.tree_submit_b      = ui.Button(text='Edit')
                        self.tree_new_b         = ui.Button(text='New')
                        self.file_path_b        = ui.Button(text='Browse')
                        self.tree_duplicate_b   = ui.Button(text='Duplicate')
                        self.tree_remove_b      = ui.Button(text='Remove')
                self.tree = ui.TreeWidget(flex=0.2, max_selected=1)
                self.tree.text = 'Top_level'
                ui.Label(text='__________________')
            with ui.VSplit(flex=0.6) as self.canvas_lay:
                with ui.layouts._form.BaseTableLayout(flex=0.03, style='min-height: 35px; max-height: 35px;'):
                    with ui.HSplit(style='min-height: 30px; max-height: 30px;'):
                        self.tree_module_b = ui.ComboBox(title='Use Module:', editable=False, text='Choose Module',
                                                         style='min-width: 300px;',
                                                         placeholder_text='Choose Module',
                                                         options=MODULES_TEMPLATES.keys())
                        self.tree_create_new_step_b = ui.Button(text='Create New Step')
                        self.tree_Load_WorkFlow_b = ui.Button(text='Load WorkFlow')
                        self.tree_save_WorkFlow_b = ui.Button(text='Save WorkFlow')
                self.Graphical_panel = Graphical_panel(flex=0.5, style='min-height:600px; overflow-y: auto;')
                with self.tree:
                    self.create_tree(self.Graphical_panel.Steps_Data)
                    self.collapse_all_not_selectd(self.tree)

        
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
                self.tree_value_b.set_text(self.file_path[0][0])
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
        self.set_flag(True)
        for ev in events:
            if self.tree_module_b.selected_index != -1:
                if MODULES_TEMPLATES[
                    self.tree_module_b.selected_key].keys() not in self.Graphical_panel.Steps_Data.keys():
                    self.set_Vars_data(MODULES_TEMPLATES[self.tree_module_b.selected_key])
                    with self.tree:
                        self.create_tree(MODULES_TEMPLATES[self.tree_module_b.selected_key])

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
                        steps[tree.title] = tree.text.lstrip('[').rstrip(']')
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
                        if (tree.text.startswith('[') and tree.text.endswith(']') ): #(tree.title in FIELDS2SPLIT):
                            steps[tree.title] = tree.text.lstrip('[').rstrip(']').split(',')
                        else:
                            steps[tree.title] = [tree.text]
                    else:
                        steps[tree.title] = [tree.text.lstrip('[').rstrip(']')]
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
        options = {'base': lambda: filter(lambda x: x != self.current_selected.parent.text,
                                          self.Graphical_panel.Steps_Data.keys()),
                   'scope': lambda: ['sample', 'project']
                   }

        if key in options.keys():
            return options[key]()
        else:
            return None

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
                        if self.tree_value_b.text != '':
                            self.current_selected.set_text(self.tree_value_b.text)
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
                        if self.tree_value_b.text.lstrip('[').rstrip(']') != '':
                            if (self.current_selected.title == 'base') or (len(self.current_selected.title) ==0 and self.current_selected.text=='base') or (self.tree_value_b.text.startswith('[') and self.tree_value_b.text.endswith(']')):
                                self.tree_value_b.set_text('['+self.tree_value_b.text.lstrip('[').rstrip(']') + ',' + self.tree_value_options_b.text+']')
                            else:
                                self.tree_value_b.set_text(self.tree_value_b.text + ' ' + self.tree_value_options_b.text)
                        elif self.tree_value_b.text.startswith('[') and self.tree_value_b.text.endswith(']'):
                            self.tree_value_b.set_text('['+self.tree_value_options_b.text+']')
                        else:
                            self.tree_value_b.set_text(self.tree_value_options_b.text)
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

    @event.reaction('tree_duplicate_b.pointer_click')
    def tree_duplicate_button_click(self, *events):
        for ev in events:
            if self.current_selected != None:
                with self.current_selected.parent:
                    if len(self.current_selected.title) > 0:
                        self.create_tree({self.current_selected.title:self.current_selected.text})
                    else:
                        dict=self.tree2dict(self.current_selected)
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
                        if len(self.options) > 0:
                            self.tree_value_options_b.set_options(self.options)
                            self.tree_value_options_b.set_editable(True)
                        else:
                            self.tree_value_options_b.set_editable(False)
                            self.tree_value_options_b.set_options([])
                            self.tree_value_options_b.set_selected_index(-1)
                            self.tree_value_options_b.set_text('')


                else:
                    self.tree_key_b.set_text(self.current_selected.text)
                    self.tree_value_b.set_text('')
                    if len(self.current_selected.children) > 0:
                        self.tree_value_b.set_disabled(True)
                        self.tree_value_options_b.set_editable(False)
                        self.tree_value_options_b.set_options([])
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
                                self.tree_value_options_b.set_options([])
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
                        steps[tree.title] = tree.text.lstrip('[').rstrip(']')
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
                        if self.tree_value_b.text.lstrip('[').rstrip(']') != '':
                            if (self.current_selected.title == 'base') or (len(self.current_selected.title) ==0 and self.current_selected.text=='base') or (self.tree_value_b.text.startswith('[') and self.tree_value_b.text.endswith(']')):
                                self.tree_value_b.set_text('['+self.tree_value_b.text.lstrip('[').rstrip(']') + ',' + self.tree_value_options_b.text+']')
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
                        self.tree_value_options_b.set_options([])
                        self.tree_value_options_b.set_selected_index(-1)
                        self.tree_value_options_b.set_text('')


                else:
                    self.tree_key_b.set_text(self.current_selected.text)
                    self.tree_value_b.set_text('')
                    if len(self.current_selected.children) > 0:
                        self.tree_value_b.set_disabled(True)
                        self.tree_value_options_b.set_editable(False)
                        self.tree_value_options_b.set_options([])
                        self.tree_value_options_b.set_selected_index(-1)
                        self.tree_value_options_b.set_text('')
                    else:
                        self.tree_value_b.set_disabled(False)
                        if self.get_options(self.current_selected.text) != None:
                            self.tree_value_options_b.set_options(self.get_options(self.current_selected.text))
                            self.tree_value_options_b.set_editable(True)
                        else:
                            self.tree_value_options_b.set_editable(False)
                            self.tree_value_options_b.set_options([])
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
        with ui.VSplit(flex=0.1, padding=20) as self.layout:
            with ui.layouts._form.BaseTableLayout(flex=0.05, style='min-height: 35px; max-height: 35px;'):
                with ui.HSplit(style='min-height: 30px; max-height: 30px;'):
                    self.tree_title_b = ui.LineEdit(text='',
                                                    placeholder_text='Project Title')
                    self.add_project_file_b = ui.Button(text='Add Project File')
                    self.add_sample_file_b  = ui.Button(text='Add Sample File')
                    self.load_sample_file_b = ui.Button(text='Load Sample File')
                    self.save_sample_file_b = ui.Button(text='Save Sample File')
                    
            ui.Label(text='Project Level:',style='padding-left: 20px; font-size: 120% ;')
            with ui.Layout(flex=0.2,title='Project Level',style='overflow-y:auto;padding: 15px ;min-height:130px ;border: 1px solid gray; border-radius: 10px;'):
                self.project = ui.VSplit()
                
            ui.Label(text='Sample Level:',style='padding-left: 20px; font-size: 120% ;')
            with ui.Layout(flex=0.5, title='Sample Level',style='overflow-y:auto;padding: 15px ;min-height:250px ;border: 1px solid gray; border-radius: 10px;'):
                self.sample = ui.VSplit()

            self.project.spacer = None
            self.sample.spacer = None
            ui.Label(flex=0.1, text='')

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
        if 'Title' in samples_data.keys():
            self.tree_title_b.set_text(samples_data['Title'])

        if 'project_data' in samples_data.keys():
            for project_type in samples_data['project_data'].keys():
                for project_file in samples_data['project_data'][project_type]:
                    self.add_project_file(project_file, project_type)

        for name in samples_data.keys():
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
            if project.id.startswith('HBox'):
                project_file_type = project.file_type.text
                project_file_path = project.file_path.text
                if project_file_type != '':
                    if project_file_type in sample_data['project_data'].keys():
                        sample_data['project_data'][project_file_type].append(project_file_path)
                    else:
                        sample_data['project_data'][project_file_type] = [project_file_path]
        for samples in self.sample.children:
            if samples.id.startswith('HBox'):
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
            with ui.HBox(padding=0) as sample:
                sample.sample_name = ui.LineEdit(placeholder_text='Sample Name', text=sample_name)
                sample.sample_file_type = ui.ComboBox(placeholder_text='File Type', editable=True, text=file_type,
                                                      options=FILE_TYPES)
                sample.sample_file_path = ui.LineEdit(placeholder_text='File Path', text=file_path)
                ui.Button(text='Remove')
            self.sample.spacer = ui.Label(flex=0.1, text='_')

    def add_project_file(self, file_path='', file_type=''):
        with self.project:
            if self.project.spacer != None:
                self.project.spacer.dispose()
            with ui.HBox(padding=0) as project:
                project.file_type = ui.ComboBox(placeholder_text='File Type', editable=True, text=file_type,
                                                options=FILE_TYPES)
                project.file_path = ui.LineEdit(placeholder_text='File Path', text=file_path)
                ui.Button(text='Remove')

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


def select_files(select_style='Single', select_type='Open', wildcard='*'):
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
                    return [[path, path]]
                else:
                    return []
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
        return path
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
                return [[path, path]]
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
        
        return path
        
        
        
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


def setup_yaml(yaml, OrderedDict):
    """ http://stackoverflow.com/a/8661021 """
    represent_dict_order = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
    yaml.add_representer(OrderedDict, represent_dict_order)
    return yaml


class Run_NeatSeq_Flow(ui.Widget):
    open_filepicker = event.StringProp('', settable=True)
    NeatSeq_bin = event.ListProp([], settable=True)
    conda_bin = event.ListProp([], settable=True)
    conda_env = event.ListProp([], settable=True)
    Project_dir = event.ListProp([], settable=True)
    sample_file = event.ListProp([], settable=True)
    parameter_file = event.ListProp([], settable=True)
    command = event.ListProp([], settable=True)
    Terminal = event.StringProp('', settable=True)
    

    def init(self):
        with ui.Layout(style='padding: 30px;'):
            with ui.HSplit():               
                with ui.Layout(title='NeatSeq-Flow Information', style='min-height: 250px; max-height: 250px;'):
                    with ui.VSplit():
                       
                        with ui.Layout(title='NeatSeq-Flow script location', style='min-height: 70px; max-height: 70px;'):
                            ui.Label(text='NeatSeq-Flow script location:',style='padding-left: 0px; font-size: 120% ;')
                            with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                self.NeatSeq_bin_L = ui.LineEdit(text='neatseq_flow.py')
                                self.NeatSeq_bin_b = ui.Button(text='Browse', style='max-width: 100px; ')

                        with ui.Layout(title='Conda bin location', style='min-height: 70px; max-height: 70px;'):
                            ui.Label(text='Conda bin location:',style='padding-left: 0px; font-size: 120% ;')
                            with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                self.conda_bin_L = ui.LineEdit(text='')
                                self.conda_bin_b = ui.Button(text='Browse', style='max-width: 100px; ')

                        with ui.Layout(title='Conda environment to use', style='min-height: 70px; max-height: 70px;'):
                            ui.Label(text='Conda environment to use:',style='padding-left: 0px; font-size: 120% ;')
                            with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                self.conda_env_L = ui.ComboBox(editable=True, text='',
                                                               placeholder_text='Choose Conda Environment')
                                self.conda_env_b = ui.Button(text='Search', style='max-width: 100px; ')

                with ui.Layout(title='Project Information', style='min-height: 250px; max-height: 250px;'):
                    with ui.VSplit():
                        with ui.Layout(title='Project Directory', style='min-height: 70px; max-height: 70px;'):
                            ui.Label(text='Project Directory:',style='padding-left: 0px; font-size: 120% ;')
                            with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                self.Project_dir_L = ui.LineEdit(text='')
                                self.Project_dir_b = ui.Button(text='Browse', style='max-width: 100px; ')

                        with ui.Layout(title='Sample File', style='min-height: 70px; max-height: 70px;'):
                            ui.Label(text='Sample File:',style='padding-left: 0px; font-size: 120% ;')
                            with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                self.sample_file_L = ui.LineEdit(text='')
                                self.sample_file_b = ui.Button(text='Browse', style='max-width: 100px;')

                        with ui.Layout(title='Parameter File', style='min-height: 70px; max-height: 70px;'):
                            ui.Label(text='Parameter File:',style='padding-left: 0px; font-size: 120% ;')
                            with ui.HSplit(style='min-height: 35px; max-height: 35px;'):
                                self.parameter_file_L = ui.LineEdit(text='')
                                self.parameter_file_b = ui.Button(text='Browse', style='max-width: 100px;')
            self.Generate_scripts_b = ui.Button(text='Generate scripts', style='max-height: 35px; max-width: 200px;')
            self.Run_scripts_b      = ui.Button(text='Run scripts', style='max-height: 35px; max-width: 200px;')
            self.Run_Monitor_b      = ui.Button(text='Run Monitor', style='max-height: 35px; max-width: 200px;')
            
            ui.Label(text='Terminal:',style='padding-left: 0px; padding-top: 20px; font-size: 120% ;')
            self.label = ui.Label(wrap=0, style='padding: 15px ;border: 1px solid gray; border-radius: 10px; height: 150px; overflow-y: auto;')
            ui.Label()

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

    @event.reaction('Generate_scripts_b.pointer_click')
    def on_Generate_scripts_b_click(self, *events):
        for ev in events:
            self.set_command(['Generate_scripts', self.NeatSeq_bin_L.text, self.conda_bin_L.text, self.conda_env_L.text,
                              self.Project_dir_L.text, self.sample_file_L.text, self.parameter_file_L.text])
    
    @event.reaction('Run_scripts_b.pointer_click')
    def on_Run_scripts_b_click(self, *events):
        for ev in events:
            self.set_command(['Run_scripts',self.Project_dir_L.text])
    
    @event.reaction('Run_Monitor_b.pointer_click')
    def on_Run_Monitor_b_b_click(self, *events):
        for ev in events:
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
            overflow-x: auto;
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

          border-radius: 8px;
          background-color: white;
          border: 2px solid gray;
          box-shadow: 0 2px 2px 0 rgba(0,0,0,0.24), 0 2px 2px 0 rgba(0,0,0,0.19);
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
          padding-right: 25px;

        }

    .flx-Button:hover:after {
          right: 0;
        }


     .flx-Graphical_panel .flx-Button {

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




        """

    Running_script               = event.IntProp(0, settable=True)
    Generating_scripts           = event.IntProp(0, settable=True)
    Running_Commands             = event.DictProp({}, settable=True)
    
    
    def init(self):
        with ui.VSplit():
            with ui.TabLayout(flex=0.9) as self.TabLayout:
                self.step_info = Step_Tree_Class(title='Work-Flow')
                self.samples_info = Samples_info(title='Samples')
                self.vars_info = Only_Tree_Class(VARS, title='Vars')
                self.cluster_info = Only_Tree_Class(CLUSTER, title='Cluster')
                self.Run = Run_NeatSeq_Flow(title='Run')
                ui.IFrame(url='http://neatseq-flow.readthedocs.io/projects/neatseq-flow-modules/en/latest/index.html',
                          title='Help')
            
            self.label = ui.Label(text='NeatSeq-Flow Graphical User Interface By Liron Levin',
                                  style='padding-left: 40px; background: #e8eaff; min-height: 15px; font-size:15px; transition: all 0.5s;')
            self.label.set_capture_mouse(2)
            self.label.set_html(html_cite)
            self.TabLayout.set_capture_mouse(2)
            self.Terminal_string = ''

    @event.reaction('label.pointer_click')
    def on_label_click(self, *events):
        self.label.set_flex(0.2)

    @event.reaction('TabLayout.pointer_move')
    def on_label_after(self, *events):
        self.label.set_flex(0.02)


    def filepicker_options(self, key):
        options = {'file_path': lambda: self.step_info.set_file_path(select_files('Single', 'Open')),
                   'NeatSeq_bin': lambda: self.Run.set_NeatSeq_bin(select_files('Single', 'Open')),
                   'conda_bin': lambda: self.Run.set_conda_bin(select_files('Single', 'Dir')),
                   'Project_dir': lambda: self.Run.set_Project_dir(select_files('Single', 'Dir')),
                   'sample_file_to_run': lambda: self.Run.set_sample_file(select_files('Single', 'Open')),
                   'parameter_file_to_run': lambda: self.Run.set_parameter_file(select_files('Single', 'Open')),
                   'Cluster_file_path': lambda: self.cluster_info.set_file_path(select_files('Single', 'Open')),
                   'Vars_file_path': lambda: self.vars_info.set_file_path(select_files('Single', 'Open')),
                   'workflow_file': lambda: self.step_info.set_workflow_file(select_files('Single', 'Open')),
                   'save_workflow_file': lambda: self.step_info.set_save_workflow_file(select_files('Single', 'Save')),
                   'project': lambda: self.samples_info.set_project_files(select_files(select_style='Multy')),
                   'samples': lambda: self.samples_info.set_sample_files(select_files(select_style='Multy')),
                   'load_samples_file': lambda: self.samples_info.set_load_samples_file(select_files('Single', 'Open')),
                   'save_samples_file': lambda: self.samples_info.set_save_samples_file(select_files('Single', 'Save'))
                   }
        if key in options.keys():
            return options[key]()
        else:
            return None

    def command_pars(self, key):
        options = {'conda_env': lambda: self.conda_env_options(key[1]),
                   'Generate_scripts': lambda: self.Generate_scripts_command(key[1], key[2], key[3], key[4], key[5],
                                                                             key[6]),
                   'Run_scripts': lambda: self.Run_scripts_command(key[1]),
                   'Run_Monitor': lambda: self.Run_Monitor_command(key[1]),
                   
                   }
        if key[0] in options.keys():
            return options[key[0]]()
        else:
            return None

    def conda_env_options(self, conda_bin):
        import os
        from subprocess import Popen, PIPE, STDOUT
        temp_command = ''
        if len(conda_bin) > 0:
            temp_command = conda_bin
        temp_command = os.path.join(temp_command, 'conda')
        temp_command = temp_command + ' info --env'
        err_flag = False
        try:
            self.Run.set_Terminal(self.Terminal_string + '[Searching for Conda Environments]: Searching...\n')
            conda_proc = Popen(temp_command, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
            outs, errs = conda_proc.communicate(timeout=15)

        except :
            err_flag = True
            conda_proc.kill()
            outs, errs = conda_proc.communicate()
            
        
        if len(errs) > 0:
            self.Terminal_string = self.Terminal_string + '[Searching for Conda Environments]: Error:\n' + errs
        if len(outs) > 0:
            options = list(map(lambda y: y.split(os.sep)[0].replace('*', '').replace(' ', ''),
                           filter(lambda x: len(x.split(os.sep)) > 1, outs.split('\n'))))
            self.Run.set_conda_env(options)
            if len(options) > 0:
                self.Terminal_string = self.Terminal_string +  ' [Searching for Conda Environments]: '+ str(len(options)) + ' Conda Environments were found \n'
        if err_flag:
            self.Terminal_string = self.Terminal_string + '[Searching for Conda Environments]: Finished with Error!! \n'    
        self.Run.set_Terminal(self.Terminal_string)

    def Generate_scripts_command(self, NeatSeq_bin, conda_bin, conda_env, Project_dir, sample_file, parameter_file):
        import os
        from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
        
        if len(Project_dir) == 0:
            Project_dir=os.getcwd()
        
        Error = ''
        if len(NeatSeq_bin) > 0:
            temp_command = ''
            if len(conda_env) > 0:
                # temp_command = 'bash  '
                temp_command = temp_command + ' source '
                if len(conda_bin) > 0:
                    temp_command = temp_command + os.path.join(conda_bin, 'activate') + ' ' + conda_env + ';'
                    temp_command = temp_command + 'export CONDA_BASE=$(' + os.path.join(conda_bin,
                                                                                        'conda') + ' info --root) ;'
                else:
                    temp_command = temp_command + 'activate' + ' ' + conda_env + ';'
                    temp_command = temp_command + 'export CONDA_BASE=$(conda  info --root); '
            if NeatSeq_bin.startswith(os.sep):
                temp_command = temp_command + ' python2 ' + NeatSeq_bin
            else:
                temp_command = temp_command + ' ' + NeatSeq_bin

            if len(sample_file) > 0:
                temp_command = temp_command + ' -s ' + sample_file
            else:
                Error = Error + 'Error:\n No Sample File\n'

            if len(parameter_file) > 0:
                temp_command = temp_command + ' -p ' + parameter_file
            else:
                Error = Error + 'Error:\n No Parameter File\n'

            if len(Project_dir) > 0:
                temp_command = temp_command + ' -d ' + Project_dir
            else:
                Error = Error + 'Error:\n No Project directory \n'
            
            if len(Error) == 0:
                err_flag = False
                try:
                    self.Run.set_Terminal(self.Terminal_string + '[Generating scripts]:  Generating...\n')
                    Generating_proc = Popen(temp_command, stdout=PIPE, stderr=PIPE, shell=True,
                                            universal_newlines=True , executable='/bin/bash')
                    outs, errs = Generating_proc.communicate(timeout=15)

                except :
                    err_flag = True
                    Generating_proc.kill()
                    outs, errs = Generating_proc.communicate()
                
                if len(errs) > 0:
                    for line in errs.split('\n'):
                        if len(line)>0:
                            self.Terminal_string = self.Terminal_string + '[Generating scripts]:  ' + line + '\n'
                if len(outs) > 0:
                    for line in outs.split('\n'):
                        if len(line)>0:
                            self.Terminal_string = self.Terminal_string + '[Generating scripts]:  ' + line + '\n'
                if err_flag:
                    self.Terminal_string = self.Terminal_string + '[Generating scripts]: Finished with Error!! \n'
                self.Run.set_Terminal(self.Terminal_string)
                
                
                # if self.Generating_scripts == 0:
                    # try:
                        # self.Running_Commands['Generating_scripts'] =  Run_command_in_thread(temp_command)
                        # self.Running_Commands['Generating_scripts'].Run()
                    # except :
                        # pass
                    # self.set_Generating_scripts(1)

            else:
                self.Run.set_Terminal(Error)
    
    
    
    def Run_scripts_command(self,Project_dir):
        import os
        from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
        
        if len(Project_dir) == 0:
            Project_dir=os.getcwd()
        
        Error = ''
        temp_command = ''
        if len(Project_dir) > 0:
            fname = os.path.join(Project_dir,'scripts', '00.workflow.commands.sh')
            if os.path.isfile(fname): 
                temp_command = 'bash ' + fname 
            else:
                Error = Error + 'Error:\n You first need to generate the scripts \n'
        else:
            Error = Error + 'Error:\n No Project directory \n'
            
        if len(Error) == 0:
            if self.Running_script == 0:
                try:
                    self.Running_Commands['Running_script'] =  Run_command_in_thread(temp_command)
                    self.Running_Commands['Running_script'].Run()
                except :
                    pass
                self.set_Running_script(1)
        else:
            self.Run.set_Terminal(Error)

    
    
    def Run_Monitor_command(self,Project_dir):
        import os
        import curses, argparse
        import neatseq_flow_monitor  
        import threading
        
        Error = ''
        
        if len(Project_dir) == 0:
            Project_dir=os.getcwd()
            
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

    @event.action
    def change_value(self,obj,prop_name,value):
        obj._mutate(prop_name,value)
    
    @event.reaction('Running_script') #,'Generating_scripts')
    def update_Terminal(self, *events):
            for ev in events:
                if ev.new_value>0:
                    Task_End=False
                    Title = ''
                    stat=True
                    outs = ''
                    errs = ''
                    try:
                        if self.Running_Commands[ev.type].proc.poll() is None:
                           outs, errs = self.Running_Commands[ev.type].output()
                           self.change_value(ev.source,ev.type,ev.new_value + 1)
                        else: 
                            outs, errs = self.Running_Commands[ev.type].output()
                            self.Running_Commands[ev.type].Stop()
                            self.change_value(ev.source,ev.type,0)
                            Task_End=True
                    except Exception: 
                        stat=False
                        
                    if stat:
                        if len(outs) > 0:
                            Title = Title + outs 
                        if len(errs) > 0: 
                            Title = Title  + errs 
                        if Task_End:
                            Title = Title + ' Finished!!'
                        
                        if len(Title) > 0:
                            
                            for line in Title.split('\n'):
                                if len(line)>0:
                                    self.Terminal_string = self.Terminal_string + '[ '+ ev.type.replace('_',' ') +' ] : ' + line + '\n'
                            self.Run.set_Terminal(self.Terminal_string)
                    
                    
    
    
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
                if len(self.samples_info.samples_data.keys()) > 0:
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
                                    sample_file.write(sample_name + '\t' + sample_types + '\t' + sample_path + '\n')
                    sample_file.close()
                    self.samples_info.set_save_samples_file([])

    @event.reaction('samples_info.load_samples_file')
    def load_sample_file(self, *events):
        from neatseq_flow_gui.modules.parse_sample_data import parse_sample_file
        samples_data = self.samples_info.samples_data
        for ev in events:
            if len(self.samples_info.load_samples_file) > 0:
                try:
                    samples_data = parse_sample_file(self.samples_info.load_samples_file[0][0])
                except:
                    samples_data = []
                    self.samples_info.set_load_samples_file([])
                if len(samples_data) > 0:
                    self.update_samples_data(samples_data)

    @event.action
    def update_samples_data(self, samples_data):
        converer = {}
        self.correct_dict(samples_data, 1, converer)
        self.samples_info.set_samples_data(samples_data)
        self.samples_info.set_converter(converer)
        self.samples_info.set_samples_data_update(True)

    @event.reaction('step_info.workflow_file')
    def load_workflow_file(self, *events):
        from neatseq_flow_gui.modules.parse_param_data import parse_param_file
        for ev in events:
            if len(self.step_info.workflow_file) > 0:
                try:
                    param_data = parse_param_file(self.step_info.workflow_file[0][0])
                except:
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

    @event.reaction('step_info.save_workflow_file')
    def save_workflow_file(self, *events):
        import yaml
        from collections import OrderedDict
        setup_yaml(yaml, OrderedDict)

        for ev in events:
            if len(self.step_info.save_workflow_file) > 0:
                try:

                    with open(self.step_info.save_workflow_file[0][0], 'w') as outfile:
                        param_data = {}
                        param_data['Global_params'] = OrderedDict(self.cluster_info.Data)
                        yaml.dump(param_data, outfile, default_flow_style=False,width=float("inf"))
                        param_data = {}
                        param_data['Vars'] = OrderedDict(self.vars_info.Data)
                        yaml.dump(param_data, outfile, default_flow_style=False,width=float("inf"))
                        param_data = {}
                        param_data['Step_params'] = OrderedDict(self.step_info.Data)
                        yaml.dump(param_data, outfile, default_flow_style=False,width=float("inf"))


                except:
                    pass
                self.step_info.set_save_workflow_file([])

    @event.reaction('vars_info.Data')
    def send_Vars_options(self, *events):
        for ev in events:
            options = list()
            self.dic2list(self.vars_info.Data, options)
            self.step_info.set_options(options)

    @event.action
    def update_steps_data(self, Steps_Data):
        converer = {}
        self.correct_dict(Steps_Data, 1, converer)
        self.step_info.set_Steps_Data(Steps_Data)
        self.step_info.set_converter(converer)
        self.step_info.set_Steps_Data_update(True)

    @event.action
    def update_cluster_data(self, Cluster_Data):
        converer = {}
        self.correct_dict(Cluster_Data, 1, converer)
        self.cluster_info.set_Data(Cluster_Data)
        self.cluster_info.set_converter(converer)
        self.cluster_info.set_Data_update(True)

    @event.action
    def update_vars_data(self, Vars_Data):
        converer = {}
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


class Run_command_in_thread(object):
   
    
    def __init__(self,command):
       
        import threading
        import multiprocessing 
        import queue 
        
        
        self.stdout       =   queue.Queue()
        self.stderr       =   queue.Queue()
        self.get_std_err  =   threading.Thread(target=self.collect_err)
        self.get_std_out  =   threading.Thread(target=self.collect_out)
        self.proc         =   None
        self.Run_command  =   command
        
        
    def collect_out(self):
        for stdout in iter(self.proc.stdout.readline, ''):
            if len(stdout)>0:
                self.stdout.put(stdout,False)
                
    def collect_err(self):
        for stderr in iter(self.proc.stderr.readline, ''):
            if len(stderr)>0:
                self.stderr.put(stderr,False)
        
    def Run(self):
        from subprocess import Popen, PIPE, STDOUT
        self.proc = Popen(self.Run_command , shell=True, executable='/bin/bash', stdout=PIPE, stderr=PIPE,
                             universal_newlines=True)
        self.get_std_out.start()
        self.get_std_err.start()
       
    def Stop(self):
        self.get_std_out.join()
        self.get_std_err.join()
        self.proc.kill()
        
    
    
    def output(self):
        import time
        all_out = ''
        all_err = ''
        while self.stdout.empty()==False:
            out = self.stdout.get()
            all_out = all_out + out 
            self.stdout.task_done()
            
        out=all_out
        
        while self.stderr.empty()==False:
            err = self.stderr.get()
            all_err = all_err + err 
            self.stderr.task_done()
            
        err=all_err
        time.sleep(0.000001)
        return [ out , err]
    
if __name__ == '__main__':
    temp_MODULES_TEMPLATES = Load_MODULES_TEMPLATES()
    if len(temp_MODULES_TEMPLATES) > 0:
        MODULES_TEMPLATES = temp_MODULES_TEMPLATES
    icon=os.path.join(os.path.realpath(os.path.expanduser(os.path.dirname(os.path.abspath(__file__))+os.sep+"..")),'neatseq_flow_gui','NeatSeq_Flow.ico')
    #icon = app.assets.add_shared_data('ico.icon', open(icon, 'rb').read())
    m = app.App(NeatSeq_Flow_GUI).launch(runtime ='app',size=(1200, 650),title='NeatSeq-Flow GUI',icon=icon)
    app.run()




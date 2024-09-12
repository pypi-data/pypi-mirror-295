from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
from customtkinter import CTkTextbox
from customtkinter import CTkImage
from PIL import Image
import os

from . import BoundsList
from . import FunctionsList
from . import ListEditor


class StepView(CTkScrollableFrame):
    def __init__(self, *args,
                 option_manager: None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.option_manager = option_manager
        self.analysisFrame = None
        self.containerFrame = None

        self.render()

    def refresh(self):
        self.clear()
        self.render()

    def clear(self):
        if self.containerFrame != None:
            self.containerFrame.destroy()

        if self.analysisFrame != None:
            self.analysisFrame.destroy()

    def create_new_step(self):

        self.clear()
        example_step = [{    # step 1
            'param': [
                {
                    'name': 'soilOutLPS',
                    'bounds': (0.0, 2.0)
                },
                {
                    'name': 'lagInterflow',
                    'bounds': (10.0, 80.0)
                }
            ],
            'objfunc': [
                {
                    'name': 'ns',
                    'of': 'ns',
                    'data': ('obs_data02_14.csv/obs/orun[1]',
                             'output/csip_run/out/Outlet.csv/output/catchmentSimRunoff')
                }
            ],
            'open': True
        }]
        self.option_manager.add_steps(example_step)

        self.render()

    def render(self):

        row = 0
        index = 0

        self.containerFrame = CTkFrame(self)
        self.containerFrame.grid(row=0, column=0, padx=(
            10, 10), pady=(10, 10), sticky="nsew")
        self.containerFrame.grid_columnconfigure((0, 1), weight=1)

        self.steps = self.option_manager.get_steps()
        self.mode = self.option_manager.get_arguments()['mode'].get()

        for step in self.steps:

            up_image = CTkImage(Image.open(os.path.join("./images", "up.png")), size=(20, 20))
            down_image = CTkImage(Image.open(os.path.join("./images", "down.png")), size=(20, 20))
            trash_image = CTkImage(Image.open(os.path.join("./images", "trash.png")), size=(20, 20))
            expand_image = CTkImage(Image.open(os.path.join("./images", "expand.png")), size=(20, 20))
            collapse_image = CTkImage(Image.open(os.path.join("./images", "collapse.png")), size=(20, 20))


            expand_func = lambda index=index: (self.clear(), self.option_manager.toggle_step_open(index), self.render())
            up_func = lambda index=index: (self.clear(), self.option_manager.move_step_up(index), self.render())
            down_func = lambda index=index: (self.clear(), self.option_manager.move_step_down(index), self.render())
            remove_func = lambda index=index: (self.clear(), self.option_manager.remove_step(index), self.render())
            
            if (self.mode == "Optimization: MG-PSO"):
                button_container = CTkFrame(self.containerFrame, width=200)
                button_container.grid(row=row, column=1, sticky="nse", padx=(10, 10), pady=(10, 10))
                button_container.grid_rowconfigure(0, weight=1)
                button_container.grid_columnconfigure(0, weight=1)
                
                CTkEntry(self.containerFrame, textvariable=step['name'], width=500).grid(row=row, column=0, padx=(20, 20), pady=(20, 20), sticky="nsw")
            
                CTkButton(button_container, width=30, text=None, image=expand_image if not step['open'] else collapse_image, command=expand_func).grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
                CTkButton(button_container, width=30, text=None, image=up_image, state="disabled" if index==0 else "normal", fg_color="gray" if index==0 else None, command=up_func).grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
                CTkButton(button_container, width=30, text=None, image=down_image, state="disabled" if index==(len(self.steps)-1) else "normal", fg_color="gray" if index==(len(self.steps)-1) else None, command=down_func).grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
                CTkButton(button_container, width=30, text=None, image=trash_image, command=remove_func).grid(row=0, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")

                row += 1

            if step['open'] or (self.mode == "Sampling: Halton" or self.mode == "Sampling: Random" or self.mode == "Sensitivity: Halton" or self.mode == "Sensitivity: Random"):
                bounds = BoundsList.BoundsList(
                    self.containerFrame, option_manager=self.option_manager, step_index=index)
                bounds.grid(row=row, column=0, padx=(10, 10),
                            pady=(10, 10), sticky="nsew")
                bounds.grid_columnconfigure(0, weight=1)
                bounds.grid_rowconfigure(0, weight=1)
                
                funcs = FunctionsList.FunctionsList(
                    self.containerFrame, option_manager=self.option_manager, step_index=index)
                funcs.grid(row=row, column=1, padx=(10, 10),
                            pady=(10, 10), sticky="nsew")
                funcs.grid_columnconfigure(0, weight=1)
                funcs.grid_rowconfigure(0, weight=1)
                
            row += 1
            index += 1
            
            if (self.mode != "Optimization: MG-PSO"):
                break

        # Create an "Add step button that is centered
        if (self.mode == "Optimization: MG-PSO" or len(self.steps) == 0):
            CTkButton(self.containerFrame, text="Add Group", command=self.create_new_step).grid(
                row=row, columnspan=2, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")
            
        """
        if (self.mode == "Sampling: Halton" or self.mode == "Sampling: Random" or self.mode == "Sensitivity Analysis"):
            self.analysisFrame = CTkFrame(self)
            self.analysisFrame.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
            self.analysisFrame.grid_columnconfigure((0, 1, 2), weight=1)

            columns = ["n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10"]

            self.params_editor = ListEditor.ListEditor(self.analysisFrame, option_manager=self.option_manager, 
                                                       title="Parameters",
                                                       columns=columns,
                                                       parameter_name="sensitivity_parameters",
                                                       parameter_remove_func=self.option_manager.remove_sensitivity_parameter,
                                                       parameter_add_func=self.option_manager.add_sensitivity_param)
            self.params_editor.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
            self.params_editor.grid_columnconfigure(0, weight=1)
            self.params_editor.grid_rowconfigure(0, weight=1)


            self.positive_editor = ListEditor.ListEditor(self.analysisFrame, option_manager=self.option_manager, 
                                                       title="Positive Best Metrics",
                                                       columns=columns,
                                                       parameter_name="sensitivity_positiveBestMetrics",
                                                       parameter_remove_func=self.option_manager.remove_sensitivity_positiveBestMetrics,
                                                       parameter_add_func=self.option_manager.add_sensitivity_positiveBestMetrics)
            self.positive_editor.grid(row=0, column=1, padx=(10, 10), pady=(10, 0), sticky="nsew")
            self.positive_editor.grid_columnconfigure(0, weight=1)
            self.positive_editor.grid_rowconfigure(0, weight=1)

            self.negative_editor = ListEditor.ListEditor(self.analysisFrame, option_manager=self.option_manager, 
                                                       title = "Zero Best Metrics",
                                                       columns=columns,
                                                       parameter_name="sensitivity_negativeBestMetrics",
                                                       parameter_remove_func=self.option_manager.remove_sensitivity_negativeBestMetrics,
                                                       parameter_add_func=self.option_manager.add_sensitivity_negativeBestMetrics)
            self.negative_editor.grid(row=0, column=2, padx=(10, 10), pady=(10, 0), sticky="nsew")
            self.negative_editor.grid_columnconfigure(0, weight=1)
            self.negative_editor.grid_rowconfigure(0, weight=1)
        """

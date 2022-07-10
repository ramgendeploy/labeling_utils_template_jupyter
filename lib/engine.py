# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)
import abc
from turtle import width
from lib.utils import (
  HBoxAlign,
  ButtonCenter,
  ImagePathWidget,
  ToggleButtonsCenter,
  ToggleButtonFill
  )

from IPython.display import display, clear_output
from ipywidgets import Label,GridspecLayout,Output, HBox, Layout, VBox
import shutil
import os
import itertools


class labeling_display():

  # output_init = Output(layout={'border': '1px solid transparent'})
  # output_controls = Output(layout={'border': '1px solid transparent'})
  # output_images = Output(layout={'border': '1px solid transparent'})
  # output_progress = Output(layout={'border': '1px solid transparent'})

  def __init__(self, to_label, primary_labels, secondary_labels, output_path):
    self.output_path = output_path
    self.to_label = to_label
    self.primary_labels = primary_labels
    self.secondary_labels = secondary_labels

    self.index = -1
    self.current_img = None
    
    self.progress_label = HBoxAlign([Label()])

    self.progress_label = HBoxAlign([Label(f'{self.index}/{len(self.to_label)-1}')])
    self.image_label = HBoxAlign([Label('Image Name')])

    self.controls = GridspecLayout(2, 6)
    
    nextBtn = ButtonCenter('Next','info','fa-arrow-right',onClick=lambda _: self.next_set(1))    
    addBtn =  ButtonCenter('Add','primary','fa-check-circle','#2CC77F', onClick=lambda _: self.add_image_pair())
    discardBtn = ButtonCenter('Discard','warning','fa-trash', onClick=lambda _: self.discard_image_pair())    
    backBtn = ButtonCenter('Back','info','fa-arrow-left', onClick=lambda _: self.next_set(-1))
    progress_info = HBoxAlign([self.progress_label])
    img_name_info = HBoxAlign([self.image_label])

    self.controls[0, 0] = discardBtn
    self.controls[0, 1] = progress_info
    self.controls[0, 2] = img_name_info
    self.controls[0, 3] = addBtn
    self.controls[0, 4] = backBtn
    self.controls[0, 5] = nextBtn    
    self.controls[1, :] = ToggleButtonsCenter(self.primary_labels)

    self.output_controls = Output(layout={'border': '0px solid transparent'})
    self.output_images = Output(layout={'border': '0px solid transparent'})
    self.output_progress = Output(layout={'border': '0px solid transparent'})

  def getImgOptions(self, img_path):
    return VBox(children=[
      HBoxAlign([ToggleButtonFill(name, 'success') for name in  self.secondary_labels],'space-around'),
      HBox(children=[ImagePathWidget(img_path)])],
      layout=Layout(height='auto',width='40vw', border='1px solid #ddd', justify_content='center')
    )

  def next_set(self, direc):
    self.index += direc
    if self.index == len(self.to_label):
      with self.output_images:
        display(HBox(children=[Label('Finished this image batch.',)],
                layout=Layout(height='auto', width='auto', justify_content='center')))
      return      
    self.progress_label.children[0].value=f'{self.index}/{len(self.to_label)-1}'
    self.image_label.children[0].value=self.to_label[self.index]
  
    self.current_img = self.getImgOptions(self.to_label[self.index])
    with self.output_images:

      display(HBoxAlign([self.current_img], justify='center'), clear=True)

  def add_image_pair(self):
    flabel= self.controls[1,:].value
    fpath = self.to_label[self.index]

    slabel_opt = self.current_img.children[0].children
    slabel = [slabel_opt.index(slabels) for slabels in slabel_opt if slabels.value==1]
    slabel = self.secondary_labels[slabel[0]]

    shutil.copy(fpath,
      f"{self.output_path}/{flabel}/{slabel}/{fpath.split('/')[-1]}")  
    
    with self.output_progress:
      print(f"copied {fpath} to \n{self.output_path}/{flabel}/{slabel}/{fpath.split('/')[-1]}")

    self.next_set(1)

  def discard_image_pair(self):
    fpath=self.to_label[self.index]
    shutil.copy(fpath, f"{self.output_path}/Discard/{fpath.split('/')[-1]}")    
    with self.output_progress:
      print(f"Discarted {fpath}")
    self.next_set(1)

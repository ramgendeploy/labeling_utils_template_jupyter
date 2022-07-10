from turtle import width
from ipywidgets import (
  Button, 
  HBox,
  Layout,
  ButtonStyle,
  ToggleButton,
  ToggleButtons,
  Image,
)

def ToggleButtonsCenter(options,style='primary'):
  return ToggleButtons(options=options, button_style=style, 
          layout=Layout(height='auto', width='auto', justify_content='space-around'))

def HBoxAlign(children, align='center', justify=None):
  return HBox(
    children=children, 
    layout=Layout(width='auto', align_content=align, justify_content=justify))

def ButtonCenter(desc, style='primary', icon='fa-check-circle', color=None, onClick=None):
  btn = Button(
    description=desc, 
    button_style=style, 
    style=ButtonStyle(button_color=color), icon=icon, layout=Layout(height='auto', width='auto'))
  btn.on_click(onClick)
  return btn

def ToggleButtonFill(desc, style='success', icon='none'):
  return ToggleButton(description=desc, button_style=style, icon=icon, layout=Layout(height='auto', width='100%'))

def ImagePathWidget(path):
    widget_img=None
    with open(path, "rb") as a_file:
        widget_img = Image(value=a_file.read(), format="jpg")
    return widget_img

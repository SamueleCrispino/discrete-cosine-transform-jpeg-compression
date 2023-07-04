import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from jpeg_utils import get_jpeg


Builder.load_file("my_conf_file.kv")




class LoadDialog(FloatLayout):
    load_image = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MyGridLayout(Widget):

    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)

    f_value = ObjectProperty(None)
    d_value = ObjectProperty(None)
    imagePath = ObjectProperty(None)
    secondImagePath = ObjectProperty(None) 

    def switch_on_widgets(self, widgets):
        for widget in widgets:
            widget.opacity = 1

    def switch_off_widgets(self, widgets):
        for widget in widgets:
            widget.opacity = 0


    def get_d_widgets(self):
        label_d = self.ids.label_d
        slider_d = self.ids.d
        sumbit_d = self.ids.getInputButtonD

        return label_d, slider_d, sumbit_d
    

    def get_f_widgets(self):
        label_f = self.ids.label_f
        textInput_f = self.ids.f
        submit_f = self.ids.getInputButtonF

        return label_f, textInput_f, submit_f




    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load_image=self.load_image, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load_image(self, filename):
        print("**************load image")
        try:
            print(filename)
            self.imagePath = filename[0]

            firstImage = self.ids.firstImage
            firstImage.source = filename[0]
            firstImage.opacity = 1
            self.dismiss_popup()

            self.ids.searchImage.opacity = 0

            self.switch_on_widgets(list(self.get_f_widgets()))
        
        
        except Exception as e:
            print("ouch!")
            print(str(e))

    def on_slider_value_change(self, instance, value):
        self.ids.label_d.text = "Blocks dimensions: " + str(value)
        

    
    def my_click_funcF(self):
        self.f_value = int(self.f.text)
        

        label_d, slider_d, sumbit_d = self.get_d_widgets()


        slider_d.min = 0
        slider_d.value = int(round((2*self.f_value - 2)/2)) 
        slider_d.max = 2*self.f_value - 2 
        slider_d.bind(value=self.on_slider_value_change)

        label_d.text = str(slider_d.value)

        self.switch_on_widgets(list((label_d, slider_d, sumbit_d) ))


        label_f, textInput_f, submit_f = self.get_f_widgets()

        label_f.text = f"Blocks dimensions: {self.f_value}"

        self.switch_off_widgets(list((textInput_f, submit_f)))
        

    def my_click_funcD(self):
        self.d_value = int(self.d.value)
        print(f"image = ", self.imagePath)
        print("f = ", self.f_value)
        print("d = ", self.d_value)

        label_d = self.ids.label_d
        slider_d = self.ids.d
        sumbit_d = self.ids.getInputButtonD

        label_d.text = f"Frequency threshold: {self.d_value}"

        self.switch_off_widgets(list((slider_d, sumbit_d)))

        jpeg_path = get_jpeg(self.imagePath, self.f_value, self.d_value)

        self.secondImagePath = self.ids.secondImage
        self.secondImagePath.source = jpeg_path
        self.secondImagePath.opacity = 1

    
    def clean_all(self):
        self.f_value = ObjectProperty(None)
        self.d_value = ObjectProperty(None)
        self.imagePath = ObjectProperty(None)
        self.secondImagePath = ObjectProperty(None)

        self.switch_off_widgets(list(self.get_f_widgets()))
        self.switch_off_widgets(list(self.get_d_widgets()))

        im1 = self.ids.firstImage
        im2 = self.ids.secondImage
        im1.source = ''
        im2.source = ''
        self.switch_off_widgets(list((im1, im2)))

        self.ids.searchImage.opacity = 1

        label_f, textInput_f, submit_f = self.get_f_widgets()
        label_f.text = "Blocks dimensions: "
        textInput_f.value = ''
    



    


# if you are not using kive.lang.Builder
# .kv file must been called as this $<My> part of the class name $<My>App: my.kv
class MyApp(App):

    def build(self):
        return MyGridLayout()


Factory.register('MyGridLayout', cls=MyGridLayout)
Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    MyApp().run()
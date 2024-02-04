
'''from turtle import width
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import tkinter as tk
import Backend as bknd
from PIL import Image
import time'''

import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
import customtkinter as ctk
import PIL.Image

theme_path = r"App data\Defaults\custom_Theme.json"
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(theme_path)
appWidth, appHeight = 1500,800

img_path_global = ""
output_predicted = ""

class AboutFrame(ctk.CTkScrollableFrame):
     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #header for about application
        self.header=ctk.CTkLabel(self, text="About Application",anchor = "center" ,font=("Roman",25,"bold"))
        self.header.grid(row=0,column=0,padx=15,pady=15,sticky="nsew")
        #Text info of application
        self.text_to_display= tk.Text(self ,background = "#333333", fg = "#CCCCCC" , borderwidth= 1 , state = "normal" , font=("Times New Roman",15,"italic"))
        self.file_path = r"App data\Texts\About_Application.txt"
        with open(self.file_path, "r") as file:
                self.text_content = file.read()
        self.text_to_display.insert("1.0",self.text_content)
        self.text_to_display.config(state="disabled")
        # Configure row and column weights for proper expansion
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.text_to_display.grid(row=1,column=0,padx=15,pady=15 , sticky="ew")

class ImagepreviewFrame(ctk.CTkFrame):

        def load_img_and_update(self):
                global img_path_global
                self.img_path = bknd.selectimg()
                img_path_global = self.img_path
                # Update the label to display the selected image path
                self.image_path_label.configure(text=self.img_path)

        def cleaning_img(self):
                bknd.clean()
                self.image_path_label.configure(text = "No Image Loaded")

        def preview_img(self):
                #load image
                self.image_loaded = PIL.Image.open(self.img_path)
                self.image_loaded.resize(size=(250,250))
                self.image = ctk.CTkImage(dark_image=self.image_loaded, size = (100,100))
                #configure lable img_lable for image display
                self.img_lable.configure(image = self.image)

        def clear_preview_img(self):
                self.image_empty = PIL.Image.open("App data/Defaults/image_noot_found.jpg")
                self.image_empty.resize(size=(200,200))
                self.empty_image = ctk.CTkImage(dark_image=self.image_empty , size=(100, 100))
                self.img_lable.configure(image = self.empty_image)

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                #header for Image preview
                self.header=ctk.CTkLabel(self, text="Image Preview",anchor = "center" ,font=("Roman",25,"bold"))
                self.header.grid(row=0,column=0,columnspan = 4,padx=15,pady=15,sticky="nsew")
                #image selection lable
                self.imgloadlable = ctk.CTkLabel(self, text="Load Image:",anchor = "center",font=("Times New Roman",20,"italic"))
                self.imgloadlable.grid(row=1,column=0,padx=15,pady=15,sticky="nsew")
                #button for image selection
                self.loadimgbutton = ctk.CTkButton(self , text = "Load" , command = self.load_img_and_update)
                self.loadimgbutton.grid(row=1,column=1,padx=15,pady=15,sticky="nsew")
                # Image path label to display the loaded image path
                self.image_path_label = ctk.CTkLabel(self, text="No Image Loaded", anchor="center", font=("Times New Roman", 10, "italic"))
                self.image_path_label.grid(row=2, column=0, padx=15, pady=15, sticky="nsew")
                #image clear lable
                self.imgclearlable = ctk.CTkLabel(self, text="Clear Image:",anchor = "center",font=("Times New Roman",20,"italic"))
                self.imgclearlable.grid(row=3,column=0,padx=15,pady=15,sticky="nsew")
                #button for image clear
                self.clearimgbutton = ctk.CTkButton(self , text = "Clear" , command =self.cleaning_img)
                self.clearimgbutton.grid(row=3,column=1,padx=15,pady=15,sticky="nsew")
                #button to see preview
                self.seepreviewbutton = ctk.CTkButton(self , text = "Preview Image" , command =self.preview_img)
                self.seepreviewbutton.grid(row=3,column=2,padx=15,pady=15,sticky="nsew")
                #button to clear preview
                self.clearpreviewbutton = ctk.CTkButton(self , text = "Clear Preview" , command =self.clear_preview_img)
                self.clearpreviewbutton.grid(row=3,column=3,padx=15,pady=15,sticky="nsew")
                #image preview lable
                self.img_lable = ctk.CTkLabel(self, text="", compound= "center", anchor = "center",font=("Times New Roman",20,"italic"))
                self.img_lable.grid(row=1,column=2,columnspan = 3,rowspan = 2 , padx=15,pady=15,sticky="nsew")
                

class PredictionFrame(ctk.CTkFrame):
        def prediction(self):
                #start prediction and progressbar
                self.image_path = img_path_global
                if(self.image_path == ""):
                        self.messagedisplay = CTkMessagebox(self,title="Error",message="No image selected",icon="cancel",option_1="Go Back" )
                        if self.messagedisplay.get() == "Go Back":
                                self.messagedisplay.destroy()
                else:
                        #self.incrementvalue = bknd.Predict(self.image_path)
                        #for progress in range(0, 101, self.incrementvalue):
                        #        self.update_progress(progress)
                        self.progressvariable.set(0)  # Set progress bar to 0 before prediction
                        self.after(100, self.predict_with_progress, 0)

        def update_progress_bar(self ,progress_value):
                self.progressvariable.set(progress_value)
                self.progress.update_idletasks()

        def predict_with_progress(self, progress):
                if progress <= 100:
                        global output_predicted
                        self.result = bknd.Predictions(self.image_path , progress_callback = self.update_progress_bar)
                        #print(self.result)
                        self.outputlable.configure(text = self.result)
                        output_predicted = self.result
                        increment_value = 10
                        self.update_progress(progress)
                        #self.after(100, self.predict_with_progress, progress + increment_value)
                        progress += increment_value
                        time.sleep(0.1)

        def update_progress(self, progress):
                # Update progress bar
                self.progressvariable.set(progress)
                self.progress.update_idletasks()

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                #header for Image preview
                self.header=ctk.CTkLabel(self, text="Prediction",anchor = "center" ,font=("Roman",25,"bold"))
                self.header.grid(row=0,column=0,columnspan = 3,padx=15,pady=15,sticky="nsew")
                #lable to ask for prediction
                self.lableprediction = ctk.CTkLabel(self , text = "Predict:",anchor = "center",font=("Times New Roman",20,"italic"))
                self.lableprediction.grid(row=1,column=0,columnspan = 1,padx=15,pady=15,sticky="nsew")
                #button to start prediction
                self.predictbutton = ctk.CTkButton(self , text = "start prediction" , command =self.prediction)
                self.predictbutton.grid(row=1,column=1,padx=15,pady=15,sticky="nsew")
                #progressbar for prediction process
                self.progressvariable = ctk.IntVar()
                self.progressvariable.set(0)
                self.progress = ctk.CTkProgressBar(self , width=100 , height=15 , border_width=2 ,variable = self.progressvariable , progress_color= "green" ,mode= "determinate")
                self.progress.grid(row=2,column=0,columnspan =3 ,padx=15,pady=15,sticky="nsew")
                #Lable to display output
                self.resultlable = ctk.CTkLabel(self , text = "Predicted:" ,anchor = "center",font=("Times New Roman",20,"italic"))
                self.resultlable.grid(row=3,column=0,columnspan =1 ,padx=15,pady=15,sticky="nsew")
                #output lable
                self.outputlable = ctk.CTkLabel(self , text = "" ,anchor = "center", font=("Times New Roman",23,"bold"))
                self.outputlable.grid(row=3,column=1,columnspan =2 ,padx=15,pady=15,sticky="nsew")

class InfoFrame(ctk.CTkScrollableFrame):
     def update_info_text(self):
        global output_predicted
        #self.file_path = ""
        if(output_predicted == "AI Generated art"):
            self.file_path = "App data/Texts/AI_Info.txt"
        elif(output_predicted == "Human generated art"):
            self.file_path = "App data/Texts/Human_info.txt"
        #else:
        #       self.file_path = ""
        #self.file_path = "App data/Texts/AI_Info.txt" if output_predicted == "AI Generated art" else "App data/Texts/Human_info.txt"
        if self.file_path:
            with open(self.file_path, "r") as file:
                self.text_content = file.read()
            self.text_to_display.config(state="normal")
            self.text_to_display.delete("1.0", "end")
            self.text_to_display.insert("1.0", self.text_content)
            self.text_to_display.config(state="disabled")
        else:
            # You can display a message or take appropriate action
            print("file path is empty")

     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        #header for info application
        self.header=ctk.CTkLabel(self, text="Information",anchor = "center" ,font=("Roman",25,"bold"))
        self.header.grid(row=0,column=0,padx=15,pady=15,sticky="nsew")
        #lable info
        self.lableinfo=ctk.CTkLabel(self, text="what's next?",anchor = "center" ,font=("Roman",25,"bold"))
        self.lableinfo.grid(row=1,column=0,padx=15,pady=15,sticky="nsew")
        #button to get info
        self.infobutton = ctk.CTkButton(self , text = "Know more" , command =self.update_info_text)
        self.infobutton.grid(row=2,column=0,padx=15,pady=15,sticky="nsew")
        #Text info of output
        self.text_to_display= tk.Text(self ,background = "#333333", fg = "#CCCCCC" , borderwidth= 1 , state = "normal" , font=("Times New Roman",15,"italic"))
        self.text_content = ""
        #self.file_path = "App data/Texts/AI_Info.txt" if output_predicted == "AI Generated art" else "App data/Texts/Human_info.txt"
        #with open(self.file_path, "r") as file:
        #        self.text_content = file.read()
        self.text_to_display.insert("1.0",self.text_content)
        self.text_to_display.config(state="disabled")
        # Configure row and column weights for proper expansion
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.text_to_display.grid(row=3,column=0,columnspan =1 ,padx=15,pady=15 , sticky="ew")

class AllFrame(ctk.CTkScrollableFrame):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                #header for Image preview
                self.header=ctk.CTkLabel(self, text="M.U.R.A.L",anchor = "center" ,font=("Roman",30,"bold"))
                self.header.grid(row=0,column=0,columnspan = 8,padx=15,pady=15,sticky="nsew")
                #frame about app
                self.About_frame = AboutFrame(master = self , fg_color = "#252525" ,scrollbar_button_hover_color = "#585858", scrollbar_button_color = "#252525" , border_width = 2 , border_color = "#111109")
                self.About_frame.grid(row=1, column=0,columnspan=8, padx=20, pady=5, sticky="nsew")
                self.About_frame._set_dimensions(width=1425,height=350)

                #frame image preview
                self.imgpreview_frame = ImagepreviewFrame(master = self , fg_color = "#252525" , border_width = 2 , border_color = "#111109")
                self.imgpreview_frame.grid(row=2, column=0,columnspan=5, padx=5, pady=10, sticky="nsew")
                self.imgpreview_frame._set_dimensions(width = 100 ,height = 350)
                
                #frame Prediction
                self.predictionFrame = PredictionFrame(master = self , fg_color = "#252525" , border_width = 2 , border_color = "#111109")
                self.predictionFrame.grid(row=2, column=5,columnspan=3, padx=5, pady=10, sticky="nsew")
                self.predictionFrame._set_dimensions(width = 2 ,height = 350)

                #frame info
                self.Info_frame = InfoFrame(master = self , fg_color = "#252525" ,scrollbar_button_hover_color = "#585858", scrollbar_button_color = "#252525" , border_width = 2 , border_color = "#111109")
                self.Info_frame.grid(row=3, column=0,columnspan=8, padx=20, pady=5, sticky="nsew")
                self.Info_frame._set_dimensions(width=1425,height=350)



class Mainpageapp(ctk.CTk):
    def import_modules(self):
        # List of modules to import with aliasing
        modules_to_import = [
            ("turtle", "t"),
            ("CTkMessagebox", "CTkMessagebox"),
            ("customtkinter", "ctk"),
            ("tkinter", "tk"),
            ("Backend", "bknd"),
            ("PIL", "Image"),
            ("time", "time"),
        ]

        # Display loading screen
        with tqdm(total=len(modules_to_import), desc="Importing Modules", dynamic_ncols=True) as pbar:
            for module_name, alias in modules_to_import:
                globals()[alias] = __import__(module_name)
                pbar.update(1)  # Update progress bar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Main Page")
        
        # Calculate the coordinates for centering the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = (screen_width - appWidth) // 2
        y_position = (screen_height - appHeight) // 2

        # Set the geometry of the window to open it at the center
        self.geometry(f"{appWidth}x{appHeight}+{x_position}+{y_position}")
        self.resizable(True, True)
        self.attributes('-topmost', True)

        # Import modules with aliasing and loading screen
        self.import_modules()
        #Add the all encompassing mighty frame
        self.allframe = AllFrame(master = self , border_width = 2 , scrollbar_button_hover_color = "#585858", scrollbar_button_color = "#252525" , fg_color = "#1B1B1B", border_color = "#111109")
        self.allframe.grid(row=1, column=0,columnspan=1, padx=15, pady=15, sticky="nsew")
        self.allframe._set_dimensions(width = 1482,height =795 )

if __name__=="__main__":
        mainpage_app=Mainpageapp()
        mainpage_app.mainloop()


import os
from PIL import Image
from tkinter import * 
from tkinter.ttk import Progressbar
from tkinter import filedialog
import PIL.Image
from pathlib import Path

current_path = os.getcwd()

def bar(current_progress):
    progress['value'] = current_progress
    percent.set(str(int(current_progress))+"%")
    root.update_idletasks()

def convert_images(source_path, target_path, final_extension):
    output_path = "{}\\output".format(source_path)
    Path(output_path).mkdir(parents=True, exist_ok=True)
    files_list = []
    output_list = []
    for root, files in os.walk(target_path, topdown=False):
        for name in files:
            current_extension = os.path.splitext(os.path.join(root, name))[1].lower()
            if current_extension == ".tiff" or current_extension == ".tif":
                if os.path.isfile(os.path.splitext(os.path.join(output_path, name))[0] + ".{}".format(final_extension)):
                    print("A {} file already exists for {}".format(final_extension, name))
                    pass
                else:
                    output_list.append(os.path.splitext(os.path.join(output_path, name))[0] + ".{}".format(final_extension))
                    files_list.append(os.path.join(root, name))
    
    l = len(files_list)
    if l > 0:
        for index, (file, outfile) in enumerate(zip(files_list, output_list)):
            index += 1
            progress = 100 * index / l
            bar(progress)
            try:
                im = PIL.Image.open(file)
                print("Generating {} for {}".format(final_extension, file))
                im.thumbnail(im.size)
                im.save(outfile, final_extension.upper(), quality=100)
            except Exception as e:
                print(e)
    else:
        bar(100)

root = Tk()
root.title('converter')
app_width = 250
app_height = 150
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2 ) - (app_height / 2)
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

def select_directory():
    directory = filedialog.askdirectory(title='select a directory with tif/tiff files')
    convert_images(current_path, directory, "png")

def explore_directory():
    current_path = os.getcwd()
    output_path = "{}\\output".format(current_path)
    os.startfile(output_path)

def close_app():
    root.destroy()

percent = StringVar()
text = StringVar()
progress = Progressbar(root,orient=HORIZONTAL,length=200)
progress.pack(pady=10)
percentLabel = Label(root,textvariable=percent).pack()
taskLabel = Label(root,textvariable=text).pack()
button = Button(root,text="convert",command=select_directory).pack()
button_output = Button(root,text="explore",command=explore_directory).pack()
root.mainloop()
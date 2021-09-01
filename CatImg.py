import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time, os, random, string, argparse
from pathlib import Path
import numpy as np
from PIL import ImageTk, Image
import cv2
import copy

class Page(tk.Tk):
    count = 0

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("A simple image pre-processing application")

        container = tk.Frame(self)
        container.grid()

        # title
        self.empty_name = tk.Label(self, text="A simple image pre-processing application", font=("Arial", 16))
        self.empty_name.grid(row=0, column=0, pady=5, padx=10, sticky="sw")

        # intro
        self.intro_lbl = tk.Label(self,
                                  text="Please choose a image.",
                                  font=("Arial", 11), fg="#202020")
        self.intro_lbl.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nw")

        # select image
        self.browse_lbl = tk.Label(self, text="Select Image :", font=("Arial", 10), fg="#202020")
        self.browse_lbl.grid(row=4, column=0, columnspan=3, padx=24, pady=10, sticky="w")

        self.browse_entry = tk.Entry(self, text="", width=60)
        self.browse_entry.grid(row=4, column=0, columnspan=3, padx=120, pady=10, sticky="w")

        self.browse_btn = tk.Button(self, text="     Browse     ", bg="#ffffff", relief="flat", width=10,
                                    command=lambda: self.show_image())
        self.browse_btn.grid(row=4, column=0, padx=500, pady=10, columnspan=3, sticky="w")

        # file info
        self.lbl_Height = tk.Label(self, text="Image Height: ", font=("Arial", 10), fg="#202020")
        self.lbl_Width = tk.Label(self, text="Image Width: ", font=("Arial", 10), fg="#202020")
        self.lbl_Type = tk.Label(self, text="Image Type: ", font=("Arial", 10), fg="#202020")

        self.text_H = tk.StringVar()
        self.lbl_Height_01 = tk.Label(self, textvariable=self.text_H, font=("Arial", 10), fg="#202020")

        self.text_W = tk.StringVar()
        self.lbl_Width_01 = tk.Label(self, textvariable=self.text_W, font=("Arial", 10), fg="#202020")

        self.text_T = tk.StringVar()
        self.lbl_Type_01 = tk.Label(self, textvariable=self.text_T, font=("Arial", 10), fg="#202020")

        # place holder for document thumbnail
        self.lbl_image = tk.Label(self, image="")
        self.lbl_image.grid(row=8, column=0, pady=25, padx=10, columnspan=3, sticky="nw")

        # status text
        self.label_text_progress = tk.StringVar()
        self.scan_progress = tk.Label(self, textvariable=self.label_text_progress, font=("Arial", 10), fg="#0000ff")

        # gray button
        self.gray_btn = tk.Button(self, text=" Change to gray ", bg="#ffffff", relief="flat",
                                  width=15, command=lambda: self.to_gray())
        # transformation button
        self.tran_btn = tk.Button(self, text=" Transformation ", bg="#ffffff", relief="flat",
                                  width=15, command=lambda: self.trans_page())
        # gray level button
        self.level_btn = tk.Button(self, text=" Change gray level ", bg="#ffffff", relief="flat",
                                  width=15, command=lambda: self.gray_page())
        # equlize button
        self.equlize_btn = tk.Button(self, text=" Histogram Equalization ", bg="#ffffff", relief="flat",
                                   width=20, command=lambda: self.equlize())
        # smooth button
        self.smooth_btn = tk.Button(self, text=" Smooth ", bg="#ffffff", relief="flat",
                                     width=10, command=lambda: self.smooth())
        # equlize button
        self.edge_btn = tk.Button(self, text=" Edge ", bg="#ffffff", relief="flat",
                                     width=10, command=lambda: self.edge())


    def show_image(self):

        global path
        # open file dialog
        self.path = filedialog.askopenfilename(defaultextension="*.jpg", filetypes=(("JPG", "*.jpg"), ("PNG", "*.png")))
        self.browse_entry.delete(0, tk.END)
        self.browse_entry.insert(0, self.path)

        self.label_text_progress.set("Image loaded - ready to be processed.")
        self.scan_progress.grid(row=18, column=0, padx=10, pady=0,
                                columnspan=3, sticky="w")

        #image information
        image=cv2.imread(self.path) #load image
        img = Image.open(self.path)

        if len(img.split()) == 3:
            self.text_T.set("图像类型为彩色图片")
        else:
            self.text_T.set("图像类型为黑白图片")

        self.text_H.set(image.shape[0])
        self.text_W.set(image.shape[1])

        # resize image
        cv_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, no_channels = cv_img.shape

        HEIGHT = 400
        imgScale = HEIGHT / height
        newX, newY = cv_img.shape[1] * imgScale, cv_img.shape[0] * imgScale
        newimg = cv2.resize(cv_img, (int(newX), int(newY)))
        photo = ImageTk.PhotoImage(image=Image.fromarray(newimg))

        # show image
        self.lbl_image.configure(image=photo)
        self.lbl_image.image = photo

        # show file information
        self.lbl_Height.grid(row=5, column=0, pady=0, padx=10, columnspan=3, sticky="nw")
        self.lbl_Height_01.grid(row=5, column=0, pady=0, padx=100, columnspan=3, sticky="nw")
        self.lbl_Width.grid(row=6, column=0, pady=0, padx=10, sticky="nw")
        self.lbl_Width_01.grid(row=6, column=0, pady=0, padx=100, columnspan=3, sticky="nw")
        self.lbl_Type.grid(row=7, column=0, pady=0, padx=10, sticky="nw")
        self.lbl_Type_01.grid(row=7, column=0, pady=0, padx=100, columnspan=3, sticky="nw")

        # add button
        self.gray_btn.grid(row=17, column=0, padx=10, pady=10,columnspan=3, sticky="w")
        self.tran_btn.grid(row=17, column=0, padx=130, pady=10,columnspan=3, sticky="w")
        self.level_btn.grid(row=17, column=0, padx=250, pady=10, columnspan=3, sticky="w")
        self.equlize_btn.grid(row=17, column=0, padx=370, pady=10, columnspan=3, sticky="w")
        self.smooth_btn.grid(row=17, column=0, padx=525, pady=10, columnspan=3, sticky="w")
        self.edge_btn.grid(row=17, column=0, padx=610, pady=10, columnspan=3, sticky="w")


    def equlize(self):
        image = cv2.imread(self.path)
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        equlizeimg = cv2.equalizeHist(image_gray)

        file_name = os.path.basename(self.path).strip('.jpg')
        dir_path = os.path.join(os.path.dirname(os.getcwd()), 'image') #不用exe直接运行用这个
        file_name = file_name + "_equlize.jpg"
        save_path = os.path.join(dir_path, file_name)

        cv2.imwrite(save_path, equlizeimg)

        messagebox.showinfo(title='Info', message='Successful save the changed image')

    def smooth(self):
        image = cv2.imread(self.path)
        img_mean = cv2.blur(image, (5,5))#均值滤波

        file_name = os.path.basename(self.path).strip('.jpg')
        dir_path = os.path.join(os.path.dirname(os.getcwd()), 'image')
        file_name = file_name + "_smooth.jpg"
        save_path = os.path.join(dir_path, file_name)

        cv2.imwrite(save_path, img_mean)

        messagebox.showinfo(title='Info', message='Successful save the changed image')

    def edge(self):
        image = cv2.imread(self.path)
        sobel_img = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)#sobel's operator

        file_name = os.path.basename(self.path).strip('.jpg')
        dir_path = os.path.join(os.path.dirname(os.getcwd()), 'image')
        file_name = file_name + "_edge.jpg"
        save_path = os.path.join(dir_path, file_name)

        cv2.imwrite(save_path,sobel_img)

        messagebox.showinfo(title='Info', message='Successful save the changed image')

    def to_gray(self):
        image=cv2.imread(self.path)
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        file_name = os.path.basename(self.path).strip('.jpg')
        dir_path = os.path.join(os.path.dirname(os.getcwd()), 'image')
        file_name = file_name + "_gray.jpg"
        save_path = os.path.join(dir_path, file_name)

        cv2.imwrite(save_path, image_gray)

        messagebox.showinfo(title='Info', message='Successful save the changed image')

    def trans_page(self):
        self.count += 1
        id = "New window #%s" % self.count
        window = tk.Toplevel(self)#open new window
        window.geometry("300x300+100+100")#set window size

        #label
        window.lbl_Rotation = tk.Label(window, text="Rotation: ", font=("Arial", 12), fg="#202020")
        window.lbl_Scal = tk.Label(window, text="Scal: ", font=("Arial", 12), fg="#202020")
        window.lbl_Translation = tk.Label(window, text="Translation: ", font=("Arial", 12), fg="#202020")
        window.lbl_Rotation_d = tk.Label(window, text="°", font=("Arial", 12), fg="#202020")
        window.lbl_Scal_p = tk.Label(window, text="%", font=("Arial", 12), fg="#202020")
        window.lbl_Translation_x = tk.Label(window, text="X: ", font=("Arial", 10), fg="#202020")
        window.lbl_Translation_y = tk.Label(window, text="Y: ", font=("Arial", 10), fg="#202020")

        #show label
        window.lbl_Rotation.grid(row=1, column=0, pady=10, padx=10, columnspan=3, sticky="nw")
        window.lbl_Scal.grid(row=2, column=0, pady=10, padx=10, sticky="nw")
        window.lbl_Rotation_d.grid(row=1, column=0, pady=10, padx=160, columnspan=3, sticky="nw")
        window.lbl_Scal_p.grid(row=2, column=0, pady=10, padx=160, sticky="nw")
        window.lbl_Translation.grid(row=3, column=0, pady=10, padx=10, sticky="nw")
        window.lbl_Translation_x.grid(row=3, column=0, pady=15, padx=120, sticky="nw")
        window.lbl_Translation_y.grid(row=4, column=0, pady=10, padx=120, sticky="nw")

        #text input
        degree_var = tk.StringVar()
        scale_var=tk.StringVar()
        x_var = tk.StringVar()
        y_var = tk.StringVar()
        rotation_entry = tk.Entry(window, width=10, textvariable=degree_var)
        rotation_entry.grid(row=1, column=0, columnspan=3, padx=80, pady=10, sticky="w")
        scale_entry = tk.Entry(window, width=10,textvariable=scale_var)
        scale_entry.grid(row=2, column=0, columnspan=3, padx=80, pady=10, sticky="w")

        window.translation_x_entry = tk.Entry(window, width=10,textvariable=x_var)
        window.translation_x_entry.grid(row=3, column=0, columnspan=3, padx=140, pady=15, sticky="w")
        window.translation_y_entry = tk.Entry(window, width=10,textvariable=y_var)
        window.translation_y_entry.grid(row=4, column=0, columnspan=3, padx=140, pady=10, sticky="w")


        degree=0
        scale=100
        x=0
        y=0

        window.ok_btn = tk.Button(window, text="     OK     ", bg="#ffffff", relief="flat",
                              width=10, command=lambda: self.trans(degree_var.get(),scale_var.get(),x_var.get(),y_var.get()))

        window.ok_btn.grid(row=7, column=0, padx=100, pady=10,
                            columnspan=3, sticky="w")


    def trans(self,degree,scale,x,y):
        image = cv2.imread(self.path)
        (h, w) = image.shape[:2]
        (cx, cy) = (w / 2, h / 2)
        try:
            degree = int(degree)
        except ValueError:
            messagebox.showinfo(title='Info', message='Please enter a number at degree.')
            return
        try:
            x = int(x)
        except ValueError:
            messagebox.showinfo(title='Info', message='Please enter a number at X.')
            return
        try:
            y = int(y)
        except ValueError:
            messagebox.showinfo(title='Info', message='Please enter a number at Y.')
            return
        try:
            scale=int(scale)
            if scale<=0:
                messagebox.showinfo(title='Info', message='Please enter an integer at scale.')
                return
        except ValueError:
            messagebox.showinfo(title='Info', message='Please enter a number at scale.')
            return

        # 设置旋转矩阵
        M = cv2.getRotationMatrix2D((cx, cy), -int(degree), 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        # 计算图像旋转后的新边界
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # 调整旋转矩阵的移动距离（t_{x}, t_{y}）
        M[0, 2] += (nW / 2) - cx
        M[1, 2] += (nH / 2) - cy

        rotation_image = cv2.warpAffine(image, M, (nW, nH))

        #缩放
        scale_n=int(scale)/100
        newX, newY = rotation_image.shape[1] * scale_n, rotation_image.shape[0] * scale_n
        newimg = cv2.resize(rotation_image, (int(newX), int(newY)))

        #平移
        img_info = newimg.shape
        height = img_info[0]
        width = img_info[1]

        mat_translation = np.float32([[1, 0, 20], [0, 1, 50]])
        finalimg = cv2.warpAffine(newimg, mat_translation, (width + int(x), height + int(y)))

        #save image
        file_name = os.path.basename(self.path).strip('.jpg')
        dir_path = os.path.join(os.path.dirname(os.getcwd()), 'image')
        file_name = file_name + "_transformation.jpg"
        save_path = os.path.join(dir_path, file_name)

        cv2.imwrite(save_path, finalimg)

        messagebox.showinfo(title='Info', message='Successful save the changed image')

    def gray_page(self):
        window = tk.Toplevel(self)  # open new window

        window.geometry("400x200+100+100")  # set window size

        # label
        window.lbl_notice = tk.Label(window, text="Please enter gray level (2，4，8，16，32，64，128).",
                                     font=("Arial", 12), fg="#202020")
        window.lbl_level = tk.Label(window, text="Gray level: ", font=("Arial", 12), fg="#202020")

        # show label
        window.lbl_notice.grid(row=1, column=0, pady=10, padx=10, columnspan=3, sticky="nw")
        window.lbl_level.grid(row=2, column=0, pady=10, padx=10, columnspan=3, sticky="nw")

        # text input
        level_var = tk.StringVar()

        level_entry = tk.Entry(window, width=10, textvariable=level_var)
        level_entry.grid(row=2, column=0, columnspan=3, padx=120, pady=10, sticky="w")

        window.ok_btn = tk.Button(window, text="     OK     ", bg="#ffffff", relief="flat",
                                  width=10, command=lambda: self.gray_level(level_var.get()))

        window.ok_btn.grid(row=7, column=0, padx=150, pady=10,columnspan=3, sticky="w")

    def gray_level(self, level):
        img = cv2.imread(self.path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        file_name = os.path.basename(self.path).strip('.jpg')
        dir_path = os.path.join(os.path.dirname(os.getcwd()), 'image')

        newimg = copy.deepcopy(gray)
        rows = img.shape[0]
        cols = img.shape[1]

        if level=="2":
            ret, newimg = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            file_name = file_name + "_gray_2.jpg"
        elif level=="4":
            for i in range(rows):
                for j in range(cols):
                    newimg[i][j] = newimg[i][j]//64*85
            file_name = file_name + "_gray_4.jpg"
        elif level=="8":
            for i in range(rows):
                for j in range(cols):
                    newimg[i][j] = newimg[i][j]//32*36
            file_name = file_name + "_gray_8.jpg"
        elif level=="16":
            for i in range(rows):
                for j in range(cols):
                    newimg[i][j] = newimg[i][j]//16*17
            file_name = file_name + "_gray_16.jpg"
        elif level=="32":
            for i in range(rows):
                for j in range(cols):
                    newimg[i][j] = newimg[i][j]//8*8
            file_name = file_name + "_gray_32.jpg"
        elif level=="64":
            for i in range(rows):
                for j in range(cols):
                    newimg[i][j] = newimg[i][j]//4*4
            file_name = file_name + "_gray_64.jpg"
        elif level=="128":
            for i in range(rows):
                for j in range(cols):
                    newimg[i][j] = newimg[i][j]//2*2
            file_name = file_name + "_gray_128.jpg"
        else:
            messagebox.showinfo(title='Info', message='Please enter a correct level.')
            return

        save_path = os.path.join(dir_path, file_name)
        cv2.imwrite(save_path, newimg)

        messagebox.showinfo(title='Info', message='Successful save the changed image')

if __name__ == "__main__":
    app = Page()
    app.geometry("750x750+150+50")
    app.mainloop()
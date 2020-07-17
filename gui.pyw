from tkinter import *
import pickle
import torch 
from PIL import ImageGrab
from PIL import Image	

class Le_Net(torch.nn.Module):
    def __init__(self,conv_size=5,activation="tanh",pooling="avg",use_batch_normalize=False):
        super(Le_Net,self).__init__()
        self.conv_size=conv_size
        self.use_batch_normalize=use_batch_normalize
        
        if activation=="tanh":
            activation_func=torch.nn.Tanh()
        elif activation=="relu":
            activation_func=torch.nn.ReLU()
        else:
            raise NotImplementedError
        
        if pooling=="avg":
            pooling_layer=torch.nn.AvgPool2d(kernel_size=2,stride=2)
        elif pooling=="max":
            pooling_layer=torch.nn.MaxPool2d(kernel_size=2,stride=2)
        else:
            raise NotImplementedError
        
        
        # first convolutional layer
        if self.conv_size==5:
            self.conv1=torch.nn.Conv2d(in_channels=1,out_channels=6,kernel_size=5,padding=2)
        elif self.conv_size==3:
            self.conv1_1=torch.nn.Conv2d(in_channels=1,out_channels=6,kernel_size=3,padding=1)
            self.conv1_2=torch.nn.Conv2d(in_channels=6,out_channels=6,kernel_size=3,padding=1)
        else:
            raise NotImplementedError
        
        self.act1=activation_func
        self.bn1=torch.nn.BatchNorm2d(num_features=6)
        self.pool1=pooling_layer

        #second convolutional layer
        if self.conv_size==5:
            self.conv2=torch.nn.Conv2d(in_channels=6,out_channels=16,kernel_size=5,padding=0)
        elif self.conv_size==3:
            self.conv2_1=torch.nn.Conv2d(in_channels=6,out_channels=16,kernel_size=3,padding=0)
            self.conv2_2=torch.nn.Conv2d(in_channels=16,out_channels=16,kernel_size=3,padding=0)
        else:
            raise NotImplementedError
        self.act2=activation_func
        self.bn2=torch.nn.BatchNorm2d(num_features=16)
        self.pool2=pooling_layer
        
        #fullconnected layers
        self.fc1=torch.nn.Linear(5*5*16,120)
        self.act3=activation_func
        self.fc2=torch.nn.Linear(120,84)
        self.act4=activation_func
        self.fc3=torch.nn.Linear(84,10)
        
    def forward(self,x):
        if self.conv_size==5:
            x=self.conv1(x)
        elif self.conv_size==3:
            x=self.conv1_1(x)
            x=self.conv1_2(x)
        x=self.act1(x)
        x=self.bn1(x)
        x=self.pool1(x)
        
        if self.conv_size==5:
            x=self.conv2(x)
        elif self.conv_size==3:
            x=self.conv2_1(x)
            x=self.conv2_2(x)
        x=self.act2(x)
        x=self.bn2(x)
        x=self.pool2(x)
        
        x = x.view(x.size(0), x.size(1) * x.size(2) * x.size(3))
        
        x=self.fc1(x)
        x=self.act3(x)
        x=self.fc2(x)
        x=self.act4(x)
        x=self.fc3(x)
        return x

class Input_window:
	__slots__=("master","canv","x","y","oval_width")
	def __init__(self,master):
		self.master=master
		self.canv=Canvas(self.master,width=300,height=370,bg="white")

		self.x=None
		self.y=None
		self.oval_width=12

		self.canv.bind("<Button-1>",self.draw_click)
		self.canv.bind("<B1-Motion>",self.draw_motion)

		self.canv.pack()
	def draw_click(self,event):
		self.x=None
		self.y=None
		self.canv.create_oval(event.x-self.oval_width,event.y-self.oval_width,event.x+self.oval_width,event.y+self.oval_width,fill="black")

	def draw_motion(self,event):
		if self.x==None and self.y==None:
			self.x=event.x
			self.y=event.y
			self.canv.create_oval(event.x,event.y,event.x+self.oval_width,event.y+self.oval_width,fill="black")
		else:
			self.canv.create_oval(event.x-self.oval_width,event.y-self.oval_width,event.x+self.oval_width,event.y+self.oval_width,fill="black")
			self.canv.create_line(self.x,self.y,event.x,event.y,width=self.oval_width*2)
			self.x=event.x
			self.y=event.y

class Main_panel:
	__slots__=("master","input_window","classifier_btn","clear_btn","info_output","result_label","neural_net")
	def __init__(self,master,input_window):
		self.master=master
		self.input_window=input_window

		self.classifier_btn=Button(self.master,text="Классифицировать",bg="white",width=20,pady=10,padx=20,command=self.classifier)
		self.clear_btn=Button(self.master,text="Очистить",bg="white",width=20,pady=10,padx=20,command=self.clear)
		self.info_output=Label(self.master,text="")
		self.result_label=Label(self.master,text="")

		self.classifier_btn.pack(fill="x")
		self.clear_btn.pack(fill="x")
		self.info_output.pack(fill="x")
		self.result_label.pack(fill="x")

		with open(r"C:\Users\egor-\OneDrive\Рабочий стол\Егор\Программирование\Распознавание цифр\neural_net.txt","rb") as file:
			self.neural_net=pickle.load(file)


	def classifier(self):
		x=self.input_window.master.winfo_rootx()+self.input_window.canv.winfo_x()
		y=self.input_window.master.winfo_rooty()+self.input_window.canv.winfo_y()
		x1=x+self.input_window.canv.winfo_width()
		y1=y+self.input_window.canv.winfo_height()

		image=ImageGrab.grab().crop((x,y,x1,y1))

		bbox = Image.eval(image, lambda px: 255-px).getbbox()
		# Оригинальные длины сторон
		widthlen = bbox[2] - bbox[0]
		heightlen = bbox[3] - bbox[1]

		# Новые
		if heightlen > widthlen:
			widthlen = int(20.0 * widthlen / heightlen)
			heightlen = 20
		else:
			heightlen = int(20.0 * widthlen / heightlen)
			widthlen = 20

		# Стартовая точка рисования
		hstart = int((28 - heightlen) / 2)
		wstart = int((28 - widthlen) / 2)

		# Отмасштабированная картинка
		img_temp = image.crop(bbox).resize((widthlen, heightlen), Image.NEAREST)

		# Перенос на белый фон с центрированием
		new_img = Image.new('L', (28,28), 255)
		new_img.paste(img_temp, (wstart, hstart))

		# Конвертация в np.array и нормализация
		imgdata = list(new_img.getdata())
		imgdata_res,k=[],0
		for i in range(28):
			imgdata_res.append([])
			for j in range(28):
				imgdata_res[-1].append((255.0 - imgdata[k]) / 255.0)
				k+=1


		imgdata_res=torch.FloatTensor(imgdata_res).unsqueeze(0).unsqueeze(0).float()

		result=self.neural_net.forward(imgdata_res)

		self.info_output["text"]=result
		self.result_label["text"]=result.argmax(dim=1)

	def clear(self):
		self.input_window.canv.delete("all")
		self.info_output["text"]=""
		self.result_label["text"]=""

def main():
	root=Tk()
	root.title("Classifier")

	frame_1=Frame(root)
	frame_2=Frame(root)

	input_window=Input_window(frame_1)
	checkbox_window=Main_panel(frame_2,input_window)

	frame_1.pack(side="left")
	frame_2.pack(side="left")


	root.mainloop()

if __name__=="__main__":
	main()


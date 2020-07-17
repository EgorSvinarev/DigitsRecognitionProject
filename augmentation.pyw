from tkinter import *
from PIL import ImageGrab
from PIL import Image
import numpy as np
import pickle
import random
from skimage import transform

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


class Checkbox_window:
	__slots__=("master","input_window","var","label","info_label",
		"radiobutton_0","radiobutton_1","radiobutton_2","radiobutton_3",
		"radiobutton_4","radiobutton_5","radiobutton_6","radiobutton_7",
		"radiobutton_8","radiobutton_9","save_btn","clear_btn")
	def __init__(self,master,input_window):
		self.master=master
		self.input_window=input_window

		self.var=IntVar()
		self.var.set(100)

		self.label=Label(self.master,text="")
		self.info_label=Label(self.master,text="Укажите метку класса цифры.")

		self.radiobutton_0=Radiobutton(self.master,text="0",variable=self.var,value=0)
		self.radiobutton_1=Radiobutton(self.master,text="1",variable=self.var,value=1)
		self.radiobutton_2=Radiobutton(self.master,text="2",variable=self.var,value=2)
		self.radiobutton_3=Radiobutton(self.master,text="3",variable=self.var,value=3)
		self.radiobutton_4=Radiobutton(self.master,text="4",variable=self.var,value=4)
		self.radiobutton_5=Radiobutton(self.master,text="5",variable=self.var,value=5)
		self.radiobutton_6=Radiobutton(self.master,text="6",variable=self.var,value=6)
		self.radiobutton_7=Radiobutton(self.master,text="7",variable=self.var,value=7)
		self.radiobutton_8=Radiobutton(self.master,text="8",variable=self.var,value=8)
		self.radiobutton_9=Radiobutton(self.master,text="9",variable=self.var,value=9)

		self.save_btn=Button(self.master,text="Сохранить",bg="white",width=20,pady=7,padx=50,command=self.save)
		self.clear_btn=Button(self.master,text="Очистить",bg="white",width=20,pady=7,padx=50,command=self.clear)

		self.label.pack(fill="x")
		self.info_label.pack(fill="x")

		self.radiobutton_0.pack(fill="x")
		self.radiobutton_1.pack(fill="x")
		self.radiobutton_2.pack(fill="x")
		self.radiobutton_3.pack(fill="x")
		self.radiobutton_4.pack(fill="x")
		self.radiobutton_5.pack(fill="x")
		self.radiobutton_6.pack(fill="x")
		self.radiobutton_7.pack(fill="x")
		self.radiobutton_8.pack(fill="x")
		self.radiobutton_9.pack(fill="x")

		self.save_btn.pack(fill="both")
		self.clear_btn.pack(fill="both")

	def clear(self):
		self.input_window.canv.delete("all")
		self.var.set(100)

	def save(self):
		if self.var.get()!=100:
			try:
				with open("labels.txt","rb") as file:
					labels=pickle.load(file)
			except:
				labels=[]
			try:
				with open("features.txt","rb") as file:
					features=pickle.load(file)
			except:
				features=[]

			label=self.var.get()

			x=self.input_window.master.winfo_rootx()+self.input_window.canv.winfo_x()
			y=self.input_window.master.winfo_rooty()+self.input_window.canv.winfo_y()
			x1=x+self.input_window.canv.winfo_width()
			y1=y+self.input_window.canv.winfo_height()

			image=ImageGrab.grab().crop((x,y,x1,y1))

			angles=np.arange(-15,15,5)

			bbox = Image.eval(image, lambda px: 255-px).getbbox()
			# Оригинальные длины сторон
			widthlen = bbox[2] - bbox[0]
			heightlen = bbox[3] - bbox[1]

			# Новые
			if heightlen > widthlen:
				widthlen = int(20.0 * widthlen/heightlen)
				heightlen = 20
			else:
				heightlen = int(20.0 * widthlen/heightlen)
				widthlen = 20

			# Стартовая точка рисования
			hstart = int((28 - heightlen) / 2)
			wstart = int((28 - widthlen) / 2)

			# 4 варианта масштабирования
			for i in [min(widthlen, heightlen), max(widthlen, heightlen)]:
				for j in [min(widthlen, heightlen), max(widthlen, heightlen)]:
					# Отмасштабированная картинка
					resized_img = image.crop(bbox).resize((i, j), Image.NEAREST)
					# Перенос на белый фон с центрированием
					resized_image = Image.new('L', (28,28), 255)
					resized_image.paste(resized_img, (wstart, hstart))

					# Случайный выбор 6 значений из 12.
					angles_ = random.sample(set(angles), 6)
					for angle in angles_:
						# Поворот изображений
						transformed_image = transform.rotate(np.array(resized_image),
							angle, cval=255, preserve_range=True).astype(np.uint8)

						labels.append(int(label))

						# Преобразование в картинку для удобства
						img_temp = Image.fromarray(np.uint8(transformed_image))

						# Конвертация в np.array и нормализация
						imgdata_res,k=[],0
						imgdata = list(img_temp.getdata())
						for i in range(28):
							imgdata_res.append([])
							for j in range(28):
								imgdata_res[-1].append((255.0 - imgdata[k]) / 255.0)
								k+=1
						features.append(imgdata_res)

			with open("labels.txt","wb") as file:
				pickle.dump(labels,file)
			with open("features.txt","wb") as file:
				pickle.dump(features,file)
			self.clear()
		else:
			print("Не указана метка класса.")


def main():
	root=Tk()
	root.title("Augmentation")

	frame_1=Frame(root)
	frame_2=Frame(root)

	input_window=Input_window(frame_1)
	checkbox_window=Checkbox_window(frame_2,input_window)

	frame_1.pack(side="left",fill=X)
	frame_2.pack(side="left",fill=X)

	root.geometry('550x370+200+100')

	root.mainloop()

if __name__=="__main__":
	main()
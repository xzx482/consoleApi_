import ctypes, msvcrt,os,sys

class COORD(ctypes.Structure):
	_fields_=[("X", ctypes.c_short),("Y", ctypes.c_short)] 
	def __init__(self,x=0,y=0):
		self.X=x
		self.Y=y
	def 列表(self):
		return [self.X,self.Y]


class SMALL_RECT(ctypes.Structure):
	_fields_=[("Left",ctypes.c_short),("Top",ctypes.c_short),("Right",ctypes.c_short),("Bottom",ctypes.c_short)] 
	def __init__(self,left=0,top=0,right=0,bottom=0):
		self.Left=left
		self.Top=top
		self.Right=right
		self.Bottom=bottom
	def 列表(self):
		return [self.Left,self.Top,self.Right,self.Bottom]

class CONSOLE_CURSOR_INFO(ctypes.Structure):
	_fields_=[("dwSize", COORD),("bVisible", ctypes.c_bool)]
	def __init__(self,dwSize=COORD(),bVisible=False):
		self.dwSize=dwSize
		self.bVisible=bVisible



class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
	_fields_=[("dwSize",COORD),("dwCursorPosition",COORD),("wAttributes",ctypes.c_short),("srWindow",SMALL_RECT),("dwMaximumWindowSize",COORD)]
	def __init__(self,dwSize=COORD(),dwCursorPosition=COORD(),wAttributes=0,srWindow=SMALL_RECT(),dwMaximumWindowSize=COORD()):
		self.dwSize=dwSize
		self.dwCursorPosition=dwCursorPosition
		self.wAttributes=wAttributes
		self.srWindow=srWindow
		self.dwMaximumWindowSize=dwMaximumWindowSize


w=ctypes.windll.kernel32
handle=w.GetStdHandle(-11)

def 打印(值):
	#print(值,end='',flush=True)
	sys.stdout.write(str(值))
	sys.stdout.flush()

def 清屏():
	return os.system("cls")

#光标信息=CONSOLE_CURSOR_INFO()
#w.GetConsoleCursorInfo(handle,ctypes.pointer(光标信息))

def 获取缓冲区信息():
	a=CONSOLE_SCREEN_BUFFER_INFO()
	w.GetConsoleScreenBufferInfo(handle,ctypes.pointer(a))
	return [a.dwSize.列表(),a.dwCursorPosition.列表(),a.wAttributes,a.srWindow.列表(),a.dwMaximumWindowSize.列表()]


def 获取光标位置():
	return 获取缓冲区信息()[1]

def 设置光标位置(x,y):
	return w.SetConsoleCursorPosition(handle,COORD(x,y))

#默认颜色=0x07
默认颜色=获取缓冲区信息()[2]
#w.SetConsoleTextAttribute(handle,默认颜色)


'''
0:黑
1:红
2:绿
3:黄
4:蓝
5:紫
6:深绿
7:白
'''

'''
颜色属性由两个十六进制数字指定 -- 第一个
对应于背景，第二个对应于前景。每个数字
可以为以下任何值:

	0 = 黑色       8 = 灰色
	1 = 蓝色       9 = 淡蓝色
	2 = 绿色       A = 淡绿色
	3 = 浅绿色     B = 淡浅绿色
	4 = 红色       C = 淡红色
	5 = 紫色       D = 淡紫色
	6 = 黄色       E = 淡黄色
	7 = 白色       F = 亮白色

color /?
'''
l2wl=[0,4,2,6,1,5,3,7]
def 设置颜色(文字颜色=None,背景颜色=None,默认颜色=默认颜色):
	颜色=0
	if 背景颜色:
		颜色+=l2wl[背景颜色]*0xf
	else:
		颜色+=(默认颜色&0xff)-(默认颜色&0xf)
	if 文字颜色:
		颜色+=l2wl[文字颜色]
	else:
		颜色+=默认颜色&0xf

	return w.SetConsoleTextAttribute(handle,颜色)

def 打印彩色文字(文字="",文字颜色=None,背景颜色=None):
	默认颜色=获取缓冲区信息()[2]
	设置颜色(文字颜色,背景颜色,默认颜色)
	打印(文字)
	w.SetConsoleTextAttribute(handle,默认颜色)

def 设置样式(文字颜色=None,背景颜色=None,高亮=None,下划线=None,闪烁=None,反显=None):
	设置颜色(文字颜色,背景颜色)

def 打印多样式文字(文字="",文字颜色=None,背景颜色=None,高亮=None,下划线=None,闪烁=None,反显=None):#暂时用不到, 缩点水
	打印彩色文字(文字,文字颜色,背景颜色)
	#设置样式(文字颜色,背景颜色,高亮,下划线,闪烁,反显)
	#打印(文字)

def 设置缓冲区大小(x,y):
	#缓冲区大小需不小于窗口大小
	return w.SetConsoleScreenBufferSize(handle,COORD(x,y))


光标位置_=[]

def 保存光标位置():
	global 光标位置_
	光标位置_=获取光标位置()

def 恢复光标位置():
	设置光标位置(*光标位置_)


def 设置显示区域(left,top,right,bottom):
	return w.SetConsoleWindowInfo(handle,True,ctypes.pointer(SMALL_RECT(left,top,right,bottom)))

def 设置窗口大小(x,y):
	return str(设置显示区域(0,0,x,y))+str(设置缓冲区大小(x-1,9001))+str(设置显示区域(0,0,x,y))

def 设置光标大小(大小,是否显示):
	return w.SetConsoleCursorInfo(handle,ctypes.pointer(CONSOLE_CURSOR_INFO(大小,是否显示)))

def 按任意键继续(提示信息="",提示信息_0="按",提示信息_1="任意",提示信息_2="键",提示信息_3="继续"):
	打印(提示信息+提示信息_0+提示信息_1+提示信息_2+提示信息_3)
	if(msvcrt.getch()==b'\x03'):
		raise KeyboardInterrupt
	打印("\n")

def 密码输入(提示文字="密码:"):
	'''
在win使用,调用后可输入显示为星号"*"的密码,左右键可移动光标(部分命令行或终端不支持),输入完成后按回车,返回值为输入的密码

参数:
	提示文字
		调用函数后给用户输入密码的提示文字,显示在左侧

返回值:
	输入的密码

'''
	文本=""
	光标位置=0
	print(提示文字,end="",flush=True)
	#if(1):
	while 1:
		try:
			键盘输入=''
			键盘输入=msvcrt.getch()#.decode(encoding="utf-8").decode("hex")#.decode(encoding="utf-8")
		except:print('1')
		#print(" "+str(键盘输入.hex()),end="",flush=True)
		#'''
			#return input("12")
		if(键盘输入==""):
			''
		elif(键盘输入==b'\r'):
			break
		elif(键盘输入==b'\x03'):#Ctrl+C
			raise KeyboardInterrupt
		elif(键盘输入==b'\x08'):#退格
			if(光标位置):
				文本=文本[0:光标位置-1]+文本[光标位置:]
				光标位置-=1
				#print("*"*(len(文本)-光标位置)+"\b "+"\b"*(len(文本)-光标位置+1),end="",flush=True)
		elif(键盘输入==b'\xe0'):#方向键
			键盘输入=msvcrt.getch()
			if(键盘输入==b'\x4b'):#左
				if(光标位置):
					#print("\b",end="",flush=True)
					光标位置-=1
			if(键盘输入==b'\x4d'):#右
				if(光标位置<len(文本)):
					#print("*",end="",flush=True)
					光标位置+=1
		else:
			#print("//"+str(键盘输入.hex())+"//")
			try:文本=文本[0:光标位置]+键盘输入.decode(encoding="utf-8")+文本[光标位置:]
			except:
				''#print("\r提示:无效的文本   ")
			else:
				光标位置+=1
				#print("*"*(len(文本)-光标位置+1)+"\b"*(len(文本)-光标位置),end="",flush=True)
		#print("\b"*(光标位置-1)+"*"*len(文本)+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#
		print("\r"+提示文字+"*"*len(文本)+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#星号输入
		#print("\r"+提示文字+文本+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#明文输入
		#'''
	print()
	return 文本


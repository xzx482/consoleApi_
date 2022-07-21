import atexit
import ctypes
import msvcrt

from .cmdp import 写缓冲区, 刷新缓冲区, 打印, 获取屏幕宽高, 获取用户输入_基类, 设置光标位置


class 更改终端错误(Exception):
	pass


#https://docs.microsoft.com/en-us/windows/console/getstdhandle
STD_INPUT_HANDLE=-10
STD_OUTPUT_HANDLE=-11
STD_ERROR_HANDLE=-12

#https://docs.microsoft.com/en-us/windows/console/setconsolemode
ENABLE_VIRTUAL_TERMINAL_PROCESSING=4
DISABLE_NEWLINE_AUTO_RETURN=8
ENABLE_VIRTUAL_TERMINAL_INPUT=512


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

输出句柄=w.GetStdHandle(STD_OUTPUT_HANDLE)
输入句柄=w.GetStdHandle(STD_INPUT_HANDLE)

if not(输出句柄 and 输入句柄):
	raise 更改终端错误("无法获取终端句柄")

原输出模式=ctypes.c_uint(0)
原输入模式=ctypes.c_uint(0)


if not (
	w.GetConsoleMode(输出句柄,ctypes.byref(原输出模式))
	and w.GetConsoleMode(输入句柄,ctypes.byref(原输入模式))
):
	raise 更改终端错误("无法获取终端模式")


#打印s('hello, world',2,5,1,1,1,1,0)

dwRequestedOutModes=ENABLE_VIRTUAL_TERMINAL_PROCESSING | DISABLE_NEWLINE_AUTO_RETURN
dwRequestedInModes=ENABLE_VIRTUAL_TERMINAL_INPUT

dwOutMode=ctypes.c_uint(原输出模式.value | dwRequestedOutModes)
dwInMode=ctypes.c_uint(原输入模式.value | dwRequestedInModes)

已初始=False

def 初始():
	global 已初始,dwOutMode,dwInMode
	if not w.SetConsoleMode(输出句柄,dwOutMode):
		dwRequestedOutModes=ctypes.c_uint(ENABLE_VIRTUAL_TERMINAL_PROCESSING)
		dwOutMode=ctypes.c_uint(原输出模式 | dwRequestedOutModes)
		if not w.SetConsoleMode(输出句柄,dwOutMode):
			raise 更改终端错误("无法设置终端模式")
	'''
	if not w.SetConsoleMode(输入句柄,dwInMode):
		raise 更改终端错误("无法设置终端模式")
	'''
	
	已初始=True
	"""
	atexit.register(关闭)


def 关闭():
	global 已初始
	if not w.SetConsoleMode(输出句柄,原输出模式):
		raise 更改终端错误("无法设置终端模式")
	'''
	if not w.SetConsoleMode(输入句柄,原输入模式):
		raise 更改终端错误("无法设置终端模式")
	'''
	已初始=False

#"""

初始()


class 获取用户输入(获取用户输入_基类):
	def 创建(s):
		# 原本想用 虚拟终端序列 来实现 (虚拟终端序列_查询状态:https://docs.microsoft.com/zh-cn/windows/console/console-virtual-terminal-sequences#query-state)
		# 但是虚拟终端总是在输入大量字符后失效 (具体表现为
		#		执行  w.SetConsoleMode(输入句柄,ENABLE_VIRTUAL_TERMINAL_INPUT)  后, 输入的字符不应显示,
		# 		但一通乱按或长按按键后, 按方向键等控制键会在输出终端中显示奇怪的字符,且SetConsoleMode失效,控制台可能崩溃;
		#
		#		即使慢慢地输入可以解决, 那么如果在cmd.exe中执行获取光标位置, 将无论如何都不能得到其返回的值, 结束python后才会看到要获取的值显示在终端中
		# )
		# 最终放弃了 虚拟终端序列 的大一统, 改用 msvcrt.getwch
		# 若有方法能够大一统, 可以提交 Pull request
		'''
		s.原输出模式=ctypes.c_uint(0)
		s.原输入模式=ctypes.c_uint(0)
		if not (
			w.GetConsoleMode(输出句柄,ctypes.byref(s.原输出模式)) 
			and w.GetConsoleMode(输入句柄,ctypes.byref(s.原输入模式))
		):
			raise 更改终端错误("无法获取终端模式")
		
		s.设置()
		

	def 设置(s):
		if not (
			(
				w.SetConsoleMode(输出句柄,ENABLE_VIRTUAL_TERMINAL_PROCESSING | DISABLE_NEWLINE_AUTO_RETURN)
				or w.SetConsoleMode(输出句柄,ENABLE_VIRTUAL_TERMINAL_PROCESSING)
			)
			and w.SetConsoleMode(输入句柄,ENABLE_VIRTUAL_TERMINAL_INPUT)
		):
			raise 更改终端错误("无法设置终端模式")

	def 重设(s):
		os.system('')
		s.设置()
		"""
		#'''
	def 获取输入(s):
		return msvcrt.getwch()
		#"""

	def 清理(s):
		'''
		if not (
			w.SetConsoleMode(输出句柄,s.原输出模式)
			and w.SetConsoleMode(输入句柄,s.原输入模式)
		):
			raise 更改终端错误("无法设置终端模式")
		#'''
		

def 获取光标位置():
	with 获取用户输入() as h:
		打印("\x1b[6n")
		buf=""
		while True:
			buf+=h.获取输入()
			if buf[-1]=="R":
				break
	x,y=1,1
	if buf[:2]=="\x1b[" and buf[-1]=="R":
		buf=buf[2:-1].split(";")
		x,y=int(buf[1]),int(buf[0])
	elif buf=='\x1bOR':
		x,y=1,1
	else:
		raise Exception("无法获取光标位置")
	return x,y




def 获取缓冲区信息():
	bufInfo=CONSOLE_SCREEN_BUFFER_INFO()
	if not w.GetConsoleScreenBufferInfo(输出句柄,ctypes.byref(bufInfo)):
		raise 更改终端错误("无法获取缓冲区信息")
	return bufInfo


#基于普通终端控制字符获取光标位置在windos上不可用,使用下面的方法
def 获取光标位置():
	cp=获取缓冲区信息().dwCursorPosition
	return cp.X,cp.Y



def 密码输入(提示文字="密码:"):
	文本=''
	with 获取用户输入() as h:
		设置光标位置(0)
		打印(提示文字)
		光标位置=获取光标位置()
		提示宽=光标位置[0]
		光标线位置_=提示宽
		文本数_=提示宽
		文本数_旧=0
		
		光标线位置=0
		
		while True:
			buf=h.获取输入()
			#print(buf.__repr__(),ord(buf))
			#Windows下getwch的方向键与普通的终端控制字符部分不同
			if buf=='\x03':#Ctrl+C
				raise KeyboardInterrupt()
			elif buf=='\r':#回车
				break
			elif buf=='\x08':#退格 ; 原 elif buf=='\x7f':
				if(光标线位置>0):
					文本=文本[0:光标线位置-1]+文本[光标线位置:]
					光标线位置-=1
			elif(buf=='\x00' or buf=='\xe0'):#原 elif(buf=='\x1b'):
				#buf=h.获取输入()
				#if buf=='[':
				#windows的方向键只有两个字符

					buf=h.获取输入()
					#原:
					##A:光标上移;B:光标下移;C:光标右移;D:光标左移
					##H:光标到行首;F:光标到行尾

					#H:光标上移;P:光标下移;M:光标右移;K:光标左移
					#G:光标到行首;O:光标到行尾
					if buf=='M':
						if(光标线位置<len(文本)):
							光标线位置+=1
					elif buf=='K':
						if(光标线位置>0):
							光标线位置-=1
					elif buf=='G':
						光标线位置=0
					elif buf=='O':
						光标线位置=len(文本)
					elif buf=='S':#Delete
						if 光标线位置<len(文本):
							文本=文本[0:光标线位置]+文本[光标线位置+1:]

							
				#else:
				#	pass
			else:
				if 32<=ord(buf)<=126:
					文本=文本[0:光标线位置]+buf+文本[光标线位置:]
					光标线位置+=1
			
			文本数=len(文本)
			显示宽=获取屏幕宽高()[0]
			新旧差=文本数-文本数_旧



			yg_旧,xg_旧=divmod(光标线位置_,显示宽)
			y_旧,x_旧=divmod(文本数_,显示宽)

			光标线位置_=光标线位置+提示宽
			文本数_=文本数+提示宽
			yg,xg=divmod(光标线位置_,显示宽)
			y,x=divmod(文本数_,显示宽)


			填充值='*' if 新旧差>0 else ' '

			y差=y-y_旧
			x差=x-x_旧

			
			if y差:
				if y差>0:
					x1=x_旧
					x2=x
					y1=y_旧
					y2=y
				elif y差<0:
					x1=x
					x2=x_旧
					y1=y
					y2=y_旧

				设置光标位置(x1-xg_旧,y1-yg_旧,True)
				写缓冲区(填充值*(显示宽-x1))
				写缓冲区('\n')
				设置光标位置(0)
				y差_=abs(y差)-1
				if y差_>0:
					for i in range(y差_):
						写缓冲区(填充值*显示宽)
						写缓冲区('\n')
						设置光标位置(0)
				写缓冲区(填充值*x2)
				设置光标位置(xg-x2,yg-y2,True)

			elif x差:
				if x差>0:
					x1=x_旧
					x2=x
				elif x差<0:
					x1=x
					x2=x_旧

				设置光标位置(x1-xg_旧,y-yg_旧,True)
				写缓冲区(填充值*(x2-x1))
				设置光标位置(xg-x2,yg-y,True)
			
			else:
				设置光标位置(xg-xg_旧,yg-yg_旧,True)

			
			
			刷新缓冲区()
			

			文本数_旧=文本数
			
	print()
	return 文本


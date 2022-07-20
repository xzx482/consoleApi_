import sys,os
import atexit
from .import 回溯


__doc__='''
这是一个对控制台操作的封装
可以进行 光标位置 文字样式 等操作
对于所有位置操作 x,y 均从 0 开始; 先x后y
'''

def 获取屏幕宽高():
	x,y=os.get_terminal_size()
	return (x,y)


def 打印(内容):
	sys.stdout.write(内容)
	sys.stdout.flush()

def 写缓冲区(内容):
	sys.stdout.write(内容)

def 刷新缓冲区():
	sys.stdout.flush()

'''
https://docs.microsoft.com/zh-cn/windows/console/console-virtual-terminal-sequences
'''


E='\x1b'
E1=E+'['
E2=E+']'


def 清屏(n=2,重设光标位置=None):
	'''
	n:
		0:擦除从当前光标位置到末尾
		1:擦除从开始到当前光标位置
		2:擦除整个屏幕
	'''
	写缓冲区(E1+str(n)+'J')
	if 重设光标位置 is None:
		if n==2:
			重设光标位置=True
		else:
			重设光标位置=False
	if 重设光标位置:
		设置光标位置(0,0)


def 清行(n=2,重设光标位置=None):
	'''
		0:擦除从当前光标位置到行尾
		1:擦除从行头到当前光标位置
		2:擦除整行
	'''
	写缓冲区(E1+str(n)+'K')
	if 重设光标位置 is None:
		if n==2:
			重设光标位置=True
		else:
			重设光标位置=False
	if 重设光标位置:
		设置光标位置(0)




def 设置光标位置(x=None,y=None,相对=False):
	'''
	相对:
		False:从左上开始
		True:从当前位置开始
	若 相对 为 False, 则 x,y 为从1开始;
	若没有指定 x或y, 则 x或y 不变.
	'''
	if 相对:
		if y:
			if y<0:
				写缓冲区(E1+str(-y)+'A')
			elif y>0:
				写缓冲区(E1+str(y)+'B')
		if x:
			if x<0:
				写缓冲区(E1+str(-x)+'D')
			elif x>0:
				写缓冲区(E1+str(x)+'C')
	else:
		if y is None:
			if x is None:
				raise Exception('至少设置一个参数')
			else:
				写缓冲区(E1+str(x+1)+'G')
		else:
			if x is None:
				写缓冲区(E1+str(y+1)+'d')
			else:
				写缓冲区(E1+str(y+1)+';'+str(x+1)+'H')


def 设置光标相对行(y):
	'''
	y将由当前位置相对移动
	x设置为0
	即 光标移动n行后移动到开头

	注意 它只能在缓冲区内移动,当到达屏幕边界时,不会移动
	'''
	if y>0:
		写缓冲区(E1+str(y)+'E')
	elif y<0:
		写缓冲区(E1+str(-y)+'F')



def 保存光标位置():
	写缓冲区(E1+'s')

def 恢复光标位置():
	写缓冲区(E1+'u')



def 设置光标可见(b):
	写缓冲区(E1+'?25'+('h' if b else 'l'))

def 设置光标闪烁(b):
	写缓冲区(E1+'?12'+('h' if b else 'l'))


def 设置文本样式(前景色=None,背景色=None,亮前景=None,亮背景=None,粗体=None,下划线=None,反色=None):
	'''
	亮前景 亮背景 粗体 下划线 反色 可为True 或 False ; 
	对于前景色和背景色, 可以是以下值:
	0:黑
	1:红
	2:绿
	3:黄
	4:蓝
	5:紫
	6:深绿
	7:白

	'''
	sl=[]
	if isinstance(前景色,int):
		前景色=str(前景色)
	if isinstance(背景色,int):
		背景色=str(背景色)

	if 前景色:
		sl.append( ('9' if 亮前景  else '3')+前景色)
	if 背景色:
		sl.append( ('10' if 亮背景  else '4')+背景色 )

	if isinstance(粗体,bool):
		sl.append( '1' if 粗体 else '22' )
	if isinstance(下划线,bool):
		sl.append( '4' if 下划线 else '24' )
	if isinstance(反色,bool):
		sl.append( '7' if 反色 else '27' )
		
	if not sl:
		sl.append('0')
	写缓冲区(E1+';'.join(sl)+'m')


def 设置滚动区域(y1,y2):
	'''
	文档中是这样写的, 但是它似乎不起作用
	'''
	写缓冲区(E1+str(y1)+';'+str(y2)+'r')



def 设置窗口标题(标题,更改图标名称=True,更改窗口标题=True):
	if 更改图标名称:
		if 更改窗口标题:
			s='0'
		else:
			s='1'
	else:
		if 更改窗口标题:
			s='2'
		else:
			raise ValueError('至少更改一个')
	写缓冲区(E2+s+';'+标题+E+'\x5c')

已启用备用缓冲区=False
def 设置备用缓冲区(b):
	global 已启用备用缓冲区
	已启用备用缓冲区=bool(b)
	写缓冲区(E1+'?1049'+('h' if b else 'l'))

def 软重置():
	写缓冲区(E1+'!p')


e=['']

@atexit.register
def 退出时返回主缓冲区():
	if e[0]:
		print(e[0])
		if e[1]:
			input('发生异常, 按回车键退出')
	if 已启用备用缓冲区:
		设置备用缓冲区(0)


def excepthook(exc_type, value, tb):
		e[0]=''
		e.append(exc_type not in (KeyboardInterrupt, SystemExit))
		for line in 回溯.TracebackException(
			type(value), value, tb).format(chain=True):
			e[0]+=line

#捕获错误, 防止错误在打印后被清除
sys.excepthook=excepthook




'''

'''

def 打印s(文本,前景色=None,背景色=None,亮前景=None,亮背景=None,粗体=None,下划线=None,反色=None):
	'''
	亮前景 亮背景 粗体 下划线 反色 可为True 或 False ; 
	对于前景色和背景色, 可以是以下值:
	0:黑
	1:红
	2:绿
	3:黄
	4:蓝
	5:紫
	6:深绿
	7:白
	'''
	设置文本样式(前景色,背景色,亮前景,亮背景,粗体,下划线,反色)
	打印(文本)
	设置文本样式()






class 获取用户输入_基类:
	锁=0

	def __init__(s):
		if not __class__.锁:
			s.创建()
			写缓冲区("\x1b[?1l")#https://docs.microsoft.com/zh-cn/windows/console/console-virtual-terminal-sequences#mode-changes
		__class__.锁+=1


	def 创建(s):
		'''
		继承的类,
		在此处,
		应先获取并保存终端的原始状态,
		再对终端进行修改,
		以便之后恢复到原来的状态.

		修改后的终端,输入应不被缓冲,
		即 用户输入一个字符 就能立即被获取.
		'''
	
	def 清理(s):
		'''
		继承的类,
		在此处,
		应对终端进行修改,
		使终端恢复到原来的状态.
		'''

	def 关闭(s):
		s.__exit__()

	def 获取输入(s):
		r=sys.stdin.read(1)
		if r=='\x03':
			raise KeyboardInterrupt
		return r

	def __enter__(s):
		return s

	def __exit__(s,exc_type,exc_value,traceback):
		__class__.锁-=1
		if not __class__.锁:
			s.清理()
		
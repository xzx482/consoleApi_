import re,sys,termios,tty

def 打印(值):
	#print(值,end='',flush=True)
	sys.stdout.write(str(值))
	sys.stdout.flush()

def 获取光标位置():
#此部分代码来自https://www.coder.work/article/4947338
    buf = ""
    stdin = sys.stdin.fileno()
    tattr = termios.tcgetattr(stdin)

    try:
        tty.setcbreak(stdin, termios.TCSANOW)
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()

        while True:
            buf += sys.stdin.read(1)
            if buf[-1] == "R":
                break

    finally:
        termios.tcsetattr(stdin, termios.TCSANOW, tattr)
	
    try:
        matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
        groups = matches.groups()
    except AttributeError:
        return None

    return [int(groups[1])-1, int(groups[0])-1]


def 设置光标位置(x,y):
	打印("\033["+str(y)+";"+str(x)+"H")

def 清除所有属性():
	打印("\033[0m")

def 清屏():
	打印("\033[2J")
	设置光标位置(0,0)

def 光标显示(显示=True):
	if(显示):
		打印("\033[?25h")
	else:
		打印("\033[?25l")

def 保存光标位置():
	打印("\033[s")

def 恢复光标位置():
	打印("\033[u")

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
def 设置颜色_lin(文字颜色=9,文字亮度=0,背景颜色=9):
	if(文字亮度==-1):
		打印("\033[2m")
	if(文字亮度==1):
		打印("\033[1m")
	打印("\033[3"+str(文字颜色)[0]+";4"+str(背景颜色)[0]+"m")


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
'''

win颜色_值="04261537"

def 设置颜色_win颜色属性(颜色):
	下划线=False
	反显=False
	if(颜色>0x8000):
		下划线=True
		颜色-=0x8000
	if(颜色>0x4000):
		反显=True
		颜色-=0x4000
	if(颜色>0x2000):
		颜色-=0x2000
	if(颜色>0x1000):
		颜色-=0x1000
	
	if(颜色>0x800):
		颜色-=0x800
	if(颜色>0x400):
		颜色-=0x400
	if(颜色>0x200):
		颜色-=0x200
	if(颜色>0x100):
		颜色-=0x100

	'''
	颜色=hex(颜色)[2:4]
	if(len(颜色)==1):
		颜色="0"+颜色
	a={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'A':10,'b':11,'B':11,'c':12,'C':12,'d':13,'D':13,'e':14,'E':14,'f':15,'F':15}
	背景颜色=a[颜色[0]]
	文字颜色=a[颜色[1]]
	'''
	背景颜色,文字颜色=divmod(颜色,16)
	文字亮度=0
	if(文字颜色-7>0):
		文字亮度+=1
	if(背景颜色-7>0):
		文字亮度-=1
	背景颜色%=8
	文字颜色%=8
	#未完成
	设置样式(win颜色_值[文字颜色],文字亮度,win颜色_值[背景颜色],False,下划线,False,反显)



def 设置样式(文字颜色=9,亮度=0,背景颜色=9,斜体=False,下划线=False,闪烁=False,反显=False):
	设置颜色_lin(文字颜色,亮度,背景颜色)
	if(斜体):
		打印("\033[3m")
	if(下划线):
		打印("\033[4m")
	if(闪烁):
		打印("\033[5m")
	if(反显):
		打印("\033[7m")

def 打印多样式文字(文字="",文字颜色=9,亮度=0,背景颜色=9,斜体=False,下划线=False,闪烁=False,反显=False):
	设置样式(文字颜色,亮度,背景颜色,斜体,下划线,闪烁,反显)
	打印(文字)
	清除所有属性()

def 打印彩色文字_win颜色属性(颜色,文字=""):
	设置颜色_win颜色属性(颜色)
	打印(文字)
	清除所有属性()

def 移动光标(右,下):
	if(下<0):
		打印("\033["+str(-下)+"A")
	if(下>0):
		打印("\033["+str(下)+"B")
	if(右<0):
		打印("\033["+str(-右)+"D")
	if(右>0):
		打印("\033["+str(右)+"C")


def 获取键盘输入():
	'''
在类linux使用,调用后可得到一个键盘输入而不显示在屏幕

返回值:
	输入键盘的字符

'''
	fd=sys.stdin.fileno()
	old_settings=termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		键盘输入=sys.stdin.read(1)
	except:''
	termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
	return 键盘输入

def 按任意键继续(提示信息="",提示信息_0="按",提示信息_1="任意",提示信息_2="键",提示信息_3="继续"):
	打印(提示信息+提示信息_0+提示信息_1+提示信息_2+提示信息_3)
	if(获取键盘输入()=='\x03'):
		raise KeyboardInterrupt
	打印("\n")

def 密码输入(提示文字="密码:"):
	'''
在类linux使用,调用后可输入显示为星号"*"的密码,左右键可移动光标(部分终端不支持),输入完成后按回车,返回值为输入的密码

参数:
	提示文字
		调用函数后给用户输入密码的提示文字,显示在左侧

返回值:
	输入的密码

'''
	文本=""
	光标位置=0
	print(提示文字,end="",flush=True)
	while 1:
		键盘输入=获取键盘输入()
		if(键盘输入==""):
			''
		elif(键盘输入=='\r'):
			break
		elif(键盘输入=='\x03'):#Ctrl+C
			raise KeyboardInterrupt
		elif(键盘输入=='\b' or 键盘输入=='\x7f'):#退格
			if(光标位置):
				文本=文本[0:光标位置-1]+文本[光标位置:]
				光标位置-=1
				#print("*"*(len(文本)-光标位置)+"\b "+"\b"*(len(文本)-光标位置+1),end="",flush=True)
		elif(键盘输入=='\x1b'):
			键盘输入=获取键盘输入()
			if(键盘输入=='\x5b'):#方向键
				键盘输入=获取键盘输入()
				if(键盘输入=='\x44'):#左
					if(光标位置):
						#print("\b",end="",flush=True)
						光标位置-=1
				if(键盘输入=='\x43'):#右
					if(光标位置<len(文本)):
						#print("*",end="",flush=True)
						光标位置+=1
		else:
			#print("//"+str(键盘输入.hex())+"//")
			try:文本=文本[0:光标位置]+键盘输入+文本[光标位置:]
			except:
				''#print("\r提示:无效的文本   ")
			else:
				光标位置+=1
				#print("*"*(len(文本)-光标位置+1)+"\b"*(len(文本)-光标位置),end="",flush=True)
		#print("\b"*(光标位置-1)+"*"*len(文本)+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#
		print("\r"+提示文字+"*"*len(文本)+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#星号输入
		#print(hex(ord(str(键盘输入))))
		#print("\r"+提示文字+文本+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#明文输入
		#'''
	print()
	return 文本


#设置颜色_win颜色属性(0x5a)
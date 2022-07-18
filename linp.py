import re,sys,termios,tty
from cmdp import 打印

class 获取用户输入_基类:
	锁=False

	def __init__(s):
		if __class__.锁:
			raise Exception("只能创建一个实例")
		__class__.锁=True
		sys.stdout.write("\x1b[?1l")
		sys.stdout.flush()

	def 关闭(s):
		s.__exit__()

	def 获取输入(s):
		pass

	def __enter__(s):
		return s

	def __exit__(s,exc_type,exc_value,traceback):
		if __class__.锁:
			__class__.锁=False

class 获取用户输入(获取用户输入_基类):
	def __init__(s):
		super().__init__()
		s.fd=sys.stdin.fileno()
		s.old_settings=termios.tcgetattr(s.fd)
		tty.setraw(sys.stdin.fileno())
	
	def 获取输入(s):
		return sys.stdin.read(1)

	def __exit__(s,exc_type,exc_value,traceback):
		termios.tcsetattr(s.fd,termios.TCSANOW,s.old_settings)
		super().__exit__(exc_type,exc_value,traceback)


def 获取光标位置():
	with 获取用户输入() as h:
		sys.stdout.write("\x1b[6n")
		sys.stdout.flush()
		buf=""
		while True:
			buf=h.获取输入()
			if buf=='c':
				break
	matches=re.match(r"^\x1b\[(\d*);(\d*)R", buf)
	groups=matches.groups()
	return int(groups[0]),int(groups[1])

def 密码输入(提示文字="密码:"):
	文本=''
	光标位置=0
	with 获取用户输入() as h:
		打印(提示文字)
		
		while True:
			buf=h.获取输入()
			
			if buf=='\x03':#Ctrl+C
				raise KeyboardInterrupt()
			elif buf=='\r':#回车
				break
			elif buf=='\x7f':#退格
				if(光标位置>0):
					文本=文本[0:光标位置-1]+文本[光标位置:]
					光标位置-=1
			elif(buf=='\x1b'):
				buf=h.获取输入()
				if buf=='[':
					buf=h.获取输入()
					#A:光标上移;B:光标下移;C:光标右移;D:光标左移
					#H:光标到行首;F:光标到行尾
					if buf=='C':
						if(光标位置<len(文本)):
							光标位置+=1
					elif buf=='D':
						if(光标位置>0):
							光标位置-=1
					elif buf=='H':
						光标位置=0
					elif buf=='F':
						光标位置=len(文本)
					elif buf=='3':
						buf=h.获取输入()
						if buf=='~':#Delete
							if 光标位置<len(文本):
								文本=文本[0:光标位置]+文本[光标位置+1:]

							
				else:
					pass
			else:
				if 32<=ord(buf)<=126:
					文本=文本[0:光标位置]+buf+文本[光标位置:]
					光标位置+=1
			
			打印("\r"+提示文字+"*"*len(文本)+" "+"\b"*(len(文本)-光标位置+1))
	print()
	return 文本


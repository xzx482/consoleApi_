import sys
import termios
import tty

from .cmdp import 写缓冲区, 刷新缓冲区, 打印, 获取屏幕宽高, 获取用户输入_基类, 设置光标位置


class 获取用户输入(获取用户输入_基类):
	def __init__(s):
		super().__init__()
		s.fd=sys.stdin.fileno()
		s.old_settings=termios.tcgetattr(s.fd)
		tty.setraw(sys.stdin.fileno())
	

	def __exit__(s,exc_type,exc_value,traceback):
		termios.tcsetattr(s.fd,termios.TCSANOW,s.old_settings)
		super().__exit__(exc_type,exc_value,traceback)


def 获取光标位置():
	with 获取用户输入() as h:
		写缓冲区("\x1b[6n")
		buf=""
		while True:
			buf+=h.获取输入()
			if buf[-1]=="R":
				break
	x,y=1,1
	if buf[:2]=="\x1b[" and buf[-1]=="R":
		buf=buf[2:-1].split(";")
		x,y=int(buf[1])-1,int(buf[0])-1
	elif buf=='\x1bOR':
		x,y=0,0
	else:
		raise Exception("无法获取光标位置")
	return x,y


def 密码输入(提示文字="密码:"):
	文本=''
	光标位置=0
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
			
			文本数=len(文本)
			#print("\r"+提示文字+"*"*len(文本)+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)
			显示宽=获取屏幕宽高()[0]
			光标位置=获取光标位置()
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
				y差_=abs(y差)-1
				if y差_>0:
					for i in range(y差_):
						写缓冲区(填充值*显示宽)
						写缓冲区('\n')
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


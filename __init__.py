import os
import time
def 获取屏幕宽高():
	x,y=os.get_terminal_size()
	return [x,y]
try:
	from .lincmd import *
	设置颜色=设置颜色_win颜色属性
	打印彩色文字=打印彩色文字_win颜色属性
	def 打印不支持信息():
		pass
except:
	try:
		from .wincmd import *
		def 打印不支持信息():
			pass
	except:
		import os
		def 打印(值):
			print(值,end='',flush=True)
		def 清屏():
			'''
		清空屏幕,部分命令行或终端不支持

		'''
			if(os.name=="nt"):
				os.system('cls')
			elif(os.name=="posix"):
				os.system('clear')
		def 打印不支持信息():
			打印("当前终端或控制台可能不支持某些功能(如彩色文字等)")
		def 获取光标位置(*a):
			return None
		def 设置光标位置(*a):
			return None
		def 设置颜色(*a):
			return None
		def 打印彩色文字(颜色,文字=""):
			return 打印(文字)
		def 按任意键继续(提示信息="",提示信息_0="按",提示信息_1="回车",提示信息_2="键",提示信息_3="继续"):
			打印(提示信息+提示信息_0+提示信息_1+提示信息_2+提示信息_3)
			input()
		def 密码输入(提示文字="密码:"):
			'''
		在不支持使用星号"*"来隐藏密码时使用

		参数:
			提示文字
				调用函数后给用户输入密码的提示文字,显示在左侧

		返回值:
			输入的密码

		'''
			print("注意:密码会显示")
			return input(提示文字)


class 动画:
	def __init__():
		raise

	def 渐退至行首(速度=.05):
		x,y=获取光标位置()
		for i in range(x):
			打印("\b \b")
			time.sleep(速度)
	
	def 渐打印(文字,速度=.05):
		for i in range(len(文字)):
			打印(文字[i])
			time.sleep(速度)

	



__all__=[打印,清屏,获取光标位置,设置光标位置,设置颜色,打印彩色文字,按任意键继续,密码输入]

if __name__=='__main__':
	清屏()
	打印不支持信息()
	打印彩色文字(4|2|0x8000,"hello, world")
	打印("\n光标位置:\n")
	打印(获取光标位置())
	设置光标位置(0,8)
	按任意键继续()
	打印("\n光标位置:")
	打印(获取光标位置())
	打印("\n")
	打印彩色文字(4,"R")
	打印("!")
	打印彩色文字(2,"G")
	打印("!")
	打印彩色文字(1,"B")
	打印("!")
	打印("\n")
	打印(密码输入())
	打印("\n")
	按任意键继续(提示信息_3="退出")

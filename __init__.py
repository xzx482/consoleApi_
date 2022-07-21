import time


相对导入=bool(__package__)


if 相对导入:
    from .p import cmdp as c
    try:
        from .p import linp as p
    except ImportError:
        from .p import winp as p
else:
    import p.cmdp as c
    try:
        import p.linp as p
    except ImportError:
        import p.winp as p



#通用终端方法
获取屏幕宽高=c.获取屏幕宽高
打印=c.打印
写缓冲区=c.写缓冲区
刷新缓冲区=c.刷新缓冲区
清屏=c.清屏
清行=c.清行
插入字符=c.插入字符
删除字符=c.删除字符
擦除字符=c.擦除字符
插入行=c.插入行
删除行=c.删除行
设置光标位置=c.设置光标位置
设置光标相对行=c.设置光标相对行
保存光标位置=c.保存光标位置
恢复光标位置=c.恢复光标位置
设置光标可见=c.设置光标可见
设置光标闪烁=c.设置光标闪烁
设置文本样式=c.设置文本样式
设置滚动区域=c.设置滚动区域
设置窗口标题=c.设置窗口标题
设置备用缓冲区=c.设置备用缓冲区
软重置=c.软重置
打印s=c.打印s


#平台特异的方法
获取用户输入=p.获取用户输入
获取光标位置=p.获取光标位置
密码输入=p.密码输入


def 按任意键继续(提示信息="",提示信息_0="按",提示信息_1="任意",提示信息_2="键",提示信息_3="继续"):
	with 获取用户输入() as h:
		print(提示信息+提示信息_0+提示信息_1+提示信息_2+提示信息_3,end="",flush=True)
		if(h.获取输入()=='\x03'):
			raise KeyboardInterrupt
		print()


def 清除光标后内容():
	x,y=获取屏幕宽高()
	x0,y0=获取光标位置()
	打印(' '*(x-x0+(y-y0)*x))
	设置光标位置(x0,y0)


class 动画:
	def __init__():
		raise

	def 渐退(x,速度=.05):
		for i in range(x):
			打印("\b \b")
			time.sleep(速度)
	
	def 渐退至(x,速度=.05):
		x_,y_=获取光标位置()
		if x_<=x:
			设置光标位置(x,y_)
		else:
			for i in range(x_-x):
				打印("\b \b")
				time.sleep(速度)


	def 渐退至行首(速度=.05):
		动画.渐退至(0,速度)
	
	def 渐打印(文字,速度=.05):
		for i in range(len(文字)):
			打印(文字[i])
			time.sleep(速度)

	



def main():
	设置备用缓冲区(1)
	清屏()
	设置文本样式(1,5,1,1,1,1,1)
	动画.渐打印("Hello, World",0.1)
	设置文本样式()
	打印("\n光标位置:")
	打印(str(获取光标位置()))
	time.sleep(1)
	设置光标位置(0,8)
	按任意键继续()
	打印("\n光标位置:")
	打印(str(获取光标位置()))
	time.sleep(1)
	打印("\n")
	打印s("R",1)
	打印("!")
	打印s("G",2)
	打印("!")
	打印s("B",4)
	打印("!")
	打印("\n")
	打印(密码输入())
	打印("\n")
	raise Exception("这是一个错误")
	按任意键继续(提示信息_3="退出")
	设置备用缓冲区(0)



if __name__=='__main__':
	main()
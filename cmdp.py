import sys

def 打印(内容):
    sys.stdout.write(内容)
    sys.stdout.flush()


'''
https://docs.microsoft.com/zh-cn/windows/console/console-virtual-terminal-sequences
'''


E='\x1b'
E1=E+'['
E2=E+']'

def 设置光标位置(x,y,相对=False):
    '''
    相对:
        False:从左上开始
        True:从当前位置开始
    若 相对 为 False, 则 x,y 为从1开始
    '''
    if 相对:
        if y<0:
            打印(E1+str(-y)+'A')
        elif y>0:
            打印(E1+str(y)+'B')
        if x<0:
            打印(E1+str(-x)+'D')
        elif x>0:
            打印(E1+str(x)+'C')
    else:
        打印(E1+str(y)+';'+str(x)+'H')


def 保存光标位置():
    打印(E1+'s')

def 恢复光标位置():
    打印(E1+'u')



def 设置光标可见(b):
    打印(E1+'?25'+('h' if b else 'l'))

def 设置光标闪烁(b):
    打印(E1+'?12'+('h' if b else 'l'))


def 设置文本样式(前景色=None,背景色=None,亮前景=None,亮背景=None,粗体=None,下划线=None,反色=None):
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
    打印(E1+';'.join(sl)+'m')



def 设置窗口标题(标题):
    打印(E2+'0;'+标题+E+'\x5c')

def 设置备用缓冲区(b):
    打印(E1+'?1049'+('h' if b else 'l'))

def 软重置():
    打印(E1+'!p')




'''

'''

def 打印s(文本,前景色=None,背景色=None,亮前景=None,亮背景=None,粗体=None,下划线=None,反色=None):
    设置文本样式(前景色,背景色,亮前景,亮背景,粗体,下划线,反色)
    打印(文本)
    设置文本样式()

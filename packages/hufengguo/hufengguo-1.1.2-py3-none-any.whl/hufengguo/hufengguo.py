# 作者：中国传媒大学，胡凤国
# 欢迎关注公众号：语和言
# 欢迎选购作者新书：
# 胡凤国，《Python程序设计（基于计算思维和新文科建设）》，
# ISBN：9787121435577，电子工业出版社，2022年6月。



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 加载标准库中的对象
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from os.path import abspath, basename, dirname, exists, expanduser, isabs, isdir, isfile, join, splitext
from os import listdir, makedirs, popen, sep, system, walk
from sys import argv
from importlib.util import find_spec
import sys


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 加载扩展库中的对象
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# from chardet.universaldetector import UniversalDetector
try:
    from chardet.universaldetector import UniversalDetector
except:
    print("扩展库 chardet 没有安装，正在尝试为你安装……")
    try:
        system("pip install chardet")        # 注意：执行系统命令安装扩展库，system可以，但popen报错
    except Exception as e:
        print("扩展库 chardet 没有安装成功，请您手动安装。")
        print(e)
        sys.exit()
    else:
        print("安装成功。")
        from chardet.universaldetector import UniversalDetector



#----------------------------------------------------------------
# 本书配套纸质版图书中的自定义函数
#
# 功能：从1加到n
#----------------------------------------------------------------
def mysum(n):
    return sum(range(1, n+1))



#----------------------------------------------------------------
# 本书配套纸质版图书中的自定义函数
#
# 功能：判定给定的整数n是否质数（素数）
#----------------------------------------------------------------
def isprime(n):
    "判定n是否素数，n的数据类型是整数。"
    flag = False
    if n >= 2:
        k = int(n**0.5) + 1
        for i in range(2, k):
            if n%i == 0:
                break
        else:
            flag = True
    return flag



#----------------------------------------------------------------
# 本书配套纸质版图书中的自定义函数
#
# 函数名：
#     find_files_listdir
#
# 功能：
#     获取目录下所有指定类型的文件（不含子目录）——listdir实现
#
# 参数说明：
#     p           ：要从中查找文件的目录
#     filetypelist：文件扩展名列表，其值可以是如下几种类型
#                   []  ：表示查找所有文件
#                   [""]：表示查找不带扩展名的文件
#                   [".txt"]：表示查找扩展名是*.txt的文件
#                   [".doc", ".docx"]：表示查找所有的WORD文件
#
# 返回值：
#     返回一个字符串列表，列表的每个元素都是一个查找出来的文件名
#
#----------------------------------------------------------------
def find_files_listdir(p, filetypelist = []):
    if not isdir(p):
        return []
    p = abspath(p)
    filetypelist = list(map(lambda x:x.lower(), filetypelist))
    filelist = [join(p,f) for f in listdir(p) \
                if isfile(join(p,f)) and
                   (not filetypelist or
                   splitext(f)[-1].lower() in filetypelist)]
    return filelist



#----------------------------------------------------------------
# 本书配套纸质版图书中的自定义函数
#
# 函数名：
#     find_files_walk
#
# 功能：
#     获取目录下所有指定类型的文件（含子目录）——walk实现
#
# 参数说明：
#     p           ：要从中查找文件的目录
#     filetypelist：文件扩展名列表，其值可以是如下几种类型
#                   []  ：表示查找所有文件
#                   [""]：表示查找不带扩展名的文件
#                   [".txt"]：表示查找扩展名是*.txt的文件
#                   [".doc", ".docx"]：表示查找所有的WORD文件
#
# 返回值：
#     返回一个字符串列表，列表的每个元素都是一个查找出来的文件名
#
#----------------------------------------------------------------
def find_files_walk(p, filetypelist = []):
    if not isdir(p):
        return []
    filetypelist = list(map(lambda x:x.lower(), filetypelist))
    filelist = [join(d, f)
                 for (d, s, fs) in walk(p)
                 for f in fs
                 if filetypelist == [] or splitext(f.lower())[-1] in filetypelist]
    return filelist



#----------------------------------------------------------------
# 本书配套纸质版图书中的自定义函数
#
# 函数名：
#     my_path2path
#
# 功能：
#     目录对目录操作，保持操作结果的相对路径不变
#
# 参数说明：
#     pathin       ：源目录
#     filetypelist ：源目录下的文件扩展名列表
#     pathout      ：目标目录
#     func         ：处理函数，将程序运行结果数据写入目标文件
#     fnoutext     ：目标文件的扩展名，默认值为None表示维持原扩展名不变
#
# 调用说明：
#     调用函数my_path2path()时需传递给它一个具体的处理函数
#     调用示例：
#         pathin       = r"in"       # 源目录
#         filetypelist = [".txt"]    # 查找的文件类型
#         pathout      = r"out"      # 目标目录
#         func         = None        # 处理单个文件的函数，必须要提供
#         outext       = None        # 值为 None 表示文件处理之后扩展名不变
#         my_path2path(pathin, filetypelist, pathout, func, outext)
#
#----------------------------------------------------------------
def my_path2path(pathin, filetypelist, pathout, func=None, fnoutext=None):
    # 检查用户有没有设置自己的文件处理函数
    if func == None:
        print("您需要定义自己的文件处理函数，并将此函数名"
              "作为第4参数来调用函数my_path2path。")
        return

    # 判断目录是否存在
    if not isdir(pathin):
        print(f"目录\n{pathin}\n不存在。")
        return
    pathin = abspath(pathin)

    # 确保目录存在
    pathout = abspath(pathout)
    if not exists(pathout):
        makedirs(pathout)

    # 查找源目录下所有指定类型的文件
    files = find_files_walk(pathin, filetypelist)
    if not files:
        print("源目录\n%s\n下面没有找到符合要求的文件。" % pathin)
        return

    # 循环处理每一个文件
    for fn in files:
        # 得到目标文件名
        newfn = join(pathout, fn[len(pathin):].lstrip(sep))

        # 根据需要决定是否更改目标文件扩展名
        if fnoutext:
            newfn = splitext(newfn)[0] + "."*int("." not in fnoutext) + \
                    fnoutext.strip()

        # 确保目标文件所在的目录存在且文件可写
        newpath = dirname(newfn)
        if not exists(newpath):
            makedirs(newpath)

        # 调用自定义函数处理源文件并把结果保存到目标文件
        func(fn, newfn)



#----------------------------------------------------------------
# 本书电子版图书引入的自定义函数
#
# 函数名：
#     my_read_from_txtfile
#
# 功能：
#     自动猜测文本文件的编码并读取文件内容
#
# 参数说明：
#     fn          ：要读取的文本文件名
#     encoding    ：读取文本文件内容时指定的编码，如指定编码可提高读取速度
#     ignore_error：读取文件时是否忽略读取错误
#
# 调用示例：
#     my_read_from_txtfile(r"test.txt")  # 猜测编码，不忽略错误
#     my_read_from_txtfile(r"test.txt", "gb18030")  # 指定编码，不忽略错误
#     my_read_from_txtfile(r"test.txt", None, True) # 猜测编码，忽略读取错误
#     my_read_from_txtfile(r"test.txt", "utf-8", True) # 指定编码，忽略读取错误
#
#----------------------------------------------------------------
def my_read_from_txtfile(fn, encoding=None, ignore_error=False):
    # 判断文件是否存在
    if not isfile(fn):
        print(f"文件 {fn} 不存在。")
        return None

    # 采用直接指定的编码或探测编码
    if encoding:
        enc = encoding
    else:
        # 探测编码
        detector = UniversalDetector()
        with open(fn, "rb") as fpr:
            for line in fpr:
                detector.feed(line)
                if detector.done:
                    break
        detector.close()
        enc = detector.result["encoding"]
        # 如果探测到的编码gb2312，就需要换成gb18020
        if enc and enc.lower() == "gb2312":
            enc = "gb18030"

    # 读取文件
    action = "指定" if encoding else "猜测"
    try:
        serr = "ignore" if ignore_error else "strict"
        with open(fn, "rt", encoding=enc, errors=serr) as fpr:
            txt = fpr.read()
    except Exception as e:
        s = f"按{action}的编码 {enc} 去读取文件 {fn} 出错，" \
            f"出错信息如下：\n{str(e)}"
        print(s)
        txt = None
    return txt 



#----------------------------------------------------------------
# 本书电子版图书引入的自定义函数
#
# 函数名：
#     my_write_to_txtfile
#
# 功能：
#     建字符串写入文本文件
#
# 参数说明：
#     fnout    ：要写入的文本文件名
#     s        ：要写入的字符串
#     encoding ：文本文件的编码，默认是utf-8-sig
#
# 调用示例：
#     my_write_to_txtfile(r"result.txt", "你好")
#     my_write_to_txtfile(r"result.txt", "你好", "gb18030")
#
#----------------------------------------------------------------
def my_write_to_txtfile(fnout, s, encoding="utf-8-sig"):
    pnout = dirname(fnout)
    if pnout and not exists(pnout):
        makedirs(pnout)
    fpw = open(fnout, "w", encoding=encoding)
    if encoding.lower().startswith("utf-16") and len(encoding)>6:
        fpw.write('\ufeff')
    fpw.write(s)
    fpw.close()



#----------------------------------------------------------------
# 本书电子版图书引入的自定义函数
#
# 函数名：
#     my_abspath
#
# 功能：
#     获取以当前Python程序文件所在路径为基准路径的绝对路径
#
# 参数说明：
#     fp：相对于基准路径的路径名，可以为None
#         如果fp为None，则获取当前Python程序文件所在的绝对路径
#         所谓当前Python程序，是指主动运行而不是被import才运行的Python程序
#
# 调用示例：
#     print(my_abspath())            # 获取当前Python程序文件所在的绝对路径
#     print(my_abspath("."))         # 获取当前Python程序文件所在的绝对路径
#     print(my_abspath(".."))        # 获取当前Python程序文件的父目录的绝对路径
#     print(my_abspath("abc"))       # 获取当前Python程序文件所在目录的abc子目录的绝对路径
#     print(my_abspath("test.txt"))  # 获取当前Python程序文件所在目录下的test.txt的绝对路径
#
#----------------------------------------------------------------
def my_abspath(fp=None):
    if fp and isabs(fp):
        fp = abspath(fp)
    else:
        module_name = splitext(basename(argv[0]))[0]
        script_path = dirname(find_spec(module_name).origin)
        if fp:
            fp = abspath(join(script_path, fp))
        else:
            fp = script_path
    return fp



#----------------------------------------------------------------
# 本书电子版图书引入的自定义函数
#
# 函数名：
#     my_desktop_path
#
# 功能：
#     获取以Windows桌面所在路径为基准路径的绝对路径
#
# 参数说明：
#     fp：相对于基准路径的路径名，可以为None
#         如果fp为None，则获取Windows桌面所在的绝对路径
#
# 调用示例：
#     print(my_desktop_path())            # 获取当前Python程序文件所在的绝对路径
#     print(my_desktop_path("."))         # 获取当前Python程序文件所在的绝对路径
#     print(my_abspath(".."))        # 获取当前Python程序文件的父目录的绝对路径
#     print(my_abspath("abc"))       # 获取当前Python程序文件所在目录的abc子目录的绝对路径
#     print(my_abspath("test.txt"))  # 获取当前Python程序文件所在目录下的test.txt的绝对路径
#
#----------------------------------------------------------------
def my_desktop_path(fp=""):
    return abspath(join(expanduser("~"), "Desktop", fp))






#----------------------------------------------------------------
# 本书电子版图书引入的自定义函数
#
# 函数名：
#     make_dir_exists
#
# 功能：
#     确保一个目录或一个文件所在的目录存在
#
# 参数说明：
#     fp       ：目录名或文件名
#     fileflag ：说明fp表示文件名还是目录名
#
# 调用示例：
#     p = r"e:\123\abc"
#     if make_dir_exists(p):
#         pass
#
#----------------------------------------------------------------
def make_dir_exists(fp, fileflag=False):
    try:
        pn = dirname(fp) if fileflag else fp
        if pn and not exists(pn):
            makedirs(pn)
        flag = True
    except Exception as e:
        print(f"创建目录 {pn} 失败，出错信息如下：", e, sep="\n")
        flag = False
    return flag

# 需要PATH 下存在python， cflow, dot命令(apt install python3, cflow, graphviz)
# 原理：使用cflow生成调用关系，grep剔除无用信息，cut提取函数名，然后生成dot文件，方便绘图

import os

max_depth = 20
rm_dotfile = 1
source, dotfile, svgfile = "blktrace.c", "blktrace.dot", "blktrace.svg"

dotcmd = "cflow -i _ " + source + " | grep -v cflow | grep \< | cut -d'(' -f 1"
svgcmd = 'dot -Tsvg '+ dotfile + ' -o ' + svgfile
start, end = '''digraph G{ 
        rankdir=LR; 
        size="1920,1080"; 
        node [fontsize=16,fontcolor=blue,style=filled,fillcolor=Wheat,shape=box]; 
''', '}'
stack, out = [""] * max_depth, set()

for line in os.popen(dotcmd).readlines():
    space = min(max_depth, line.count(' ') / 4)
    stack[space] = line.strip()
    if space != 0:
        out.add('\t\t"' + stack[space - 1] + '" -> "' + stack[space] + '" ;\n')

with open(dotfile, "w") as f:
    f.write(start)
    for item in out:
        f.write(item)
    f.write(end)

os.system(svgcmd)
if rm_dotfile:
    os.system("rm " + dotfile)


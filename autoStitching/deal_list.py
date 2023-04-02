import os
import re
from tkinter import filedialog as fl

path = fl.askdirectory()
ijmPath = path + '\\stitching.ijm'
ijmBegin = r'run("Grid/Collection stitching","type=[Unknown position] order=[All files in directory] directory=' + path + r' confirm_files output_textfile_name=TileConfiguration.txt fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 computation_parameters=[Save memory (but be slower)] image_output=[Fuse and display] '
res = r'(.*)-(1|2)\.bgData_0001\.tif$'
pathTemp = ''

with open(ijmPath, 'w') as f:
    f.write("")
for curDir, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.tif'):
            print(file)
            goupAll = re.match(res, file)
            if pathTemp == '':  # 为第一个
                pathTemp = goupAll.group(1)
                with open(ijmPath, 'a') as f:
                    f.write(ijmBegin)
            if files.index(file) == len(files) - 2:  # 为最后一个
                with open(ijmPath, 'a') as f:
                    f.write(
                        goupAll.group(0)+' '+'");\nrun("RGB Color");\nsaveAs("Tiff", "' + path + r'/output/' + pathTemp + '.tif");\nclose();\nselectWindow("Fused");\nclose();\n')
                break
            if pathTemp != goupAll.group(1):  # 为下一组，则写入run后面的程序
                with open(ijmPath, 'a') as f:
                    f.write(
                        '\b");\nrun("RGB Color");\nsaveAs("Tiff", "' + path + r'/output/' + pathTemp + '.tif");\nclose();\nselectWindow("Fused");\nclose();\n' + ijmBegin)
            pathTemp = goupAll.group(1)  # 为当前组，则写入run内程序
            with open(ijmPath, 'a') as f:
                f.write(goupAll.group(0)+' ')

- [1. ImageJ_Script](#1-imagej_script)
  - [1.1. 截图](#11-截图)
    - [1.1.1. 手动截图的步骤](#111-手动截图的步骤)
    - [1.1.2. 半自动截图脚本(Crop&Save.ijm)](#112-半自动截图脚本cropsaveijm)
    - [1.1.3. 快捷键快速截图(press_c2AutoCrop.ijm)](#113-快捷键快速截图press_c2autocropijm)
  - [1.2. Scale Bar](#12-scale-bar)
    - [1.2.1. 手动添加Scale Bar](#121-手动添加scale-bar)
    - [1.2.2. 自动添加Scale Bar(ScaleBar.ijm)](#122-自动添加scale-barscalebarijm)
  - [1.3. 图片拼接](#13-图片拼接)
    - [1.3.1. 手动图片拼接](#131-手动图片拼接)
    - [1.3.2. 自动图片拼接(autoStitching)](#132-自动图片拼接autostitching)
# 1. ImageJ_Script
Fiji官网下载地址：https://imagej.net/software/fiji/

Fiji是Fiji is just ImageJ的简写

- 我认为它的优点：
  - 可以录制操作到代码，操作和代码之间的转换非常方便。
  - 可以将脚本绑定快捷键。
  - 以及非常多的插件，但是都需要一定的学习成本。

以下内容包含本人使用到的功能：
- [截图](#11-截图)
- [比例尺](#12-scale-bar)
- [拼图](#13-图片拼接)
## 1.1. 截图
应该可以写自动找最大值or质心截图的程序，但是懒了，因为多模不能这么干。
### 1.1.1. 手动截图的步骤
- 打开图像。拖一个图像到Fiji工具条中。
- 选取截图部分。选中`矩形`，画出想要的区域，如果想要精细调整或指定大小，可以右键圈出的矩形选择`Add to ROI manager`；在ROI manager窗口内右键新加入的选区，选择`Specify...`，在Specify窗口内即可调节矩形区域的宽、高、位置。
- 截取。`Image`→`Crop`。
- 保存。
### 1.1.2. 半自动截图脚本(Crop&Save.ijm)
根据手动截图步骤，以及Recorder给出信息，可以写出以下脚本。
```java
roiManager("Update");//更新区域
run("Crop");//截图
run("Save");//保存
run("Open Next");//打开下一张图
roiManager("Select", 0);//选择区域
```
### 1.1.3. 快捷键快速截图(press_c2AutoCrop.ijm)
绑定快捷键可以将代码添加在StartupMacros的末尾，位于`Plugins`→`Marcos`→`Startup Marcos...`。
```java
macro "myAutoCorp [c]" {
	sizeX = 330; sizeY = 330;//截图像素大小，可自行更改
	getCursorLoc(x, y, z, flags);//获取当前鼠标坐标并赋值到变量，详见https://imagej.net/ij/macros/GetCursorLocDemo.txt
	makeRectangle(x-sizeX/2, y-sizeY/2, sizeX, sizeY);//划区
	run("Crop");//截图
	run("Save");//保存，这个保存可能有一定的问题，仅支持tif，因为tif使用Save可以直接原位替换，而bmp等格式可能需要使用Save As
	run("Open Next");//开启下一个
}
```
## 1.2. Scale Bar
### 1.2.1. 手动添加Scale Bar
- 打开定标图像。将定标图拖到Fiji工具条中。
- 划出定标长度。选中`直线`，划出定标长度。
- 添加全局比例。`Analyze`→`Set Scale...`，在Set Scale窗口中，Distance in pixels为`直线`像素长度；Known distance需填入定标长度；Unit of length为定标长度的单位，一般填入um；勾选Global，即其它图片使用相同比例尺。
- 打开需要添加Scale Bar的图像。
- 添加Scale Bar。`Analyze`→`Tools`→`Scale Bar...`，在Scale Bar窗口中，Width为横向比例尺的长度；Height一般不用，为纵向比例尺的长度；Thickness为比例尺粗细；勾选Horizontal使用横向比例尺，及Hide Text，其它都不勾。Vertical为使用Height的比例尺，横纵比1：1时没必要；标注文本不能选字体，建议PPT自己加，反正也就加一个就行；Overlay一定要取消勾选，如果勾选了，实际图片没改变，只有用Fiji打开图片时才有比例尺。
### 1.2.2. 自动添加Scale Bar(ScaleBar.ijm)
从手动添加Scale Bar中可以总结出添加Scale Bar分为定标和添加两个步骤，其中定标只能手动完成，因为每次定标尺寸不一定一致，当然如果你每次使用相同的显微镜参数那当我没说；添加可以遍历文件夹下的文件，并执行固定语句自动完成。下面给出脚本，实际使用时仅需把文件拖到Fiji工具条中。
```java
dir = getDirectory("Choose a Directory ");
count = 1;
listFiles(dir); //遍历dir文件夹下的所有文件，详见https://imagej.net/ij/macros/ListFilesRecursively.txt

function listFiles(dir) {
	list = getFileList(dir);
	for (i=0; i<list.length; i++) {
		print((count++) + ": " + dir + list[i]);
   		ScaleBar(dir + list[i]);//遍历时顺便添加ScaleBar
}}

function ScaleBar(path) { 
	open(path);//打开图片
	//run("Flip Vertically");//垂直翻转
	//setMinAndMax(0, 208);//Adjust Brightness
	run("Scale Bar...", "width=5 height=4 thickness=20 font=14 color=White background=None location=[Lower Right] horizontal hide");//添加ScaleBar，这句代码建议从Recorder中复制
	//replaceSave(path);//按后缀替换
	run("Save");//保存
	close();
}

function replaceSave(path) {
	if (endsWith(path, ".tiff"))
		saveAs("Tiff", path);
	if (endsWith(path, ".jpg"))
		saveAs("Jpeg", path);
	if (endsWith(path, ".bmp"))
		saveAs("BMP", path);
}
```
## 1.3. 图片拼接
这部分功能我使用的还是比较麻烦，希望大家能找到更好的办法。手动方面操作繁琐；半自动方面Recorder没有代码，可能由于本身操作的地方就是插件，所以没有代码；自动方面可靠度不高。
### 1.3.1. 手动图片拼接
- 建立画布。`File`→`New`→`TrakEM2(blank)`，在TrakEM2窗口中Layers→Top Level[layer set]右键，选择`Resize LayerSet...`，建立一个足够大的画布。
- 拼接图片。将待拼接的图片拖入画布中进行拼接，键盘PageDown、PageUp可以快速调整图片上下层，空格键可以快速切换选中图片透明度为100或50。
- 输出图片。使用ROI manager(`Analyze`→`Tools`→`ROI manager...`)，固定划区域位置。右键划出的区域选择`Export`→`make flat image..`。在Choose窗口中，Type改为RGB，8bit为灰度图片；Export下拉栏选择Save to file；保存图片。
建议：一开始拼好的图片锁定，作为后续拼图的基准，这样所有图基准相同。
### 1.3.2. 自动图片拼接(autoStitching)
主要使用插件：`Plugins`→`Stitching`→`Grid/Collection stitching`，大概就是用python正则匹配命名，然后生成一个.ijm，Fiji运行.ijm进行拼接。
```python
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

```

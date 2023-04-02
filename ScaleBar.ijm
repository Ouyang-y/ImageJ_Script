dir = getDirectory("Choose a Directory ");
count = 1;
listFiles(dir); 

function listFiles(dir) {
	list = getFileList(dir);
	for (i=0; i<list.length; i++) {
		print((count++) + ": " + dir + list[i]);
   		ScaleBar(dir + list[i]);
}}

function ScaleBar(path) { 
	open(path);
	//run("Flip Vertically");
	//setMinAndMax(0, 208);//Adjust Brightness
	run("Scale Bar...", "width=5 height=4 thickness=20 font=14 color=White background=None location=[Lower Right] horizontal hide");
	//replaceSave(path);
	run("Save");
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

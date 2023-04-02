dir = getDirectory("Choose a Directory ");
count = 1;
listFiles(dir); 

function listFiles(dir) {
	list = getFileList(dir);
	for (i=0; i<list.length; i++) {
		print((count++) + ": " + dir + list[i]);
		if (endsWith(list[i], ".bmp"))
   			Crop(dir + list[i]);
}}

function Crop(path) { 
	open(path);
	roiManager("Select", 0);
	run("Crop");
	saveAs("tiff", path);
	close();
}
function treeData = treeLoad(filenum)
    filename = "/home/esl/kyuyong/RRTstar/result/" + num2str(filenum) + "output.xlsx";
    treeData = readtable(filename,'Sheet','Tree Data');
end
function treeData = treeLoad(filenum)
    filename = "/home/esl/kyuyong/RRTstar/result5/" + num2str(filenum) + "output.xlsx";
    treeData = readtable(filename,'Sheet','Tree Data');
end
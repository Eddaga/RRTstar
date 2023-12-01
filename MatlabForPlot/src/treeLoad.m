function treeData = treeLoad(filenum)
    filename = "/home/esl/kyuyong/RRTstar/result4/" + num2str(filenum) + "output.xlsx";
    treeData = readtable(filename,'Sheet','Tree Data');
end
function treeData = treeLoad(filenum)
    filename = "/home/esl/kyuyong/RRTstar/resultNormalRRT/" + num2str(filenum) + "output.xlsx";
    treeData = readtable(filename,'Sheet','Tree Data');
end
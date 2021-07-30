import re #import regex

importFileAdr=["pseudosyringae_proteins.fa","P.boem.v1.proteins.fa"]#files to be searched
FileIdent=["pseudosyringae","boehmeriae"]#name of proteins

patternlist=["R.LR.{0,50}[ED][ED][RK]","A.MY.S.{2}FPKDSPVTGLGHR", "GHRHDWE", "H.GPCE.{3}D{2}", "VWNQPVRGFKV.E","L.LFLAK"]#patterns to search
patternNameList=["RXLR","NLP1","NLP2","HXGPCE","PEP13","CRN"]#pattern names

def FindHeader():
    IndexHArr=[]
    patHead=re.compile(">");patHeadE=re.compile("\n")#.index() was inefficient
    fileMatchObjS=patHead.search(file)

    while fileMatchObjS:#while a pattern match exists
        fileMatchObjE=patHeadE.search(file,fileMatchObjS.start()+1)
        startpos=fileMatchObjS.start();endpos=fileMatchObjE.start()
        IndexHArr.append([startpos,endpos])#append header start/end indexes to array
        fileMatchObjS=patHead.search(file,fileMatchObjS.start()+1)
    return IndexHArr

def spliceSequences(IndexHArr):
    SequencesArr=[]
    for index in range(len(IndexHArr)):
        try:
            SequencesArr.append(file[IndexHArr[index][1]+1:IndexHArr[index+1][0]].replace("\n",""))
        except IndexError:#occurs on last index
            SequencesArr.append(file[IndexHArr[index][1]+1:].replace("\n",""))
    return SequencesArr

def LocatePattern(SequencesArr,locPatIndex):
    isPresentArr=[]
    pat=re.compile(patternlist[locPatIndex])
    for item in SequencesArr:
        isPresentArr.append(bool(pat.search(item)))#append whether match was found       
    return isPresentArr

def OutputData(IndexHArr,SequencesArr,isPresentArr,fIndex,locPatIndex):
    writefile=open("#"+FileIdent[fIndex]+"_"+patternNameList[locPatIndex]+".txt","w")#concatenate filename
    count=0
    for index in range(len(IndexHArr)):
        if isPresentArr[index]:
            count+=1
            writefile.write(file[IndexHArr[index][0]:IndexHArr[index][1]]+"\t\t"+SequencesArr[index]+"\n")#write data to file
    writefile.close()
    return count

def hitsOutput(totals, fIndex):
    totalsFile=open("#"+FileIdent[fIndex]+"_total_hits.txt","w")
    for index in range(len(totals)):
        totalsFile.write(patternNameList[index]+":\t"+str(totals[index])+"\n")
    totalsFile.close()

#main program
for fileIndex in range(len(importFileAdr)):
    totalHits=[]
    fileObj=open(importFileAdr[fileIndex],"r");file=fileObj.read()#open proteins file
    IndexHArr=FindHeader()#call FindHeader subprogram
    SequencesArr=spliceSequences(IndexHArr)#call spliceSequences subprogram
    fileObj.close()
    for patIndex in range(len(patternlist)):#loop through patterns
        isPresentArr=LocatePattern(SequencesArr,patIndex)#call LocatePattern subprogram
        totalHits.append(OutputData(IndexHArr,SequencesArr,isPresentArr,fileIndex,patIndex))#call OutputData subprogram
    hitsOutput(totalHits,fileIndex)
    

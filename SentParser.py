class SentParser():
    ''' [1] tokenize  : sentence                         -> tokens
        [2] cfgReader : .cfg                             -> terminal & non-terminal Dictionary
        [3] ChartInit : N Token                          -> N x N array Chart
        [4] ChartFeed : N x N array & rule dict & tokens -> Fill the Chart
        [5] ChartShow : Print function for chart components
        [6] CellCheck : Result of ChartFeed              -> Print the trees and Flag Setting
        [7] ChartFinal: Using CellCheck and FLAGs        -> Print the trees
    '''
    def __init__(self, sent, CFG_PATH):
        self.sent, self.path, self.FLAG = sent,CFG_PATH,[(0,0,0)]
        self.finals = []


    def tokenize(self):
        from nltk import word_tokenize
        self.tokens = word_tokenize(self.sent)
        self.nToken = len(self.tokens)

    def cfgReader(self):
        NTR, TMR = {}, {}# NTR : Non-terminal rule / TMR : Terminal rule
        with open(self.path, "rt") as cfg:
            while True:
                line = cfg.readline()
                if line == '':
                    break
                else:
                    rule = line[:-1].split()
                    key, values, val_list = rule[0], rule[2:], []
                    nValue = values.count('|')
                    for n in range(nValue+1):
                        if rule[2][0] == '"' or rule[2][0] == "'":
                            val_list.append(values[n*2][1:-1])
                            TMR[key] = val_list
                        else:
                            val_list.append(values[(3*n):(3*n)+2])
                            NTR[key] = val_list
        self.NTR, self.TMR = NTR, TMR


    def ChartInit(self):
        CHART = [[[] for i in range(self.nToken)] for i in range(self.nToken)]
        self.InitChart = CHART

    def ChartFeed(self):
        feed_chart = self.InitChart
        for j in range(self.nToken):
            for i in range(j,-1,-1):
                CELL = []
                if i == j:
                    for k, v in self.TMR.items():
                        if self.tokens[i] in v:
                            CELL.append([k,[i,j],[i,j]])
                    feed_chart[i][j] = CELL
                else:
                    hors, vers = [[i,b] for b in range(j-1, -1, -1)], [[a,j] for a in range(i+1, j+1)]
                    for hor in hors:
                        for ver in vers:
                            cell_hor = feed_chart[hor[0]][hor[1]]
                            cell_ver = feed_chart[ver[0]][ver[1]]
                            if (len(cell_ver) == 0) or (len(cell_hor) == 0):
                                pass
                            else:
                                for hor_element in cell_hor:
                                    for ver_element in cell_ver:
                                        for k, v in self.NTR.items():
                                            if ([hor_element[0],ver_element[0]] in v) and (hor[1]+1 == ver[0]):
                                                CELL.append([k,[hor[0],hor[1]],[ver[0],ver[1]]])
                                            else:
                                                pass
                    if len(CELL) >= 2:
                        if CELL[-1] in CELL[:-1]:
                            CELL.pop()
                    feed_chart[i][j] = CELL
        self.ChartComplete = feed_chart

    def ChartShow(self):
        for i in range(self.nToken):
            for j in range(self.nToken):
                print("{0}\t\t".format(self.ChartComplete[i][j]), end = '')
            print("\n\n", end = '')

    def CellCheck(self, DEPTH, I, J):
        if len(self.ChartComplete[I][J]) == 1:
            target = self.ChartComplete[I][J][-1]
        else:
            self.FLAG.append([DEPTH, I, J])
            target = self.ChartComplete[I][J].pop()
        if target[1] == target[2]:
            print(DEPTH*"\t",end = '')
            self.finals.append(DEPTH*"\t")
            print("{0} {1}".format(target[0],self.tokens[target[1][0]]))
            self.finals.append(target[0])
            self.finals.append(self.tokens[target[1][0]])
        else:
            print(DEPTH*"\t",end = '')
            self.finals.append(DEPTH*"\t")
            print("{0}".format(target[0]))
            self.finals.append(target[0])
            self.CellCheck(DEPTH+1, target[1][0], target[1][1])
            self.CellCheck(DEPTH+1, target[2][0], target[2][1])

    def ChartFinal(self):
        ntree = 0
        while True:
            if len(self.FLAG) == 0:
                print("Parsing Done : {0} trees".format(ntree))
                break
            else:
                ntree += 1
                print("\n< TREE [{0}] >".format(ntree))
                self.FLAG.pop()
                self.CellCheck(0,0,self.nToken-1)

    def ChartShow(self):
        for i in range(self.nToken):
            for j in range(self.nToken):
                print("{0}\t\t".format(self.ChartComplete[i][j]), end = '')
            print("\n\n", end = '')

from data_process import *

class factor:

    def __init__(self, data):
        self.data = data

    def ADTM(self):
        DTM = pd.DataFrame(index=self.data.index,columns=['DTM'])
        DBM = pd.DataFrame(index=self.data.index,columns=['DBM'])

        for row_index, row in self.data.iterrows():
            if row_index == '2013/1/16':
                continue
            if self.data.loc[row_index,'open'] > self.data.shift().loc[row_index,'open']:
                DTM.loc[row_index] = max(self.data.loc[row_index,'high'] - self.data.loc[row_index,'open'] , self.data.loc[row_index,'open'] - self.data.shift().loc[row_index,'open'])
            else:
                DTM.loc[row_index] = 0
            if self.data.loc[row_index,'open'] >= self.data.shift().loc[row_index,'open']:
                DBM.loc[row_index] = 0
            else:
                DBM.loc[row_index] = max(self.data.loc[row_index,'open'] - self.data.loc[row_index,'low'] , self.data.loc[row_index,'open'] - self.data.shift().loc[row_index,'open'])
            
        STM = DTM.rolling(23).sum().dropna()
        SBM = DBM.rolling(23).sum().dropna()
        
        ADTM = pd.DataFrame(index=STM.index,columns=['ADTM'])
        for row_index, row in ADTM.iterrows():
            if STM.loc[row_index,'DTM'] > SBM.loc[row_index,'DBM']:
                ADTM.loc[row_index,'ADTM']=(STM.loc[row_index,'DTM']-SBM.loc[row_index,'DBM'])/STM.loc[row_index,'DTM']
            elif STM.loc[row_index,'DTM'] < SBM.loc[row_index,'DBM']:
                ADTM.loc[row_index,'ADTM']=(STM.loc[row_index,'DTM']-SBM.loc[row_index,'DBM'])/SBM.loc[row_index,'DBM']
            else:
                ADTM.loc[row_index,'ADTM'] = 0

        return ADTM
            
    
    def ATR(self):
        TR = pd.DataFrame(index=self.data.index,columns=['TR'])
        
        for row_index, row in self.data.iterrows():
            if row_index == '2013/1/16':
                continue
            
            TR.loc[row_index] = max(abs(self.data.loc[row_index,'high']-self.data.loc[row_index,'low']), abs(self.data.loc[row_index,'high']-self.data.shift().loc[row_index,'close']), abs(self.data.loc[row_index,'low']-self.data.shift().loc[row_index,'close']))
            
        ATR = TR.rolling(14).mean()
        ATR.dropna(inplace = True)

        return ATR
    
    def CCI(self, n):
        TP = pd.DataFrame(index=self.data.index,columns=['TP'])
        MD = pd.DataFrame(index=self.data.index,columns=['MD'])
        
        for row_index, row in self.data.iterrows():
            if row_index == '2013/1/16':
                continue
            
            TP.loc[row_index] = (self.data.loc[row_index,'high']+self.data.loc[row_index,'low']+self.data.loc[row_index,'close'])/3
            
        MA = TP.rolling(n).mean()
        MA.dropna(inplace=True)
        
        for row_index, row in MA.iterrows():
            MD.loc[row_index] = abs(MA.loc[row_index,'TP']-TP.loc[row_index,'TP'])
            
        MD1 = MD.rolling(n).mean()
        MD1.dropna(inplace=True)
        CCI = pd.DataFrame(index=MD1.index,columns=['CCI'])
        
        for row_index, row in MD1.iterrows():
            CCI.loc[row_index] = (TP.loc[row_index,'TP']-MA.loc[row_index,'TP'])/(0.015*MD1.loc[row_index,'MD'])
        
        return CCI
            
    def MACD(self):
        EMA_12 = pd.DataFrame(index=self.data.index,columns=['EMA'])
        EMA_26 = pd.DataFrame(index=self.data.index,columns=['EMA'])
        DEA = pd.DataFrame(index=self.data.index,columns=['EMA'])
        
        EMA_12.loc['2013/1/17','EMA'] = self.data.loc['2013/1/16','close']*11/13+self.data.loc['2013/1/17','close']*2/13
        EMA_26.loc['2013/1/17','EMA'] = self.data.loc['2013/1/16','close']*25/27+self.data.loc['2013/1/17','close']*2/27
        
        for row_index, row in self.data.iterrows():
            if row_index == '2013/1/16' or row_index == '2013/1/17':
                continue
            
            EMA_12.loc[row_index] = EMA_12.shift().loc[row_index]*11/13+self.data.loc[row_index,'close']*2/13
            EMA_26.loc[row_index] = EMA_26.shift().loc[row_index]*25/27+self.data.loc[row_index,'close']*2/27
            
        EMA_12.dropna(inplace = True)
        EMA_26.dropna(inplace = True)

        DIFF = EMA_12-EMA_26
        
        DEA.loc['2013/1/17','EMA'] = self.data.loc['2013/1/16','close']*8/10+DIFF.loc['2013/1/17','EMA']*2/10
        for row_index, row in data.iterrows():
            if row_index == '2013/1/16' or row_index == '2013/1/17':
                continue
            DEA.loc[row_index] = DEA.shift().loc[row_index]*8/10+DIFF.loc[row_index]*2/10
        
        MACD = (DIFF - DEA)*2
        MACD.columns = ['MACD']
        MACD.dropna(inplace = True)

        return MACD

    def MTM(self, n):
        MTM = pd.DataFrame(self.data.loc[:,'close']-self.data.shift(n).loc[:,'close'])
        MTM.columns = ['MTM']
        MTM.dropna(inplace = True)

        return MTM
    
    def ROC(self, n):
        ROC = pd.DataFrame(self.data.loc[:,'close']-self.data.shift(n).loc[:,'close'])/pd.DataFrame(self.data.shift(n).loc[:,'close'])
        ROC.dropna(inplace = True)
        return ROC
        

    def SOBV(self):
        SOBV = pd.DataFrame(index=self.data.index,columns=['SOBV'])
        
        for row_index, row in self.data.iterrows():
            if row_index == '2013/1/4':
                SOBV.loc[row_index] = self.data.loc[row_index, 'volumn']
                continue
            
            if self.data.loc[row_index, 'open'] > self.data.loc[row_index, 'close']:
                SOBV.loc[row_index] = self.data.loc[row_index, 'volumn'] - SOBV.shift().loc[row_index]
                
            elif self.data.loc[row_index, 'open'] < self.data.loc[row_index, 'close']:
                SOBV.loc[row_index] = self.data.loc[row_index, 'volumn'] + SOBV.shift().loc[row_index]
                
            else:
                SOBV.loc[row_index] = SOBV.shift().loc[row_index]
                
        SOBV.dropna(inplace = True)

        return SOBV
    
    def STD(self):
        STD26 = self.data.loc[:,'close'].rolling(26).std()
        STD5 = self.data.loc[:,'close'].rolling(5).std()
        
        STD26.dropna(inplace = True)
        STD5.dropna(inplace = True)

        return STD26, STD5

    def week_return_rate(self):
        weekly_rr = pd.DataFrame((self.data.loc[:,'close']-self.data.shift().loc[:,'close'])/self.data.shift().loc[:,'close'])
        weekly_rr.columns = ['weekly_rr']
        weekly_rr.dropna(inplace = True)

        return weekly_rr

    def get_all_factors(self):
        
        ADTM = self.ADTM()
        ATR = self.ATR()
        CCI = self.CCI()
        MACD = self.MACD()
        MTM = self.MTM()
        ROC = self.ROC()
        SOBV = self.SOBV()
        week_return_rate = self.week_return_rate()
        STD26, STD5 = self.STD()
        factor = pd.concat([ADTM, ATR, CCI, MACD, MTM, ROC, SOBV, week_return_rate, STD26, STD5], join = 'inner', axis = 1)
        factor.dropna(inplace = True)
        factor_ = self.ind_standardize(factor)
        # drop the first trading year,and shift the indicator to next index:just for prediction
        return factor_
from data_process import *

class factor:

    def __init__(self, data):
        self.data = data
        self.time = pd.to_datetime('2013/1/4', format="%Y/%m/%d")

    def ADTM(self):
        DTM = pd.DataFrame(index=self.data.index,columns=['DTM'])
        DBM = pd.DataFrame(index=self.data.index,columns=['DBM'])

        for row_index, row in self.data.iterrows():
            if row_index == self.time:
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
            if row_index == self.time:
                continue
            
            TR.loc[row_index] = max(abs(self.data.loc[row_index,'high']-self.data.loc[row_index,'low']), abs(self.data.loc[row_index,'high']-self.data.shift().loc[row_index,'close']), abs(self.data.loc[row_index,'low']-self.data.shift().loc[row_index,'close']))
            
        ATR = TR.rolling(14).mean()
        ATR.dropna(inplace = True)

        return ATR
    
    def CCI(self, n):
        TP = pd.DataFrame(index=self.data.index,columns=['TP'])
        MD = pd.DataFrame(index=self.data.index,columns=['MD'])
        
        for row_index, row in self.data.iterrows():
            if row_index == self.time:
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
            CCI.loc[row_index, 'CCI'] = (TP.loc[row_index,'TP']-MA.loc[row_index,'TP'])/(0.015*MD1.loc[row_index,'MD'])
        
        return CCI
            
    def MACD(self):
        EMA_12 = pd.DataFrame(index=self.data.index,columns=['EMA'])
        EMA_26 = pd.DataFrame(index=self.data.index,columns=['EMA'])
        DEA = pd.DataFrame(index=self.data.index,columns=['EMA'])
        
        time1 = pd.to_datetime('2013/1/4', format="%Y/%m/%d")
        time2 = pd.to_datetime('2013/1/11', format="%Y/%m/%d")
        EMA_12.loc[time2,'EMA'] = self.data.loc[time1,'close']*11/13+self.data.loc[time2,'close']*2/13
        EMA_26.loc[time2,'EMA'] = self.data.loc[time1,'close']*25/27+self.data.loc[time2,'close']*2/27
        
        for row_index, row in self.data.iterrows():
            if row_index == time1 or row_index == time2:
                continue
            
            EMA_12.loc[row_index] = EMA_12.shift().loc[row_index]*11/13+self.data.loc[row_index,'close']*2/13
            EMA_26.loc[row_index] = EMA_26.shift().loc[row_index]*25/27+self.data.loc[row_index,'close']*2/27
            
        EMA_12.dropna(inplace = True)
        EMA_26.dropna(inplace = True)

        DIFF = EMA_12-EMA_26
        
        DEA.loc[time2,'EMA'] = self.data.loc[time1,'close']*8/10+DIFF.loc[time2,'EMA']*2/10
        for row_index, row in data.iterrows():
            if row_index == time1 or row_index == time2:
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
        ROC.columns = ['ROC']
        ROC.dropna(inplace = True)
        return ROC
        

    def SOBV(self):
        SOBV = pd.DataFrame(index=self.data.index,columns=['SOBV'])
        
        for row_index, row in self.data.iterrows():
            if row_index == self.time:
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
        STD26 = pd.DataFrame(self.data.loc[:,'close'].rolling(26).std())
        STD5 = pd.DataFrame(self.data.loc[:,'close'].rolling(5).std())
        
        STD26.columns = ['STD26']
        STD5.columns = ['STD5']
        
        STD26.dropna(inplace = True)
        STD5.dropna(inplace = True)

        return STD26, STD5

    def week_return_rate(self):
        weekly_rr = pd.DataFrame((self.data.loc[:,'close']-self.data.shift().loc[:,'close'])/self.data.shift().loc[:,'close'])
        weekly_rr.columns = ['weekly_rr']
        weekly_rr.dropna(inplace = True)

        return weekly_rr
    
    def goal(self):
        time1 = pd.to_datetime('2023/3/10', format="%Y/%m/%d")
        time2 = pd.to_datetime('2023/3/17', format="%Y/%m/%d")
        goal = pd.DataFrame(self.get_all_factors().loc[:,'weekly_rr'])
        
        for row_index, row in goal.iterrows():
            if row_index == time1 or row_index == time2:
                break
            
            if goal.shift(-2).loc[row_index, 'weekly_rr'] > 0:
                goal.loc[row_index] = 1
            else:
                goal.loc[row_index] = 0
        
        return goal

    def get_all_factors(self):
        
        ADTM = self.ADTM()
        ATR = self.ATR()
        CCI = self.CCI(4)
        MACD = self.MACD()
        MTM = self.MTM(4)
        ROC = self.ROC(4)
        SOBV = self.SOBV()
        week_return_rate = self.week_return_rate()
        STD26, STD5 = self.STD()
        # factor = pd.concat([ADTM, ATR, CCI, MACD, MTM, ROC, SOBV, week_return_rate, STD26, STD5], join = 'inner', axis = 1)
        factor = pd.concat([ADTM, ATR, CCI, MACD, MTM, ROC, week_return_rate, STD26, STD5], join = 'inner', axis = 1)
        factor.dropna(inplace = True)
        # factor_ = self.ind_standardize(factor)
        # drop the first trading year,and shift the indicator to next index:just for prediction
        return factor

# factor = factor(data)
# x = factor.get_all_factors()
# x.drop(x.tail(2).index,inplace=True) 
# x = x.apply(lambda x:(x-np.min(x))/(np.max(x)-np.min(x)))
# y = factor.goal()
# y.drop(y.tail(2).index,inplace=True) 
# clf_linear = svm.SVC(kernel='rbf', C=5.0, gamma=20)   # kernel = 'linear'
# y = y.T.iloc[0,:]
# clf_linear.fit(x,y)
# score_linear = clf_linear.score(x,y)
# y_pred = clf_linear.predict(x)
# print(score_linear)
# print(y_pred)
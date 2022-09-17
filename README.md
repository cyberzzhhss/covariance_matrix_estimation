*Covariance Matrix Estimation
**Authors**:  Zhehan Shi, Shubo Xu, Xiaobin Ou

Please arrange the files according to the file directory below

### Step 1 Prepare returns matrix

```
Run the PrepareReturnsMatrix.py
python3 PrepareReturnsMatrix.py

It will output the test_returns.txt from trades folder
Rename the file {test_returns.txt} to {returns.txt}
Since this step is time consuming, 
we decided to include the file returns.txt in our folder
```

### Step 2 Prepare SP500 daily returns from [SP500 Kaggle Dataset](https://www.kaggle.com/datasets/camnugent/sandp500)

```
Run the KaggleDataETL.py
python3 KaggleDataETL.py

It will output the test_daily_returns.txt from the kaggle dataset. 
It might be a hassle to download the dataset; therefore, we decided to include kaggle csv file all_stocks_5yr.csv.
Rename the file {test_daily_returns.txt} to {daily_returns.txt}.
Since this step is slightly time consuming, 
we decided to include the file returns.txt in our folder
```

### Step 3 Run the Risk Analysis

```
In order to better visualize the results.
You can open the RiskAnalysis_Runner.ipynb to follow the output step by step
The plots will be plotted accordingly
Since the exponential weighting covariance estimator is time consuming.
We decided to include the output in the RiskAnalysis_Runner_Output.pdf               
```

### Others

We also include the output of the unit tests in **Tests_Runner_Output.pdf** in case you find running the unit tests time consuming.

### Directory Structure

```
Folder
├─ code                                                          
│  ├─ dbReaders                                         
│  │  ├─ FileNames.py                              
│  │  ├─ TAQQuotesReader.py                        
│  │  └─ TAQTradesReader.py                        
│  ├─ helperCode                                            
│  │  ├─ pyRMT.py                                  
│  │  └─ rie_estimator.py                          
│  ├─ impactModel                                                   
│  │  ├─ FileManager.py                            
│  │  ├─ FirstPriceBuckets.py                      
│  │  ├─ LastPriceBuckets.py                       
│  │  ├─ TickTest.py                               
│  │  └─ VWAP.py                                   
│  ├─ KaggleDataETL.py                             
│  ├─ PrepareReturnsMatrix.py                      
│  ├─ ReturnBuckets.py                             
│  ├─ RiskAnalysis.py                              
│  ├─ RiskAnalysis_Runner.ipynb                    
│  ├─ RiskAnalysis_Runner_Output.pdf               
│  ├─ Test_KaggleDataETL.py                        
│  ├─ Test_PrepareReturnsMatrix.py                 
│  ├─ Test_RiskAnalysis.py                         
│  ├─ Tests_Runner.ipynb                           
│  ├─ Tests_Runner_Output.pdf                      
│  ├─ all_stocks_5yr.csv                           
│  ├─ daily_returns.txt                            
│  ├─ returns.txt                                  
│  ├─ validDays.txt                                
│  └─ validTickers.txt   
├─ trades                                                          
│  ├─ 20070620   
│  │  ├─ A_trades.binRT  
│  │  ├─ ...
│  │  └─ ZZ_trades.binRT   
│  ├─ 20070621                                
│  └─ 20070920  
├─ quotes    
│  ├─ 20070620   
│  │  ├─ A_quotes.binRQ  
│  │  ├─ ...
│  │  └─ ZZ_quotes.binRQ
│  ├─ 20070621                                
│  └─ 20070920
└─ README.md                                       
```
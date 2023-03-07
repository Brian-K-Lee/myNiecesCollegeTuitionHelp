######################################
##My 2 Year-Old Niece's Tuition Help##
######################################
# This program calculates the future value of an ordinary annuity based on monthly  monthly interest rate, and number of months.
# It also compares different payment amounts and their contribution to annual tuition (national in-state average).
# It uses pandas and locale libraries.

### Load Libraries
import pandas as pd
import locale

### Set the Local to The United States
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

### Create a Future Value of An Ordinary Annuity Function
def future_value_of_annuity(P,i,n):
    # P is the monthyly payment
    # i is the monthly interest rate
    # n is the number of months
    FVA = round(P * ((((1+i)**n)-1)/i),0)
    return FVA

### Create a Data Frame
df = pd.DataFrame({'Amount':[50,100,150,200,250,300,400,500]})

### Run "future_value_of_annuity" with Average Annual Fed Fund Rates for 192 months (16 year)
# Federal Funds Effective Rate from 2007 - 2022 (16 years) From FRED Economic Data
# https://fred.stlouisfed.org/series/FEDFUNDS#
# Exported as 'FEDFUNDS.csv'
# Open 'FEDFUNDS.csv' and Get the Mean of monthly Fedral Funds Rates
fedFundRate = pd.read_csv('C:/Users/KT/Documents/Python/ForFun/myNiecesColleageTuition/FEDFUNDS.csv')
yearlyRate =  fedFundRate['FEDFUNDS'].mean()
yearlyRate/12

### Cross-Check with Free-Online-Calculator-Use
# https://www.free-online-calculator-use.com/future-value-annuity-calculator.html
# Monthly Saving of $50 Returned $10,373
# Let's Check
if 10373==future_value_of_annuity(df.Amount[0],yearlyRate/12/100,16*12):  
    # Add Sum of Period Payment (without Interest) Column to "df" For Comparison
    df['futureValueofAnnuity'] = future_value_of_annuity(df.Amount, yearlyRate/12/100, 16*12)
    print("Your Future Value of Annuity Calculation Is Right! Added To The 'df' Data Frame.") 

# Add Sum of Period Payment (without Interest) Column to "df" For Comparison
df['sumofPayments'] = df.Amount*12*16
#df.drop('sumofPayments',axis=1,inplace=True)

# Swap 'futureValueofAnnuity' and 'sumofPayments' for Better Readability
df = df[['Amount','sumofPayments','futureValueofAnnuity']]

# Variance Test Between Present Value Annuity vs. Total Sum of Monthly Payments Without Interest Rate
df['Variance'] = round((df.futureValueofAnnuity-df.sumofPayments)/df.sumofPayments,2)*100
df.Variance = df.Variance.astype(str) + '%'

### Let's See How Much % Each Payment Can Contribute to Annual Tution (National In-State Average)
# Import Annual Average In-State Tution From Business Insider
# https://www.businessinsider.com/personal-finance/average-college-tuition
avgTuition = pd.read_excel('C:/Users/KT/Documents/Python/ForFun/myNiecesColleageTuition/AnnualAverageInStateTuition.xlsx')
# Retrieve 2021-2022 Annual In-State Tution Per US State
avgTuition.iloc[:,2]
# Get National Average In-Station Tuition
avgTuition.dtypes
avgTuition.iloc[:,2] = avgTuition.iloc[:,2].str.replace(',','').str.replace('$','').astype(float)
natAvgTuition = round(avgTuition.iloc[:,2].mean(),0)
natAvgTuition = natAvgTuition.astype(int)
print('Annual average in-state tuition at public colleages and universities in 2021-22 was',
       locale.currency(natAvgTuition))

### Get the Future Value of Annual Average National Tuition
# Create a Future Value Function
def future_value(PV, i, n):
    # PV is the present value
    # i is the yearly inflation rate
    # n is the number of years
    FV = round(PV*(1+i)**n,0)
    return FV

### Run "future_value" with Average Annual Fed Fund Rates for 16 years
# Add to 'df' Data Frame
df['futureAnnualTuition'] = future_value(natAvgTuition, yearlyRate/100, 16)

### Compare To The Future Value of an Ordinary Annuity
df['yearCoverage'] = round(df.futureValueofAnnuity/df.futureAnnualTuition,2)
df.yearCoverage = df.yearCoverage.astype(str) + ' Years'

### Change 'Amount' to The Currency Format
df.Amount = df.Amount.apply(lambda x: locale.currency(x))
# Change 'sumofPayments', 'futureValueofAnnuity','futureAnnualTuition' to Currency Format
print(df.columns)
df[['sumofPayments', 'futureValueofAnnuity','futureAnnualTuition']] = df[['sumofPayments', 'futureValueofAnnuity','futureAnnualTuition']].applymap(lambda x: locale.currency(x, grouping=True))

### Print The Minimum Monthly Saving Amounts that Could Cover 4+ Years
print("The Minimum Monthly Saving That Can Cover 4 Years of Colleage Tuition Is",
      df.loc[df.yearCoverage.str.replace(' Years','').astype(float)>4,['Amount']].head(1).iloc[0].to_string(index=False,header=False),
      "Which Covers",
      df.loc[df.yearCoverage.str.replace(' Years','').astype(float)>4,['yearCoverage']].head(1).iloc[0].to_string(index=False,header=False))
#print(df.iloc[:, [0,5]][df.yearCoverage.str.replace(' Years','').astype(float)>4])
# Print The Minimum Monthly Saving Amounts that Could Cover 2+ Years
print("The Minimum Monthly Saving That Can Cover 2 Years of Colleage Tuition Is",
      df.loc[df.yearCoverage.str.replace(' Years','').astype(float)>2,['Amount']].head(1).iloc[0].to_string(index=False,header=False),
      "Which Covers",
      df.loc[df.yearCoverage.str.replace(' Years','').astype(float)>2,['yearCoverage']].head(1).iloc[0].to_string(index=False,header=False))

###Export 'df' Data Frame
df.to_csv("C:/Users/KT/Documents/Python/ForFun/myNiecesColleageTuition/myNiecesTutionHelp.csv",index=False)
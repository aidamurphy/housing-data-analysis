
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


Annual = pd.read_excel('gdplev.xls', skiprows=8, header=None, usecols=[0,1,2], names=['Year','GDP','GDP_Chained'])
Annual.dropna(inplace=True)
Annual['Year'] = Annual['Year'].astype('int32')
Quarterly = pd.read_excel('gdplev.xls', skiprows=8, header=None, usecols=[4,5,6], names=['Quarter','GDP','GDP_Chained'])
Quarterly['Quarterly_Recession_Indicator']='None'
Quarterly['Year'] = Quarterly['Quarter'].str.slice(stop=4).astype(int)
Quarter=Quarterly['Quarter']
Quarterly_GDP=Quarterly['GDP_Chained']
Quarterly_RI=Quarterly['Quarterly_Recession_Indicator']
index=int(0)
bottom_index = int(0)
In_Recession = False
Recession_Bottom = 999999
for i, j, k in zip(Quarterly_GDP, Quarterly_GDP[1:], Quarterly_GDP[2:]):
    index=index+int(1)
    if (not In_Recession):
        if (j<i) & (k<j):
            Quarterly_RI[index] = 'START'
            In_Recession = True
    elif (j < Recession_Bottom):
        Recession_Bottom = j
        bottom_index = index
    elif ((i<j) & (j < k)):
            Quarterly_RI[index +int(1)] = 'END'
            Quarterly_RI[bottom_index] = 'BOTTOM'
            Recession_Bottom = 999999
            In_Recession = False
        
Quarterly_Filtered = Quarterly[Quarterly['Year']>= 2000]


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    df = pd.read_table('university_towns.txt', header=None, names=['raw_text'])
    df['State'] = df['raw_text'].str.replace('\[.*$','').where(df['raw_text'].str.contains('[edit]', regex=False))
    df['RegionName'] = df['raw_text'].str.replace(' \(.*$','')
    df['NAN'] = 'NAN'
    df=df.replace('NAN', np.nan)
    mask = df['RegionName'].str.contains('[edit]', regex=False)
    df.loc[mask, 'RegionName'] = df['NAN']
    df['State'] = df['State'].fillna(method='ffill')
    df.dropna(subset=['RegionName'], inplace=True)
    df = df[['State', 'RegionName']]
    return df
get_list_of_university_towns()


# In[4]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    Recession = Quarterly_Filtered[(Quarterly_Filtered['Quarterly_Recession_Indicator']=='START')]
    index = Recession['Year'].idxmax()
    Recession_Quarter = Recession['Quarter']
    return Recession_Quarter[index]
get_recession_start()


# In[5]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    Recession = Quarterly_Filtered[(Quarterly_Filtered['Quarterly_Recession_Indicator']=='END')]
    index = Recession['Year'].idxmax()
    Recession_Quarter = Recession['Quarter']
    return Recession_Quarter[index]
get_recession_end()


# In[6]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    Recession = Quarterly_Filtered[(Quarterly_Filtered['Quarterly_Recession_Indicator']=='BOTTOM')]
    index = Recession['Year'].idxmax()
    Recession_Quarter = Recession['Quarter']
    return Recession_Quarter[index]
get_recession_bottom()


# In[8]:


def get_month(q):
    '''
    Returns a series listing the months in quarter q
    '''
    return {
        1: ['01', '02', '03'],
        2: ['04', '05', '06'],
        3: ['07', '08', '09'],
        4: ['10', '11', '12']
    } [q]

def add_mean_column(df, quarter, year):
    '''
    Adds to df a column named yyyyqn where yyyy is the year and n is the quarter. 
    The new columns is the mean of the three months making up the quarter.
    '''
    label = str(year) + 'q' + str(quarter)
    months = get_month(quarter)
    month1 = str(year) + '-' + months[0]
    month2 = str(year) + '-' + months[1]
    month3 = str(year) + '-' + months[2]
    if (year==2016 and quarter==3):
        data=df[[month1, month2]]
    else:
        data = df[[month1, month2, month3]]
    df[label] = np.mean(data, axis=1)
    return df


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    Housing_Data = pd.read_table('City_Zhvi_AllHomes.csv', header=0, delimiter=',')
    #need to drop un-needed columns and convert months into quarters - use group-by
    Housing_Data['State']=Housing_Data['State'].map(states)
    Housing_Data = Housing_Data.set_index(['State', 'RegionName'])
    end_quarter=3
    end_year=2016
    quarter=1
    year=2000
    quarter_labels=[]
    while True:
        Housing_Data = add_mean_column(Housing_Data,quarter,year)
        quarter_labels.append(str(year) + 'q' + str(quarter))
        if((year==end_year) and (quarter == end_quarter)):
            break
        if quarter < 4: 
            quarter = quarter + 1
        else:
            year = year + 1
            quarter = 1
    Housing_Data = Housing_Data[quarter_labels]
    return(Housing_Data)

convert_housing_data_to_quarters()


# In[26]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    #Create Mean_Price_Ratio = Price at Start / Price at Bottom 
    Housing_Data = convert_housing_data_to_quarters()
    Housing_Data['price_ratio'] = Housing_Data[get_recession_start()]/Housing_Data[get_recession_bottom()]
    #Create two sets of housing data.  One for university towns, and another for non-university towns
    University_Towns = get_list_of_university_towns()
    University_Towns_List = University_Towns.to_records(index=False).tolist()
    University_Housing = Housing_Data.loc[Housing_Data.index.isin(University_Towns_List)]
    Non_University_Housing = Housing_Data.loc[~Housing_Data.index.isin(University_Towns_List)]
    #Determine which is better (has a lower mean price ratio):  University or Not_University
    if (University_Housing['price_ratio'].mean() < Non_University_Housing['price_ratio'].mean()):
        better = 'university town'
    else:
        better = 'non-university town'
    #Run the t-test.
    from scipy import stats
    p=stats.ttest_ind(University_Housing['price_ratio'], Non_University_Housing['price_ratio'], nan_policy='omit')[1]
    if (p<0.01):
        different=True 
    else:
        different=False
    return (different, p, better)

run_ttest()


# In[ ]:





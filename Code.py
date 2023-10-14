#Importing all the required packages
import pandas as pd
import scipy.stats as stat
import math
import numpy as np
from datetime import datetime
# Reading the CSV file
#df = pd.read_csv("Test_1.csv")
#df.event_date = pd.to_datetime(df.event_date) #Conversion of dates to datetime values

# Extracting Important values (not used anywhere in the current version)
#pages = df.grouped_page_name.unique() #Unique page names
#countries = df.country_name.unique()  #Unique country names
#devices = df.Device.unique()          #Unique Device names
#cookies = df.cookies.unique()         #Unique cookie names
#min_date = df.event_date.min()        #Getting the earliest date in the dataset
#max_date = df.event_date.max()        #Getting the oldest date in the dataset

# Initializing filter variables {Entered by the user} (used for the filter_data() function)
#MDE = 0.01                           # Minimum Detectable effect
#start = pd.to_datetime("2021-08-26") # The earliest date the user wants (should be less than max_date)
#end = pd.to_datetime("2021-08-29")   # The oldest date the user wants (should be more than min_date)
#days = (end - start).days            # The no days between start and end
#ramp = pd.to_datetime("2021-09-01")  # The day when the treatment will be fully activated
#lift = 0.01                          # The amount of increse in conversion rates that the user expects 
#Metric = "Raw Prospector"            # The Metric with respect to which all the calculations are performed (The selected Metric/The Denominator Metric)
#pagename = 'PayPal Home Page'        # The page selected for calculation
#country = "US"                       # The country selected for the calculations
#device = ['Mobile','OTHERS','Desktop'] # The device selected for the calculations
#ookie = 0                           # The cookie selected for calculations

# The various metrics that can be selected
#Metrics = ["Visitor","Raw Prospector","Qualified Prospector","Signup Start","Signup Complete"]
#m = Metrics.index(Metric) # The index of the selected Metric (The denominator Metric)

def get_sample_size(mde, baseline_val,alpha = 0.05, beta = 0.2,relative=True):
    """
    Calculates the MSS of an experiment given the significance level, beta which determines power of test,
    minimum detectable effect, baseline conversion rate and whether change is relative or absolute.
    
    Parameters:
    alpha(percentage): level of significance
    beta (percentage): statistical power is 1-beta
    mde: minimum detectable effect
    baseline_val: conversion rate of the control group

    Output:
    The number of days needed to conduct the test, given the input parameters.
    """
    # https://stats.stackexchange.com/questions/392979/ab-test-sample-size-calculation-by-hand
    conf = alpha/2 # for two-tailed test, we need to split alpha by 2, for either side
    z_a = stat.norm.ppf(conf) # z-score of alpha/2
    z_b = stat.norm.ppf(beta) # z-score of beta
    p1 = baseline_val
    if relative:
        p2 = p1 + p1*mde
    else:
        p2 = p1 + mde
    
    num = z_a*math.sqrt(2*p1*(1-p1)) + z_b*math.sqrt(p1*(1-p1) + p2*(1-p2))
    num = num**2
    den = (p2-p1)**2
    
    return num//den

# This function filters the data from the CSV according to the filter values
# Inputs:
# df : The dataframe read from the CSV file
# start_date, end_date, country, pagenames, device_type, cookies : The different parameters we want to filter out

#Output:
# A Dataframe that only contains the data within the constraints provided by the user

def filter_data(df, start_date, end_date, country, pagenames, device_type, cookies):
    filtered_df = df[(df['event_date']>= start_date) & (df['event_date']<= end_date) \
                & (df['country_name'] == country) & (df['grouped_page_name'] == pagenames) \
                & (df['Device'].isin(device_type)) & (df['cookies'] == cookies) ] 
    return filtered_df

# Testing the filter_data function
#fl = filter_data(df, start, end, country, pagename, device, cookie)
#fl.head(5)

# This function counts all the KPI values and selects the KPI values based on the funnel type selected
# Inputs
# filtered_df: The dataframe that has already been filtered
# funnel_type : The funnel type we want, options: "overall", "merchant", "consumer"

#Output:
# A pivoted DataFrame that counts the values of the Selected KPI's we want
def pivot_data(filtered_df,funnel_type = "overall"):
    # We first count all the KPI values after grouping by KPI
    pivoted = filtered_df.groupby(['KPI']).sum().drop(labels = 'cookies',axis = 1).transpose()
    if funnel_type == 'overall': # overall funnel ignores merchant and consumer KPIs
        pivoted = pivoted[['#_Visitors','#_Raw_Prospects','#_QLFD_Prospects','#_Signup_Start','#_Signup_Complete','#_Active_7_Days']]
    elif funnel_type == 'merchant': # merchant funnel only selects merchant KPIs
        pivoted = pivoted[['#_Visitors','#_Raw_Prospects','#_QLFD_Prospects','#_Merchant_Signup_Start','#_Merchant_Signup_Complete','#_Merchant_Active_7_Days']]
    elif funnel_type == 'consumer': # consumer funnel only selects consumer KPIs
        pivoted = pivoted[['#_Visitors','#_Raw_Prospects','#_QLFD_Prospects','#_Consumer_Signup_Start','#_Consumer_Signup_Complete','#_Consumer_Active_7_Days']]
    return pivoted   
    
# Testing the pivot_data function
#pt = pivot_data(fl,'overall')
#pt

# This function gives us the calculted conversion rate with respect to the selected Metic (The denominator Metric)
# Inputs
# pivoted_df : The Dataframe containing the counts of different KPIs
# m : The index of selected Metric

#Output:
# A Dataframe that calculates the conversion rate with respect to the selected Metric

def conversions_data(pivoted_df,m):
    # The list that contains the names of various Mterics in a short form
    Met = ['Visitors', 'RP', 'QP', 'SS', 'SC', 'Activations']
    conversions = pd.DataFrame() # We create an empty DataFrame
    for i in range(m,5): # We start from selected Metric to the the end of the pivoted DataFrame
        # the conversion rate is calculated as percentage of the smaller KPI from the selected KPI (The selected Metic/The denominator Metric)
        conversions[Met[i+1]+'/'+Met[m]] = pd.Series(round(pivoted_df.iloc[0,i+1] * 100 / pivoted_df.iloc[0,m],2))
    return conversions
    
# Testing the conversions_data function
#con = conversions_data(pt,m)
#con

# This is a simple function that takes in sample size, the total KPI count and days between start and end to return the duration (in days) it will take for the eperiment
def test_duration(sample_size, total, days):
    avg = total/days
    return(sample_size//avg)

# This function helps us calculate the Minimum Sample Size and the duration (in Days and Weeks) it will take to complete the experiment
# Inputs:
# MDE : Minimum Detectable Effect
# conversion_df: The DataFrame containg the conversion rate for the various metrics (KPIs) with respect to the selected Metric
# pivoted_df : The DataFRame containg the KPI counts for select KPIs
# m : index of the Metric selected
# days : The days between the selected starting day and the ending day

# Output: A dataframe with a row containg the conversion, rate, sample size, Days and weeks for each Metric conversion
def sizing(mde, conversion_df, pivoted_df, m, days):
    col = conversion_df.shape[1] # We take the no columns in conversion_df to know the no of metrics we may need
    sizing_df = pd.DataFrame() # We create an Empty DataFrame
    # We add empty columns to the DataFrame
    sizing_df[["Metrics","Conversion","Sample Size","Days","Weeks"]] = ""
    for i in range(col): 
        m = m+1 # We advance the Metric by one (here both m and i refer to same metric but in different DataFames: pivoted and convesion_df)
        ss = [] # We create an empty list
        ss.append(conversion_df.columns[i]) # Metrics We add the Metric name from conversion_df to the list
        ss.append(conversion_df.iloc[0,i])  # The conversion of the Metric
        ss.append(get_sample_size(mde,(conversion_df.iloc[0,i]/100)))  # The calculated sample size for the Mteric
        ss.append(test_duration(ss[2], pivoted_df.iloc[0,m],days))  # The duration of the Experiment in days
        ss.append(round(ss[3]/7,2)) # The duration in Weeks
        sizing_df.loc[i] = ss # We attach the list as a row in the DataFame
    return sizing_df

# Testing the sizing function
#ss = sizing(MDE,con,pt,m,days)
#ss

# This function calculates the the amount of conversions (Activations) we can get for a given ampunt of lift
# MDE : Minimum Detectable Effect
# conversion_df: The DataFrame containg the conversion rate for the various metrics (KPIs) with respect to the selected Metric
# lift : The supposed increase in the conversion rate that the user enters
# pivoted_df : The DataFRame containg the KPI counts for select KPIs
# m : index of the Metric selected
# days : The days between the selected starting day and the ending day

#Output
# A DataFrame that calculates the conversions (Activations) we can expect for a given lift on a Daily Basis, Yearly Basis and By the end of the year after the treatment is ramped

def get_nna(ramp, conversion_df, lift, pivoted, m, days):
    col = conversion_df.shape[1] # We take the no columns in conversion_df to know the no of metrics we may need
    eoy = pd.to_datetime(str(ramp.year)+"-12-31") # We get the end of the year from ramped date
    ramped_days = (eoy - ramp).days # We calculate the no of days from ramped date to end of the year
    activations_df = pd.DataFrame() # We create an Empty DataFrame
    # We add empty columns to the DataFrame
    activations_df[["Metrics","Activations(Daily)","Activations(Yearly)","Activations(Year End)"]] = ""
    daily_rate = pivoted.iloc[0,m]/days # The daily conversions of the denominator Metric (The selected Metric)
    for i in range(col):
        ac = [] # We create an empty list
        base = conversion_df.iloc[0,i]/100 # We get the conversion for a given Metric and divide it by 100 to get it in decimal points
        ac.append(conversion_df.columns[i]) # We take the name of the Metic
        ac.append(math.ceil(daily_rate * lift * base)) # We calculate the expected daily conversions for the Metic using lift
        ac.append(ac[1] * 365) # We calculate the Yearly conversions using the daily conversions
        ac.append(ac[1] * ramped_days) # We calculate the conversions by the end of the Year
        activations_df.loc[i] = ac #We attach the list as row to the DataFrame
    return activations_df
        
# Testing the NNA function
#get_nna(ramp, con, lift, pt, m, days)

# This function calculates the conversion rate for the subsequent funnels (very different to conversions_data() as that only calculates conversion rates with respect to a selected Metric)
def funnel_data(pivoted):
    funnel = pd.DataFrame() # We create an Empty DataFrame
    col = pivoted.shape[1]  # We take the no of columns in pivoted to know the no of metrics we may need
    funnel["#_Visitors"] = [100.00] # We set Visitors as 100% because it is the parent funnel to all funnels
    for i in range(1,col):
        # We calculate the conversion rate as pecentage of KPI counts of the child funnel to its parent funnel
        funnel[pivoted.columns[i]] = [round(pivoted.iloc[0,i] * 100 / pivoted.iloc[0,i-1],2)]
    return funnel   
#funnel_data(pt)
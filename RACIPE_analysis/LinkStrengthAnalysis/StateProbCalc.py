import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import islice 
import itertools 
from scipy.special import comb
import glob
from functools import reduce

#returns probability as a dict, where state is key and probability is value 
def get_prob(str_file, phase_file): 
  df = pd.read_csv(str_file) #read link strength file
  num_edges = df.shape[1] - 2
  phase = pd.read_csv(phase_file) #read phase file
  df = df.iloc[:,0:num_edges].apply(lambda x:np.where(x > x.mean(), 1, 0)) #Binarize link strength as 0,1 depending on if it is lower,higher than mean for that link
  full_df = pd.merge(df, phase['Phase'], left_index=True, right_index=True) 
  str_states = ["".join(i) for i in list(itertools.product(["0", "1"], repeat=4))] #get list of all possible states
  count_dict = dict(zip(str_states, np.zeros(len(str_states)))) #create empty dict where key is states and value is 0
  for i in range(full_df.shape[0]):# loop over all parameters
    prob = (0.5)**full_df.iloc[i,0:num_edges].sum() #prob = 0.5^(number of link strengths that are 1)
    if type(full_df.iloc[i,-1]) == float: #ignore if parameter set gives rise to no states
      continue
    states = full_df.iloc[i,-1].split('-') #if more than one state, spilt into list of states
    for s in states: 
      count_dict[s] += prob/len(states) #prob = prob for that paramater set/number of states obtained
  count_dict = {k: v / full_df.shape[0] for k, v in count_dict.items()} #divide by total number of parameter sets to get frequency
  return count_dict

str_fl = '/tmp/C10WT_'
phase_fl = '/tmp/C10WT_'
count_full = [get_prob(str_fl+str(i) + "_linkStrength.csv", phase_fl+str(i) + "_phases.csv") for i in range(1,4)] #get probability for each repeat n=1:3
count_df = [pd.DataFrame.from_dict(i, orient='index') for i in count_full] 
df_final = reduce(lambda left,right: pd.merge(left,right,left_index=True, right_index=True), count_df) #add all dicts as dataframe
df_final.columns = ["Freq1","Freq2","Freq3"] 
df_final.index = [ "'" + "".join(i) + "'" for i in list(itertools.product(["0", "1"], repeat=4))] 
df_final.to_csv('/content/C10_merged.csv')


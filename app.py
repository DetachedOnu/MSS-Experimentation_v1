import streamlit as st
import Code
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import terminology as t
from PIL import Image

img = Image.open('calculator.png')
st.set_page_config(page_title='MSScalculator', page_icon = img, layout = 'wide', initial_sidebar_state = 'auto')
# favicon being an object of the same kind as the one you should provide st.image() with (ie. a PIL array for example) or a string (url or local file path)
# Custom CSS styling for the divider
# Custom CSS styling for the divider
divider_style = """
<style>
.custom-divider {
    margin: 0;
    padding: 0;
    border-top: 1px;
}
</style>
"""

# Apply the custom CSS styling
st.markdown(divider_style, unsafe_allow_html=True)


st.title("A/B Test Minimum Sample Size Calculator")

st.markdown("### Sample Size Calculator Terminology")
dis = t.displayterminology()

dis.display_BCR()
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
dis.display_MDE()
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
dis.display_siglevel()
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
dis.display_statpower()
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


#inputs
st.sidebar.title("Parameters")
variations=st.sidebar.number_input("Variations",min_value=1)
start_event=st.sidebar.number_input("Start Event count") # 
end_event=st.sidebar.number_input("End event count") # 
ramp_up=st.sidebar.number_input("Percent of Users to be Involved in the Experiment",min_value=1,max_value=100,value=100)
baseline_val=st.sidebar.number_input("Baseline convertion percent [0.01-1.0]")
mde=st.sidebar.text_input("Minimum Detectable Effect [0.01-1.0] ") 
alpha=st.sidebar.number_input("Alpha",value=0.05,min_value=0.01,max_value=0.21)
beta=st.sidebar.number_input("Statistical Power",value=0.80,min_value=0.01,max_value=0.9)
show_analysis_button = st.sidebar.button("show analysis")
beta=1-beta

flag=0 #to validate start and end event numbers
if start_event!=0 and end_event!=0 and start_event>end_event:
     baseline_val= end_event/start_event
else:
    if baseline_val>0:
        baseline_val=baseline_val
        flag=0
    else:
        #st.header("Enter proper Start and end event numbers or Baseline value")
        flag=1

#analysis
if flag==0:    
    flag=0
    if show_analysis_button:
        sample_sizes={}
        st.columns(1)
        if mde:
            flag=1
            mde_flag=1
            mde=float(mde)
            ss=Code.get_sample_size(mde,baseline_val,alpha,beta)
            sample_sizes[mde]=ss   
        else:
            mde_flag=0
            for i in range(1,16): # 
                mde=i/100
                ss=Code.get_sample_size(mde, baseline_val,alpha = 0.05, beta = 0.2,relative=True)
                sample_sizes[mde]=ss #creating dictionary of MDE and sample sizes

        
        df=pd.DataFrame([sample_sizes]).T.reset_index()
        df['Alpha']=alpha * 100
        df['Beta']=(1-beta)*100
        df['Baseline rate']=(baseline_val)*100
        df.columns=['MDE %','Sample Size per variation in thousands','Alpha %','Beta %','Baseline rate %']
        df['Total Sample Size in thousands']=np.round((df['Sample Size per variation in thousands']*variations)/1000)   
        df['Sample Size per variation in thousands']=np.ceil(df['Sample Size per variation in thousands']/1000)
        if start_event:
            df['time_required (weeks)']=[np.ceil(
                ((x*1000)/(start_event*(ramp_up/100)))/7) for x in df['Total Sample Size in thousands']]
            df['MDE %']=df['MDE %']*100
            op=df.T
            op.columns=np.round(op.iloc[0])
        else:
            df['time_required (weeks)']=''
            flag=1
            df['MDE %']=df['MDE %']*100
            op=df.T
            # op.columns=np.round(op.iloc[0])
        
        
        if flag==0:
            fig,ax=plt.subplots()
            ax.plot(df['MDE %'],df['time_required (weeks)'])
            ax.set_xlabel("MDE %")
            ax.set_ylabel("time_required (weeks)")
            ax.axvline(5, color='r', linestyle='--')
            st.header("Time required - MDE")
            st.pyplot(fig)
        else:
            if mde_flag!=1:
                fig,ax=plt.subplots()
                ax.plot(df['MDE %'],df['Total Sample Size in thousands'])
                ax.set_xlabel("MDE %")
                ax.set_ylabel("Total sample size in thousands")
                ax.axvline(5, color='r', linestyle='--')
                st.header("Sample Size - MDE")
                st.pyplot(fig)

        st.header("Sample size required")
        op=op.reindex(['MDE %','Total Sample Size in thousands','time_required (weeks)','Sample Size per variation in thousands','Alpha %','Beta %','Baseline rate %'])
        st.dataframe(op)
        st.download_button(label="Download",data=df.T.to_csv(),file_name="sample_size.csv",mime="text/csv")

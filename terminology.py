import streamlit as st


ref_docstring = """ **Baseline Conversion Rate :** 

- The conversion rate for your control or original version. (Usually labelled “version A” when setting up an A/B test).
- For ex,
	- you simply divide the number of sales or sign-ups the page has produced by the number of visitors the control page receives.


**Minimum Detectable Effect :** 

- Minimum = smallest
- Detectable = what you want to see from running the experiment
- Effect = conversion difference between the control and treatment

	*how do you choose MDE and what does it depend on?* 
	- Historical data: observations you've made overtime that show, in general, most tests tend to achieve a certain lift, so this one should too.
	- What's worth it: a number you choose, based on what you consider worth it to take the time and resources to run the experiment. For example, a testing agency may, by default, set the MDE at 10% for every experiment at because that's the minimum needed to declare a win for the client.
	- Organizational maturity: a large, mature testing organization, with a lot of traffic, may set the MDE at 1-3% because, through ongoing optimization, getting gains any higher would be unrealistic.



	*General Uplift to expect :* 
- Conversion Rate Optimisation experts agree it is very difficult to get an uplift of more than 10% on a single webpage
- Achieving uplift beyond 10% requires “innovative” changes to your site or your business (for example, lowering your prices, changing you offers, rebranding or restructuring your website.)
- Less dramatic “iterative” changes (such as adjusting a button colour, headline or image) generally produce an increase of less than 7%. It is possible that this kind of change would produce no change or, even, a negative uplift.
- Therefore, in most cases, we would recommend 5% as a realistic projected increase.

**MDE can be expressed as an absolute or relative amount**

- Absolute:

	- The actual raw number difference between the conversion rates of the control and variant.
	- For example, if the baseline conversion rate is 0.77% and you’re expecting the variant to achieve a MDE of ±1%, the absolute difference is 0.23% (Variant: 1% - Control: 0.77% = 0.23%) OR 1.77% (Variant 1% + Control 0.7&% = 1.77%).

- Relative:

	- The percentage difference between the baseline conversion rate and the MDE of the variant.
	- For example, if the baseline conversion rate is 0.77% and you’re expecting the variant to achieve a MDE of ±1%, the relative difference between the  percentages is 29.87% (increase from Control: 0.77% to Variant: 1% = 29.87% gain) or -23% (decrease from Control: 0.77% to Variant 1% =-23%).


**Statistical power 1−β:**


- The probability of finding an “effect,” or difference between the performance of the control and variant(s), assuming there is one
- A power of 0.80 is considered standard best practice.
- In testing, your aim is to ensure you have enough power to meaningfully detect a difference in conversion rates. Therefore, a higher power is always better. But the trade-off is, it requires a larger sample size..


**Significance Level α:** 


- significance level alpha is the false positive rate, or the percentage of time a conversion difference will be detected -- even though one doesn't actually exist.
- your significance level should be 5% or lower.
- This number means there’s less than a 5% chance you find a difference between the control and variant -- when no difference actually exists.


**Why do we need to calculate sample size before starting the ab test?** 

1. So you know you have a large enough sample size for your test to be adequately powered to accurately detect a meaningful effect.
2. So you don’t prematurely stop the test and incorrectly declare a winner before one has truly emerged.
Remember: you need a large enough sample size, or amount of traffic, to adequately represent your entire audience.
	
	
	

**How long do you need to run your test to achieve a valid sample size?**

Duration depends on
- The type of test you're running
- How many variants you're testing
- Seasonal factors
- Sales cycles

The general A/B testing best practice is to let a test run for a minimum of 2-weeks but no longer than 6-8 weeks.This time period is selected so that any trends observed over a one-week period, or less, can be confirmed and validated over again.
	
Running a test for more than 3 months is risky because many of the conditions will have changed over such a long period.
For example, 10% of internet users erase their cookies once a month, on average. Most tools use these cookies to keep each visitor on one version of your webpage so they need to remain in place throughout the test.
	"""
 
 
 # Define the text and additional information
 
 
class displayterminology():
    
    def display(self, text, additional_info):
        # Create a markdown section with a dropdown effect
        dropdown_section = f"""
        <details>
            <summary>{text}</summary>
            {additional_info}
        </details>
        """

        st.markdown(dropdown_section, unsafe_allow_html=True)
        
    
    def display_BCR(self):
        text = "<b>Baseline Conversion Rate<b>"
        additional_info = """

        - The conversion rate for your control or original version. (Usually labelled “version A” when setting up an A/B test).
        - For ex,
            - you simply divide the number of sales or sign-ups the page has produced by the number of visitors the control page receives. 
        
        """
        self.display(text, additional_info)
    
        
    def display_MDE(self):
        text = "<b>Minimum Detectable Effect<b>"
        additional_info = """
        - Minimum = smallest
        - Detectable = what you want to see from running the experiment
        - Effect = conversion difference between the control and treatment

            *how do you choose MDE and what does it depend on?* 
            - Historical data: observations you've made overtime that show, in general, most tests tend to achieve a certain lift, so this one should too.
            - What's worth it: a number you choose, based on what you consider worth it to take the time and resources to run the experiment. For example, a testing agency may, by default, set the MDE at 10% for every experiment at because that's the minimum needed to declare a win for the client.
            - Organizational maturity: a large, mature testing organization, with a lot of traffic, may set the MDE at 1-3% because, through ongoing optimization, getting gains any higher would be unrealistic.

        *General Uplift to expect :* 
        - Conversion Rate Optimisation experts agree it is very difficult to get an uplift of more than 10% on a single webpage
        - Achieving uplift beyond 10% requires “innovative” changes to your site or your business (for example, lowering your prices, changing you offers, rebranding or restructuring your website.)
        - Less dramatic “iterative” changes (such as adjusting a button colour, headline or image) generally produce an increase of less than 7%. It is possible that this kind of change would produce no change or, even, a negative uplift.
         
        Therefore, in most cases, we would recommend 5% as a realistic projected increase.

        **MDE can be expressed as an absolute or relative amount**

        - Absolute:

            - The actual raw number difference between the conversion rates of the control and variant.
            - For example, if the baseline conversion rate is 0.77% and you’re expecting the variant to achieve a MDE of ±1%, the absolute difference is 0.23% (Variant: 1% - Control: 0.77% = 0.23%) OR 1.77% (Variant 1% + Control 0.7&% = 1.77%).

        - Relative:

            - The percentage difference between the baseline conversion rate and the MDE of the variant.
            - For example, if the baseline conversion rate is 0.77% and you’re expecting the variant to achieve a MDE of ±1%, the relative difference between the  percentages is 29.87% (increase from Control: 0.77% to Variant: 1% = 29.87% gain) or -23% (decrease from Control: 0.77% to Variant 1% =-23%).
        """

        # Create a markdown section with a dropdown effect
        self.display(text, additional_info)
        
    def display_siglevel(self):
        text = "<b>Significance Level α<b>"
        additional_info = """
        - significance level alpha is the false positive rate, or the percentage of time a conversion difference will be detected -- even though one doesn't actually exist.
        - your significance level should be 5% or lower.
        - This number means there’s less than a 5% chance you find a difference between the control and variant -- when no difference actually exists.
        """

        # Create a markdown section with a dropdown effect
        self.display(text, additional_info)
        
    def display_statpower(self):
        text = "<b>Statistical power 1−β<b>"
        additional_info = """
        - The probability of finding an “effect,” or difference between the performance of the control and variant(s), assuming there is one
        - A power of 0.80 is considered standard best practice.
        - In testing, your aim is to ensure you have enough power to meaningfully detect a difference in conversion rates. Therefore, a higher power is always better. But the trade-off is, it requires a larger sample size.
        """

        # Create a markdown section with a dropdown effect
        self.display(text, additional_info)
        
        
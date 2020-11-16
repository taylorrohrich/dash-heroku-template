#!/usr/bin/env python
# coding: utf-8

# # Lab Assignment 12: Interactive Visualizations
# ## DS 6001: Practice and Application of Data Science
#
# ### Instructions
# Please answer the following questions as completely as possible using text, code, and the results of code as needed. Format your answers in a Jupyter notebook. To receive full credit, make sure you address every part of the problem, and make sure your document is formatted in a clean and professional way.

# ## Problem 0
# Import the following libraries:

# In[1]:


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# For this lab, we will be working with the 2019 General Social Survey one last time.

# In[2]:


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                  encoding='cp1252', na_values=['IAP', 'IAP,DK,NA,uncodeable', 'NOT SURE',
                                                'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])
# Here is code that cleans the data and gets it ready to be used for data visualizations:

# In[3]:


mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk']
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss': 'weight',
                              'educ': 'education',
                              'coninc': 'income',
                              'prestg10': 'job_prestige',
                              'mapres10': 'mother_job_prestige',
                              'papres10': 'father_job_prestige',
                              'sei10': 'socioeconomic_index',
                              'fechld': 'relationship',
                              'fefam': 'male_breadwinner',
                              'fehire': 'hire_women',
                              'fejobaff': 'preference_hire_women',
                              'fepol': 'men_bettersuited',
                              'fepresch': 'child_suffer',
                              'meovrwrk': 'men_overwork'}, axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older': '89'})
gss_clean.age = gss_clean.age.astype('float')


# The `gss_clean` dataframe now contains the following features:
#
# * `id` - a numeric unique ID for each person who responded to the survey
# * `weight` - survey sample weights
# * `sex` - male or female
# * `education` - years of formal education
# * `region` - region of the country where the respondent lives
# * `age` - age
# * `income` - the respondent's personal annual income
# * `job_prestige` - the respondent's occupational prestige score, as measured by the GSS using the methodology described above
# * `mother_job_prestige` - the respondent's mother's occupational prestige score, as measured by the GSS using the methodology described above
# * `father_job_prestige` -the respondent's father's occupational prestige score, as measured by the GSS using the methodology described above
# * `socioeconomic_index` - an index measuring the respondent's socioeconomic status
# * `satjob` - responses to "On the whole, how satisfied are you with the work you do?"
# * `relationship` - agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."
# * `male_breadwinner` - agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."
# * `men_bettersuited` - agree or disagree with: "Most men are better suited emotionally for politics than are most women."
# * `child_suffer` - agree or disagree with: "A preschool child is likely to suffer if his or her mother works."
# * `men_overwork` - agree or disagree with: "Family life often suffers because men concentrate too much on their work."

# ## Problem 1
# Our goal in this lab is to build a dashboard that presents our findings from the GSS. A dashboard is meant to be shared with an audience, whether that audience is a manager, a client, a potential employer, or the general public. So we need to provide context for our results. One way to provide context is to write text using markdown code.
#
# Find one or two websites that discuss the gender wage gap, and write a short paragraph in markdown code summarizing what these sources tell us. Include hyperlinks to these websites. Then write another short paragraph describing what the GSS is, what the data contain, how it was collected, and/or other information that you think your audience ought to know. A good starting point for information about the GSS is here: http://www.gss.norc.org/About-The-GSS
#
# Then save the text as a Python string so that you can use the markdown code in your dashboard later.
#
# It should go without saying, but no plagiarization! If you summarize a website, make sure you put the summary in your own words. Anything that is copied and pasted from the GSS webpage, Wikipedia, or another website without attribution will receive no credit.
#
# (Don't spend too much time on this, and you might want to skip it during the Zoom session and return to it later so that you can focus on working on code with your classmates.) [1 point]

# #### Gender Wage Gap
#
# Based on a recent article from [cnbc](https://www.cnbc.com/2020/09/18/new-census-data-reveals-no-progress-has-been-made-closing-the-gender-pay-gap.html), recent census data from 2019 shows that women still make \$0.82 dollars for every dollar a man makes. The data also shows that this gap can be widened when looking at other factors such as race. There are also concerns that this gap will be made wider as a result of the pandemic. Additionally, the [Center for American Progress](https://www.americanprogress.org/issues/women/reports/2020/03/24/482141/quick-facts-gender-wage-gap/) explains some of the reasons for this wage gap, ranging from field of work, hours worked, and discrimination. This dashboard intends to provide more context for the issues in regards to gender and income above.
#
# #### GSS Background Information
#
# The GSS (General Social Survey) attempts to capture the dynamic, changing sentiments and behaviors of current Americans surrounding topics like well being, crime, politics, and racial sentiment. The GSS is undertaken every 2 years, and provides a cost-effective way to capture overarching sentiments of the American people that can be used in a variety of settings ranging from academia to policy making. We will utilize GSS data in this dashboard to make claims about the gender wage gap listed above.

# In[4]:


markdown_text = '''
#### Gender Wage Gap

Based on a recent article from [cnbc](https://www.cnbc.com/2020/09/18/new-census-data-reveals-no-progress-has-been-made-closing-the-gender-pay-gap.html), recent census data from 2019 shows that women still make \$0.82 dollars for every dollar a man makes. The data also shows that this gap can be widened when looking at other factors such as race. There are also concerns that this gap will be made wider as a result of the pandemic. Additionally, the [Center for American Progress](https://www.americanprogress.org/issues/women/reports/2020/03/24/482141/quick-facts-gender-wage-gap/) explains some of the reasons for this wage gap, ranging from field of work, hours worked, and discrimination. This dashboard intends to provide more context for the issues in regards to gender and income above.

#### GSS Background Information

The GSS (General Social Survey) attempts to capture the dynamic, changing sentiments and behaviors of current Americans surrounding topics like well being, crime, politics, and racial sentiment. The GSS is undertaken every 2 years, and provides a cost-effective way to capture overarching sentiments of the American people that can be used in a variety of settings ranging from academia to policy making. We will utilize GSS data in this dashboard to make claims about the gender wage gap listed above.
'''


# ## Problem 2
# Generate a table that shows the mean income, occupational prestige, socioeconomic index, and years of education for men and for women. Use a function from a `plotly` module to display a web-enabled version of this table. This table is for presentation purposes, so round every column to two decimal places and use more presentable column names. [3 points]

# In[8]:


# Group by sex, get the columns we are interested in
tab = gss_clean.groupby('sex')[
    ['income', 'job_prestige', 'socioeconomic_index', 'education']].mean().reset_index().round(2)
# Rename to be clearer
tab = tab.rename(columns={'income': 'income (USD)', 'job_prestige': 'occupational prestige score',
                          'socioeconomic_index': 'socioeconomic score', 'education': 'years of education'})
# Create table
table = ff.create_table(tab)


# ## Problem 3
# Create an interactive barplot that shows the number of men and women who respond with each level of agreement to `male_breadwinner`. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# In[12]:


# Group by sex, male breadwinner, get size, and rename columns
bar_data = gss_clean.groupby(['sex', 'male_breadwinner']).size(
).reset_index().rename(columns={0: 'count'})
bar_data


# In[14]:


# Bar with color sex, change labels to be more easily red
bar = px.bar(bar_data, x='male_breadwinner', y='count', color='sex',
             labels={
                 'male_breadwinner': "Response to Male Breadwinner Question", 'count': 'Frequency'},
             barmode='group')
# Add settings
bar.update_layout(showlegend=True)
bar.update(layout=dict(title=dict(x=0.5)))


# ## Problem 4
# Create an interactive scatterplot with `job_prestige` on the x-axis and `income` on the y-axis. Color code the points by `sex` and make sure that the figure includes a legend for these colors. Also include two best-fit lines, one for men and one for women. Finally, include hover data that shows us the values of `education` and `socioeconomic_index` for any point the mouse hovers over. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# In[29]:


# Plot scatter with job prestige on x, income on y, split by sex, color by sex
scatter = px.scatter(gss_clean, x='job_prestige', y='income', color='sex',
                     trendline='ols',  # add regression line
                     height=600, width=600,
                     labels={'job_prestige': 'occupational prestige score'},
                     # hover data
                     hover_data=['education', 'socioeconomic_index'],
                     )
scatter.update(layout=dict(title=dict(x=0.5)))


# ## Problem 5
# Create two interactive box plots: one that shows the distribution of `income` for men and for women, and one that shows the distribution of `job_prestige` for men and for women. Write presentable labels for the axis that contains `income` or `job_prestige` and remove the label for `sex`. Also, turn off the legend. Don't bother with titles because we will be using subtitles on the dashboard for these graphics. [3 points]

# In[17]:


# sex vs income, color by sex
box1 = px.box(gss_clean, y='sex', x='income', color='sex',
              labels={'sex': '', 'income': 'income (USD)'},
              )
box1.update(layout=dict(title=dict(x=0.5)))
# Remove legend
box1.update_layout(showlegend=False)


# In[18]:


# Sex vs. job prestige, color by sex
box2 = px.box(gss_clean, y='sex', x='job_prestige', color='sex',
              labels={'job_prestige': "occupational prestige score", 'sex': ''},
              )
box2.update(layout=dict(title=dict(x=0.5)))
# Remove legend
box2.update_layout(showlegend=False)


# ## Problem 6
# Create a new dataframe that contains only `income`, `sex`, and `job_prestige`. Then create a new feature in this dataframe that breaks `job_prestige` into six categories with equally sized ranges. Finally, drop all rows with any missing values in this dataframe.
#
# Then create a facet grid with three rows and two columns in which each cell contains an interactive box plot comparing the income distributions of men and women for each of these new categories.
#
# (If you want men to be represented by blue and women by red, you can include `color_discrete_map = {'male':'blue', 'female':'red'}` in your plotting function. Or use different colors if you want!) [3 points]

# In[25]:


# Make new dataframe with only income, sex and job_prestige
facetData = gss_clean[['income', 'sex', 'job_prestige']]
# Create new feature that breaks job_prestige into sex categories w/ equally sized ranges
facetData['job_prestige_cat'] = pd.cut(facetData['job_prestige'], 6)
# Drop missing values
facetData.dropna(inplace=True)


# In[26]:


facetData


# In[31]:


# Facet Box Plot with sex vs. income broken into the job prestige categories created above
facbox = px.box(facetData, y='sex', x='income', color='sex', facet_col_wrap=2,
                color_discrete_map={'male': 'blue', 'female': 'red'},
                labels={'job_prestige_cat': "job prestige category"},
                facet_col='job_prestige_cat',
                )


# ## Extra Credit (up to 10 bonus points)
# Dashboards are all about good design, functionality, and accessability. For this extra credit problem, create another version of the dashboard you built for problem 7, but take extra steps to improve the appearance of the dashboard, add user-inputs, and host it on the internet with its own URL.
#
# **Challenge 1**: Be creative and use a layout that significantly departs from the one used for the ANES data in the module 12 notebook. A good place to look for inspiration is the [Dash gallery](https://dash-gallery.plotly.host/Portal/). We will award up to 3 bonus points for creativity, novelty, and style.
#
# - Added an image at the beginning, used flexbox to put graphs inline, change font colors
#
# **Challenge 2**: Alter the barplot from problem 3 to include user inputs. Create two dropdown menus on the dashboard. The first one should allow a user to display bars for the categories of `satjob`, `relationship`, `male_breadwinner`, `men_bettersuited`, `child_suffer`, or `men_overwork`. The second one should allow a user to group the bars by `sex`, `region`, or `education`. After choosing a feature for the bars and one for the grouping, program the barplot to update automatically to display the user-inputted features. One bonus point will be awarded for a good effort, and 3 bonus points will be awarded for a working user-input barplot in the dashboard.
#
# - See below
#
# **Challenge 3**: Follow the steps listed in the module notebook to deploy your dashboard on Heroku. 1 bonus point will be awarded for a Heroku link to an app that isn't working. 4 bonus points will be awarded for a working Heroku link.
#
# - https://trr2as-lab-12.herokuapp.com/

# In[51]:


gss_clean['education_category'] = pd.cut(gss_clean['education'], [-1, 10, 11, 12, 13, 14, 15, 16, 999], labels=['10 years or fewer', '11 years', '12 years', '13 years', '14 years', '15 years',
                                                                                                                '16 years', 'More than 16 years'])
gss_clean['education_category']


# In[91]:


app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)
app.layout = html.Div(
    [
        html.H1("Exploring the Gender Wage Gap by Job Prestige"),
        html.H2("Taylor Rohrich (trr2as)"),
        html.Div(
            html.Img(src="https://static01.nyt.com/images/2014/11/15/business/money/money-articleLarge.jpg?quality=75&auto=webp&disable=upscale"),
            style=({"display": 'flex', 'justify-content': 'center', 'align-items': 'center'})),
        dcc.Markdown(children=markdown_text),

        html.H3("Comparing Mean Income, Occupational Prestige, Socioeconomic index, and Years of Education for Men and for Women"),

        dcc.Graph(figure=table, style={'margin': 30}),

        html.H3("Comparing the Number of Men and Women who Respond with Each Level of Agreement to male_breadwinner"),

        dcc.Graph(figure=bar),
        html.Div([
            html.Div([
                html.H3('feature'),

                dcc.Dropdown(id='feature',
                             options=[{'label': i, 'value': i} for i in [
                                 'satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']],
                             value='male_breadwinner'),

                html.H3("group"),

                dcc.Dropdown(id='group',
                             options=[{'label': i, 'value': i}
                                      for i in ['sex', 'region', 'education_category']],
                             value='sex'),
            ], style={'flex': 1}),
            html.Div([

                dcc.Graph(id="graph")

            ], style={'flex': 2}),
        ],   style=({"display": 'flex', 'flex-direction': 'row', 'align-items': 'center'})),
        html.Div(html.Div(
            [html.H2("Comparing Job Prestige and Income by Gender"),
             dcc.Graph(figure=scatter)]),
            style=({"display": 'flex', 'justify-content': 'center', 'align-items': 'center'})),


        html.Div([
            html.Div([
                html.H3("Distribution of Income by Gender"),

                dcc.Graph(figure=box1),
            ], style={'flex': 1}),
            html.Div([

                html.H3("Distribution of Occupational Prestige by Gender"),

                dcc.Graph(figure=box2),

            ], style={'flex': 1}),
        ],   style=({"display": 'flex', 'flex-direction': 'row', 'align-items': 'center'})),


        html.H3("Distribution of Income by Occupational Prestige Category "),

        dcc.Graph(figure=facbox),



    ], style={'color': '#44475a'}
)


@app.callback(Output(component_id="graph", component_property="figure"),
              [Input(component_id='feature', component_property="value"),
               Input(component_id='group', component_property="value")])
def make_figure(feature, group):
    # Group by sex, male breadwinner, get size, and rename columns
    bar_data = gss_clean.groupby([group, feature]).size(
    ).reset_index().rename(columns={0: 'count'})
    bar_data
    # Bar with color sex, change labels to be more easily red
    bar = px.bar(bar_data, x=feature, y='count', color=group,
                 labels={'feature': f"Response to {feature} Question",
                         'count': 'Frequency'},
                 barmode='group')
    # Add settings
    bar.update_layout(showlegend=True)
    bar.update(layout=dict(title=dict(x=0.5)))
    return bar


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')

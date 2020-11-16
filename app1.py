
import dash
import dash_core_components
import numpy as np
import pandas as pd
print(dash_core_components.__version__)
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px


df = pd.read_csv('country_profile_variables.csv')
smile = pd.read_csv('2019.csv')
sd_df_m = pd.read_csv("suicide-death-rates.csv")
sd_df = sd_df_m[sd_df_m['Year'] == 2017]

smile.rename(columns = {'Country or region':'country'}, inplace = True) 
happy_country = df[['country','Pop. using improved sanitation facilities (urban/rural, %)','Pop. using improved drinking water (urban/rural, %)','Education: Government expenditure (% of GDP)','Labour force participation (female/male pop. %)']]
happ_world = pd.merge(smile, happy_country, on='country')
pop = happ_world['Pop. using improved drinking water (urban/rural, %)'].str.split("/", n = 2, expand = True)
happ_world['sanitation_urban'] = pd.to_numeric(pop[0], errors='coerce')
happ_world['sanitation_rural'] = pd.to_numeric(pop[1], errors='coerce')
happ_world = happ_world[(happ_world["sanitation_urban"] > 0)]
happ_world = happ_world[(happ_world["sanitation_rural"] > 0)]
happ_world = happ_world[0:16]
happ_world['Score'] = happ_world['Score']*10


country_gdp = df[['country','GDP per capita (current US$)']].sort_values(by=['GDP per capita (current US$)'], ascending=False)
country_gdp['GDP per capita (current US$)'] = pd.to_numeric(country_gdp['GDP per capita (current US$)'], errors='coerce')
country_gdp = country_gdp[(country_gdp["GDP per capita (current US$)"] != -99)]
#top 20 Countries GDP 
gdp_count = country_gdp[0:21]
gdp_count_bad = country_gdp[-31:]

line_multi = df[['country','Unemployment (% of labour force)','Employment: Industry (% of employed)','Economy: Industry (% of GVA)']].sort_values(by=['Economy: Industry (% of GVA)'], ascending=False)
line_multi.dropna()
line_multi = line_multi[0:31]
line_multi = line_multi[(line_multi["Unemployment (% of labour force)"] != "...") & (line_multi["Employment: Industry (% of employed)"] != "...") & (line_multi["Economy: Industry (% of GVA)"] != "...")]
s = line_multi['Unemployment (% of labour force)']
line_multi['Unemployment (% of labour force)'] = pd.to_numeric(s, errors='coerce')
line_multi['Employment: Industry (% of employed)'] = pd.to_numeric(line_multi['Employment: Industry (% of employed)'], errors='coerce')
line_multi['Economy: Industry (% of GVA)'] = pd.to_numeric(line_multi['Economy: Industry (% of GVA)'], errors='coerce')
line_multi = line_multi[(line_multi["Unemployment (% of labour force)"] != -99 ) ]
line_multi = line_multi[(line_multi["Employment: Industry (% of employed)"] != -99 ) ]
line_multi = line_multi[(line_multi["Economy: Industry (% of GVA)"] != -99 ) ]
#& (line_multi["Employment: Industry (% of employed)"] != '-99') & (line_multi["Economy: Industry (% of GVA)"] != '-99')


lif = df['Life expectancy at birth (females/males, years)'].str.split("/", n = 2, expand = True)
df['Avg_man'] = pd.to_numeric(lif[0], errors='coerce')
df['Avg_women'] = pd.to_numeric(lif[1], errors='coerce')
df['Avg'] = (df['Avg_man'] + df['Avg_women'])/2
gdp_lif = df[['Region','Avg','GDP per capita (current US$)','country']]
gdp_lif = gdp_lif[(gdp_lif["Avg"] > 0)]

df.drop(df.columns[40], axis=1, inplace=True)

mobile_country =  df[['country','Mobile-cellular subscriptions (per 100 inhabitants)','Individuals using the Internet (per 100 inhabitants)']]
mobile_country['Mobile-cellular subscriptions (per 100 inhabitants)'] = pd.to_numeric(mobile_country['Mobile-cellular subscriptions (per 100 inhabitants)'], errors='coerce')
mobile_country['Individuals using the Internet (per 100 inhabitants)'] = pd.to_numeric(mobile_country['Individuals using the Internet (per 100 inhabitants)'], errors='coerce')

mobile_country = mobile_country.sort_values(by=['Individuals using the Internet (per 100 inhabitants)'], ascending=False)
mobile_country = mobile_country[(mobile_country["Mobile-cellular subscriptions (per 100 inhabitants)"] != -99 ) ]
mobile_country = mobile_country[(mobile_country["Individuals using the Internet (per 100 inhabitants)"] != -99 ) ]
mobile_country1 = mobile_country[0:21]
mobile_country1.shape
print(mobile_country1)

df_con = pd.concat([df.set_index('country'), sd_df.set_index('Entity')], axis = 1).dropna()

#def check(age):
#    if pd.isnull(age):
#       return None
#    age = age.split('/')[0]
#    age = age.replace('/', '')
#    return int(age)
#df['AGE'] = df['Life expectancy at birth (females/males, years)'].apply(check)
    




app = dash.Dash()
#data
trace1 = go.Bar(x = gdp_count['country'],y = gdp_count['GDP per capita (current US$)'])
trace2 = go.Bar(x = gdp_count_bad['country'],y = gdp_count_bad['GDP per capita (current US$)'])
trace3 = [
            go.Scatter(
                x=gdp_lif[gdp_lif['Region'] == i]['GDP per capita (current US$)'],
                y=gdp_lif[gdp_lif['Region'] == i]['Avg'],
                text=gdp_lif[gdp_lif['Region'] == i]['country'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in gdp_lif.Region.unique()
        ]
#defining layout
layout_1 = go.Layout(
 title=('Top 20 countries ranked by GDP per Capita'))

layout_2 = go.Layout(
 title=('Last 30 countries ranked by GDP per Capita'))

layout_3 = go.Layout(
                title =('Donfvmff'),
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy '},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )

#defining figure and plotting
fig_1 = go.Figure(data=trace1,layout=layout_1)
fig_2 = go.Figure(data=trace2,layout=layout_2)
fig_3 = go.Figure(data=trace3,layout=layout_3)
fig_4 = go.Figure()
fig_4.add_trace(go.Scatter(x=line_multi['country'], y=line_multi['Unemployment (% of labour force)'], name='unemployement rate',
                         line=dict(color='firebrick', width=4)))
fig_4.add_trace(go.Scatter(x=line_multi['country'], y=line_multi['Employment: Industry (% of employed)'], name='employement rate',
                         line=dict(color='royalblue', width=4)))
fig_4.add_trace(go.Scatter(x=line_multi['country'], y=line_multi['Economy: Industry (% of GVA)'], name='Economy rate at rate Industry',
                         line=dict(color='royalblue', width=4, dash='dot')))

fig_4.update_layout(title='Rate of Economy , unemployment and  employement sorted by Economy Industrail rate',
                   xaxis_title='Country',
                   yaxis_title='Rate')

fig_5 = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                    shared_yaxes=False, vertical_spacing=0.001)

fig_5.append_trace(go.Bar(
    x=mobile_country1['Mobile-cellular subscriptions (per 100 inhabitants)'],
    y=mobile_country1['country'],
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(
            color='rgba(50, 171, 96, 1.0)',
            width=1),
    ),
    name='Mobile cellur subscription',
    orientation='h',
), 1, 1)
fig_5.append_trace(go.Scatter(
    x=mobile_country1['Individuals using the Internet (per 100 inhabitants)'], y=mobile_country1['country'],
    mode='lines+markers',
    line_color='rgb(128, 0, 128)',
    name='Individuals Internet Usage ',
), 1, 2)

fig_5.update_layout(
    title='user scription and internet usage',
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        domain=[0, 0.85],
    ),
    yaxis2=dict(
        showgrid=False,
        showline=True,
        showticklabels=False,
        linecolor='rgba(102, 102, 102, 0.8)',
        linewidth=2,
        domain=[0, 0.85],
    ),
    xaxis=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0, 0.42],
    ),
    xaxis2=dict(
        zeroline=False,
        showline=False,
        showticklabels=True,
        showgrid=True,
        domain=[0.47, 1],
        side='top',
        dtick=25000,
    ),
    legend=dict(x=0.029, y=1.038, font_size=10),
    margin=dict(l=100, r=20, t=70, b=70),
    paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',
)


fig_6 = go.Figure()
fig_6.add_trace(go.Bar(
    x=happ_world['country'],
    y=happ_world['sanitation_urban'],
    name='improved drinking water Urban',
    marker_color='indianred'
))

fig_6.add_trace(go.Bar(
    x=happ_world['country'],
    y=happ_world['Score'],
    name='Happnies Score',
    marker_color='royalblue'
))

fig_6.add_trace(go.Bar(
    x=happ_world['country'],
    y=happ_world['sanitation_rural'],
    name='improved drinking water Rural',
    marker_color='lightsalmon'
))


fig_6.update_layout(title = 'Top Happy Country and Drinking Water Development' ,barmode='group', xaxis_tickangle=-45)

#world map
data_7 = [ dict(
 type='choropleth',
 locations = df['country'],
 autocolorscale = True,
 z = df['Surface area (km2)'],
 locationmode = 'country names',
 marker = dict(
 line = dict (
 color = 'rgb(255,255,255)',
 width = 2
 )
 ),
 colorbar = dict(
 title = "Surface Area"
 )
 ) ]
layout_7 = dict(
 title = 'Top Countries by Area')
fig_7 = go.Figure(data = data_7, layout = layout_7)

#Tree map
df['world'] = 'world'
df.rename(columns = {'Food production index (2004-2006=100)':'Food production index'}, inplace = True) 

fig_8 = px.treemap(df, path=['world','Region','country'], values='Population in thousands (2017)',
                  color='Food production index', hover_data=['Population in thousands (2017)'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df['Food production index'], weights=df['Population in thousands (2017)']))

df_con.rename(columns = {'Deaths - Self-harm - Sex: Both - Age: Age-standardized (Rate) (deaths per 100,000 individuals)':'Suicide deaths rates per 100,000 individuals'}, inplace = True) 
fig_9 = px.bar(df_con, y='Suicide deaths rates per 100,000 individuals', x='Region', text='Population in thousands (2017)')
fig_9.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_9.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')


data_10 = df[df['Region']== 'WesternEurope' ]
#data_10 = data_10.dropna()
fig_10 = px.pie(data_10, values='Agricultural production index (2004-2006=100)', names='country',
             title='Agriculture Production of WesternEurope',
             hover_data=['Urban population (% of total population)'])
fig_10.update_traces(textposition='inside', textinfo='percent+label')

# Step 4. Create a Dash layout
app.layout = html.Div([
                dcc.Graph(id = 'plot', figure = fig_1),
                dcc.Graph(id = 'plot2', figure = fig_2),
                dcc.Graph(id = 'plot3', figure = fig_3),
                dcc.Graph(id = 'plot4', figure = fig_4),
                dcc.Graph(id = 'plot5', figure = fig_5),
                dcc.Graph(id = 'plot6', figure = fig_6),
                dcc.Graph(id = 'plot7', figure = fig_7),
                dcc.Graph(id = 'plot8', figure = fig_8),
                dcc.Graph(id = 'plot9', figure = fig_9),
                dcc.Graph(id = 'plot10', figure = fig_10),
                      ])
# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug = False)

import seaborn as sns 
import pandas as pd 
import numpy as np
import plotly
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from IPython.core.debugger import set_trace

# Add colorbar
def discrete_colorscale(bvals, colors):
    """
    bvals - list of values bounding intervals/ranges of interest
    colors - list of rgb or hex colorcodes for values in [bvals[k], bvals[k+1]],0<=k < len(bvals)-1
    returns the plotly  discrete colorscale
    """
    if len(bvals) != len(colors)+1:
        raise ValueError('len(boundary values) should be equal to  len(colors)+1')
    bvals = sorted(bvals)     
    nvals = [(v-bvals[0])/(bvals[-1]-bvals[0]) for v in bvals]  #normalized values
    
    dcolorscale = [] #discrete colorscale
    for k in range(len(colors)):
        dcolorscale.extend([[nvals[k], colors[k]], [nvals[k+1], colors[k]]])
    return dcolorscale  

# Function to generate buttons switching between countries 
def generate_personbuttons(top):
    bool_mask = np.identity(len(top), dtype=bool)
    bool_mask = np.vstack(([True for _ in top], bool_mask)) # add Trues -> all items visible
    top = ['All'] + top
    buttons = []
    for i, person in enumerate(top):
        mydict = {'label': person,
                 'method': 'update',
                 'args': [{'visible': bool_mask[i, :]}]
                      }
        buttons.append(mydict)
    return buttons   

def plot_main(df, num_topics, save_name, model):
    # Prepare data
    data = []
    citites = df.City.unique()
    if isinstance(num_topics, np.ndarray):
        #pal_hls = sns.hls_palette(len(num_topics)).as_hex()
        pal_hls = sns.hls_palette(num_topics.max() + 1).as_hex()
        #set_trace()
        color_dict = {i : pal_hls[i] for i in num_topics}
        num_topics = len(num_topics)
    else:
        pal_hls = sns.hls_palette(num_topics).as_hex()
        color_dict = {i : pal_hls[i] for i in range(num_topics)}

    for city in citites:  

        doctext = df.loc[df['City'] == city,'Todo'].str.wrap(100).apply(lambda x: x.replace('\n', '<br>')).tolist()
        topicwords = df.loc[df['City'] == city,'{}_Topic_Keywords'.format(model)].tolist()
        topics = df.loc[df['City'] == city,'topic_string'].values.astype(str)
        topics_num = df.loc[df['City'] == city,'{}_Topic'.format(model)].values
        colors = [color_dict[i] for i in topics_num]
        hovertext = [[t] + ['<br>'] + [w] + ['<br>'] + [d] for t, w,d in zip(topics, topicwords, doctext)]  
        #set_trace()
        event_data = dict(
                x = df.loc[df['City'] == city,'x'],
                y = df.loc[df['City'] == city,'y'],    

                hovertext = hovertext,
                name = city,
                marker = dict(size = 12, opacity = 0.9, color=colors),
                type = 'scatter',
                mode="markers+text",
            )
        data.append(event_data)


    bvals = np.linspace(0, 1, num_topics + 1)
    colors = list(color_dict.values())
    dcolorsc = discrete_colorscale(bvals, colors)

    bvals = np.array(bvals)
    tickvals = list(range(1, num_topics+1))
    ticktext = ['topic_{}'.format(i) for i in range(len(df.topic_string.unique()))]

    colorbar_trace  = go.Scatter(x=[None],
                                 y=[None],
                                 mode='markers',
                                 marker=dict(
                                     showscale=True,
    #                                  colorscale = list(color_dict.values()),
                                     colorscale = dcolorsc,
                                     cmin=0.5,
                                     cmax=num_topics+0.5,
                                     colorbar=dict(
                                         title='Topics',
                                         tickvals=tickvals, 
                                         ticktext=ticktext,
                                         )

                                 ),
                                 hoverinfo='none'
                                )

    data.append(colorbar_trace)    


    # Set layout
    layout = dict(
        height = 800,
        # top, bottom, left and right margins
        margin = dict(t = 0, b = 0, l = 0, r = 0),
        font = dict(color = '#FFFFFF', size = 11),
        paper_bgcolor = '#000000',
        showlegend = False
    )    

    # Set title and background 
    annotations = [dict(
                  text = 'Airbnb',              
                  # font and border characteristics
                  font = dict(color = '#FFFFFF', size = 14), borderpad = 10, 
                  # positional arguments
                  x = 0.05, y = 0.05, xref = 'paper', yref = 'paper', align = 'left', 
                  # don't show arrow and set background color
                  showarrow = False, bgcolor = 'black'
                  )]

    # assigning the annotations to the layout
    layout['annotations'] = annotations


    # Add country-buttons and maps-buttons to layout
    updatemenus=list([
        dict(
            buttons = generate_personbuttons(list(df.City.unique())),
            # direction where the drop-down expands when opened
            direction = 'down',
            # positional arguments
            x = 0.01,
            xanchor = 'left',
            y = 0.99,
            yanchor = 'bottom',
            # fonts and border
            bgcolor = '#000000',
            bordercolor = '#FFFFFF',
            font = dict(size=11)
        )

    ])

    # # assign the list of dictionaries to the layout dictionary
    layout['updatemenus'] = updatemenus

    #Plot and plotly

    plotly.offline.init_notebook_mode(connected=True)

    figure = dict(data = data, layout = layout)
    plotly.offline.plot(figure, filename=save_name)

import pandas as pd


fastapi_url_limits = "https://dev1.dmtool.info/alembic/limits"

def parse_series_and_values(limits_dataframe_in):
    limit_data = []
    for index, row in limits_dataframe_in.iterrows():
        #print(row['id'], row['data_values'])
        data_label = row[['data_label']].iloc[0]
        data_string = row[['data_values']].iloc[0]
        data_string = data_string.replace("{[", "")
        data_string = data_string.replace("]}", "")
        #print(data_string)
        data_series = data_string.split("]")
        #print(len(data_series))
        for l in range(0,len(data_series)):
            next_colour = next(palette)
            single_set = data_series[l]
            set_list = single_set.split(";")
            for i in set_list:
                z = i.split(" ");
                new_x = z[0].replace(",[", "")
                try:
                    appendthis = [row['id'],data_label,l,new_x,z[1],next_colour]
                except:
                    appendthis = [row['id'],'data_label',l,0,0]
                limit_data.append(appendthis)
        #lol
    #print('parsed limit data >>>>',limit_data) 
    
    ## the datatable needed a unique id
    ## the id of the limit table was renamed to limit_id
    ## a new column was created called id
    
    limit_data_df_out = pd.DataFrame(data=limit_data,columns=['id','data_label','trace_id','raw_x','raw_y','trace_color_default'])
    limit_data_df_out['masses'] = limit_data_df_out['raw_x'].astype(str).astype(dtype = float, errors = 'ignore')
    limit_data_df_out['cross_sections'] = limit_data_df_out['raw_y'].astype(str).astype(dtype = float, errors = 'ignore')
    limit_data_df_out = limit_data_df_out.rename(columns={"id": "limit_id" })
    limit_data_df_out = limit_data_df_out.reset_index()
    limit_data_df_out['id'] = limit_data_df_out.index
    limit_data_df_out.set_index('id', inplace=True, drop=False)
    
    #columns=['id','data_label','series','raw_x','raw_y','series_color','masses','cross_sections']

    limit_list_df_out = limit_data_df_out[['limit_id','data_label']].copy()
    limit_list_df_out.drop_duplicates(inplace=True)
    limit_list_df_out = limit_list_df_out.reset_index()
    limit_list_df_out['id'] = limit_list_df_out.index
    limit_list_df_out.set_index('id', inplace=True, drop=False)
    
    trace_list_df_out = limit_data_df_out[['limit_id','data_label','trace_id','trace_color_default']].copy()
    trace_list_df_out.drop_duplicates(inplace=True)
    trace_list_df_out = trace_list_df_out.reset_index()
    trace_list_df_out['id'] = trace_list_df_out.index
    trace_list_df_out.set_index('id', inplace=True, drop=False)
        
    return limit_list_df_out, trace_list_df_out, limit_data_df_out




def GetLimits():
    url = fastapi_url_limits
    r = requests.get(url)
    response_data = r.json()
    #print("+++++++++ response data ++++++++++++")
    #print(response_data)
    response_data_frame = pd.DataFrame(response_data)
    #print("+++++++++++ response_data_frame ++++++++++++")
    #print(response_data_frame)
    limit_list_df_resp, trace_list_df_resp, limit_data_df_resp = parse_series_and_values(response_data_frame)
    column_names=['id','data_label','data_comment','data_values']
    limit_columns = ['id','limit_id','data_label']
    trace_columns = ['id','limit_id','data_label','trace_id','trace_color_default']
    limit_data_columns = ['id','limit_id','data_label','trace_id','raw_x','raw_y','trace_color','masses','cross_sections']

    #print('limit_list_df >>', limit_list_df_resp)
    #print('trace_list_df >>', trace_list_df_resp)
    #print('limit_data_df >>', limit_data_df_resp)

    
    if response_data_frame.empty:
       
        limit_empty_data = [['id','limit_id','data_label']]
        trace_empty_data = [['id','limit_id','data_label','trace_id','trace_color_default']]
        limit_data_empty_data = [['id','limit_id','data_label','trace_id','raw_x','raw_y','trace_color','masses','cross_sections']]
        
        limit_list_df_ret = pd.DataFrame(columns=limit_columns)
        trace_list_df_ret = pd.DataFrame(columns=trace_columns)
        limit_data_df_ret = pd.DataFrame(columns=limit_data_columns)
        
        limit_list_dict_ret = trace_list_df_ret.to_dict('records')
    else:
        limit_list_df_ret = limit_list_df_resp
        trace_list_df_ret = trace_list_df_resp
        limit_data_df_ret = limit_data_df_resp
        limit_list_dict_ret = limit_list_df_ret.to_dict('records')

    return limit_list_df_ret, trace_list_df_ret, limit_data_df_ret, limit_list_dict_ret, limit_columns, limit_data_columns, trace_columns


def GetLimitDict():
    limit_list_df, trace_list_df, limit_data_df, limit_list_dict, limit_columns, limit_data_columns, trace_columns = GetLimits()
    return limit_list_dict

def GetLimitColumns():
    limit_list_df, trace_list_df, limit_data_df, limit_list_dict, limit_columns, limit_data_columns, trace_columns = GetLimits()
    return limit_columns


def GetLimitsTable():

    font_size = '12px'
    row_height = '13px'

    limits_table_raw = dash_table.DataTable(
            id='limits_table_select',
            data=GetLimitDict(),
            columns=[{"name": c, "id": c} for c in GetLimitColumns()],
            fixed_rows={'headers': True},
            #fixed_rows={'headers': True},
            #page_size=5,
            filter_action='none',
            row_selectable='multi',
            selected_rows=[],
        
            style_cell={'textAlign': 'left','padding': '0px','font_size': font_size,
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'border': '1px solid black',
                            'height': row_height,
                        },
             css=[
                        {"selector": ".Select-menu-outer", "rule": "display: block !important"},
                        {"selector": "p", "rule" :"margin: 0px; padding:0px"},
                        {"selector": ".spreadsheet-inner tr td", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of header
                        {"selector": ".dash-spreadsheet-inner tr", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},
                        {"selector": ".dash-spreadsheet tr td", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of body rows
                        {"selector": ".dash-spreadsheet tr th", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},  # set height of header
                        {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"},
                        {"selector": ".dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr:first-of-type", "rule": "min-height: " + row_height + "; height: " + row_height + ";line-height: " + row_height + ";max-height: " + row_height + ";"}
                        ],
            
            style_table={'height': '30vh',},
            style_cell_conditional=[
                {'if': {'column_id': 'id'},
                 'width': '2%'},
                {'if': {'column_id': 'limit_id'},
                 'width': '10%'},
                {'if': {'column_id': 'data_label'},
                 'width': '50%'},
            ],
            #style_data={
            #    'whiteSpace': 'normal',
            #    'height': 'auto',
            #},
            #style_header=style_header_var,
            #tooltip_data=[
            #    {
            #        column: {'value': str(value), 'type': 'markdown'}
            #        for column, value in row.items()
            #    } for row in data
            #],
            tooltip_duration=None,
            )
            
    limits_table_ret = html.Div(
        children=[limits_table_raw],
        style={
            "text-align": "center",
            'width': '100%',
            'display': 'inline-block',
            'height': '35%'}
    )
    
    return limits_table_ret


def button_add_limits():
    add_limits_div_ret = html.Div(
        [
            html.Button(
                id="add-button",
                children="Add Selected Limit(s)",
                style={
                    "margin": "auto",
                }
            )
        ],
        style={
            "text-align": "center",
            'width': '100%',
            'display': 'inline-block',
            'height': '5%'}
    )
    return add_limits_div_ret

def create_plot_div():
    plot_container_ret = html.Div(id="limit-plot-container", style={'width': '100%', 'display': 'inline-block', 'height': '60%'})
    return plot_container_ret

def serve_layout():
    layout_out = html.Div(children=[
            GetLimitsTable(),
            button_add_limits(),
            create_plot_div(),
        ],
    style={'width': '100%', 'display': 'inline-block', 'height': '100%'})
    return layout_out

def CreateEmptyFig():
    x_title_text = r"$\text{WIMP Mass [GeV}/c^{2}]$"
    y_title_text = r"$\text{Cross Section [cm}^{2}\text{] (normalized to nucleon)}$"
    fig_ret = go.Figure(data=[go.Scatter(x=[], y=[])])
    fig_ret.update_xaxes(
        title_text=x_title_text,
        #type="log"
        type="linear"
    )
    fig_ret.update_yaxes(
        title_text=y_title_text,
        #type="log"
        type="linear"
    )
    return fig_ret

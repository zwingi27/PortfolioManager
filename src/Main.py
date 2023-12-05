
from components.packages import *   
from components.GeneralFunction import *
from ServerInitialization import app
from pages import Bank, Home, UploadData, Visualization


APP_LOGO = "assets/Finanzguru2.png" # constant for the path of the App Logo

#Constants
PAGE1 = "Home"          # Name of the page
PAGE1_HREF = "/pages/Home"  # Href link for the page
PAGE2 = "Bank"
PAGE2_HREF = "/pages/Bank"
PAGE3 = "Stocks"
PAGE3_HREF = "/pages/Stocks"
PAGE4 = "Upload"
PAGE4_HREF = "/pages/UploadData"


CURRENT_VERSION = html.Footer(html.Div([ 
                                 "Version 0.1"]),

                     style={'position':'absolute', 'bottom':70})


#---------------------------- Sidebar/Layout of the App----------------------------------------
#layout of the navigationbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.Button("Bank", size="md", color="info", className="mr-1", href="/pages/Bank"),
        dbc.Button("Stocks", size="md", color="info", className="mr-1", href="/pages/Stocks"),
        dbc.Button("Upload Data", size="md", color="info", className="mr-1", href="/pages/UploadData"),
        dbc.Button("Sidebar", outline=True, color="dark", className="mr-1", id="btn_sidebar")
    ],
    brand="Finance Portfolio Manager",
    brand_href="/page-1",
    color='#0ffdd9',
    dark=True,
    fluid=True,
    sticky='top',
    brand_style={"color": "rgb(0,0,0)", "textAlign": "left"},  # Adjust the text alignment to the left
)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
    
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_FONT = {
    "color": "rgb(86, 87, 89)",
}

#layout of the sidebar
sidebar = html.Div(
    [
        html.Div([ # show Grenzebach Logo on the sidebar
            html.Img(src=APP_LOGO, style={'width': '200px', 'height': '100px'})  
        ], style={'textAlign': 'center'}),

        html.Hr(), # horizontal line
        dbc.Nav(
            [   # Navigationlinks on the sidebar, one for each page
                dbc.NavLink(PAGE1, href=PAGE1_HREF, id="page-1-link", style=SIDEBAR_FONT),
                dbc.NavLink(PAGE2, href=PAGE2_HREF, id="page-2-link", style=SIDEBAR_FONT),
                dbc.NavLink(PAGE3, href=PAGE3_HREF, id="page-3-link", style=SIDEBAR_FONT),
                dbc.NavLink(PAGE4, href=PAGE4_HREF, id="page-4-link", style=SIDEBAR_FONT),
            ],
            vertical=True,
            pills=True,   
        ),
        
        CURRENT_VERSION,
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

# the content of each page is stored in the id through the callback and loaded in the app.layout
content = html.Div(
    id="page-content",
    style=CONTENT_STYLE
)

app.layout = html.Div(
    [   
        dcc.Store(id='uploadedData', storage_type='memory'),        # 'memory' allows to store larger data than 'session' but data is lost if browser refreshes
       
        dcc.Store(id='side_click'),
        dcc.Location(id="url", refresh=False),
        navbar,                                                     #layout for the navigation bar
        sidebar,                                                    #layout for the sidebar
        content,                                                    #visualizes the content of the corresponding page
    ],
)


# callback to open/close the sidebar
@app.callback(
    [ Output("sidebar", "style"), Output("page-content", "style"), Output("side_click", "data"),],
    [ Input("btn_sidebar", "n_clicks")],
    [ State("side_click", "data"),]
)
def ToggleSidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell which page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)], # if you add more pages you have to update the range()
    [Input("url", "pathname")],
)
def ToggleActiveLinks(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False, False            #each side needs one return, true to select the homepage
    return [pathname == f"/page-{i}" for i in range(1, 6)] # if you add more pages you have to update the range()

# callback to switch to the corresponding page
# the layout/content of the page gets stored in "page-content" and visualized in app.layout
@app.callback(Output("page-content", "children"),
              Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == PAGE2_HREF:
        return Bank.layoutDataSelection
    elif pathname == PAGE3_HREF:
        return Visualization.layoutVisualization
    elif pathname == PAGE4_HREF:
        return UploadData.layoutStoreData
    else:
        return Home.layoutStart



#run app on local host
if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:8050/')
    app.run_server(debug=True, dev_tools_ui=True) # set debug = False to run the app without debugging, set dev_tools_ui = False to disable the debug menu (blue button)



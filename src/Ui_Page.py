import dash
from dash import dcc, html,Input,Output

app = dash.Dash(__name__)

# Layout definieren
app.layout = html.Div([
    # Sidebar
    html.Div(
        [
            dcc.Link('Bank', href='/bank'),
            dcc.Link('Aktien', href='/aktien'),
            dcc.Link('Tanken', href='/tanken'),
        ],
        style={'width': '20%', 'position': 'fixed', 'top': 0, 'left': 0, 'bottom': 0, 'backgroundColor': '#f8f9fa'}
    ),
    # Hauptinhalt
    html.Div(id='page-content', style={'margin-left': '25%'})
])

# Dummy-Callbacks für die Seiteninhalte
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    return html.Div([
        html.H1(f'{pathname} Inhalt (Dummy)'),
        html.P('Dies ist ein Dummy-Callback, der keinen echten Inhalt generiert.')
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
"""
This is the entry point for the Dash application
"""

import dash  # type: ignore
import dash_bootstrap_components as dbc  # type: ignore
import webbrowser

# This is for caching global variables
from flask_caching import Cache

# Do not print request logs
import logging

logging.getLogger("werkzeug").setLevel(logging.WARNING)

# bootstrap theme (https://bootswatch.com/cerulean/)
external_stylesheets = [dbc.themes.CERULEAN]
external_scripts = [
    {
        "src": "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p",
        "crossorigin": "anonymous",
    }
]

# initialize the application
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    title="Mocca",
    use_pages=True,
    suppress_callback_exceptions=True,
)
server = app.server

# this suppresses exceptions when html elements accessed by callbacks were not created yet
app.config.suppress_callback_exceptions = True

# Initialize cache - needed for global variables
flask_cache = Cache()
flask_cache.init_app(
    app.server, config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 1e30}
)

# define directory for caching files
CACHE_DIR = "_cache"

# Pages must be imported after cache and campaign are initialized
import cache
import campaign


# # create callback for loading content for different URL paths
# @app.callback(
#     dash.dependencies.Output("page-content", "children"),
#     [dash.dependencies.Input("url", "pathname")],
# )
# def display_page(pathname: str):
#     """
#     When URL changes, the content of `div#page-content` is updated accordingly
#     """
#     if pathname in ["", "/", "/home"]:
#         return pages.home.get_layout()
#     elif pathname == "/data":
#         return pages.data.get_layout()
#     elif pathname == "/process":
#         return pages.process.get_layout()
#     elif pathname == "/results":
#         return pages.results.get_layout()
#     else:
#         # TODO: add page not found page
#         return None

from dash import html, dcc # type: ignore

from pages.base_layout.layout_navbar import navbar

def get_layout() -> html.Div:
    """Returns the basic layout shared by all pages"""
    return html.Div(
        id="outermost-wrapper",
        children=[
            dcc.Location(id='url', refresh=False),
            navbar(),
            html.Div(
                id="page-content",
                className="px-5 pb-5 pt-3",
                style={
                    'display': 'flex',
                    'flex-flow': 'column',
                    'align-items': 'normal'
                })
        ])

def get_multipage_layout():
    layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}",
                    href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),
    dash.page_container
    ])
    return layout
# start the server
if __name__ == "__main__":
    # initialize global variables and file caching
    cache.init()

    import pages
    import pages.base_layout
    import pages.home
    import pages.data
    #import pages.process
    #import pages.results

    print(dash.page_registry)
    # load the base layout
    app.layout = get_multipage_layout()

    webbrowser.open("http://localhost:8050")
    app.run(host="127.0.0.1", debug=False, port=8050)
    #server= app.server
    print(dash.page_registry)
    #server.run(debug=True)
    

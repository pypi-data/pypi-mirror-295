import base64
import io
import tempfile
import os
import pandas as pd
from dash import Dash, dcc, html, no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from hein_hplc.peak_analysis.peak_analysis_main import PeakAnalysis
from hein_hplc.peak_analysis.utils import read_uv

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Hein Lab - HPLC tool'
server = app.server
app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Upload(id='upload-data',
                           children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                           style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px',
                                  'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center',
                                  'margin': '5px',
                                  },
                           ),

                dbc.Label("Select data column"),
                dcc.Dropdown(id="dropdown", options=[], value=""),

                dbc.Label("Dead volume (sec)"),
                dcc.Slider(
                    id="dead-volume", min=0, max=100, step=1, value=50,
                    marks={i: str(i) for i in range(0, 101, 10)},
                ),

                dbc.Label("Peak detection mode "),
                dbc.Checklist(
                    options=[{"label": "Find hidden peaks", "value": 1}],
                    value=[], id="use-derivative", switch=True,
                ),
                dbc.Checklist(
                    options=[{"label": "Smooth derivatives", "value": 1}],
                    value=[], id="smooth-derivative", switch=True,
                ),
                dbc.Checklist(
                    options=[{"label": "Show second derivatives", "value": 1}],
                    value=[], id="show-derivative", switch=True,
                ),

                dbc.Label("Peak Height (%)"),
                dcc.Slider(
                    id="peak-height", min=0, max=100, step=1, value=10,
                    marks={i: str(i) for i in range(0, 101, 10)},
                ),

                dbc.Label("Smooth Window"),
                dcc.Slider(
                    id="smooth-window", min=1, max=101, step=2, value=21,
                    marks={i: str(i) for i in range(0, 101, 25)},
                ),

                dbc.Label("Range of interest"),
                dcc.RangeSlider(id='x-range-slider', marks=None, step=0.1, min=0, max=10, value=[0, 10], ),

                dbc.Label("Max peak width"),
                dcc.Slider(
                    id="peak-width", min=1, max=100, step=1, value=5,
                    marks={i: str(i) for i in range(0, 101, 10)},
                ),

                dbc.Label("Maximum peak count"),
                dcc.Slider(
                    id="max-peak-num", min=1, max=20, step=1, value=10,
                    marks={i: str(i) for i in range(0, 21, 5)},
                ),

                dbc.Label("Peak shift tolerance (sec) in trend plot"),
                dcc.Slider(
                    id="peak-shift", min=0, max=2, step=0.1, value=0.5,
                    marks={i / 10: str(i / 10) for i in range(0, 21, 5)},
                ),
                dbc.Form([
                    dbc.Label("Area unit: ", style={'white-space': 'pre'}),
                    dbc.RadioItems(
                        id="unit",
                        options=[{"label": "Minute", "value": False}, {"label": "Second", "value": True}],
                        value=False,
                        inline=True,
                    ),
                ], style={'display': 'flex', }),

                dbc.Form([
                    dbc.Label("Peak asymmetry: ", style={'white-space': 'pre'}),
                    dbc.RadioItems(
                        id="tailing",
                        options=[{"label": "Tailing", "value": "tailing"}, {"label": "Fronting", "value": "fronting"}],
                        value="tailing",
                        inline=True,
                    ),
                ], style={'display': 'flex', }),
                dbc.Button('Download plot CSV', id='plot-csv', color='primary', className='me-2'),
                dcc.Download(id="download-plot-csv"),

                dbc.Button('Download volume CSV', id='generate-button', color='success', className='me-2'),
                dcc.Download(id="download-all-csv"),
            ]),
            width=3
        ),

        # plot
        dbc.Col(
            html.Div([
                # html.H2("Peak analysis tool", style={"text-align": "center"}),
                html.Div(id='output-file-upload'),
                html.Div(id='output-deconvolution'),
                dcc.Graph(id="interactive-plot"),
            ]),
            width=9,
        ),
    ], style={'margin-left': '15px', 'margin-top': '25px', 'margin-right': '15px'})
])


@app.callback(
    Output("dropdown", "options"),
    Output('x-range-slider', 'min'),
    Output('x-range-slider', 'max'),
    Output('x-range-slider', 'value'),
    Output('x-range-slider', 'marks'),
    Output('output-file-upload', 'children'),
    Input("upload-data", "contents"),
    State("upload-data", "filename")
)
def update_widget(contents, filename):
    """
    when file is uploaded, update the dropdown menu and retention time range accordingly
    """
    if contents is None:
        return [], 0, 1, [0, 1], None, html.H5("Upload:\tno file! upload .csv or .UV file",
                                               style={'background-color': '#f8d7da', 'white-space': 'pre'})
    else:
        df = parse_contents(contents, filename)
        if not df.empty:
            x_data = df[df.columns[0]].values

            # update dropdown menu
            columns = df.columns.tolist()
            columns.pop(0)
            options = [{"label": option, "value": option} for option in columns]

            # update range slider
            x_range_min = min(x_data)
            x_range_max = max(x_data)
            x_range_value = [x_range_min, x_range_max]
            x_range = range(0, int(x_range_max) + 1, int(x_range_max) // 10 or 1)
            marks = {str(x): str(x) for x in x_range}

            return (options, x_range_min, x_range_max, x_range_value, marks,
                    html.H5(f"Upload:\tsuccess, {filename}",
                            style={'background-color': '#dcf8c6', 'white-space': 'pre'}))
        else:
            return [], 0, 1, [0, 1], None, html.H5("Upload:\tfile type not supported!",
                                                   style={'background-color': '#f8d7da', 'white-space': 'pre'})


@app.callback(
    Output("interactive-plot", "figure"),
    Output('output-deconvolution', 'children'),
    Input("peak-height", "value"),
    Input("smooth-window", "value"),
    Input("dropdown", "value"),
    Input("tailing", "value"),
    Input("unit", 'value'),
    Input('x-range-slider', 'value'),
    Input("peak-width", "value"),
    Input("smooth-derivative", "value"),
    Input("use-derivative", "value"),
    Input("show-derivative", "value"),
    Input("dead-volume", "value"),
    Input("max-peak-num", "value"),
    State("upload-data", "contents"),
    State('upload-data', 'filename'),
    prevent_initial_call=True,
)
def update_plot(peak_height, smooth_window, dropdown_value, tailing, area_in_second, range_of_interest, peak_width,
                smooth_derivative, use_derivative, show_derivative, dead_volume, max_peak_num, contents, filename):
    """
    Generate your plot based on the widget inputs
    """
    if contents is not None:
        df = parse_contents(contents, filename)
        peak_analysis_tool = PeakAnalysis(df) if not df.empty else None
    else:
        df = pd.DataFrame()
    if len(df.columns) == 2:
        # auto-select for non-time-course data (1-D)
        dropdown_value = df.columns[1]
    if dropdown_value in df.columns:
        # Generate the plot using the selected column
        fig, msg = peak_analysis_tool.peak_deconvolution(column_name=dropdown_value, smooth_window=smooth_window,
                                                         peak_width=peak_width / 1000, area_in_second=area_in_second,
                                                         peak_height=peak_height, smooth_derivative=smooth_derivative,
                                                         tailing_fronting=tailing, range_of_interest=range_of_interest,
                                                         use_derivative=use_derivative, dead_volume=dead_volume,
                                                         show_derivative=show_derivative, max_peak_num=max_peak_num
                                                         )
        # plot_df = DataFrame(peak_analysis_tool.plot)
        # peak_analysis_tool.plot.to_csv('filename.csv', index=False, encoding='utf-8')
        fig.update_layout(title_text=f"Selected Column: {dropdown_value}", height=800, )
        color = '#dcf8c6' if msg.startswith('success') else '#FDE2CD'
        return fig, html.H5(f"Analyze: \t{msg}", style={'background-color': color, 'white-space': 'pre'})
    else:
        # Return an empty figure if the selected column is not found
        return {}, html.H5("Analyze: \tplease select a column!",
                           style={'background-color': '#f8d7da', 'white-space': 'pre'})


def parse_contents(contents, filename: str = ''):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.DataFrame()
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        if filename.endswith('.UV'):
            # temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.' + filename.split('.')[-1])
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.UV')
            try:
                with open(temp_file.name, 'wb') as f:
                    f.write(decoded)
                df = read_uv(temp_file.name, )
            finally:
                temp_file.close()  # Explicitly close the temp file handle
                os.unlink(temp_file.name)  # Safely delete the file
            # os.unlink(temp_file.name)
        if df.shape[0] > 30000:
            df.iloc[::8, :]
        return df


@app.callback(
    Output("download-all-csv", "data"),
    Input('generate-button', 'n_clicks'),
    State('peak-shift', 'value'),
    State("peak-height", "value"),
    State("peak-width", "value"),
    State("smooth-window", "value"),
    State("tailing", "value"),
    State('x-range-slider', 'value'),
    State("smooth-derivative", "value"),
    State("use-derivative", "value"),
    State("dead-volume", "value"),
    State("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True,
)
def generate_csv(n_clicks, peak_shift,
                 peak_height, peak_width, smooth_window, tailing, range_of_interest, smooth_derivative,
                 use_derivative,
                 dead_volume,
                 contents, filename):
    if n_clicks is None or contents is None:
        return no_update
    df = parse_contents(contents, filename)
    if df.empty:
        return no_update
    hplc_analysis_tool = PeakAnalysis(df)
    hplc_analysis_tool.generate_report(smooth_window=smooth_window, peak_shift=peak_shift / 60,
                                       peak_height=peak_height, peak_width=peak_width / 1000,
                                       smooth_derivative=smooth_derivative,
                                       tailing_fronting=tailing, range_of_interest=range_of_interest,
                                       use_derivative=use_derivative, dead_volume=dead_volume,

                                       )
    output_filename = 'results.csv'
    return dcc.send_file(output_filename)


@app.callback(
    Output("download-plot-csv", "data"),
    Input('plot-csv', 'n_clicks'),
)
def plot_csv(n_clicks):
    if n_clicks is None:
        return no_update
    output_filename = 'plot_data.csv'
    return dcc.send_file(output_filename)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()

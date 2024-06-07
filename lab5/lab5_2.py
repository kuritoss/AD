import numpy as np
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Початкові значення параметрів
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
show_noise = True

previous_noise = None
previous_noise_mean = None
previous_noise_covariance = None

# Згенеруємо часовий ряд
t = np.linspace(0, 10, 1000)

# Фільтр для сигналу
def my_filter(signal, window_size=5):
    filtered_signal = np.zeros_like(signal)
    half_window = window_size // 2
    
    for i in range(len(signal)):
        start = max(0, i - half_window)
        end = min(len(signal), i + half_window + 1)
        filtered_signal[i] = np.mean(signal[start:end])
    
    return filtered_signal

# Створення головного вікна
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph'),
    html.Div([
        html.Label('Amplitude'),
        dcc.Slider(id='amplitude-slider', min=0.1, max=2, step=0.1, value=initial_amplitude),
        html.Label('Frequency'),
        dcc.Slider(id='frequency-slider', min=0.1, max=2, step=0.1, value=initial_frequency),
        html.Label('Phase'),
        dcc.Slider(id='phase-slider', min=0.0, max=2 * np.pi, step=0.1, value=initial_phase),
        html.Label('Noise Mean'),
        dcc.Slider(id='noise-mean-slider', min=-1.0, max=1.0, step=0.1, value=initial_noise_mean),
        html.Label('Noise Covariance'),
        dcc.Slider(id='noise-covariance-slider', min=0.1, max=1.0, step=0.1, value=initial_noise_covariance),
        html.Label('Window'),
        dcc.Slider(id='window', min=1, max=100, step=1, value=10),
        html.Label('Show Noise'),
        dcc.Checklist(id='show-noise-checkbox', options=[{'label': 'Show Noise', 'value': 'show'}], value=['show']),
        html.Button('Reset', id='reset-button', n_clicks=0),
        html.Label('Select Graph Type'),
        dcc.Dropdown(id='graph-type-dropdown',
                     options=[
                         {'label': 'Clean Signal', 'value': 'clean-signal'},
                         {'label': 'Filtered Signal', 'value': 'filtered-signal'}
                     ],
                     value='clean-signal'),
    ], style={'width': '50%', 'margin': 'auto'}),
    html.Div(id='selected-graph-container')
])

@app.callback(
    Output('graph', 'figure'),
    [
        Input('amplitude-slider', 'value'),
        Input('frequency-slider', 'value'),
        Input('phase-slider', 'value'),
        Input('noise-mean-slider', 'value'),
        Input('noise-covariance-slider', 'value'),
        Input('show-noise-checkbox', 'value'),
    ]
)
def update_graph(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    global previous_noise, previous_noise_mean, previous_noise_covariance
    
    # Перевірка, чи параметри шуму змінилися
    if (noise_mean != previous_noise_mean or
        noise_covariance != previous_noise_covariance):
        
        previous_noise_mean = noise_mean
        previous_noise_covariance = noise_covariance
        previous_noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
    
    noise = previous_noise if 'show' in show_noise else np.zeros(len(t))
    
    # Обчислення гармоніки
    y = amplitude * np.sin(2 * np.pi * frequency * t + phase) + noise
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Signal with Noise' if 'show' in show_noise else 'Signal'))
    
    # Додамо графіки сигналу без шуму та відфільтрованого шуму
    if 'show' in show_noise:
        clean_signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
        fig.add_trace(go.Scatter(x=t, y=clean_signal, mode='lines', name='Clean Signal'))
        
        filtered_noise = my_filter(previous_noise)
        signal_with_filtered_noise = clean_signal + filtered_noise
        fig.add_trace(go.Scatter(x=t, y=signal_with_filtered_noise, mode='lines', name='Signal with Filtered Noise'))
    
    return fig

@app.callback(
    Output('selected-graph-container', 'children'),
    [Input('graph-type-dropdown', 'value'),
     Input('amplitude-slider', 'value'),
     Input('frequency-slider', 'value'),
     Input('phase-slider', 'value'),
     Input('noise-mean-slider', 'value'),
     Input('noise-covariance-slider', 'value'),
     Input('show-noise-checkbox', 'value'),
     ]
    
)
def display_selected_graph(graph_type, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    if graph_type == 'clean-signal':
        return dcc.Graph(figure=update_graph(amplitude, frequency, phase, noise_mean, noise_covariance, []))
    elif graph_type == 'filtered-signal':
        return generate_filtered_signal_graph(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise)

def generate_filtered_signal_graph(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    # Фільтруємо шум
    filtered_noise = my_filter(previous_noise)
    # Отримуємо сигнал без шуму
    clean_signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    # Додаємо до нього відфільтрований шум
    signal_with_filtered_noise = clean_signal + filtered_noise
    # Побудова графіку
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=signal_with_filtered_noise, mode='lines', name='Signal with Filtered Noise'))
    return dcc.Graph(figure=fig)

@app.callback(
    Output('amplitude-slider', 'value'),
    Output('frequency-slider', 'value'),
    Output('phase-slider', 'value'),
    Output('noise-mean-slider', 'value'),
    Output('noise-covariance-slider', 'value'),
    Output('show-noise-checkbox', 'value'),
    [Input('reset-button', 'n_clicks')]
)
def reset_sliders(n_clicks):
    if n_clicks > 0:
        return initial_amplitude, initial_frequency, initial_phase, initial_noise_mean, initial_noise_covariance, ['show'],
    else:
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)
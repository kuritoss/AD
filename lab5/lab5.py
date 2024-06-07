import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
import scipy.signal as sig

# Функція гармоніки зі шумом
def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean=None, noise_covariance=None):
    global previous_noise, previous_noise_mean, previous_noise_covariance
    
    if noise_mean is None:
        noise_mean = previous_noise_mean
    if noise_covariance is None:
        noise_covariance = previous_noise_covariance

    if (noise_mean != previous_noise_mean or
        noise_covariance != previous_noise_covariance):
        
        previous_noise_mean = noise_mean
        previous_noise_covariance = noise_covariance

        previous_noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
    
    noise = previous_noise
    return amplitude * np.sin(2 * np.pi * frequency * t + phase) + noise

# Функція гармоніки без шуму
def harmonic(t, amplitude, frequency, phase):
    return amplitude * np.sin(2 * np.pi * frequency * t + phase)

# Функція для відфільтрування сигналу за допомогою фільтру Баттерворта
def butterworth_filter(signal, fs, cutoff_freq):
    order = 4 
    b, a = sig.butter(order, cutoff_freq / (fs / 2), btype='low')
    return sig.filtfilt(b, a, signal)

# Початкові значення параметрів
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1
show_noise = True
cutoff_freq = 60.0

previous_noise = None
previous_noise_mean = None
previous_noise_covariance = None

#часовий ряд
t = np.linspace(0, 10, 1000)
fs = 1000  

# Створення головного вікна
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.5)

# Побудова графіку
initial_signal = harmonic_with_noise(t, initial_amplitude, initial_frequency, initial_phase, initial_noise_mean, initial_noise_covariance)
l, = plt.plot(t, initial_signal, lw=2, linestyle ='--', color='red')
l_filtered, = plt.plot(t, initial_signal, lw=2, color='blue', alpha=0.5)
l_harmonic, = plt.plot(t, harmonic(t, initial_amplitude, initial_frequency, initial_phase), lw=2, color='green', linestyle='--')
l_harmonic.set_visible(False)

# Створення слайдерів
axcolor = 'lightgreen'
ax_amplitude = plt.axes([0.25, 0.4, 0.65, 0.03], facecolor=axcolor)
ax_frequency = plt.axes([0.25, 0.35, 0.65, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.25, 0.3, 0.65, 0.03], facecolor=axcolor)
ax_noise_mean = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_noise_covariance = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_cutoff_freq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

s_amplitude = Slider(ax_amplitude, 'Amplitude', 0.1, 20.0, valinit=initial_amplitude)
s_frequency = Slider(ax_frequency, 'Frequency', 0.1, 20.0, valinit=initial_frequency)
s_phase = Slider(ax_phase, 'Phase', 0.0, 2 * np.pi, valinit=initial_phase)
s_noise_mean = Slider(ax_noise_mean, 'Noise Mean', -1.0, 1.0, valinit=initial_noise_mean)
s_noise_covariance = Slider(ax_noise_covariance, 'Noise Covariance', 0.01, 1.0, valinit=initial_noise_covariance)
s_cutoff_freq = Slider(ax_cutoff_freq, 'Cutoff Frequency', 1, 100, valinit=cutoff_freq)

# Функція оновлення графіку при зміні параметрів
def update(val):
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val
    noise_mean = s_noise_mean.val
    noise_covariance = s_noise_covariance.val
    cutoff_freq = s_cutoff_freq.val
    
    if show_noise:
        signal_with_noise = harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance)
        l.set_ydata(signal_with_noise)

        # Відфільтрований сигнал
        filtered_signal = butterworth_filter(signal_with_noise, fs, cutoff_freq)
        l_filtered.set_ydata(filtered_signal)
        l_filtered.set_visible(True)  # Показуємо лінію l_filtered
        clean_signal = harmonic(t, amplitude, frequency, phase)
        l_harmonic.set_ydata(clean_signal)
        l_harmonic.set_visible(True)
    else:
        # Чистий сигнал без шуму
        clean_signal = harmonic(t, amplitude, frequency, phase)
        l.set_ydata(clean_signal)
        l_filtered.set_visible(False)  # Приховуємо лінію l_filtered
        l_harmonic.set_ydata(clean_signal)
        l_harmonic.set_visible(True)

    fig.canvas.draw_idle()


s_amplitude.on_changed(update)
s_frequency.on_changed(update)
s_phase.on_changed(update)
s_noise_mean.on_changed(update)
s_noise_covariance.on_changed(update)
s_cutoff_freq.on_changed(update)

# Створення чекбокса для перемикання відображення шуму
rax = plt.axes([0.025, 0.7, 0.15, 0.15], facecolor=axcolor)
check = CheckButtons(rax, ['Show Noise'], [show_noise])

def func(label):
    global show_noise
    show_noise = not show_noise
    update(None)  

check.on_clicked(func)

# Створення кнопки "Reset"
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    s_amplitude.reset()
    s_frequency.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_covariance.reset()
    s_cutoff_freq.reset()

button.on_clicked(reset)

plt.show()

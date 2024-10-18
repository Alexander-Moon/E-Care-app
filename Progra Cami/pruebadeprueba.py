import PySimpleGUI as sg

# Definir el color de fondo
color_fondo = '#a7c7e7'

# Layout de la pantalla del mapa
layout = [
    # Imagen del mapa con botones superpuestos
    [sg.Image(filename='Maps.png', key='-MAP-', size=(400, 400))],  # Imagen de mapa

    # Botones transparentes (en posiciones relativas a la imagen)
    [sg.Button('', button_color=(color_fondo, color_fondo), image_size=(50, 50), pad=((100, 0), (-380, 0)), border_width=0, key='-BTN1-')],
    [sg.Button('', button_color=(color_fondo, color_fondo), image_size=(50, 50), pad=((200, 0), (-440, 0)), border_width=0, key='-BTN2-')],
    [sg.Button('', button_color=(color_fondo, color_fondo), image_size=(50, 50), pad=((300, 0), (-500, 0)), border_width=0, key='-BTN3-')],

    # Barra de navegación inferior con tres botones
    [sg.Button('', image_filename='location_icon.png', button_color=(color_fondo, color_fondo), border_width=0, key='-LOC-'),
     sg.Button('', image_filename='user_icon.png', button_color=(color_fondo, color_fondo), border_width=0, key='-USER-'),
     sg.Button('', image_filename='group_icon.png', button_color=(color_fondo, color_fondo), border_width=0, key='-GROUP-')]
]

# Crear ventana
window = sg.Window("E-Care Map", layout, element_justification='center', size=(400, 600), background_color=color_fondo)

# Manejo de eventos
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    # Detectar eventos de los botones transparentes
    if event == '-BTN1-':
        sg.popup("Clicked on button 1")
    elif event == '-BTN2-':
        sg.popup("Clicked on button 2")
    elif event == '-BTN3-':
        sg.popup("Clicked on button 3")

window.close()

import PySimpleGUI as sg

# Definir el tema de colores
color_fondo = '#8acaf2'
sg.theme_background_color(color_fondo)
sg.theme_element_background_color(color_fondo)
sg.theme_text_color('white')

def login_window():
    layout = [
        [sg.Image(filename='login.png', background_color=color_fondo)],
        [sg.Text("Username / email", font=('Montserrat', 14), justification='left', pad=((0, 0), (10, 10)), background_color=color_fondo)],
        [sg.InputText(key='-USER-', size=(30, 1), pad=((0, 0), (0, 20)))],
        [sg.Text("Password", font=('Montserrat', 14), justification='left', pad=((0, 0), (10, 10)), background_color=color_fondo)],
        [sg.InputText(password_char='*', key='-PASS-', size=(30, 1), pad=((0, 0), (0, 20)))],
        [sg.Button("Continue", font=('Montserrat', 14), button_color=('white', color_fondo), border_width=0, size=(20, 1), pad=((0, 0), (20, 20)))]
    ]

    window = sg.Window("E-Care Login", layout, element_justification='center', size=(428, 886), background_color=color_fondo)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return None
        if event == 'Continue':
            window.close()
            return values

def location_window(image_filename):
    layout = [
        [sg.Image(filename=image_filename, pad=(0, 0))],
        [
            sg.Button(image_filename='locn.png', key='-BTN1-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10)),
            sg.Button(image_filename='usern.png', key='-BTN2-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10)),
            sg.Button(image_filename='comn.png', key='-BTN3-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10))
        ]
    ]

    window = sg.Window("Location Window", layout, element_justification='center', size=(428, 886))

    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-BTN2-':
            window.hide()
            user_window(window)
            window.un_hide()
        elif event == '-BTN3-':
            window.hide()
            community_window(window)
            window.un_hide()

    window.close()

def user_window(location_window):
    layout_user = [
        [
            sg.Button(image_filename='Settings.png', key='-USER_BTN1-', border_width=0, button_color=(color_fondo, color_fondo), pad=(10, 10)),
            sg.Image(filename='ecare.png', pad=(0, 0)),
            sg.Button(image_filename='Brain.png', key='-USER_BTN2-', border_width=0, button_color=(color_fondo, color_fondo), pad=(10, 10))
        ],
        [sg.Image(filename='Personal.png', pad=(0, 0))],
        [
            sg.Button(image_filename='locn.png', key='-BTN1-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10)),
            sg.Button(image_filename='usern.png', key='-BTN2-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10)),
            sg.Button(image_filename='comn.png', key='-BTN3-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10))
        ]
    ]

    window_user = sg.Window("User", layout_user, size=(428, 886))

    while True:
        event_user, _ = window_user.read()
        if event_user == sg.WIN_CLOSED or event_user == '-BACK_TO_MAP-':
            window_user.close()
            return
        if event_user == '-USER_BTN1-':
            window_user.hide()
            settings_window(window_user)
            window_user.un_hide()
        elif event_user == '-USER_BTN2-':
            window_user.hide()
            ia_window(window_user)
            window_user.un_hide()

    window_user.close()

def settings_window(previous_window):
    layout_settings = [
        [sg.Button(image_filename='Back.png', key='-BACK_TO_USER-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10)),
         sg.Image(filename='ecare.png', pad=(0, 0))],
        [sg.Image(filename='Settings.png', pad=(0, 0))]
    ]

    window_settings = sg.Window("Settings", layout_settings, size=(428, 886))

    while True:
        event_settings, _ = window_settings.read()
        if event_settings == sg.WIN_CLOSED:
            break
        if event_settings == '-LOG_OUT-':
            window_settings.close()
            sg.popup("Logged out")
            break  
        if event_settings == '-BACK_TO_USER-':
            window_settings.close()
            previous_window.un_hide()

def ia_window(previous_window):
    layout_additional = [
        [sg.Button(image_filename='Back.png', key='-BACK_TO_USER-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10))],
        [sg.Image(filename='IArecom.png', pad=(0, 0))],
    ]

    window_additional = sg.Window("Additional Window", layout_additional, size=(428, 886))

    while True:
        event_additional, _ = window_additional.read()
        if event_additional == sg.WIN_CLOSED or event_additional == '-BACK_TO_USER-':
            window_additional.close()
            break

def community_window(location_window):
    layout_community = [
        [
            sg.Button(image_filename='more.png', key='-COMM_BTN2-', border_width=0, button_color=(color_fondo, color_fondo), pad=(10, 10)),
            sg.Image(filename='ecare.png', pad=(0, 0)),
        ],
        [sg.Button(image_filename='Community.png', key='-COMM_BTN3-', border_width=0, button_color=(color_fondo, color_fondo), pad=(0, 0))],
        [
            sg.Button(image_filename='locn.png', key='-BTN1-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10)),
            sg.Button(image_filename='usern.png', key='-BTN2-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10)),
            sg.Button(image_filename='comn.png', key='-BTN3-', button_color=(color_fondo, color_fondo), border_width=0, pad=(10, 10))
        ]
    ]
    
    window_community = sg.Window("Community", layout_community, size=(428, 886))

    while True:
        event_community, _ = window_community.read()
        if event_community == sg.WIN_CLOSED:
            break
        if event_community == '-BACK_TO_MAP_COMM-':
            window_community.close()
            return
        if event_community == '-BTN1-':
            window_community.hide()
            location_window('Maps.png')
            window_community.un_hide()
        elif event_community == '-BTN2-':
            window_community.hide()
            user_window(window_community)
            window_community.un_hide()
        elif event_community == '-BTN3-':
            window_community.hide()
            community_window(window_community)
            window_community.un_hide()
        elif event_community == '-COMM_BTN2-':
            community_subwindow(window_community)
        elif event_community == '-COMM_BTN3-':
            window_community.hide()
            community_details_window(window_community)

    window_community.close()

def community_subwindow(previous_window):
    # Definir el layout con un botón de texto sin fondo
    layout_sub = [
        [sg.Button(image_filename='Back.png', key='-BACK_TO_COMMUNITY-', button_color=(color_fondo, color_fondo), pad=(0, 0))],
        [sg.Image(filename='Add.png', pad=(0, 0))],  # Cambia 'your_image.png' por la imagen deseada
        [sg.InputText(key='-INPUT-', size=(30, 1), pad=((0, 0), (0, 20)))],
        [sg.Button("Register", font=('Montserrat', 14), key='-REGISTER-', button_color=('white', color_fondo), border_width=0, pad=((0, 0), (20, 20)))],
        [sg.Text("", key='-MESSAGE-', size=(40, 1), visible=False, background_color=color_fondo, text_color='white')]  # Ajustamos el color de fondo y texto
    ]

    window_sub = sg.Window("Community Registration", layout_sub, size=(428, 886), element_justification='center', background_color=color_fondo)  # Añadido background_color

    while True:
        event_sub, values_sub = window_sub.read()
        if event_sub == sg.WIN_CLOSED or event_sub == '-BACK_TO_COMMUNITY-':
            window_sub.close()
            previous_window.un_hide()
            break
        if event_sub == '-REGISTER-':
            window_sub['-MESSAGE-'].update("Registrado correctamente", visible=True)

def community_details_window(previous_window):
    layout_details = [
        [sg.Button(image_filename='Back.png', key='-BACK_TO_COMMUNITY-', button_color=(color_fondo, color_fondo), pad=(0, 0)),
         sg.Image(filename='ecare.png', pad=(0, 0)),  # Primera imagen en la nueva pestaña
         sg.Button(image_filename='Brain.png', key='-OPEN_MORE-', button_color=(color_fondo, color_fondo), pad=(0, 0))],  # Botón para abrir otra pestaña
        [sg.Image(filename='Alexander.png', pad=(0, 0))]   # Segunda imagen
    ]

    window_details = sg.Window("Community Details", layout_details, size=(428, 886))

    while True:
        event_details, _ = window_details.read()
        if event_details == sg.WIN_CLOSED or event_details == '-BACK_TO_COMMUNITY-':
            window_details.close()
            previous_window.un_hide()
            break
        if event_details == '-OPEN_MORE-':
            window_details.hide()
            more_details_window(window_details)

def more_details_window(previous_window):
    layout_more_details = [
        [sg.Button(image_filename='Back.png', key='-BACK_TO_DETAILS-', button_color=(color_fondo, color_fondo), pad=(0, 0))],
        [sg.Image(filename='Alexanderbrain.png', pad=(0, 0))]  # Otra imagen en la nueva pestaña
    ]

    window_more_details = sg.Window("More Community Details", layout_more_details, size=(428, 886))

    while True:
        event_more_details, _ = window_more_details.read()
        if event_more_details == sg.WIN_CLOSED or event_more_details == '-BACK_TO_DETAILS-':
            window_more_details.close()
            previous_window.un_hide()
            break

if __name__ == "__main__":
    user_data = login_window()
    if user_data:
        location_window('Maps.png')

import random
import time
import threading
import PySimpleGUI as sg
import datetime
import json
import os
import logging

# Global variables
latest_data = {}
application_running = False
settings = {}
historical_anomalies = []
current_anomalies = set()
current_health_risks = set()
alerts = []
stop_event = threading.Event()

# --- Logging and Error Handling Functions ---


def initialize_logging():
    """
    Sets up logging configurations.
    """
    logging.basicConfig(
        filename="application.log",
        level=logging.DEBUG,  # Set to DEBUG for detailed logs
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="a",  # Append mode
    )


def log_event(event):
    """
    Records significant events.

    Args:
        event (str): Description of the event.
    """
    logging.info(event)


def handle_error(error):
    """
    Catches exceptions and logs errors.

    Args:
        error (Exception): The exception object.
    """
    logging.error(f"An error occurred: {error}", exc_info=True)
    sg.popup_error(f"An unexpected error occurred:\n{error}")


# --- Configuration Functions ---


def load_settings():
    """
    Loads settings from a JSON file or uses default values.

    Returns:
        dict: The settings dictionary.
    """
    default_settings = {
        "update_interval": 1,  # in seconds
        "normal_ranges": {
            "heart_rate": [60, 100],
            "systolic_bp": [90, 120],
            "diastolic_bp": [60, 80],
            "body_temperature": [36.1, 37.2],
            "respiratory_rate": [12, 20],
            "spo2": [95, 100],
        },
    }
    settings_file = "settings.json"
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
            log_event("Settings loaded from file.")
            return settings
        except Exception as e:
            handle_error(e)
            log_event("Using default settings due to error.")
            return default_settings
    else:
        log_event("Settings file not found. Using default settings.")
        return default_settings


def save_settings(settings):
    """
    Saves the settings to a JSON file.

    Args:
        settings (dict): The settings dictionary.
    """
    settings_file = "settings.json"
    try:
        with open(settings_file, "w") as f:
            json.dump(settings, f, indent=4)
        log_event("Settings saved to file.")
    except Exception as e:
        handle_error(e)


def apply_settings():
    """
    Applies settings to the application.
    """
    # Additional application-specific setup can be done here
    pass


# --- Data Simulation Functions ---


def simulate_sensor_data():
    """
    Generates random biometric data for testing purposes.

    Returns:
        dict: Simulated sensor data.
    """
    heart_rate = random.randint(60, 100)
    systolic_bp = random.randint(110, 140)
    diastolic_bp = random.randint(70, 90)
    body_temperature = round(random.uniform(36.5, 37.5), 1)
    respiratory_rate = random.randint(12, 20)
    spo2 = random.randint(95, 100)

    data = {
        "heart_rate": heart_rate,
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,
        "body_temperature": body_temperature,
        "respiratory_rate": respiratory_rate,
        "spo2": spo2,
    }

    return data


def update_sensor_data(data_container):
    """
    Updates the simulated data at regular intervals.

    Args:
        data_container (dict): The container to store the latest data.
    """

    def data_updater():
        try:
            while not stop_event.is_set():
                new_data = simulate_sensor_data()
                data_container.clear()
                data_container.update(new_data)
                time.sleep(settings.get("update_interval", 1))
        except Exception as e:
            handle_error(e)
            stop_event.set()

    updater_thread = threading.Thread(target=data_updater, daemon=True)
    updater_thread.start()


# --- Data Processing and AI Analysis Functions ---


def process_sensor_data(data):
    """
    Cleans and preprocesses the raw sensor data.

    Args:
        data (dict): Raw sensor data.

    Returns:
        dict: Processed sensor data.
    """
    processed_data = data.copy()

    # Handle missing values
    for key, value in processed_data.items():
        if value is None:
            if key == "heart_rate":
                processed_data[key] = 80
            elif key == "systolic_bp":
                processed_data[key] = 120
            elif key == "diastolic_bp":
                processed_data[key] = 80
            elif key == "body_temperature":
                processed_data[key] = 37.0
            elif key == "respiratory_rate":
                processed_data[key] = 16
            elif key == "spo2":
                processed_data[key] = 98

    return processed_data


def detect_anomalies(data):
    """
    Identifies abnormal readings in the sensor data.

    Args:
        data (dict): Processed sensor data.

    Returns:
        dict: Anomalies detected.
    """
    anomalies = {}

    normal_ranges = settings.get("normal_ranges", {})

    for key, value in data.items():
        range_values = normal_ranges.get(key)
        if range_values:
            lower, upper = range_values
            if lower <= value <= upper:
                anomalies[key] = "normal"
            else:
                anomalies[key] = "abnormal"
        else:
            anomalies[key] = "unknown"

    return anomalies


def predict_health_risks(data, anomalies, history=historical_anomalies):
    """
    Predicts potential health risks based on sensor data and detected anomalies.

    Args:
        data (dict): Processed sensor data.
        anomalies (dict): Detected anomalies.
        history (list): Historical anomalies.

    Returns:
        list: Predicted health risks.
    """
    health_risks = []

    # Add current anomalies to history
    history.append(anomalies.copy())

    # Keep only the last N readings for analysis
    N = 5
    if len(history) > N:
        history.pop(0)

    # Check for persistent anomalies
    for parameter in anomalies.keys():
        abnormal_count = sum(
            1 for record in history if record.get(parameter) == "abnormal"
        )
        if abnormal_count >= N:
            risk_message = f"Persistent abnormal {parameter} over last {N} readings."
            if risk_message not in health_risks:
                health_risks.append(risk_message)

    return health_risks


# --- Alerts and Notifications Functions ---


def generate_alert(message, level):
    """
    Creates an alert with a specified severity level.

    Args:
        message (str): The alert message.
        level (str): The severity level ('info', 'warning', 'critical').
    """
    if level not in ["info", "warning", "critical"]:
        level = "info"  # Default to 'info' if invalid level provided
    alert = {"message": message, "level": level, "timestamp": datetime.datetime.now()}
    alerts.append(alert)
    log_alert(alert)


def display_alerts(window):
    """
    Updates the UI to show active alerts.

    Args:
        window: The PySimpleGUI window object.
    """
    # Display the last few alerts
    MAX_ALERTS_DISPLAYED = 5
    recent_alerts = alerts[-MAX_ALERTS_DISPLAYED:]
    alerts_text = ""
    for alert in recent_alerts:
        timestamp = alert["timestamp"].strftime("%H:%M:%S")
        alerts_text += f"[{timestamp}] {alert['level'].upper()}: {alert['message']}\n"
    window["alerts"].update(alerts_text)


def log_alert(alert):
    """
    Records alerts for future reference.

    Args:
        alert (dict): The alert to log.
    """
    with open("alerts.log", "a") as f:
        timestamp = alert["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - {alert['level'].upper()}: {alert['message']}\n"
        f.write(log_message)
    log_event(f"Alert logged: {alert['message']}")


# --- UI Functions ---


def create_main_window():
    """
    Defines the main window layout, including data displays and alert sections.

    Returns:
        window: The PySimpleGUI window object.
    """
    sg.theme("LightBlue")

    # Define the GUI layout
    layout = [
        [
            sg.Text(
                "Simulated Biometric Data",
                size=(30, 1),
                font=("Helvetica", 16),
                justification="center",
            )
        ],
        [sg.HorizontalSeparator()],
        [sg.Text("Heart Rate:", size=(20, 1)), sg.Text("", key="heart_rate")],
        [sg.Text("Systolic BP:", size=(20, 1)), sg.Text("", key="systolic_bp")],
        [sg.Text("Diastolic BP:", size=(20, 1)), sg.Text("", key="diastolic_bp")],
        [
            sg.Text("Body Temperature:", size=(20, 1)),
            sg.Text("", key="body_temperature"),
        ],
        [
            sg.Text("Respiratory Rate:", size=(20, 1)),
            sg.Text("", key="respiratory_rate"),
        ],
        [sg.Text("Oxygen Saturation (SpO₂):", size=(20, 1)), sg.Text("", key="spo2")],
        [sg.HorizontalSeparator()],
        [sg.Text("Anomalies Detected:", font=("Helvetica", 12))],
        [sg.Multiline("", size=(50, 4), key="anomalies", disabled=True)],
        [sg.Text("Health Risks:", font=("Helvetica", 12))],
        [sg.Multiline("", size=(50, 4), key="health_risks", disabled=True)],
        [sg.HorizontalSeparator()],
        [sg.Text("Alerts:", font=("Helvetica", 12))],
        [sg.Multiline("", size=(50, 6), key="alerts", disabled=True, autoscroll=True)],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Start", size=(10, 1)),
            sg.Button("Stop", size=(10, 1), disabled=True),
            sg.Button("Settings", size=(10, 1)),
            sg.Button("Exit", size=(10, 1)),
        ],
    ]

    # Create the window
    window = sg.Window("Health Monitoring System", layout, finalize=True)
    return window


def create_login_window():
    """
    Provides a login interface for user authentication.

    Returns:
        window: The PySimpleGUI window object.
    """
    sg.theme("LightBlue")

    layout = [
        [sg.Text("Please enter your login credentials")],
        [sg.Text("Username:", size=(10, 1)), sg.Input(key="username")],
        [
            sg.Text("Password:", size=(10, 1)),
            sg.Input(key="password", password_char="*"),
        ],
        [sg.Button("Login"), sg.Button("Cancel")],
    ]

    window = sg.Window("Login", layout)
    return window


def create_settings_window(current_settings):
    """
    Allows users to adjust application settings.

    Args:
        current_settings (dict): The current settings.

    Returns:
        window: The PySimpleGUI window object.
    """
    sg.theme("LightBlue")

    # Extract current settings
    update_interval = current_settings.get("update_interval", 1)
    normal_ranges = current_settings.get("normal_ranges", {})

    layout = [
        [sg.Text("Settings", font=("Helvetica", 16))],
        [
            sg.Text("Update Interval (seconds):"),
            sg.InputText(update_interval, key="update_interval"),
        ],
        [sg.Text("Normal Ranges:", font=("Helvetica", 12))],
    ]

    # Add inputs for each parameter's normal range
    for param, range_values in normal_ranges.items():
        lower, upper = range_values
        layout.append(
            [
                sg.Text(f"{param}:"),
                sg.Text("Lower:"),
                sg.InputText(lower, size=(5, 1), key=f"{param}_lower"),
                sg.Text("Upper:"),
                sg.InputText(upper, size=(5, 1), key=f"{param}_upper"),
            ]
        )

    layout.append([sg.Button("Save"), sg.Button("Cancel")])

    window = sg.Window("Settings", layout)
    return window


# --- Event Handling Functions ---


def handle_events(event, values, window):
    """
    Responds to UI events (e.g., button clicks).

    Args:
        event: The event that occurred.
        values: The values from the window elements.
        window: The PySimpleGUI window object.

    Returns:
        bool: True to continue the event loop, False to exit.
    """
    global application_running, settings, stop_event

    try:
        if event == sg.WIN_CLOSED or event == "Exit":
            # Stop the data updater thread
            stop_event.set()
            log_event("Application exit requested.")
            return False  # Signal to exit the event loop

        elif event == "Start":
            if not application_running:
                application_running = True
                stop_event.clear()
                # Start updating sensor data
                update_sensor_data(latest_data)
                window["Start"].update(disabled=True)
                window["Stop"].update(disabled=False)
                log_event("Data simulation started.")

        elif event == "Stop":
            if application_running:
                application_running = False
                # Signal the data updater thread to stop
                stop_event.set()
                window["Start"].update(disabled=False)
                window["Stop"].update(disabled=True)
                log_event("Data simulation stopped.")

        elif event == "Settings":
            # Open the settings window
            settings_window = create_settings_window(settings)
            log_event("Settings window opened.")
            while True:
                s_event, s_values = settings_window.read()
                if s_event == sg.WIN_CLOSED or s_event == "Cancel":
                    settings_window.close()
                    log_event("Settings window closed without saving.")
                    break
                elif s_event == "Save":
                    # Update settings
                    try:
                        settings["update_interval"] = float(s_values["update_interval"])
                        for param in settings["normal_ranges"]:
                            lower = float(s_values[f"{param}_lower"])
                            upper = float(s_values[f"{param}_upper"])
                            settings["normal_ranges"][param] = [lower, upper]
                        save_settings(settings)
                        apply_settings()
                        sg.popup("Settings saved successfully.")
                        settings_window.close()
                        log_event("Settings updated and saved.")
                        break
                    except ValueError as ve:
                        sg.popup("Please enter valid numeric values.")
                        log_event(f"Invalid input in settings: {ve}")
                        continue

        return True  # Continue the event loop

    except Exception as e:
        handle_error(e)
        return True  # Continue the event loop despite the error


def update_ui(window, processed_data, anomalies, health_risks):
    """
    Refreshes UI elements with new data.

    Args:
        window: The PySimpleGUI window object.
        processed_data (dict): The processed sensor data.
        anomalies (dict): The detected anomalies.
        health_risks (list): The predicted health risks.
    """
    # Update the GUI elements with the latest data
    window["heart_rate"].update(f"{processed_data.get('heart_rate', 'N/A')} bpm")
    window["systolic_bp"].update(f"{processed_data.get('systolic_bp', 'N/A')} mmHg")
    window["diastolic_bp"].update(f"{processed_data.get('diastolic_bp', 'N/A')} mmHg")
    window["body_temperature"].update(
        f"{processed_data.get('body_temperature', 'N/A')} °C"
    )
    window["respiratory_rate"].update(
        f"{processed_data.get('respiratory_rate', 'N/A')} breaths/min"
    )
    window["spo2"].update(f"{processed_data.get('spo2', 'N/A')} %")

    # Display anomalies
    abnormal_parameters = [
        key for key, status in anomalies.items() if status == "abnormal"
    ]
    if abnormal_parameters:
        anomalies_text = ", ".join(abnormal_parameters)
    else:
        anomalies_text = "None"
    window["anomalies"].update(anomalies_text)

    # Display health risks
    if health_risks:
        risks_text = "\n".join(health_risks)
    else:
        risks_text = "None"
    window["health_risks"].update(risks_text)

    # Display alerts
    display_alerts(window)


def run_event_loop(window):
    """
    Main loop that keeps the application running and responsive.

    Args:
        window: The PySimpleGUI window object.
    """
    global application_running, current_anomalies, current_health_risks

    try:
        while True:
            event, values = window.read(timeout=500)

            # Handle events
            continue_loop = handle_events(event, values, window)
            if not continue_loop:
                break

            if application_running:
                # Get the latest data
                raw_data = latest_data.copy()

                # Process the sensor data
                processed_data = process_sensor_data(raw_data)

                # Detect anomalies
                anomalies = detect_anomalies(processed_data)

                # Generate alerts for new anomalies
                new_anomalies = set()
                for parameter, status in anomalies.items():
                    if status == "abnormal":
                        new_anomalies.add(parameter)
                        if parameter not in current_anomalies:
                            message = f"{parameter} reading is abnormal: {processed_data.get(parameter)}"
                            generate_alert(message, level="warning")
                            log_event(f"Alert generated: {message}")
                # Update current anomalies
                current_anomalies = new_anomalies

                # Predict health risks
                health_risks = predict_health_risks(processed_data, anomalies)

                # Generate alerts for new health risks
                new_health_risks = set(health_risks)
                for risk in new_health_risks:
                    if risk not in current_health_risks:
                        generate_alert(risk, level="critical")
                        log_event(f"Critical alert generated: {risk}")
                # Update current health risks
                current_health_risks = new_health_risks

                # Update the UI
                update_ui(window, processed_data, anomalies, health_risks)
    except Exception as e:
        handle_error(e)


# --- Main Application ---


def main():
    global settings

    # Initialize logging
    initialize_logging()
    log_event("Application started.")

    try:
        # Load settings
        settings = load_settings()
        apply_settings()
        log_event("Settings loaded successfully.")

        # Create the login window (optional)
        login_window = create_login_window()
        authenticated = False

        while True:
            event, values = login_window.read()
            if event == sg.WIN_CLOSED or event == "Cancel":
                login_window.close()
                log_event("User canceled login or closed the window.")
                return  # Exit the application
            elif event == "Login":
                username = values["username"]
                password = values["password"]
                # For demonstration, we'll accept any username/password
                authenticated = True  # In real application, verify credentials
                login_window.close()
                log_event(f"User '{username}' logged in.")
                break

        if not authenticated:
            log_event("User not authenticated. Exiting application.")
            return  # Exit if not authenticated

        # Create the main window
        window = create_main_window()
        log_event("Main window created.")

        # Run the event loop
        run_event_loop(window)

        # Close the window
        window.close()
        log_event("Application closed.")

    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    main()

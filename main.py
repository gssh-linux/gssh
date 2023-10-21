import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
gi.require_version('Gio', '2.0')
from gi.repository import Gtk, Vte, GLib, Gdk, Gio
import subprocess
import os
import time
import json

try:
  port_file = open("settings.json")
  value = json.load(port_file)
  saved_port = value["port"]
except:
 saved_port = 22


# Initialize the GTK application
app = Gtk.Application()
# Function to open the settings window
def open_settings_window(button):
    settings_window = Gtk.Window(title="Settings")
    settings_window.set_default_size(300, 200)

    # Create settings widgets (e.g., buttons, entries, labels) here
    # Create an entry for SSH port
    port_entry = Gtk.Entry()
    port_entry.set_text(str(get_saved_setting("port", 22)))  # Initialize with the default value

    # Add settings widgets to a vertical box
    settings_vbox = Gtk.VBox()
    settings_vbox.pack_start(Gtk.Label("SSH Default Port:"), False, False, 5)
    settings_vbox.pack_start(port_entry, False, False, 5)

    # Create a "Save" button to save settings
    save_button = Gtk.Button(label="Save")
    save_button.connect("clicked", lambda btn: save_settings(port_entry.get_text()))
    settings_vbox.pack_end(save_button, False, False, 5)

    settings_window.add(settings_vbox)
    settings_window.show_all()

# Function to save settings to a JSON file
def save_settings(port):
    global saved_port
    settings = {
        "port": int(port),  # Convert the port to an integer
        # Add more settings here
    }
    with open("settings.json", "w") as f:
        json.dump(settings, f)
    saved_port = int(port)

def get_saved_setting(setting_name, default_value):
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            return settings.get(setting_name, default_value)
    except FileNotFoundError:
        return default_value

    
def generate_ssh_key(key_name, file_path):
    try:

        # Ensure the chosen directory is in /home
        if not file_path.startswith("/home"):
            raise ValueError("SSH keys must be saved in /home directory")

        # Ensure the file doesn't exist by appending a timestamp to the filename
        timestamp = int(time.time())
        unique_file_path = f"{file_path}_{timestamp}"

        # Generate SSH keys without a passphrase
        ssh_keygen_command = f"ssh-keygen -t rsa -b 4096 -N \"\" -C {key_name} -f {unique_file_path}"

        subprocess.run(ssh_keygen_command, shell=True, check=True)

        # Rename the generated file to the original filename
        os.rename(unique_file_path, file_path)
        
        return True, None
    except Exception as e:
        return False, str(e)


# Function to handle the "Generate SSH keys" button click event
def generate_ssh_keys(button):
    dialog = Gtk.FileChooserDialog(
        "Save SSH Keys",
        None,
        Gtk.FileChooserAction.SAVE,
        (
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        ),
    )

    # Add a "Name" entry to specify the key name
    name_label = Gtk.Label("Name:")
    name_entry = Gtk.Entry()
    dialog.set_extra_widget(name_label)
    dialog.set_extra_widget(name_entry)

    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        # Get the chosen file path and name from the dialog
        file_path = dialog.get_filename()
        key_name = name_entry.get_text()
        if not key_name:
            key_name = "id_rsa"  # Default key name

        success, error_message = generate_ssh_key(key_name, file_path)
        
        if success:
            print("SSH key generation successful.")
        else:
            print(f"SSH key generation failed: {error_message}")

    dialog.destroy()





# Create a function to set the GTK theme based on the system's theme
def set_gtk_theme():
    # Get the current system theme name
    screen = Gdk.Screen.get_default()
    settings = Gtk.Settings.get_for_screen(screen)
    current_theme = settings.get_property("gtk-theme-name")
    print(f"Current theme: {current_theme}")
    # Set the GTK theme for the application
    Gtk.Settings.get_default().set_property("gtk-theme-name", current_theme)

# Call the function to set the initial GTK theme
set_gtk_theme()


# Function to handle the button click event
# Global variable to store the terminal process
terminal_process = None

def on_button_clicked(button):
    global terminal_process
    ip = ip_entry.get_text()
    user = user_entry.get_text()
    

    if ":" in ip:
     ssh_command = f"ssh {user}@{ip}"
    else:
     # Create the SSH command
     ssh_command = f"ssh {user}@{ip} -p {saved_port}" 

    # Create a new terminal widget
    terminal = Vte.Terminal()
    terminal.set_size(200, 200)  # Set the terminal size as desired
    terminal.spawn_sync(
        Vte.PtyFlags.DEFAULT,
        None,
        ["/bin/bash", "-c", ssh_command],
        [],
        GLib.SpawnFlags.DEFAULT,
        None,
        None,
    )

    # Create a window for the terminal
    terminal_window = Gtk.Window(title="SSH Terminal")
    terminal_window.connect("delete-event", on_terminal_window_close, terminal)
    terminal_window.add(terminal)

    # Show the terminal window
    terminal_window.show_all()

    # Store the terminal process
    terminal_process = terminal

# Function to handle the terminal window close event
def on_terminal_window_close(window, terminal):
    global terminal_process
    if terminal_process:
        # Kill the SSH process when the terminal window is closed
        terminal_process.feed_child("\x03")  # Send Ctrl+C to terminate the SSH process
        terminal_process = None
    window.destroy()





window = Gtk.Window(title="GSSH")
window.connect("delete-event", Gtk.main_quit)
window.set_default_size(400, 400)  # Set the window size to 400x400

# Create input fields
ip_label = Gtk.Label(label="IP Address:")
ip_entry = Gtk.Entry()
user_label = Gtk.Label(label="User:")
user_entry = Gtk.Entry()

# Create a button
button = Gtk.Button(label="Connect")
button.connect("clicked", on_button_clicked)

# Create a button to generate SSH keys
generate_button = Gtk.Button(label="Generate SSH Keys")
generate_button.connect("clicked", generate_ssh_keys)

# Create a vertical box to hold the widgets
vbox = Gtk.VBox()
vbox.pack_start(ip_label, False, False, 10)  # Increased spacing for better layout
vbox.pack_start(ip_entry, False, False, 10)
vbox.pack_start(user_label, False, False, 10)
vbox.pack_start(user_entry, False, False, 10)
vbox.pack_start(button, False, False, 10)
vbox.pack_start(generate_button, False, False, 10)


# Create a button to open the settings window
settings_button = Gtk.Button(label="Settings")
settings_button.connect("clicked", open_settings_window)
vbox.pack_start(settings_button, False, False, 10)  
window.add(vbox)

window.show_all()
Gtk.main()

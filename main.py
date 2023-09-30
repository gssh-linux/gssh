import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
gi.require_version('Gio', '2.0')
from gi.repository import Gtk, Vte, GLib, Gdk, Gio
import subprocess
import os
import time
# Initialize the GTK application
app = Gtk.Application()

# Function to handle the "Mount" button click event
def on_mount_button_clicked(button):
    ip = ip_entry.get_text()
    user = user_entry.get_text()
    mount_point = "/app/mountdir"
    # Create the SSHFS mount command
    sshfs_command = f"sshfs {user}@{ip}:/ {mount_point}"

    try:
        # Mount the remote SSH server files using SSHFS
        subprocess.run(sshfs_command, shell=True, check=True)

        # Open the file manager using xdg-open on the mounted directory
        subprocess.Popen(["xdg-open", mount_point])

        print("SSH server files mounted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        # Handle any error that occurs during mounting here

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


# Global variable to store the terminal process
terminal_process = None

# Function to handle the button click event
def on_button_clicked(button):
    global terminal_process
    ip = ip_entry.get_text()
    user = user_entry.get_text()

    # Create the SSH command
    ssh_command = f"ssh {user}@{ip}"

    # Create a new terminal widget
    terminal = Vte.Terminal()
    terminal.set_size(400, 400)  # Set the terminal size as desired
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
ip_label = Gtk.Label(label="IP:")
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

window.add(vbox)

window.show_all()
Gtk.main()

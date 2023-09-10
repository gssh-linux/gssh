import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Function to handle the button click event
def on_button_clicked(button):
    ip = ip_entry.get_text()
    user = user_entry.get_text()
    password = password_entry.get_text()

    # Create the SSH command
    ssh_command = f"ssh {user}@{ip}"

    # Launch a new terminal window with the SSH command
    subprocess.Popen(["flatpak spawn --host gnome-terminal", "--", "/bin/bash", "-c", ssh_command])

window = Gtk.Window(title="GSSH")
window.connect("delete-event", Gtk.main_quit)
window.set_default_size(400, 300)  # Set the window size to 2x (800x600)

# Create input fields
ip_label = Gtk.Label(label="IP:")
ip_entry = Gtk.Entry()
user_label = Gtk.Label(label="User:")
user_entry = Gtk.Entry()
password_label = Gtk.Label(label="Password:")
password_entry = Gtk.Entry()
password_entry.set_visibility(False)  # To hide the password as you type

# Create a button
button = Gtk.Button(label="Connect")
button.connect("clicked", on_button_clicked)

# Create a vertical box to hold the widgets
vbox = Gtk.VBox()
vbox.pack_start(ip_label, False, False, 10)  # Increased spacing for better layout
vbox.pack_start(ip_entry, False, False, 10)
vbox.pack_start(user_label, False, False, 10)
vbox.pack_start(user_entry, False, False, 10)
vbox.pack_start(password_label, False, False, 10)
vbox.pack_start(password_entry, False, False, 10)
vbox.pack_start(button, False, False, 10)
window.add(vbox)

window.show_all()
Gtk.main()

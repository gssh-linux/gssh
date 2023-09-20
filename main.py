import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GLib, Gdk
# Initialize the GTK application
app = Gtk.Application()

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

# Create a vertical box to hold the widgets
vbox = Gtk.VBox()
vbox.pack_start(ip_label, False, False, 10)  # Increased spacing for better layout
vbox.pack_start(ip_entry, False, False, 10)
vbox.pack_start(user_label, False, False, 10)
vbox.pack_start(user_entry, False, False, 10)
vbox.pack_start(button, False, False, 10)

window.add(vbox)

window.show_all()
Gtk.main()

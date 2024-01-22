import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
gi.require_version('Gio', '2.0')
from gi.repository import Gtk, Vte, GLib, Gdk, Gio
import sys

if len(sys.argv) != 3:
    print("Usage: python main.py ip user")
    sys.exit(1)  # Exit with an error code

# Access command-line arguments
ip = sys.argv[1]
user = sys.argv[2]


# Initialize the GTK application
app = Gtk.Application()

# Function to handle the button click event
# Global variable to store the terminal process
terminal_process = None


def on_button_clicked():
    global terminal_process
    ssh_command = f"ssh {user}@{ip}"

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
    terminal_window.resize(700, 500)
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

on_button_clicked()
Gtk.main()


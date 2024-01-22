const { app, BrowserWindow, Menu} = require('electron')
const python = require('python-shell')
const path = require('path')
Menu.setApplicationMenu(null)
const createWindow = () => {
    const win = new BrowserWindow({
        width: 400,
        height: 500,
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    })

    win.loadFile('index.html')
}
app.whenReady().then(() => {
    createWindow()
})
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})

function process_connection() {
   var ip = document.getElementById("sshHost").value;
   var user = document.getElementById("sshUser").value;

   var options = {
       scriptPath: path.join(__dirname, '/engine/'),
       args: [ip, user]
   }

   var sshConnection = new python('main.py', options)

   sshConnection.on('message', function(message) {
       console.log(message);
   })
    var python_code = `on_button_clicked("${ip}", "${user}")`
    console.log(python_code)
    // Send the code to be executed

}

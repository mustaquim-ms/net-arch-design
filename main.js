// This is the main entry point for the Electron application.
// It initializes the Electron app and creates the main window.
// The preload script is specified to securely expose APIs to the renderer process.
// The application is set to load a local URL or file, depending on the development or production
// environment.
// The main window is created with specified dimensions and web preferences.
// The application listens for the 'ready' event to create the window and handles
// the 'window-all-closed' event to quit the app when all windows are closed,
// except on macOS where it is common to keep the app running until the user explicitly quits
// the application.
// This file is essential for the Electron app to function correctly.
// It is responsible for setting up the main application window and loading the frontend application.
// It is typically located in the root directory of the Electron project.
// The preload script is used to expose APIs securely to the renderer process.
// It creates the main application window and loads the frontend application.   


const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  win.loadURL('http://localhost:5173'); // or loadFile('dist/index.html') after build
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

var LocalDevices = require('local-devices');
const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
var ip = ""
var mainAddr = ip+":5000";
var rq = require('request-promise');
var mainWindow = null;
function start(){
  LocalDevices().then(devices => {
    console.log(devices);
    console.log("here2");
    devices.forEach(d => {
        if(d.name=="dex.lan")
        {
          mainAddr = "http://"+d.ip +":5000/"
          console.log(mainAddr);
          startUp()
        }
    })

    });
  }
app.on('window-all-closed', function() {

    app.quit();
});
function run()
{
  console.log("run")


  // fire!
  //startUp();
}

var openWindow = function(){
  mainWindow = new BrowserWindow({width: 1000, height:800});
  // mainWindow.loadURL('file://' + __dirname + '/index.html');
  mainWindow.loadURL(mainAddr,{"extraHeaders" : "pragma: no-cache\n"});
  mainWindow.on('closed', function() {
    mainWindow = null;
  });
};

var startUp = function(){
  console.log("here")
  rq(mainAddr)
    .then(function(htmlString){
      console.log('server started!');
      openWindow();
    })
    .catch(function(err){
      //console.log('waiting for the server start...');
      startUp();
    });
};
app.on('ready', start)

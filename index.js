// * index.js 
// * minimal Express Socket.io websocket server 
// * run basic receiving server:
// ```$ node index```
// * run basic receiving server and a trivial e2e-broadcast simulation:
// ```$ node index e2e``` <br>
// index cmdline arg can be any char or string
// * Socket.io websocket channels use default port 8081
// * present channels are [1] a bi-directional 'sf' channel 
//   and [2] an in-only 'log' channel


// Setup basic Nodejs server
var fs = require('fs'),
    path = require('path'),
    io = require('socket.io')(),
    //exec = require("child-process"),
    live_server = require("live-server"),
    params = {
      host: "tosca",
      port: 8080,
      ignore: "."   // must turn off auto-reload or client is created each time 
    }
    argv = process.argv,
    port = argv[2] || 8081;                      //cmdline or default
    today = (new Date().toJSON()).replace(/T.*/, ''),
    index = 0;                                  // client indices



// start live-server
live_server.start(params);
console.log("launching live-server watching only root dir for auto re-start");


// write GMT-today directory (if needed)
try {
  fs.mkdirSync('./sf/' + today);
} catch(e) {
  if ( e.code != 'EEXIST' ) throw e;
}



// make connection - handle channel events<br>
// create timestamp-named sf-file and log-file per client
io.on('connection', function (socket) {
  var _index = index,      // this client index
      q,
      p = function(){
        return (new Date().toJSON()).replace(/^.*T/, '').replace(/Z/,
        '').replace(/\..+$/, '').replace(/:/g,'-');
      },
      t = function(){
        return (new Date().toJSON()).replace(/^.*T/, '').replace(/Z/, '');
      },
      now = p(), 
      sffile = './sf/' + today + '/' + now + '-client' + _index + '.sf',
      start,
      dt;


  console.log(`\nclient ${index++} makes connection `);

  // diagnostics
  console.log("\nconnection diagnostics:");
  console.log(`sffile = ${sffile}`);
  console.log(`today = ${today}`);
  console.log(`GMT timestamp = ${t()}`);
  console.log(`GMT time for filename = ${p()}`);
  argv.forEach(function(a, i){
    console.log(`argv[${i}] = ${argv[i]}`);
  });


  // handler to record sf (in)
  socket.on("sf", function(data){
    fs.appendFile(sffile, data, function(err) {
      if(err) {
        return console.log(err);
      }
      console.log(`\nappended data ${data} to csv ${sffile}`);
    }); 
  });
});


// start listening for client connection requests
io.listen(port);
console.log("Socket.io sound Server listening at port %d", port);


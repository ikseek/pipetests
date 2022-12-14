fs = require('fs')

let pipe_read = parseInt(process.argv[2]);
let pipe_write = parseInt(process.argv[3]);

function read_to_eof(err, n, bytes) {
    if (err) {
        if (err.code === 'EOF') {
            console.error("Child reached pipe EOF as error, happens on windows");
            console.error("Child terminating");
            process.exit(0);
        } else {
            console.error("Child pipe read error %s", err);
        }
    } else if (n === 0) {
        console.error("Child reached pipe EOF normally");
        console.error("Child terminating");
        process.exit(0);
    } else {
        console.error("Child read %s bytes: %s", n, bytes);
        fs.read(pipe_read, read_to_eof);
    }
}

console.error("Child started with pipe r %s w %s", pipe_read, pipe_write);
console.error("Child closing write side")
fs.close(pipe_write, (err) => { if (err) console.error("Child failed to close write side: %s", err);});
console.error("Child outputs dummy listen port")
console.log("42");
console.error("Child is waiting for EOF in pipe");
fs.read(pipe_read, read_to_eof);

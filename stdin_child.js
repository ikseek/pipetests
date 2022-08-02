fs = require('fs')

let pipe_read = 0;

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

console.error("Child started");
console.error("Child outputs dummy listen port")
console.log("42");
console.error("Child is waiting for EOF in pipe");
fs.read(pipe_read, read_to_eof);

function should_not_run() {
  console.error("Child should not print it, should terminate earlier");
}
setTimeout(should_not_run, 5000);

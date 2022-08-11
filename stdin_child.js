fs = require('fs')

console.error("Child started");
console.error("Child outputs dummy listen port")
console.log("42");
console.error("Child is waiting for EOF in pipe");
// register to `end` event of `stdin` stream
process.stdin.on('end',(err)=>{
    if (err) {
        console.error("Child pipe read error %s", err);
        process.exit(1);
    } else {
        console.error("Child end");
        process.exit(0);
    }
})
// need to trigger the data to catch the `end` event
process.stdin.on('data', () => {});

function should_not_run() {
    console.error("Child should not print it, should terminate earlier");
}
setTimeout(should_not_run, 5000);

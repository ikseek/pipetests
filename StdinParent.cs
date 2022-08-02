using System.Diagnostics;

Console.Error.WriteLine("Parent starting child");
var child = new Process {
    StartInfo = new ProcessStartInfo("node", "stdin_child.js") {
        RedirectStandardInput = true,
        RedirectStandardOutput = true,
        RedirectStandardError = false,
    }
};
child.Start();
Console.Error.WriteLine("Parent started the child, reading the port number");
var port = child.StandardOutput.ReadLine();
Console.Error.WriteLine("Parent received port number from child: " + port);
Console.Error.WriteLine("Parent goes to sleep");
Thread.Sleep(2000);
if (args.Length == 1 && args[0] == "crash") {
    Console.Error.WriteLine("Parent crashing");
    // Need means to simulate crash
    Console.Error.WriteLine("Parent should not print it, should crash");
} else {
    Console.Error.WriteLine("Parent closing child's stdin");
    child.StandardInput.Close();
    Console.Error.WriteLine("Parent waits for child to exit");
    child.WaitForExit();
    Console.Error.WriteLine("Parent exiting");
}

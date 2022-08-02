import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;

class StdinParent {
    public static void main(String[] args) throws Exception {
        System.err.println("Parent starting child");
        ProcessBuilder processBuilder = new ProcessBuilder("node", "stdin_child.js").redirectError(ProcessBuilder.Redirect.INHERIT);
        Process process = processBuilder.start();
        System.err.println("Parent started the child, reading the port number");
        String port = new BufferedReader(new InputStreamReader(process.getInputStream())).readLine();
        System.err.println("Parent received port number from child: "+ port);
        System.err.println("Parent goes to sleep");
        Thread.sleep(2);
        if (args.length == 1 && args[0].equals("crash")) {
            System.err.println("Parent crashing");
            // Need some means of crashing java
            System.err.println("Parent should not print it, should crash");
        } else {
            System.err.println("Parent closing child's stdin");
            process.getOutputStream().close();
            System.err.println("Parent waits for child to exit");
            process.waitFor();
            System.err.println("Parent waits for child to exit");
            System.err.println("Parent exiting");
        }

    }
}
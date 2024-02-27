import subprocess


def adb_setup():
    import subprocess

    commands = ['cmd /c adb start-server', 'adb devices']

    for cmd_str in commands:
        cmd = subprocess.Popen(cmd_str, shell=True, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait for the command to finish and retrieve its output
        output, error = cmd.communicate()
        # Print the output
        if cmd_str == 'adb devices':
            output_str = output.decode()
            print(output_str)
        # Print the error, if any
        if error:
            print("Error:", error.decode())


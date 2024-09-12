import subprocess

def get_terminal_output(command: str) -> str:
    """
    Executes a given command in the terminal and returns its output as a string.

    :param command: The command to execute.
    :return: The output from the command execution.
    """
    # Run the command and capture the output
    result = subprocess.run(
        command,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Decode the output using the cp850 encoding (common in Windows terminals)
    output = result.stdout.decode('cp850')

    return output.strip()

# Test
if __name__ == "__main__":
    print(get_terminal_output("dir F:\\DATA\\Programs\\Python\\X-Tunnel"))
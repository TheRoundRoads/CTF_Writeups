import subprocess

# Set the IP and port
ip = "54.85.45.101"  # Replace with the target IP
port = 8003      # Replace with the target port

print(f"Connecting to {ip}:{port}. Type 'exit' to quit.")

lookup = [chr(ord("a")+i) for i in range(26)] + [chr(ord("A")+i) for i in range(26)] + [chr(ord("0") + i) for i in range(10)]
inputs = ["aa9"]
inputs += ["ac" + chr(ord("a")+i) for i in range(26)] 
outputs = []
def print_output(user_input, ip, port):    
    # Run the "nc" command, send user input, and capture the output
    try:
        process = subprocess.Popen(
            ["nc", ip, str(port)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Ensures text mode for Python 3.7+
        )
        
        # Send user input to the process and get the output
        output, error = process.communicate(input=user_input + "\n")
        
        # Print the output from the server
        if output:
            print(f"{user_input}: {output}")
        if error:
            print("Error:", error)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return
    
    return output

for i in reversed(range(len(lookup))):
    for j in reversed(range(len(lookup))):
        print_output(lookup[i] + lookup[j], ip, port)

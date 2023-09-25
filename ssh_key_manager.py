import subprocess
import os
import time
def generate_ssh_key(key_name, file_path):
    try:
        # Ensure the chosen directory is in /home
        if not file_path.startswith("/home"):
            raise ValueError("SSH keys must be saved in /home directory")

        # Ensure the file doesn't exist by appending a timestamp to the filename
        timestamp = int(time.time())
        unique_file_path = f"{file_path}_{timestamp}"

        # Generate SSH keys without a passphrase
        ssh_keygen_command = f"ssh-keygen -t rsa -b 4096 -N \"\" -C {key_name} -f {unique_file_path}"

        subprocess.run(ssh_keygen_command, shell=True, check=True)

        # Rename the generated file to the original filename
        os.rename(unique_file_path, file_path)
        
        return True, None
    except Exception as e:
        return False, str(e)

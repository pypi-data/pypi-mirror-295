#!/usr/bin/env python3

import subprocess
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error: {error.decode('utf-8')}")
        sys.exit(1)
    return output.decode('utf-8')

def generate_code():
    # Change to the project root directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Ensure the output directories exist
    os.makedirs('client/wallet', exist_ok=True)
    os.makedirs('client/service', exist_ok=True)

    # Generate code for wallet API
    print("Generating code for wallet API...")
    run_command('openapi-generator generate -i api_specs/wallet.openapi.yaml -g python -o client/wallet')

    # Generate code for service API
    print("Generating code for service API...")
    run_command('openapi-generator generate -i api_specs/service.openapi.yaml -g python -o client/service')

    # Additional setup steps can be added here
    print("Code generation complete!")

if __name__ == "__main__":
    generate_code()
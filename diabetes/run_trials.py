#!/usr/bin/env python3
"""
Script to execute the diabetes model with different trial values.
Executes run_model.py with trial values from 0 to 49.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_trial(trial_number):
    """
    Executes run_model.py with a specific trial value.
    
    Args:
        trial_number (int): Trial number to be executed
    """
    print(f"Executing trial {trial_number}...")
    
    try:
        # Executes the run_model.py script with the trial parameter
        result = subprocess.run([
            sys.executable, 
            "diabetes/run_model.py", 
            str(trial_number)
        ], 
        check=True, 
        capture_output=True, 
        text=True
        )
        
        print(f"Trial {trial_number} completed successfully!")
        if result.stdout:
            print(f"Output: {result.stdout}")
            
    except subprocess.CalledProcessError as e:
        print(f"Error executing trial {trial_number}: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False
    
    return True

def main():
    """
    Main function that executes all trials from 0 to 49.
    """
    print("Starting trials execution...")
    
    # Checks if run_model.py file exists
    if not os.path.exists("diabetes/run_model.py"):
        print("Error: File diabetes/run_model.py not found!")
        sys.exit(1)
    
    # Executes trials from 0 to 49
    successful_trials = 0
    failed_trials = []
    
    for trial in range(50):
        success = run_trial(trial)
        if success:
            successful_trials += 1
        else:
            failed_trials.append(trial)
    
    # Final Report
    print("\n" + "="*50)
    print("FINAL REPORT")
    print("="*50)
    print(f"Trials executed successfully: {successful_trials}/50")
    
    if failed_trials:
        print(f"Trials that failed: {failed_trials}")
    else:
        print("All trials executed successfully!")
    
    print("="*50)

if __name__ == "__main__":
    main()

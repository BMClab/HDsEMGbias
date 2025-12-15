#!/bin/bash

# Script to execute the diabetes model with different trial values
# Executes run_model.py with trial values from 0 to 49

echo "Starting trials execution..."

# Checks if run_model.py file exists
if [ ! -f "diabetes/run_model.py" ]; then
    echo "Error: File diabetes/run_model.py not found!"
    exit 1
fi

# Starts disk monitoring in background
if [ -f "diabetes/monitor_disk.sh" ]; then
    echo "Starting disk monitoring in background..."
    ./diabetes/monitor_disk.sh &
    MONITOR_PID=$!
    echo "Disk monitor started (PID: $MONITOR_PID)"
fi

# Function to check disk space
check_disk_space() {
    local usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ $usage -gt 85 ]; then
        echo "Warning: Low disk space ($usage% used). Cleaning temporary files..."
        # Cleans old temporary files more aggressively
        find /tmp -name ".tmp*" -type f -exec rm -f {} \; 2>/dev/null || true
        find /tmp -name "tmp*" -type f -exec rm -f {} \; 2>/dev/null || true
        find /tmp -name "*.tmp" -type f -exec rm -f {} \; 2>/dev/null || true
        find /tmp -type f -name "*python*" -mmin +30 -exec rm -f {} \; 2>/dev/null || true

        # Cleans pip cache if it exists
        if [ -d "$HOME/.cache/pip" ]; then
            rm -rf "$HOME/.cache/pip/wheels" 2>/dev/null || true
        fi

        # Cleans old log files
        find /var/log -name "*.log.*" -mtime +1 -exec sudo rm -f {} \; 2>/dev/null || true

        # Checks again
        local new_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
        echo "Disk space after cleaning: $new_usage% used"
        if [ $new_usage -gt 92 ]; then
            echo "Error: Disk space still very low ($new_usage%). Stopping execution."
            return 1
        fi
    fi
    return 0
}

# Function to clean old results if necessary
cleanup_old_results() {
    local results_size=$(du -s diabetes/results 2>/dev/null | cut -f1)
    # If results directory is larger than 20GB (20971520 KB)
    if [ "$results_size" -gt 20971520 ]; then
        echo "Results directory too large ($(du -sh diabetes/results | cut -f1)). Cleaning older files..."
        # Removes result files older than 7 days
        find diabetes/results -type f -mtime +7 -exec rm -f {} \; 2>/dev/null || true
        echo "Old results cleaning completed."
    fi
}

# Counters
successful_trials=0
failed_trials=()

# Executes trials from 0 to 49
for trial in {0..49}; do
    echo "Executing trial $trial..."

    # Cleans old results if necessary (every 10 trials)
    if [ $((trial % 10)) -eq 0 ]; then
        cleanup_old_results
    fi

    # Checks disk space before each trial
    if ! check_disk_space; then
        echo "Error: Insufficient disk space for trial $trial"
        failed_trials+=($trial)
        continue
    fi

    if uv run python diabetes/run_model.py $trial; then
        echo "Trial $trial completed successfully!"
        ((successful_trials++))
        # Cleans temporary files after success
        find /tmp -name ".tmp*" -type f -mmin +5 -exec rm -f {} \; 2>/dev/null || true
    else
        echo "Error executing trial $trial"
        failed_trials+=($trial)
        # Cleans temporary files after error as well
        find /tmp -name ".tmp*" -type f -mmin +5 -exec rm -f {} \; 2>/dev/null || true
    fi
done

# Final Report
echo "=================================================="
echo "FINAL REPORT"
echo "=================================================="
echo "Trials executed successfully: $successful_trials/50"

if [ ${#failed_trials[@]} -gt 0 ]; then
    echo "Trials that failed: ${failed_trials[*]}"
else
    echo "All trials executed successfully!"
fi

# Stops disk monitor if running
if [ ! -z "$MONITOR_PID" ]; then
    echo "Stopping disk monitor (PID: $MONITOR_PID)..."
    kill $MONITOR_PID 2>/dev/null || true
fi

echo "=================================================="

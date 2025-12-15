#!/bin/bash

# Script to monitor disk space during trials execution
# Runs in background and cleans files when necessary

LOGFILE="diabetes/disk_monitor.log"
CLEANUP_THRESHOLD=90  # Cleans when usage > 90%
STOP_THRESHOLD=95     # Stops execution when usage > 95%

echo "$(date): Starting disk monitoring..." >> "$LOGFILE"

while true; do
    # Checks disk usage
    USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    
    if [ "$USAGE" -gt $CLEANUP_THRESHOLD ]; then
        echo "$(date): High disk usage: ${USAGE}%. Starting cleaning..." >> "$LOGFILE"
        
        # Aggressive cleaning
        find /tmp -type f -mmin +5 -delete 2>/dev/null || true
        find /tmp -name "*.tmp" -delete 2>/dev/null || true
        find /tmp -name ".tmp*" -delete 2>/dev/null || true
        
        # Cleans pip cache
        if [ -d "$HOME/.cache/pip" ]; then
            rm -rf "$HOME/.cache/pip/wheels" 2>/dev/null || true
        fi
        
        # Cleans temporary Python files
        find /tmp -name "*python*" -type f -mmin +10 -delete 2>/dev/null || true
        
        # Checks again
        NEW_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
        echo "$(date): Usage after cleaning: ${NEW_USAGE}%" >> "$LOGFILE"
        
        if [ "$NEW_USAGE" -gt $STOP_THRESHOLD ]; then
            echo "$(date): ALERT: Critical disk usage (${NEW_USAGE}%)!" >> "$LOGFILE"
            # Can send signal to stop execution if necessary
            # pkill -f "run_model.py" 2>/dev/null || true
        fi
    fi
    
    # Waits 30 seconds before next check
    sleep 30
done

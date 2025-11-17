#!/bin/bash

# TechCorp CTF Lab - Stop All Services
# This script stops all running Flask applications

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo "TechCorp CTF Lab - Stopping Services"
echo "=========================================="
echo ""

# Function to stop a service
stop_service() {
    local service_name=$1
    local pid_file="logs/${service_name}.pid"

    echo -n "Stopping ${service_name}... "

    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid 2>/dev/null
            sleep 1
            # Force kill if still running
            if ps -p $pid > /dev/null 2>&1; then
                kill -9 $pid 2>/dev/null
            fi
            echo -e "${GREEN}✓${NC} (PID: ${pid})"
        else
            echo -e "${YELLOW}⚠${NC}  Process not found (PID: ${pid})"
        fi
        rm "$pid_file"
    else
        echo -e "${YELLOW}⚠${NC}  No PID file found"
    fi
}

# Stop all services
stop_service "main-app"
stop_service "dev-app"
stop_service "staging-app"
stop_service "admin-app"

# Clean up any remaining Python processes (be careful with this)
echo ""
echo -n "Checking for remaining Flask processes... "
REMAINING=$(pgrep -f "python3 app.py" | wc -l)
if [ $REMAINING -gt 0 ]; then
    echo -e "${YELLOW}${REMAINING} found${NC}"
    echo "Cleaning up remaining processes..."
    pkill -f "python3 app.py" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Cleanup complete"
else
    echo -e "${GREEN}None${NC}"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ All services stopped${NC}"
echo "=========================================="
echo ""

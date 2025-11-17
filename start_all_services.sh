#!/bin/bash

# TechCorp CTF Lab - Start All Services
# This script starts all Flask applications for the lab

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo "=========================================="
echo "TechCorp CTF Lab - Starting Services"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Please run setup.sh first${NC}"
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Function to start a service
start_service() {
    local service_name=$1
    local service_dir=$2
    local port=$3
    local log_file="logs/${service_name}.log"
    local pid_file="logs/${service_name}.pid"

    echo -e "${YELLOW}[${4}/4]${NC} Starting ${service_name} (port ${port})..."

    # Check if already running
    if [ -f "$pid_file" ]; then
        local old_pid=$(cat "$pid_file")
        if ps -p $old_pid > /dev/null 2>&1; then
            echo -e "${GREEN}   ℹ${NC}  ${service_name} already running (PID: ${old_pid})"
            return
        else
            rm "$pid_file"
        fi
    fi

    # Start the service
    cd "$service_dir"
    ../.venv/bin/python3 app.py > "../${log_file}" 2>&1 &
    local pid=$!
    echo $pid > "../${pid_file}"
    cd ..

    # Wait a moment and check if it's running
    sleep 1
    if ps -p $pid > /dev/null 2>&1; then
        echo -e "${GREEN}   ✓${NC} ${service_name} started (PID: ${pid})"
    else
        echo -e "${RED}   ✗${NC} Failed to start ${service_name}"
        echo "   Check logs: ${log_file}"
    fi
}

# Start all services
start_service "main-app" "main-app" "5000" "1"
start_service "dev-app" "dev-app" "5001" "2"
start_service "staging-app" "staging-app" "5002" "3"
start_service "admin-app" "admin-app" "5003" "4"

echo ""
echo "=========================================="
echo -e "${GREEN}✅ All services started!${NC}"
echo "=========================================="
echo ""
echo -e "${CYAN}Access Points:${NC}"
echo ""
echo -e "  ${YELLOW}Main Application:${NC}"
echo -e "    Direct:  ${GREEN}http://localhost:5000${NC}"
echo -e "    Nginx:   ${GREEN}http://techcorp.local:8080${NC}"
echo ""
echo -e "  ${YELLOW}Dev Subdomain:${NC}"
echo -e "    Direct:  ${GREEN}http://localhost:5001${NC}"
echo -e "    Nginx:   ${GREEN}http://dev.techcorp.local:8081${NC}"
echo ""
echo -e "  ${YELLOW}Staging Subdomain:${NC}"
echo -e "    Direct:  ${GREEN}http://localhost:5002${NC}"
echo -e "    Nginx:   ${GREEN}http://staging.techcorp.local:8082${NC}"
echo ""
echo -e "  ${YELLOW}Admin Subdomain:${NC}"
echo -e "    Direct:  ${GREEN}http://localhost:5003${NC}"
echo -e "    Nginx:   ${GREEN}http://admin.techcorp.local:8083${NC}"
echo -e "    ${CYAN}Auth:${NC}    admin:admin123"
echo ""
echo -e "${CYAN}Logs:${NC} ./logs/"
echo -e "${CYAN}Stop:${NC} ./stop_all_services.sh"
echo ""
echo -e "${YELLOW}🚩 7 Flags to find! Good luck!${NC}"
echo ""

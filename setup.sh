#!/bin/bash

# TechCorp CTF Lab - Setup Script
# This script configures the local environment for the lab

set -e  # Exit on error

echo "=========================================="
echo "TechCorp CTF Lab - Setup Script"
echo "Content Discovery & Subdomain Enumeration"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root for /etc/hosts modification
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}⚠️  This script needs sudo privileges to modify /etc/hosts${NC}"
    echo "Please run: sudo ./setup.sh"
    exit 1
fi

# Step 1: Backup /etc/hosts
echo -e "${YELLOW}[1/6]${NC} Backing up /etc/hosts..."
BACKUP_FILE="/etc/hosts.backup.$(date +%Y%m%d_%H%M%S)"
cp /etc/hosts "$BACKUP_FILE"
echo -e "${GREEN}   ✓${NC} Backup created: $BACKUP_FILE"

# Step 2: Add DNS entries to /etc/hosts
echo -e "${YELLOW}[2/6]${NC} Configuring local DNS entries..."

add_host_entry() {
    local hostname=$1
    if grep -q "$hostname" /etc/hosts; then
        echo -e "${GREEN}   ✓${NC} $hostname already exists in /etc/hosts"
    else
        echo "127.0.0.1 $hostname" >> /etc/hosts
        echo -e "${GREEN}   ✓${NC} Added $hostname to /etc/hosts"
    fi
}

add_host_entry "techcorp.local"
add_host_entry "dev.techcorp.local"
add_host_entry "staging.techcorp.local"
add_host_entry "admin.techcorp.local"

# Step 3: Check Python installation
echo -e "${YELLOW}[3/6]${NC} Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}   ✓${NC} $PYTHON_VERSION found"
else
    echo -e "${RED}   ✗${NC} Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Step 4: Create virtual environment if it doesn't exist
echo -e "${YELLOW}[4/6]${NC} Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}   ✓${NC} Virtual environment created"
else
    echo -e "${GREEN}   ✓${NC} Virtual environment already exists"
fi

# Step 5: Install Python dependencies
echo -e "${YELLOW}[5/6]${NC} Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    .venv/bin/pip install -q -r requirements.txt
    echo -e "${GREEN}   ✓${NC} Dependencies installed"
else
    echo -e "${RED}   ✗${NC} requirements.txt not found"
    exit 1
fi

# Step 6: Initialize databases
echo -e "${YELLOW}[6/6]${NC} Initializing databases..."
cd main-app
if [ ! -f "instance/database.db" ]; then
    ../.venv/bin/python3 -c "from app import init_db; init_db()" > /dev/null 2>&1
    echo -e "${GREEN}   ✓${NC} Main app database initialized"
else
    echo -e "${GREEN}   ✓${NC} Database already exists"
fi
cd ..

# Create logs directory
mkdir -p logs
echo -e "${GREEN}   ✓${NC} Logs directory created"

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo -e "${YELLOW}Configuration Summary:${NC}"
echo "  • Local DNS entries added to /etc/hosts"
echo "  • Python virtual environment: .venv/"
echo "  • Database initialized: main-app/instance/database.db"
echo "  • Logs directory: logs/"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Start all services:"
echo "     ${GREEN}./start_all_services.sh${NC}"
echo ""
echo "  2. Access the lab:"
echo "     Main:    ${GREEN}http://techcorp.local:8080${NC}"
echo "     Dev:     ${GREEN}http://dev.techcorp.local:8081${NC}"
echo "     Staging: ${GREEN}http://staging.techcorp.local:8082${NC}"
echo "     Admin:   ${GREEN}http://admin.techcorp.local:8083${NC}"
echo ""
echo "  3. Read documentation:"
echo "     ${GREEN}cat README.md${NC}"
echo "     ${GREEN}cat HINTS.md${NC} (if you need help)"
echo ""
echo -e "${YELLOW}Optional - Nginx Configuration:${NC}"
echo "  If you want to use Nginx as reverse proxy:"
echo "    sudo cp nginx.conf /etc/nginx/sites-available/techcorp-lab"
echo "    sudo ln -s /etc/nginx/sites-available/techcorp-lab /etc/nginx/sites-enabled/"
echo "    sudo nginx -t"
echo "    sudo systemctl reload nginx"
echo ""
echo "Happy hacking! 🚩"
echo ""

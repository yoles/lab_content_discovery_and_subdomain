#!/bin/bash

# TechCorp CTF Lab - Flag Validation Script
# This script tests all 7 flags to ensure they are accessible

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo "=========================================="
echo "TechCorp CTF Lab - Flag Validation"
echo "=========================================="
echo ""

# Counters
passed=0
failed=0

# Function to test a flag
test_flag() {
    local flag_num=$1
    local flag_name=$2
    local command=$3
    local expected_flag=$4

    echo -en "${YELLOW}[FLAG ${flag_num}/7]${NC} Testing ${flag_name}... "

    # Execute command and capture result
    result=$(eval "$command" 2>/dev/null)

    # Check if expected flag is in result
    if echo "$result" | grep -q "$expected_flag"; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((passed++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "  Expected: $expected_flag"
        echo "  Command: $command"
        if [ -n "$result" ]; then
            echo "  Got: ${result:0:100}..."
        else
            echo "  Got: (empty response or connection error)"
        fi
        ((failed++))
        return 1
    fi
}

# Check if services are running
echo "Checking if services are running..."
echo ""

services_running=true
for port in 5000 5001 5002 5003; do
    if ! nc -z 127.0.0.1 $port 2>/dev/null; then
        echo -e "${RED}✗${NC} Service on port $port is not running"
        services_running=false
    fi
done

if [ "$services_running" = false ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Some services are not running. Please start them first:${NC}"
    echo "   ./start_all_services.sh"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓${NC} All services are running"
echo ""
echo "Testing FLAGS..."
echo ""

# Test all 7 flags
test_flag 1 "robots.txt Discovery" \
    "curl -s http://127.0.0.1:5000/robots.txt" \
    "FLAG{robots_txt_exposed_7a3f}"

test_flag 2 "Backup File Discovery" \
    "curl -s http://127.0.0.1:5000/backup/database_backup.sql.old" \
    "FLAG{backup_files_found_9b2e}"

test_flag 3 "Git Directory Exposure" \
    "curl -s http://127.0.0.1:5000/.git/config" \
    "FLAG{git_folder_leaked_4c8d}"

test_flag 4 "Undocumented API Endpoint" \
    "curl -s http://127.0.0.1:5000/api/v2/admin/users" \
    "FLAG{api_v2_discovered_1e9f}"

test_flag 5 "Dev Subdomain Discovery" \
    "curl -s http://127.0.0.1:5001/" \
    "FLAG{dev_subdomain_pwned_5f2a}"

test_flag 6 "Staging Environment phpinfo" \
    "curl -s http://127.0.0.1:5002/phpinfo.php" \
    "FLAG{staging_env_exposed_8g3b}"

test_flag 7 "Admin Portal Access" \
    "curl -s -u admin:admin123 http://127.0.0.1:5003/dashboard" \
    "FLAG{admin_portal_found_3h4c}"

echo ""
echo "=========================================="
echo "Results Summary"
echo "=========================================="
echo ""
echo -e "  ${GREEN}Passed:${NC} $passed/7"
echo -e "  ${RED}Failed:${NC} $failed/7"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✅ All flags are accessible! Lab is ready.${NC}"
    echo ""
    echo "The 7 flags:"
    echo "  1. FLAG{robots_txt_exposed_7a3f}"
    echo "  2. FLAG{backup_files_found_9b2e}"
    echo "  3. FLAG{git_folder_leaked_4c8d}"
    echo "  4. FLAG{api_v2_discovered_1e9f}"
    echo "  5. FLAG{dev_subdomain_pwned_5f2a}"
    echo "  6. FLAG{staging_env_exposed_8g3b}"
    echo "  7. FLAG{admin_portal_found_3h4c}"
    echo ""
    exit 0
else
    echo -e "${RED}⚠️  Some flags are not accessible. Please check the failed tests above.${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Ensure all services are running: ./start_all_services.sh"
    echo "  2. Check logs in ./logs/ directory"
    echo "  3. Verify /etc/hosts entries for subdomains"
    echo ""
    exit 1
fi

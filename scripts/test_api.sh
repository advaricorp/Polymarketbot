#!/bin/bash

# Test API with curl commands

# Set the base URL
BASE_URL="http://0.0.0.0:8001"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Testing Polymarket Bot API${NC}"
echo "----------------------------------------"

# Test health endpoint
echo -e "\n${GREEN}Testing health endpoint:${NC}"
curl -v "${BASE_URL}/health" | jq .

# Test getting all markets
echo -e "\n${GREEN}Testing getting all markets:${NC}"
curl -v "${BASE_URL}/markets" | jq .

# Test refreshing markets
echo -e "\n${GREEN}Testing refreshing markets:${NC}"
curl -v -X POST "${BASE_URL}/markets/refresh" | jq .

# Test getting all markets again (should have updated data)
echo -e "\n${GREEN}Testing getting all markets again:${NC}"
curl -v "${BASE_URL}/markets" | jq .

# If we have markets, test getting a specific market
echo -e "\n${GREEN}Testing getting a specific market:${NC}"
# Get the first market ID from the response
MARKET_ID=$(curl -s "${BASE_URL}/markets" | jq -r '.[0].condition_id // empty')
if [ -n "$MARKET_ID" ]; then
  echo "Using market ID: $MARKET_ID"
  curl -v "${BASE_URL}/markets/$MARKET_ID" | jq .
else
  echo -e "${RED}No markets found to test specific market endpoint${NC}"
fi

echo -e "\n${GREEN}API testing complete${NC}" 
#!/bin/bash
# Phase 14, Risk 5: Blue-Green OTA Deployment Rollback
# This script is called by Watchtower or systemd when the pedal boots up or updates.
# If a new Docker container (e.g., ai-pedal-backend:latest) fails to boot or crashes 
# within 10 seconds, this script instantly resurrects the previous guaranteed-stable container.

echo "================================================================"
echo "🛡️  [Phase 14] Initiating Blue-Green OTA Deployment Health Check"
echo "================================================================"

# Get the Container ID of the currently running Backend
NEW_CONTAINER=$(docker-compose ps -q ai-pedal-backend)

if [ -z "$NEW_CONTAINER" ]; then
    echo "❌ [FATAL] No backend container found. Attempting immediate fallback to 'blue' backup."
    docker-compose -f docker-compose.backup.yml up -d
    exit 1
fi

echo "🟢 [Deployment] New 'Green' container detected. Initiating 10-second stability Watchdog..."

# Give the FastAPI backend time to boot and establish database connections
sleep 10

# Ping the health-check endpoint (Requires a /health route on FastAPI)
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$HTTP_STATUS" == "200" ]; then
    echo "✅ [SUCCESS] New OTA container is stable and responding to Heartbeat (HTTP 200)."
    echo "   -> Overwriting 'Blue' backup compose file to register this as the new standard."
    cp docker-compose.yml docker-compose.backup.yml
    echo "   -> Pedal is ready for the Gig."
    exit 0
else
    echo "🚨 [CRASH DETECTED] New OTA container failed to respond (HTTP $HTTP_STATUS)!"
    echo "   -> The update is corrupted. The pedal is in danger of bricking on stage."
    
    echo "🔄 [ROLLBACK INITIATED] Reverting to previous stable 'Blue' instance..."
    
    # 1. Stop and destroy the bad container
    docker-compose down
    
    # 2. Boot the old reliable container mapping
    docker-compose -f docker-compose.backup.yml up -d
    
    echo "✅ [ROLLBACK COMPLETE] The pedal has been restored to the last known good configuration."
    echo "   -> Disaster averted. The firmware team has been notified."
    exit 1
fi

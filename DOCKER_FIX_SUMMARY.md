# Docker Compose Fix Summary

## Issues Fixed

### 1. Frontend Cannot Reach Backend in Docker
**Problem**: When running in Docker Compose, the frontend JavaScript code was trying to reach `http://backend:8080`, which only works inside the Docker network. The browser (running on the host) cannot resolve the `backend` hostname.

**Solution**: 
- Added nginx reverse proxy in `frontend/nginx.conf` to proxy `/api/*` requests to `http://backend:8080`
- Updated `docker-compose.yml` to pass empty `VITE_API_URL` so the frontend uses relative URLs
- Modified frontend code to use relative URLs in production (`''`) which nginx proxies to the backend
- In development mode, it still uses `http://localhost:5000`

### 2. Multiple Ride Sessions Starting Simultaneously
**Problem**: The `RideView.vue` component was starting 10+ ride sessions at once because:
- The `watch` on `userLocation` triggered every time GPS coordinates updated
- Location updates happen frequently (every few seconds) as GPS accuracy improves
- No flag to prevent multiple simultaneous start requests

**Solution**:
- Added `isStartingRide` ref flag to prevent race conditions
- Removed auto-start from the main `userLocation` watcher
- Implemented a one-time watcher in `onMounted()` that:
  - Waits for the first location fix
  - Starts the ride once
  - Unwatches itself to prevent re-triggering
- Added comprehensive checks in `startRide()` to prevent duplicate starts

## Files Modified

### Backend
- `backend/Dockerfile` - Uses `wsgi:app` for proper MongoDB initialization
- `backend/wsgi.py` - New file to initialize MongoDB before gunicorn starts
- `backend/app.py` - Ensured MongoDB initialization works in both dev and production

### Frontend
- `frontend/Dockerfile` - Accept `VITE_API_URL` build arg, default to empty for production
- `frontend/nginx.conf` - Added `/api/` proxy to backend container
- `frontend/src/views/RideView.vue` - Fixed multiple ride start issue
- `frontend/src/components/WeatherCard.vue` - Use relative URLs in production
- `frontend/src/composables/useStationMarkers.js` - Use relative URLs in production

### Docker Compose
- `docker-compose.yml` - Pass empty `VITE_API_URL` to frontend build, fixed backend health check

## How It Works Now

### Network Flow in Docker:
1. Browser → `http://localhost` (port 80) → Frontend nginx container
2. Frontend serves static files (HTML, JS, CSS)
3. Browser executes JavaScript which makes API calls to `/api/*`
4. Nginx proxies `/api/*` → `http://backend:8080/api/*`
5. Backend processes request and returns data
6. JavaScript receives response and updates UI

### Development Flow (npm run dev):
1. Browser → `http://localhost:5173` → Vite dev server
2. JavaScript makes API calls to `http://localhost:5000` (backend running separately)
3. Backend processes request and returns data

## Testing

To test the full stack in Docker:
```bash
# Start containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Open in browser
open http://localhost

# Stop containers
docker-compose down
```

To test development setup:
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev

# Open browser to http://localhost:5173
```

## Key Takeaways

1. **Docker networking**: Container hostnames (like `backend`) are only resolvable inside the Docker network, not from the host browser
2. **Nginx as API proxy**: Best practice for production - serves static files and proxies API requests
3. **Race condition prevention**: Always add flags when dealing with async operations that shouldn't run multiple times
4. **GPS location updates**: They happen frequently and can trigger watchers many times - use one-time watchers or throttling

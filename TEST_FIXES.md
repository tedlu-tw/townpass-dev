# Testing the Fixes

## Issues Fixed

### 1. Timezone Issue (8-hour offset)
**Problem**: Backend was using `datetime.now()` which returns local time, causing timezone confusion
**Fix**: Changed to `datetime.utcnow()` to use UTC time consistently

### 2. Session Not Found  
**Problem**: Ride sessions were getting lost or not persisted properly
**Fix**: Added debug logging to track session creation and lookup

## How to Test

### 1. Clear Browser Storage
Open browser console and run:
```javascript
sessionStorage.clear()
localStorage.clear()
location.reload()
```

### 2. Test New Ride
1. Open http://localhost in browser
2. Navigate to ride view
3. Check console for:
   - "First location received, auto-starting ride..."
   - Should only see ONE ride start request
4. Verify time starts at 00:00:00 (not 08:00:00)
5. Wait a few seconds and verify time increments correctly

### 3. Check Backend Logs
```bash
docker-compose logs -f backend
```

Look for:
- `✅ Found session for ride_id: xxx` (sessions are being found)
- No `❌ Session not found` errors
- Ride start and update logs

### 4. Test API Directly
```bash
# Start a ride
curl -X POST http://localhost/api/ride/start \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "start_location": {"lat": 25.033, "lng": 121.5654}
  }'

# Save the ride_id from response, then update:
curl -X POST http://localhost/api/ride/update \
  -H "Content-Type: application/json" \
  -d '{
    "ride_id": "YOUR_RIDE_ID_HERE",
    "current_location": {"lat": 25.034, "lng": 121.566},
    "speed": 15.5
  }'
```

## Expected Behavior

1. **Time Display**: Should start at `00:00:00` and increment every second
2. **Single Ride Session**: Only ONE session should be created on page load
3. **Updates Work**: Ride updates should return success, not "session not found"
4. **Logs Show**: Backend logs should show session found messages

## If Problems Persist

### Clear Database Sessions
If old sessions are causing issues:

```python
# Connect to MongoDB and clear sessions
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['townpass']
result = db.active_sessions.delete_many({})
print(f"Deleted {result.deleted_count} sessions")
```

### Check UTC Time
Verify backend is using UTC:
```bash
docker exec townpass-backend python -c "from datetime import datetime; print(f'UTC: {datetime.utcnow()}')"
```

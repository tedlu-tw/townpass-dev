# Frontend Debugging Checklist

## Quick Status Check

**Backend:** ✅ Running on http://localhost:5000  
**Frontend:** ✅ Running on http://localhost:5173  
**MongoDB:** ✅ Connected  
**Status Endpoint:** ✅ Available at `/api/ride/status`

## To Test in Browser

1. **Open the app:**
   - Navigate to: http://localhost:5173
   - Go to the Ride view (RideView.vue)

2. **Open Browser DevTools:**
   - Press F12 or Right-click > Inspect
   - Go to the Console tab

3. **Check for Console Logs:**
   You should see:
   ```
   ✅ "Ride started: {ride_id: '...', start_time: '...', ...}"
   ✅ Updates being sent every 2 seconds
   ✅ Status responses with metrics
   ```

4. **Check Network Tab:**
   - Go to Network tab
   - Filter by "XHR" or "Fetch"
   - Every 2 seconds you should see:
     - POST to `/api/ride/update` (Status: 200)
     - GET to `/api/ride/status?ride_id=...` (Status: 200)

5. **Verify Response Data:**
   Click on a `/api/ride/status` request and check the Response:
   ```json
   {
     "ride_id": "...",
     "duration_seconds": 10,
     "distance_km": 0.015,
     "avg_speed_kmh": 15.5,
     "calories": 0.75,
     "status": "active",
     ...
   }
   ```

## Expected UI Behavior

### When Location is Available:
- Ride should auto-start
- Duration timer should begin counting: `00:00:01`, `00:00:02`, etc.
- Weather card should show current location weather

### As You Move (or simulate movement):
- Distance should increase: `0.00 KM` → `0.01 KM` → `0.02 KM`
- Speed should update: `0.0 km/h` → `15.5 km/h`
- Calories should increase: `0 kcal` → `1 kcal` → `2 kcal`

## Common Issues & Solutions

### Issue 1: Metrics Still Showing 0
**Possible Causes:**
- Location permission not granted
- Ride not starting (check console for "Ride started")
- API requests failing (check Network tab)

**Solution:**
1. Check browser console for errors
2. Grant location permission if prompted
3. Verify API_URL is correct: `http://localhost:5000`

### Issue 2: No Location Updates
**Check:**
```javascript
// In RideView.vue, these should be defined:
const { location: userLocation, startWatching, stopWatching } = useGeoLocation()
```

**Verify:**
- `userLocation.value` is not null
- `userLocation.value.latitude` and `.longitude` have values

### Issue 3: API Errors
**Check Response:**
- If you see "Database not available" - restart backend
- If you see "Ride session not found" - ride didn't start properly
- If you see 404 - check endpoint URL

### Issue 4: CORS Errors
**Should NOT happen** because backend has:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

If you see CORS errors, restart both servers.

## Manual Testing via Console

You can test directly in browser console:

```javascript
// Check if ride is active
console.log('User Location:', userLocation.value)
console.log('Ride ID:', rideId.value)
console.log('Is Ride Active:', isRideActive.value)

// Manually fetch status (replace ride_id)
fetch('http://localhost:5000/api/ride/status?ride_id=YOUR_RIDE_ID_HERE')
  .then(r => r.json())
  .then(console.log)
```

## If Metrics Still Show 0

### Step 1: Check if ride started
Open Console and look for:
```
"Ride started: {ride_id: '...', ...}"
```

If NOT present:
- Location not available
- Check `userLocation.value` in console

### Step 2: Check if updates are being sent
Look for Network requests every 2 seconds:
- POST `/api/ride/update` - Should return 200
- GET `/api/ride/status` - Should return 200 with metrics

### Step 3: Check the response data
In Network tab, click on `/api/ride/status` response:
- `duration_seconds` should be > 0
- `distance_km` should increase as you move
- `calories` should increase

### Step 4: Check if UI is updating
In Console, check the ref values:
```javascript
console.log({
  duration: formatted_time.value,
  distance: distance.value,
  speed: speed.value,
  calories: calories.value
})
```

If these are "0" despite API returning values:
- Check `fetchRideStatus()` function
- Verify the response data is being assigned to refs

## Quick Test Command

Run this in terminal to verify backend is working:
```bash
# Start a test ride
RIDE_ID=$(curl -s -X POST http://localhost:5000/api/ride/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "start_location": {"lat": 25.033, "lng": 121.565}}' \
  | jq -r '.ride_id')

# Send an update
curl -X POST http://localhost:5000/api/ride/update \
  -H "Content-Type: application/json" \
  -d "{\"ride_id\": \"$RIDE_ID\", \"current_location\": {\"lat\": 25.034, \"lng\": 121.566}}"

# Check status (should show distance and calories)
curl "http://localhost:5000/api/ride/status?ride_id=$RIDE_ID" | jq
```

## Success Indicators

✅ Console shows "Ride started"  
✅ Network tab shows requests every 2 seconds  
✅ Status endpoint returns distance > 0  
✅ Status endpoint returns duration > 0  
✅ Status endpoint returns calories > 0  
✅ UI displays updating values  

## If Everything Looks Good in Network Tab But UI Still Shows 0

This means the issue is in the frontend Vue component. Check:

1. **Data binding:** Are the refs connected to the template?
2. **Type conversion:** Check if `toFixed()` is being called on undefined
3. **Reactivity:** Are the refs being updated in `fetchRideStatus()`?

Look at this section in RideView.vue:
```javascript
const fetchRideStatus = async () => {
  // ...
  if (response.ok) {
    // THIS is where values should be assigned
    formatted_time.value = formatDuration(data.duration_seconds)
    distance.value = data.distance_km.toFixed(2)
    speed.value = data.avg_speed_kmh.toFixed(1)
    calories.value = Math.round(data.calories)
  }
}
```

## Need More Help?

1. Take a screenshot of:
   - Browser console
   - Network tab showing `/api/ride/status` response
   - The UI

2. Copy any error messages from console

3. Check `/tmp/backend_output.log` for backend errors:
   ```bash
   tail -50 /tmp/backend_output.log
   ```

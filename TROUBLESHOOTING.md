# 🔧 Troubleshooting Common Errors

## Error: `process is not defined`

### Problem
```
Uncaught (in promise) ReferenceError: process is not defined
```

### Cause
This error occurs when trying to access `process.env` in a Vite project. Unlike Vue CLI which polyfills Node.js globals, Vite doesn't provide `process` in the browser environment.

### Solution
✅ **Fixed!** Use `import.meta.env` instead of `process.env`

```javascript
// ❌ Wrong (causes error in Vite)
const apiKey = process.env.VUE_APP_GOOGLE_MAPS_API_KEY

// ✅ Correct (works in Vite)
const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
```

---

## Error: Map doesn't load / API Key warnings

### Problem
- Map shows gray screen
- Console warning: "Google Maps API Key not set"
- Console errors about API key

### Solution

1. **Create `.env` file** in the `frontend` directory:
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. **Get a Google Maps API Key:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable "Maps JavaScript API"
   - Create credentials → API Key
   - Copy the API key

3. **Add the key to `.env`:**
   ```env
   VITE_GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

4. **Restart the development server:**
   ```bash
   npm run dev
   ```

### Important Notes:
- ⚠️ Never commit `.env` file to git
- ⚠️ API key must start with `VITE_` for Vite to expose it
- ⚠️ Restart dev server after changing `.env`

---

## Error: Markers not showing

### Problem
- Map loads but no markers appear
- Console shows no errors

### Possible Causes & Solutions:

#### 1. Incorrect coordinate format
```javascript
// ❌ Wrong
{ latitude: 25.037, longitude: 121.564 }

// ✅ Correct
{ lat: 25.037, lng: 121.564 }
```

#### 2. GeoJSON coordinates reversed
```json
// GeoJSON uses [longitude, latitude] order
{
  "coordinates": [121.564, 25.037]  // [lng, lat]
}
```

The MapView component automatically converts this to `{ lat, lng }`

#### 3. Zoom level too low
```vue
<!-- Try increasing zoom to see markers -->
<MapView :zoom="15" />
```

#### 4. Markers outside viewport
```javascript
// Center the map on your markers
const center = { 
  lat: markers[0].lat, 
  lng: markers[0].lng 
}
```

---

## Error: GPS button doesn't work

### Problem
- Clicking GPS button does nothing
- Console shows geolocation errors

### Solutions:

#### 1. Enable location permission
- Check browser location permissions
- Allow location access for localhost

#### 2. Use HTTPS or localhost
Geolocation API only works on:
- ✅ `https://` websites
- ✅ `localhost`
- ❌ `http://` (except localhost)

#### 3. Check browser compatibility
```javascript
if (!navigator.geolocation) {
  console.error('Geolocation not supported')
}
```

---

## Error: Failed to load GeoJSON

### Problem
```
Error loading GeoJSON: 404 Not Found
```

### Solutions:

#### 1. Check file location
File must be in `frontend/public/` directory:
```
frontend/
  └── public/
      └── map.geojson  ✅
```

#### 2. Use correct path
```vue
<!-- Correct path -->
<MapView geojsonUrl="/map.geojson" />

<!-- Not this -->
<MapView geojsonUrl="./map.geojson" />
<MapView geojsonUrl="public/map.geojson" />
```

#### 3. Verify JSON format
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [lng, lat]  // Note: lng first!
      },
      "properties": {
        "name": "Location Name"
      }
    }
  ]
}
```

---

## Error: Vite environment variable not working

### Problem
`import.meta.env.VITE_GOOGLE_MAPS_API_KEY` is undefined

### Solutions:

#### 1. Check variable name
Must start with `VITE_`:
```env
# ❌ Wrong
GOOGLE_MAPS_API_KEY=xxx
VUE_APP_GOOGLE_MAPS_API_KEY=xxx

# ✅ Correct
VITE_GOOGLE_MAPS_API_KEY=xxx
```

#### 2. Restart dev server
Vite only reads `.env` on startup:
```bash
# Stop server (Ctrl+C)
npm run dev  # Start again
```

#### 3. Check file location
`.env` must be in the same directory as `vite.config.js`:
```
frontend/
  ├── .env              ✅
  ├── vite.config.js
  └── src/
```

---

## Error: "For development purposes only" watermark

### Problem
Map shows watermark: "For development purposes only"

### Cause
- API key not set correctly
- Billing not enabled on Google Cloud
- API restrictions too strict

### Solution
1. Enable billing on Google Cloud project
2. Check API key restrictions
3. Verify Maps JavaScript API is enabled

---

## Browser Console Commands for Debugging

### Check if Google Maps loaded
```javascript
console.log('Google Maps:', window.google?.maps ? 'Loaded' : 'Not loaded')
```

### Check API key
```javascript
console.log('API Key:', import.meta.env.VITE_GOOGLE_MAPS_API_KEY)
```

### Check markers
```javascript
// In browser console after map loads
console.log('Markers:', markers.value)
```

### Test geolocation
```javascript
navigator.geolocation.getCurrentPosition(
  (pos) => console.log('Location:', pos.coords),
  (err) => console.error('Error:', err)
)
```

---

## Quick Checklist

When things don't work, check:

- [ ] `.env` file exists in `frontend/` directory
- [ ] API key starts with `VITE_`
- [ ] Dev server was restarted after creating `.env`
- [ ] Google Maps JavaScript API is enabled
- [ ] Coordinates use `{ lat, lng }` format
- [ ] GeoJSON file is in `public/` directory
- [ ] Browser console shows no errors
- [ ] Location permission granted (for GPS)

---

## Still Having Issues?

1. Check browser console for errors
2. Verify all files match the examples in documentation
3. Try the basic example first before adding complexity
4. Check that your Google Cloud project is set up correctly

## Useful Links

- [Google Maps JavaScript API Documentation](https://developers.google.com/maps/documentation/javascript)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [GeoJSON Format](https://geojson.org/)
- [Browser Geolocation API](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API)

---

**Last Updated:** 2025-11-08

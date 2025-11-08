# MapView Implementation - Quick Start Guide

## 📋 What I've Created

I've implemented a complete Google Maps integration for your TownPass project based on the reference code and LibraryMapView.vue you provided. Here's what's included:

### 1. **Enhanced MapView Component** (`frontend/src/components/MapView.vue`)
   - Full-featured Google Maps wrapper
   - Support for custom markers and GeoJSON data
   - GPS location tracking
   - Distance calculation
   - Marker clustering ready
   - Responsive design

### 2. **Demo Pages**
   - **MapDemoView** (`/map-demo`): Basic map demo with examples
   - **StationsMapView** (`/stations`): YouBike stations map integration

### 3. **Sample Data** 
   - `frontend/public/map.geojson`: Sample GeoJSON data for testing

### 4. **Documentation**
   - `MAPVIEW_README.md`: Complete API reference and usage guide

## 🚀 Quick Setup

### Step 1: Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Maps JavaScript API"
4. Create an API Key
5. (Optional) Restrict the key to your domain

### Step 2: Add API Key to Your Project

Create or update `.env` file in the `frontend` directory:

```bash
VITE_GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

### Step 3: Install Dependencies (if needed)

```bash
cd frontend
npm install
```

### Step 4: Run the Project

```bash
npm run dev
```

### Step 5: View the Demo

Open your browser and navigate to:
- Main demo: `http://localhost:5173/map-demo`
- Stations map: `http://localhost:5173/stations`

## 📝 Key Features

### 1. **Load Markers from GeoJSON**
```vue
<MapView
  geojsonUrl="/map.geojson"
  :apiKey="googleMapsApiKey"
/>
```

### 2. **Custom Markers Array**
```vue
<MapView
  :markers="[
    { lat: 25.0374865, lng: 121.5647688, name: '台北市政府' }
  ]"
  :apiKey="googleMapsApiKey"
/>
```

### 3. **Handle Marker Clicks**
```vue
<MapView
  @marker-click="handleMarkerClick"
/>
```

### 4. **Get User Location**
```vue
<MapView
  :showGpsButton="true"
  @location-found="handleLocationFound"
/>
```

## 🔧 Integration with Your Backend

The StationsMapView includes a placeholder for fetching YouBike data:

```javascript
const refreshStations = async () => {
  try {
    const response = await fetch('/api/youbike/stations')
    const data = await response.json()
    stations.value = data
  } catch (error) {
    console.error('Error loading stations:', error)
  }
}
```

You can connect this to your existing backend:
- `backend/fetch_youbike_data.py` - Already fetches YouBike data
- `backend/data/youbike_data.json` - Contains the data

## 📊 GeoJSON Format

Your map.geojson should follow this structure:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [longitude, latitude]
      },
      "properties": {
        "id": 1,
        "name": "Location Name",
        "site": "Address"
      }
    }
  ]
}
```

**Note:** GeoJSON uses `[lng, lat]` order (reversed from Google Maps)

## 🎨 Customization

### Change Map Style
```vue
<MapView
  mapTypeId="satellite"  <!-- roadmap, satellite, hybrid, terrain -->
/>
```

### Custom Marker Icons
```vue
<MapView
  :markerIcon="{
    url: '/custom-marker.png',
    scaledSize: new google.maps.Size(32, 32)
  }"
/>
```

### Adjust Initial View
```vue
<MapView
  :center="{ lat: 25.033, lng: 121.565 }"
  :zoom="15"
/>
```

## 🔍 Differences from LibraryMapView.vue

Your reference LibraryMapView.vue uses:
- Pinia stores for state management
- MarkerClusterer for grouping markers
- Custom UI components (LibraryList, LibraryDetail)

My implementation:
- Is more modular and reusable
- Doesn't require Pinia (but can be integrated)
- Provides basic clustering support
- Includes built-in info cards

You can easily combine both approaches!

## 📱 Mobile Responsive

The MapView component is fully responsive and includes:
- Touch-friendly controls
- Responsive info cards
- Mobile-optimized layout

## 🐛 Troubleshooting

### Map doesn't load
- Check if API key is correct in `.env`
- Verify Maps JavaScript API is enabled
- Check browser console for errors

### "Loading failed" error
- API key might be restricted
- Check if domain is allowed
- Try creating a new unrestricted key for testing

### Markers don't show
- Check coordinates format: `{ lat: number, lng: number }`
- Verify GeoJSON format (lng first, then lat)
- Check if zoom level is appropriate

## 📚 Next Steps

1. **Replace API Key**: Update `.env` with your actual Google Maps API key
2. **Connect Backend**: Link the map to your YouBike data backend
3. **Customize Styling**: Adjust colors and layout to match your design
4. **Add Features**: 
   - Marker clustering
   - Route planning
   - Real-time updates
   - Filtering and search

## 📖 Full Documentation

See `MAPVIEW_README.md` for complete API reference and advanced usage.

## 🤝 Integration Examples

### With Pinia Store (like LibraryMapView)
```javascript
import { useLibraryStore } from '@/stores/library'
import { storeToRefs } from 'pinia'

const libraryStore = useLibraryStore()
const { libraryList } = storeToRefs(libraryStore)

const markers = computed(() => 
  libraryList.value.map(lib => ({
    lat: lib.lat,
    lng: lib.lng,
    name: lib.name,
    address: lib.address
  }))
)
```

### With MarkerClusterer
```javascript
import { MarkerClusterer } from '@googlemaps/markerclusterer'

// In your component
onMounted(() => {
  const clusterer = new MarkerClusterer({ map, markers })
})
```

## 💡 Tips

1. **API Key Security**: Use environment variables, never commit API keys
2. **Rate Limits**: Cache data when possible to avoid hitting API limits
3. **Performance**: Use marker clustering for 100+ markers
4. **UX**: Always provide loading states and error messages

Happy mapping! 🗺️

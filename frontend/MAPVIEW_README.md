# MapView Component Documentation

## Overview
The MapView component is a Vue 3 wrapper for Google Maps that makes it easy to display maps with markers, load GeoJSON data, and handle user interactions.

## Features
- ✅ Load Google Maps dynamically
- ✅ Display custom markers
- ✅ Load markers from GeoJSON files
- ✅ User location tracking with GPS button
- ✅ Calculate distances between points
- ✅ Custom marker info cards
- ✅ Multiple map types (roadmap, satellite, hybrid, terrain)
- ✅ Responsive design

## Installation

### 1. Get Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Maps JavaScript API"
4. Create credentials (API Key)
5. (Optional) Restrict the API key to your domain

### 2. Add API Key to Your Project
Create a `.env` file in your frontend directory:
```bash
VITE_GOOGLE_MAPS_API_KEY=your_api_key_here
```

## Usage

### Basic Example
```vue
<template>
  <MapView
    :center="{ lat: 25.0374865, lng: 121.5647688 }"
    :zoom="16"
    :apiKey="googleMapsApiKey"
  />
</template>

<script setup>
import MapView from '@/components/MapView.vue'
import { ref } from 'vue'

const googleMapsApiKey = ref(import.meta.env.VITE_GOOGLE_MAPS_API_KEY)
</script>
```

### Load Markers from GeoJSON
```vue
<template>
  <MapView
    geojsonUrl="/map.geojson"
    :apiKey="googleMapsApiKey"
    @marker-click="handleMarkerClick"
  />
</template>

<script setup>
import MapView from '@/components/MapView.vue'

const handleMarkerClick = (marker) => {
  console.log('Clicked marker:', marker)
}
</script>
```

### Custom Markers
```vue
<template>
  <MapView
    :markers="customMarkers"
    :apiKey="googleMapsApiKey"
  />
</template>

<script setup>
import MapView from '@/components/MapView.vue'
import { ref } from 'vue'

const customMarkers = ref([
  {
    lat: 25.0374865,
    lng: 121.5647688,
    name: '台北市政府',
    address: '110台北市信義區市府路1號'
  },
  {
    lat: 25.0397146,
    lng: 121.5653771,
    name: '誠品信義店',
    address: '110台北市信義區松高路11號'
  }
])
</script>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `center` | Object | `{ lat: 25.0374865, lng: 121.5647688 }` | Initial center of the map |
| `zoom` | Number | `16` | Initial zoom level (3-20) |
| `markers` | Array | `[]` | Array of marker objects |
| `apiKey` | String | `''` | Google Maps API key |
| `geojsonUrl` | String | `''` | URL to GeoJSON file |
| `mapTypeId` | String | `'terrain'` | Map type: roadmap, satellite, hybrid, terrain |
| `showGpsButton` | Boolean | `true` | Show GPS location button |
| `markerIcon` | Object | `null` | Custom marker icon configuration |

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `marker-click` | `marker` | Fired when a marker is clicked |
| `map-ready` | `map` | Fired when the map is initialized |
| `location-found` | `{ lat, lng }` | Fired when user location is found |

## Exposed Methods

You can access these methods using template refs:

```vue
<template>
  <MapView ref="mapRef" />
  <button @click="centerMap">Center Map</button>
</template>

<script setup>
import { ref } from 'vue'

const mapRef = ref(null)

const centerMap = () => {
  mapRef.value?.setCenter(25.0374865, 121.5647688)
  mapRef.value?.setZoom(16)
}
</script>
```

### Available Methods
- `setCenter(lat, lng)` - Set map center
- `setZoom(zoom)` - Set zoom level
- `addMarker(markerData)` - Add a single marker
- `clearMarkers()` - Remove all markers
- `getCurrentLocation()` - Get and center on user location

## GeoJSON Format

The component expects GeoJSON data in this format:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [121.5647688, 25.0374865]
      },
      "properties": {
        "id": 1,
        "name": "Location Name",
        "site": "Address",
        "description": "Optional description"
      }
    }
  ]
}
```

**Note:** GeoJSON uses `[longitude, latitude]` order, which is automatically converted to Google Maps' `{ lat, lng }` format.

## Marker Object Format

```javascript
{
  lat: 25.0374865,      // Required: latitude
  lng: 121.5647688,     // Required: longitude
  name: 'Location Name', // Optional: marker title
  address: 'Address',    // Optional: address or description
  site: 'Site info',     // Optional: alternative to address
  distance: '1.5',       // Optional: distance from user (auto-calculated)
  icon: {                // Optional: custom icon
    url: '/icon.png',
    scaledSize: { width: 32, height: 32 }
  }
}
```

## Styling

The component uses scoped styles but you can override them:

```vue
<style>
.map-container {
  border-radius: 16px; /* Custom border radius */
}

.marker-info-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
</style>
```

## Demo

Visit `/map-demo` route to see a live demo with all features.

## Troubleshooting

### Map doesn't load
1. Check if API key is valid
2. Verify Maps JavaScript API is enabled
3. Check console for errors
4. Ensure API key restrictions allow your domain

### Markers don't appear
1. Check if coordinates are valid (lat: -90 to 90, lng: -180 to 180)
2. Verify GeoJSON format is correct
3. Check if markers array has data
4. Look for console errors

### GPS button doesn't work
1. Ensure browser has location permission
2. Use HTTPS (required for geolocation API)
3. Check browser compatibility

## Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License
MIT

import { ref, onMounted } from 'vue'
import axios from 'axios'

export function useWeather() {
  const weather = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchWeather = async (lat = null, lng = null) => {
    loading.value = true
    error.value = null

    try {
      let url = '/api/weather'
      if (lat && lng) {
        url += `?lat=${lat}&lng=${lng}`
      }

      const response = await axios.get(url)
      weather.value = {
        location: response.data.location || '未知地點',
        temperature: response.data.temperature,
        feelsLike: response.data.feelsLike,
        humidity: response.data.humidity,
        windSpeed: response.data.windSpeed,
        pressure: response.data.pressure,
        description: response.data.description,
        icon: response.data.icon,
        timestamp: Date.now()
      }
    } catch (err) {
      console.error('Error fetching weather:', err)
      error.value = '無法獲取天氣資訊'
      
      // Fallback to mock data
      weather.value = {
        location: '台北市',
        temperature: 25,
        feelsLike: 26,
        humidity: 65,
        windSpeed: 3.5,
        pressure: 1013,
        description: '晴朗',
        icon: '01d'
      }
    } finally {
      loading.value = false
    }
  }

  const fetchWeatherByLocation = async (location) => {
    if (location && location.latitude && location.longitude) {
      await fetchWeather(location.latitude, location.longitude)
    }
  }

  const getWeatherIcon = (iconCode) => {
    const icons = {
      '01d': '☀️', '01n': '🌙',
      '02d': '🌤️', '02n': '☁️',
      '03d': '☁️', '03n': '☁️',
      '04d': '☁️', '04n': '☁️',
      '09d': '🌧️', '09n': '🌧️',
      '10d': '🌦️', '10n': '🌧️',
      '11d': '⛈️', '11n': '⛈️',
      '13d': '❄️', '13n': '❄️',
      '50d': '🌫️', '50n': '🌫️'
    }
    return icons[iconCode] || '🌤️'
  }

  const getWeatherAdvice = (temp, humidity, windSpeed) => {
    const advice = []
    
    if (temp > 30) {
      advice.push('天氣炎熱，記得補充水分')
    } else if (temp < 15) {
      advice.push('天氣較冷，注意保暖')
    }

    if (humidity > 80) {
      advice.push('濕度較高，騎乘時容易出汗')
    }

    if (windSpeed > 8) {
      advice.push('風速較大，騎乘時請注意安全')
    }

    if (advice.length === 0) {
      advice.push('天氣適合騎乘，祝您騎乘愉快！')
    }

    return advice
  }

  const isGoodRidingWeather = () => {
    if (!weather.value) return null
    
    const { temperature, windSpeed, humidity } = weather.value
    
    // Good weather conditions for riding
    const tempOk = temperature >= 15 && temperature <= 30
    const windOk = windSpeed < 8
    const humidityOk = humidity < 85

    return tempOk && windOk && humidityOk
  }

  return {
    weather,
    loading,
    error,
    fetchWeather,
    fetchWeatherByLocation,
    getWeatherIcon,
    getWeatherAdvice,
    isGoodRidingWeather
  }
}

<template>
	<div class="bg-black mt-3 text-white rounded-[8px] shadow-md w-[90%] mx-auto overflow-hidden">
		<!-- background image layer (leave url empty or set via inline style / prop) -->
		<div class="absolute inset-0 bg-center bg-cover"
			style="background-image: url('https://cdn.pixabay.com/photo/2016/08/30/12/30/blue-1630583_1280.jpg');">
		</div>
		<!-- gradient mask on top of the bg image: from bottom (black) to transparent at top -->
		<div class="absolute inset-0 bg-gradient-to-b from-transparent to-[#5AB4C5] pointer-events-none"></div>
		<div class="relative z-10 px-6 pt-6 pb-3">
			<div class="flex justify-center items-center gap-6 text-shadow">
				<div class="text-6xl font-extrabold leading-none ">{{ time }}</div>

				<div class="w-full flex flex-col justify-between">
					<div class="text-xl font-semibold">
						{{ weatherData?.weather?.location_name || weather?.location || '載入中...' }}
					</div>
					<div class="flex justify-between items-center w-full">
						<div class="text-xl font-bold text-left">
							{{ weatherData?.weather?.temperature || weather?.temperature || '--°C' }}
						</div>
						<div class="flex items-center text-xl font-bold text-right">
							<!-- Rain SVG icon -->
							<svg width="32" height="24" viewBox="0 0 32 24" fill="none"
								xmlns="http://www.w3.org/2000/svg">
								<g filter="url(#filter0_d_2017_161)">
									<path
										d="M27.8369 8.66619C27.8347 9.61672 27.5836 10.5501 27.1084 11.3733C26.6332 12.1965 25.9506 12.8809 25.1285 13.3581C24.8798 13.4995 24.5853 13.5368 24.3092 13.4618C24.0332 13.3869 23.7979 13.2058 23.6549 12.958C23.5118 12.7103 23.4726 12.416 23.5457 12.1394C23.6188 11.8629 23.7984 11.6265 24.0452 11.4818C24.6653 11.1243 25.15 10.5721 25.4241 9.9109C25.6982 9.24972 25.7464 8.51654 25.5612 7.82516C25.376 7.13379 24.9677 6.52289 24.3998 6.08731C23.8318 5.65172 23.1359 5.41581 22.4202 5.41619C22.0501 5.42145 21.6836 5.49035 21.3369 5.61986C21.0698 5.71477 20.7761 5.70123 20.5189 5.58215C20.2617 5.46306 20.0614 5.24792 19.961 4.98286C19.6514 4.15976 19.0994 3.44992 18.378 2.94704C17.6566 2.44416 16.7996 2.1719 15.9202 2.16619C15.039 2.16409 14.1784 2.43328 13.4555 2.9372C12.7326 3.44111 12.1823 4.15534 11.8794 4.98286C11.7789 5.24792 11.5786 5.46306 11.3214 5.58215C11.0642 5.70123 10.7706 5.71477 10.5035 5.61986C10.1568 5.49005 9.79034 5.42115 9.42019 5.41619C8.70408 5.4154 8.00777 5.65113 7.43942 6.08678C6.87107 6.52242 6.46252 7.13358 6.27724 7.8253C6.09196 8.51702 6.14032 9.25056 6.41481 9.91197C6.68931 10.5734 7.17456 11.1256 7.79519 11.4829C7.91939 11.5535 8.02839 11.648 8.11593 11.7609C8.20346 11.8738 8.2678 12.0029 8.30523 12.1408C8.34267 12.2787 8.35246 12.4226 8.33404 12.5643C8.31563 12.7059 8.26937 12.8426 8.19793 12.9663C8.1265 13.09 8.03129 13.1984 7.9178 13.2852C7.80431 13.372 7.67477 13.4354 7.53665 13.472C7.39852 13.5085 7.25454 13.5173 7.11299 13.498C6.97143 13.4786 6.83511 13.4314 6.71185 13.3592C5.6782 12.7634 4.87015 11.8431 4.41315 10.7411C3.95615 9.63902 3.87578 8.41692 4.1845 7.26452C4.49322 6.11211 5.17378 5.09387 6.1205 4.36787C7.06722 3.64188 8.22715 3.24875 9.42019 3.24953C9.70449 3.24952 9.98827 3.27381 10.2684 3.32211C10.8291 2.31506 11.6486 1.4761 12.6423 0.892034C13.6359 0.307965 14.7676 0 15.9202 0C17.0728 0 18.2044 0.307965 19.1981 0.892034C20.1917 1.4761 21.0113 2.31506 21.5719 3.32211C21.8521 3.27381 22.1359 3.24952 22.4202 3.24953C23.8562 3.25125 25.233 3.82248 26.2484 4.83793C27.2639 5.85338 27.8351 7.23013 27.8369 8.66619ZM10.5035 12.9995C10.7908 12.9995 11.0664 12.8854 11.2696 12.6822C11.4727 12.4791 11.5869 12.2035 11.5869 11.9162V9.74953C11.5869 9.46221 11.4727 9.18666 11.2696 8.98349C11.0664 8.78033 10.7908 8.66619 10.5035 8.66619C10.2162 8.66619 9.94065 8.78033 9.73749 8.98349C9.53432 9.18666 9.42019 9.46221 9.42019 9.74953V11.9162C9.42019 12.2035 9.53432 12.4791 9.73749 12.6822C9.94065 12.8854 10.2162 12.9995 10.5035 12.9995ZM9.42019 18.4162C9.42019 18.7035 9.53432 18.9791 9.73749 19.1822C9.94065 19.3854 10.2162 19.4995 10.5035 19.4995C10.7908 19.4995 11.0664 19.3854 11.2696 19.1822C11.4727 18.9791 11.5869 18.7035 11.5869 18.4162V16.2495C11.5869 15.9622 11.4727 15.6867 11.2696 15.4835C11.0664 15.2803 10.7908 15.1662 10.5035 15.1662C10.2162 15.1662 9.94065 15.2803 9.73749 15.4835C9.53432 15.6867 9.42019 15.9622 9.42019 16.2495V18.4162ZM21.3369 12.9995C21.6242 12.9995 21.8997 12.8854 22.1029 12.6822C22.3061 12.4791 22.4202 12.2035 22.4202 11.9162V9.74953C22.4202 9.46221 22.3061 9.18666 22.1029 8.98349C21.8997 8.78033 21.6242 8.66619 21.3369 8.66619C21.0495 8.66619 20.774 8.78033 20.5708 8.98349C20.3677 9.18666 20.2535 9.46221 20.2535 9.74953V11.9162C20.2535 12.2035 20.3677 12.4791 20.5708 12.6822C20.774 12.8854 21.0495 12.9995 21.3369 12.9995ZM20.2535 18.4162C20.2535 18.7035 20.3677 18.9791 20.5708 19.1822C20.774 19.3854 21.0495 19.4995 21.3369 19.4995C21.6242 19.4995 21.8997 19.3854 22.1029 19.1822C22.3061 18.9791 22.4202 18.7035 22.4202 18.4162V16.2495C22.4202 15.9622 22.3061 15.6867 22.1029 15.4835C21.8997 15.2803 21.6242 15.1662 21.3369 15.1662C21.0495 15.1662 20.774 15.2803 20.5708 15.4835C20.3677 15.6867 20.2535 15.9622 20.2535 16.2495V18.4162ZM15.9202 9.74953C16.2075 9.74953 16.4831 9.63539 16.6862 9.43223C16.8894 9.22906 17.0035 8.95351 17.0035 8.66619V6.49953C17.0035 6.21221 16.8894 5.93666 16.6862 5.73349C16.4831 5.53033 16.2075 5.41619 15.9202 5.41619C15.6329 5.41619 15.3573 5.53033 15.1542 5.73349C14.951 5.93666 14.8369 6.21221 14.8369 6.49953V8.66619C14.8369 8.95351 14.951 9.22906 15.1542 9.43223C15.3573 9.63539 15.6329 9.74953 15.9202 9.74953ZM14.8369 15.1662C14.8369 15.4535 14.951 15.7291 15.1542 15.9322C15.3573 16.1354 15.6329 16.2495 15.9202 16.2495C16.2075 16.2495 16.4831 16.1354 16.6862 15.9322C16.8894 15.7291 17.0035 15.4535 17.0035 15.1662V12.9995C17.0035 12.7122 16.8894 12.4367 16.6862 12.2335C16.4831 12.0303 16.2075 11.9162 15.9202 11.9162C15.6329 11.9162 15.3573 12.0303 15.1542 12.2335C14.951 12.4367 14.8369 12.7122 14.8369 12.9995V15.1662Z"
										fill="white" />
								</g>
								<defs>
									<filter id="filter0_d_2017_161" x="0" y="0" width="31.8369" height="27.4995"
										filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
										<feFlood flood-opacity="0" result="BackgroundImageFix" />
										<feColorMatrix in="SourceAlpha" type="matrix"
											values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
										<feOffset dy="4" />
										<feGaussianBlur stdDeviation="2" />
										<feComposite in2="hardAlpha" operator="out" />
										<feColorMatrix type="matrix"
											values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0" />
										<feBlend mode="normal" in2="BackgroundImageFix"
											result="effect1_dropShadow_2017_161" />
										<feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_2017_161"
											result="shape" />
									</filter>
								</defs>
							</svg>
							<span>{{ weatherData?.weather?.rain_probability_3h || weather?.humidity || '--' }}</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	<div class="relative z-20 bg-[#5AB4C5] rounded-b-[8px] text-white/90 text-m px-2">
		<div class="inline-block whitespace-nowrap animate-marquee">
			<!-- render messages from prop or AQI data -->
			<template v-if="weatherData?.aqi">
				<span class="pr-[5rem]">
					{{ weatherData.weather?.weather_condition || '天氣' }} | 
					降雨機率: {{ weatherData.weather?.rain_probability_3h || '--' }} | 
					空氣品質: {{ weatherData.aqi?.aqi_level || '--' }} (AQI: {{ weatherData.aqi?.aqi || '--' }})
				</span>
				<span class="pr-[5rem]">
					{{ weatherData.weather?.weather_condition || '天氣' }} | 
					降雨機率: {{ weatherData.weather?.rain_probability_3h || '--' }} | 
					空氣品質: {{ weatherData.aqi?.aqi_level || '--' }} (AQI: {{ weatherData.aqi?.aqi || '--' }})
				</span>
			</template>
			<template v-else v-for="(msg, idx) in props.marqueeMessages" :key="`a-${idx}`">
				<span class="pr-[5rem]">{{ msg }}</span>
			</template>
		</div>
	</div>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
	coordinates: { type: Object, default: null }, // { lat, lng }
	weather: { type: Object, default: null },
	loading: { type: Boolean, default: false },
	error: { type: String, default: null },
	// marquee messages: an array of strings to display in the scrolling caption
	marqueeMessages: { type: Array, default: () => [
		'未來 1 小時內天氣預報，目前的空氣品質對敏感族群有影響',
		'1234567890',
		'2234567890'
	] }
})

const time = ref(formatTime(new Date()))
const weatherData = ref(null)
const isLoading = ref(false)
const fetchError = ref(null)
let timer = null
let fetchTimer = null

function formatTime(d) {
	try {
		// force 24-hour format (no AM/PM)
		return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false })
	} catch (e) {
		// fallback
		const h = String(d.getHours()).padStart(2, '0') // getHours() already returns 0-23
		const m = String(d.getMinutes()).padStart(2, '0')
		return `${h}:${m}`
	}
}

async function fetchWeatherData(lat, lng) {
	if (!lat || !lng) return
	
	isLoading.value = true
	fetchError.value = null
	
	try {
		const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
		const response = await fetch(`${apiUrl}/api/weather?lat=${lat}&lng=${lng}&include_aqi=true`)
		
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`)
		}
		
		const data = await response.json()
		weatherData.value = data
	} catch (error) {
		console.error('Error fetching weather data:', error)
		fetchError.value = error.message
	} finally {
		isLoading.value = false
	}
}

// Watch for coordinate changes and fetch weather data
watch(() => props.coordinates, (newCoords) => {
	if (newCoords && newCoords.lat && newCoords.lng) {
		// Debounce the fetch to avoid too many requests while dragging
		if (fetchTimer) clearTimeout(fetchTimer)
		fetchTimer = setTimeout(() => {
			fetchWeatherData(newCoords.lat, newCoords.lng)
		}, 500)
	}
}, { immediate: true })

onMounted(() => {
	timer = setInterval(() => { time.value = formatTime(new Date()) }, 30_000)
})

onUnmounted(() => {
	if (timer) clearInterval(timer)
	if (fetchTimer) clearTimeout(fetchTimer)
})
</script>
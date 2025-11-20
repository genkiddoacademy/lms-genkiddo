<template>
	<div class="p-6">
		<div class="bg-white rounded-lg shadow-sm p-6">
			<div class="flex items-end gap-4 mb-4">
				<img src="/icon-kiko-halo.png" alt="Kiko Icon" class="w-auto h-16 mt-1 flex-shrink-0" />
				<h1 class="text-[2rem] font-bold text-gray-900 mb-2">Selamat datang, {{ username }}! 👋🏻</h1>
			</div>
			<p class="text-gray-900 text-2xl mb-4">
				Mari belajar sesuatu yang baru hari ini!
			</p>

			<div>
				<h1 class="text-[1.5rem] font-bold text-gray-900 mb-2">🧑‍🏫 Performa Belajar Kamu</h1>
				<div class="flex items-center gap-4 mb-6">
					<p class="text-[#5F5F5F] text-lg">Pilih Materi Pembelajaran</p>

					<div class="relative" ref="dropdownRef">
						<!-- Button -->
						<div @click="toggle" class="cursor-pointer bg-gradient-to-br from-[#F86300] to-[#DD3A3A]
                   text-white text-lg font-semibold px-4 py-2 rounded-xl
                   flex items-center gap-2">
							{{ selected }}
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
								fill="currentColor">
								<path fill-rule="evenodd"
									d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.21 8.27a.75.75 0 01.02-1.06z"
									clip-rule="evenodd" />
							</svg>
						</div>

						<!-- Dropdown List -->
						<div v-if="open"
							class="absolute mt-2 w-full bg-white shadow-lg rounded-xl border border-gray-200 overflow-hidden z-50">
							<div v-for="item in items" :key="item" @click="selectItem(item)"
								class="px-4 py-2 hover:bg-gray-100 cursor-pointer text-gray-800 text-lg transition">
								{{ item }}
							</div>
						</div>
					</div>
				</div>

				<!-- Gauge Container -->
				<div class="gauge-wrapper">
					<div class="gauge-card">
						<div class="gauge-legend">
							<div class="legend-dot"></div>
							<div class="legend-text">Rata-rata Nilai Tugas</div>
						</div>

						<div class="gauge-container">
							<svg class="gauge-arc" viewBox="0 0 200 200">
								<!-- Background arc (beige) - 3/4 lingkaran -->
								<path 
									:stroke-width="gaugeThickness"
									d="M 30 170 A 90 90 0 1 1 170 170" 
									fill="none" 
									stroke="#f5e6d3"
									stroke-linecap="round" />

								<!-- Progress arc (orange) - 3/4 lingkaran -->
								<path 
									:stroke-width="gaugeThickness"
									:stroke-dashoffset="progressOffset"
									d="M 30 170 A 90 90 0 1 1 170 170" 
									fill="none" 
									stroke="#f97316"
									stroke-linecap="round" 
									stroke-dasharray="424"
									style="transition: stroke-dashoffset 1s cubic-bezier(0.34, 1.56, 0.64, 1);" />

								<!-- Center circle -->
								<circle 
									cx="100" 
									cy="170" 
									:r="gaugeThickness * 0.6" 
									fill="#f97316" />
							</svg>

							<div 
								class="arrow-container" 
								:style="{ transform: arrowTransform }">
								<svg class="arrow" viewBox="0 0 200 50" xmlns="http://www.w3.org/2000/svg">
									<!-- Panah gradient seperti gambar -->
									<defs>
										<linearGradient id="arrowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
											<stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:0.3" />
											<stop offset="50%" style="stop-color:#ff8c6b;stop-opacity:0.6" />
											<stop offset="100%" style="stop-color:#ff8c6b;stop-opacity:0" />
										</linearGradient>
									</defs>
									<!-- Panah segitiga -->
									<polygon points="0,15 0,35 140,25" fill="url(#arrowGradient)" />
									<!-- Lingkaran orange -->
									<circle cx="175" cy="25" r="20" fill="#f97316" />
									<circle cx="175" cy="25" r="10" fill="white" />
								</svg>
							</div>
						</div>

						<div class="score-display">
							Nilai Kamu: <span class="score-value">{{ scoreValue.toFixed(2) }}</span>
						</div>

						<div class="input-section">
							<div class="input-group">
								<input 
									type="number" 
									v-model.number="scoreInput"
									placeholder="Masukkan nilai (0-100)" 
									min="0"
									max="100" 
									step="0.01"
									class="score-input">
								<button @click="updateScore" class="update-btn">Update</button>
							</div>

							<div class="input-group">
								<label>Ketebalan Gauge:</label>
								<input 
									type="range" 
									v-model.number="gaugeThickness"
									min="10" 
									max="40"
									class="thickness-slider">
								<span class="thickness-value">{{ gaugeThickness }}</span>
							</div>
						</div>
					</div>
				</div>

			</div>

		</div>
	</div>
</template>

<script setup>
import { inject, computed, ref, onMounted, onBeforeUnmount } from 'vue'

// Dropdown logic
const open = ref(false)
const selected = ref('Sutradara Animasi Part - 1 Beginner')
const dropdownRef = ref(null)

const items = [
	'Sutradara Animasi Part - 1 Beginner',
	'Desain Karakter - Beginner',
	'Animasi 2D Fundamental',
	'Storyboarding Dasar'
]

function toggle() {
	open.value = !open.value
}

function selectItem(item) {
	selected.value = item
	open.value = false
}

function handleClickOutside(e) {
	if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
		open.value = false
	}
}

// User data
const $user = inject('$user')

const username = computed(() => {
	const name = $user.data?.username || 'User'
	return name.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
})

// Gauge logic
const scoreInput = ref(85.66)
const scoreValue = ref(85.66)
const gaugeThickness = ref(25)

const arrowTransform = computed(() => {
	const angle = -135 + (scoreValue.value / 100) * 270
	return `translate(-100%, -50%) rotate(${angle}deg)`
})

const progressOffset = computed(() => {
	const totalLength = 424
	return totalLength - (scoreValue.value / 100) * totalLength
})

function updateScore() {
	if (isNaN(scoreInput.value) || scoreInput.value < 0 || scoreInput.value > 100) {
		alert('Masukkan nilai antara 0 dan 100')
		return
	}
	scoreValue.value = scoreInput.value
}

onMounted(() => {
	document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
	document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.gauge-wrapper {
	background: white;
	border-radius: 30px;
	padding: 40px;
	box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
	max-width: 600px;
	margin: 0 auto;
}

.gauge-card {
	background: #f8f9fa;
	border-radius: 20px;
	padding: 30px;
	box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.gauge-legend {
	display: flex;
	align-items: center;
	gap: 12px;
	margin-bottom: 30px;
}

.legend-dot {
	width: 20px;
	height: 20px;
	background: #f97316;
	border-radius: 4px;
}

.legend-text {
	color: #4a5568;
	font-size: 1.1em;
	font-weight: 500;
}

.gauge-container {
	position: relative;
	width: 300px;
	height: 250px;
	margin: 0 auto 30px;
}

.gauge-arc {
	width: 100%;
	height: 100%;
}

.arrow-container {
	position: absolute;
	top: 52%;
	left: 50%;
	width: 180px;
	height: 180px;
	transform-origin: right center;
	transition: transform 1s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.arrow {
	width: 100%;
	height: 100%;
	object-fit: contain;
}

.score-display {
	text-align: center;
	font-size: 1.2em;
	color: #4a5568;
}

.score-value {
	font-size: 2.5em;
	font-weight: 700;
	color: #2d3748;
}

.input-section {
	margin-top: 30px;
	padding-top: 30px;
	border-top: 2px solid #e2e8f0;
}

.input-group {
	display: flex;
	gap: 10px;
	align-items: center;
	margin-bottom: 15px;
}

.score-input,
.thickness-slider {
	flex: 1;
	padding: 12px 16px;
	border: 2px solid #e2e8f0;
	border-radius: 10px;
	font-size: 1em;
	transition: border-color 0.3s;
}

.score-input:focus {
	outline: none;
	border-color: #f97316;
}

.thickness-slider {
	padding: 0;
	height: 40px;
	cursor: pointer;
}

label {
	color: #4a5568;
	font-weight: 500;
	min-width: 120px;
}

.update-btn {
	background: #f97316;
	color: white;
	border: none;
	padding: 12px 24px;
	border-radius: 10px;
	font-size: 1em;
	font-weight: 600;
	cursor: pointer;
	transition: background 0.3s, transform 0.1s;
}

.update-btn:hover {
	background: #ea580c;
}

.update-btn:active {
	transform: scale(0.98);
}

.thickness-value {
	min-width: 40px;
	text-align: center;
	font-weight: 600;
	color: #f97316;
}
</style>
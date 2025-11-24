<template>
  <div class="p-6">
    <div class="bg-white rounded-lg shadow-sm p-6">
      <!-- Header -->
      <div class="flex items-end gap-4 mb-4">
        <img src="/icon-kiko-halo.png" alt="Kiko Icon" class="w-auto h-16 mt-1 flex-shrink-0" />
        <h1 class="text-[2rem] font-bold text-gray-900 mb-2">Selamat datang, {{ username }}! 👋🏻</h1>
      </div>
      <p class="text-gray-900 text-2xl mb-4">
        Mari belajar sesuatu yang baru hari ini!
      </p>

      <!-- Performa Belajar -->
      <div class="mb-8">
        <h1 class="text-[1.5rem] font-bold text-gray-900 mb-2">🧑‍🏫 Performa Belajar Kamu</h1>
        <div class="flex items-center gap-4 mb-6">
          <p class="text-[#5F5F5F] text-lg">Pilih Materi Pembelajaran</p>

          <div class="relative" ref="dropdownRef">
            <!-- Button -->
            <div @click="toggle" class="cursor-pointer bg-gradient-to-br from-[#F86300] to-[#DD3A3A]
                   text-white text-lg font-semibold px-4 py-2 rounded-xl
                   flex items-center gap-2">
              {{ selectedCourse?.course_title || 'Pilih Course' }}
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.21 8.27a.75.75 0 01.02-1.06z"
                  clip-rule="evenodd" />
              </svg>
            </div>

            <!-- Dropdown List -->
            <div v-if="open"
              class="absolute mt-2 w-full bg-white shadow-lg rounded-xl border border-gray-200 overflow-hidden z-50 max-h-60 overflow-y-auto">
              <div v-for="course in courses.data" :key="course.course_name" @click="selectCourse(course)"
                class="px-4 py-2 hover:bg-gray-100 cursor-pointer text-gray-800 text-lg transition border-b border-gray-100 last:border-b-0">
                {{ course.course_title }}
              </div>
              <div v-if="!courses.data?.length" class="px-4 py-2 text-gray-500 text-lg">
                Tidak ada course
              </div>
            </div>
          </div>
        </div>

        <div class="flex lg:flex-row flex-col gap-4">
          <!-- Statistik Container -->
          <div
            class="bg-white rounded-3xl pt-0 pb-10 px-10 shadow-[0_10px_30px_rgba(0,0,0,0.08)] h-96 lg:w-1/3 w-full rounded-2xl">
            <h1 class="py-6 text-2xl font-bold text-center">Statistik Quiz</h1>
            <div class="flex flex-col gap-y-3">
              <div class="border-2 rounded-2xl py-4 px-8">
                <div class="flex items-center gap-2 mb-2">
                  <div class="text-[2rem]">🔥</div>
                  <div>
                    <div class="font-bold text-2xl">{{ Math.ceil(selectedCourse?.progress) || 0 }}%</div>
                    <div class="text-[#4a5568] text-lg font-medium">Progress Materi</div>
                  </div>
                </div>
              </div>
              <div class="border-2 rounded-2xl py-4 px-8">
                <div class="flex items-center gap-2 mb-2">
                  <div class="text-[2rem]">📖</div>
                  <div>
                    <!-- <div class="font-bold text-2xl">{{ quizData.quiz_count || 0 }}</div> -->
                    <div class="font-bold text-2xl">4</div>
                    <div class="text-[#4a5568] text-lg font-medium">Bab Materi Selesai</div>
                  </div>
                </div>
              </div>
              <div class="border-2 rounded-2xl py-4 px-8">
                <div class="flex items-center gap-2 mb-2">
                  <div class="text-[2rem]">⚡</div>
                  <div>
                    <!-- <div class="font-bold text-2xl">{{ completedQuizzes }}</div> -->
                    <div class="font-bold text-2xl">2</div>
                    <div class="text-[#4a5568] text-lg font-medium">Pertemuan Selesai</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Gauge Container -->
          <div
            class="bg-white rounded-3xl pt-0 pb-10 px-10 shadow-[0_10px_30px_rgba(0,0,0,0.08)] h-96 lg:w-1/3 w-full mx-auto rounded-2xl">
            <h1 class="py-6 text-2xl font-bold text-center">Rata-rata Nilai Quiz</h1>
            <div class="border-2 rounded-2xl p-4">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-5 h-5 bg-[#f97316] rounded"></div>
                <div class="text-[#4a5568] text-lg font-medium line-clamp-1">{{ selectedCourse?.course_title || 'Pilih Course' }}</div>
              </div>

              <div class="relative mx-auto rotate-[270deg]">
                <svg class="w-full h-48" viewBox="0 0 200 200">
                  <!-- Background arc (beige) -->
                  <path :stroke-width="gaugeThickness" :d="backgroundPath" fill="none" stroke="#f5e6d3"
                    stroke-linecap="round" />

                  <!-- Progress arc (orange) dengan animasi -->
                  <path :stroke-width="gaugeThickness" :stroke-dashoffset="animatedProgressOffset" :d="backgroundPath"
                    fill="none" stroke="#f97316" stroke-linecap="round" :stroke-dasharray="circumference"
                    class="transition-all duration-2000 ease-out" />

                  <!-- Arrow dengan animasi -->
                  <g :transform="animatedArrowTransform">
                    <image :href="'/arrow_meter.png'" :x="55" :y="70" :width="60" :height="60" />
                    <circle :cx="centerX" :cy="centerY" r="12" fill="#f97316" />
                    <circle :cx="centerX" :cy="centerY" r="5" fill="white" />
                  </g>
                </svg>
              </div>

              <div class="text-center text-[#4a5568] text-lg mt-2">
                Nilai Rata-rata: <span class="font-bold text-xl text-[#2d3748]">{{ animatedScore.toFixed(1) }}%</span>
              </div>
            </div>
          </div>

          <!-- Nilai Quiz Detail Container -->
          <div
            class="bg-white rounded-3xl pt-0 pb-10 px-8 shadow-[0_10px_30px_rgba(0,0,0,0.08)] lg:w-1/3 w-full rounded-2xl">
            <h1 class="py-6 text-2xl font-bold text-center">Nilai Tugas</h1>
            <div class="grid grid-cols-2 gap-4 max-h-80 overflow-y-auto">
              <div class="border-2 rounded-2xl py-3 px-4">
                <div class="flex items-center gap-2">
                  <div class="text-[2rem]">👉</div>
                  <div>
                    <div class="font-bold text-2xl">75</div>
                    <div class="text-[#4a5568] text-lg font-medium">Nilai Pretest</div>
                  </div>
                </div>
              </div>
              <div class="border-2 rounded-2xl py-3 px-4">
                <div class="flex items-center gap-2">
                  <div class="text-[2rem]">👉</div>
                  <div>
                    <div class="font-bold text-2xl">-</div>
                    <div class="text-[#4a5568] text-lg font-medium">Nilai Postest</div>
                  </div>
                </div>
              </div>
              <div class="border-2 rounded-2xl py-3 px-4">
                <div class="flex items-center gap-2">
                  <div class="text-[2rem]">👉</div>
                  <div>
                    <div class="font-bold text-2xl">90</div>
                    <div class="text-[#4a5568] text-lg font-medium">Nilai Quiz</div>
                  </div>
                </div>
              </div>
              <div class="border-2 rounded-2xl py-3 px-4">
                <div class="flex items-center gap-2">
                  <div class="text-[2rem]">🌅</div>
                  <div>
                    <div class="font-bold text-2xl">-</div>
                    <div class="text-[#4a5568] text-lg font-medium">Proyek Akhir</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Kelas Kamu -->
      <div>
        <h1 class="text-[1.5rem] font-bold text-gray-900 mb-2">🧑‍⚖️ Kelas Kamu</h1>

        <div class="flex md:flex-row flex-col">
          <!-- Kelas yang diambil saat ini -->
          <div class="border-2 bg-white shadow-[0_10px_30px_rgba(0,0,0,0.08)] md:w-1/2 p-6 rounded-lg mr-4 mb-4">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg text-gray-900 font-bold">Kelas yang diambil saat ini</h2>
              <router-link to="/courses" class="text-blue-600 hover:text-blue-800 font-medium transition-colors">
                Lihat Semua
              </router-link>
            </div>

            <div class="flex flex-col gap-3">
              <div
                class="flex flex-row border-2 p-4 rounded-lg hover:shadow-md transition-all duration-300 cursor-pointer group hover:border-[#FF4B00]"
                @click="$router.push('/batches/details/genlive')">
                <div class="p-2 w-fit">
                  <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 48 48"
                    class="group-hover:[&>g]:stroke-[#FF4B00]">
                    <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                      stroke-width="3">
                      <path
                        d="m40 28.594l.459-.032c2.19-.16 3.89-1.702 4.133-3.885C44.808 22.74 45 19.916 45 16s-.192-6.74-.408-8.677c-.243-2.183-1.94-3.725-4.132-3.884C37.522 3.225 32.424 3 24 3s-13.522.225-16.46.439c-2.191.159-3.89 1.7-4.132 3.884C3.192 9.26 3 12.084 3 16s.192 6.74.408 8.677c.243 2.183 1.943 3.726 4.133 3.885l.459.032" />
                      <path
                        d="M30 17a6 6 0 1 1-12 0a6 6 0 0 1 12 0M11.931 45s-.57-1.978-1.27-5m25.408 5s.57-1.978 1.27-5M8.64 34.116c-.767.014-1.435.485-1.539 1.245C7.044 35.786 7 36.328 7 37s.044 1.215.101 1.64c.104.76.772 1.23 1.538 1.244C10.81 39.926 15.833 40 24 40s13.191-.074 15.36-.116c.767-.014 1.435-.485 1.538-1.245c.058-.425.102-.967.102-1.639s-.044-1.215-.102-1.64c-.103-.76-.77-1.23-1.537-1.244C37.19 34.074 32.167 34 24 34s-13.191.074-15.36.116M24 29v5" />
                      <path
                        d="M34 28.758a35 35 0 0 0-.678-2.496c-.461-1.475-1.636-2.567-3.16-2.82C28.784 23.211 26.763 23 24 23s-4.785.212-6.161.441c-1.526.254-2.7 1.346-3.162 2.822c-.216.692-.452 1.53-.677 2.495" />
                    </g>
                  </svg>
                </div>
                <div class="flex flex-col justify-center gap-2 p-2 flex-1">
                  <div
                    class="font-semibold text-lg line-clamp-2 group-hover:text-[#FF4B00] transition-colors duration-300">
                    GenLive
                  </div>
                  <div class="flex gap-4 text-sm text-gray-600">
                    <div class="flex gap-1 items-center">
                      <FileText :size="16" stroke="#2D2D2D" stroke-width="2" aria-hidden="false" />
                      <div>1 Materi</div>
                    </div>
                    <div class="flex gap-1 items-center">
                      <Clock3 :size="16" stroke="#2D2D2D" stroke-width="2" aria-hidden="false" />
                      <div>1 Siswa</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Course dengan Nilai Quiz Terbaik -->
          <div class="border-2 bg-white shadow-[0_10px_30px_rgba(0,0,0,0.08)] md:w-1/2 p-6 rounded-lg mr-4 mb-4">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-lg text-gray-900 font-bold">Pertemuan Terjadwal </h2>
              <router-link to="/batches/genlive#jadwal" class="text-blue-600 hover:text-blue-800 font-medium transition-colors">
                Lihat Semua
              </router-link>
            </div>

            <div class="flex flex-col gap-3">
              <div
                class="flex flex-row border-2 p-4 rounded-lg hover:shadow-md transition-all duration-300 cursor-pointer group hover:border-[#FF4B00]"
                @click="$router.push('/batches/genlive#jadwal')">
                <div class="p-2 w-fit">
                  <GraduationCap size="36" color="#F86300"/>
                </div>
                
                  <div class="flex flex-col justify-center gap-2 p-2 flex-1">
                    <div
                      class="font-semibold text-lg line-clamp-2 group-hover:text-[#FF4B00] transition-colors duration-300">
                      Pertemuan 1
                    </div>
                    <div class="flex gap-4 text-sm text-gray-600">
                      <div class="flex gap-1 items-center">
                        <Clock3 :size="16" stroke="#2D2D2D" stroke-width="2" aria-hidden="false" />
                        <div>08 November 2025 6:30 PM</div>
                      </div>
                    </div>
                  </div>
              </div>
              <div
                class="flex flex-row border-2 p-4 rounded-lg hover:shadow-md transition-all duration-300 cursor-pointer group hover:border-[#FF4B00]"
                @click="$router.push('/batches/genlive#jadwal')">
                <div class="p-2 w-fit">
                  <GraduationCap size="36" color="#F86300"/>
                </div>
                
                  <div class="flex flex-col justify-center gap-2 p-2 flex-1">
                    <div
                      class="font-semibold text-lg line-clamp-2 group-hover:text-[#FF4B00] transition-colors duration-300">
                      Pertemuan 2
                    </div>
                    <div class="flex gap-4 text-sm text-gray-600">
                      <div class="flex gap-1 items-center">
                        <Clock3 :size="16" stroke="#2D2D2D" stroke-width="2" aria-hidden="false" />
                        <div>15 November 2025 6:30 PM</div>
                      </div>
                    </div>
                  </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, computed, ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import { FileText, Clock3, GraduationCap  } from 'lucide-vue-next'
import { createResource, call } from 'frappe-ui'

const router = useRouter()

// User data
const $user = inject('$user')

const username = computed(() => {
  const name = $user.data?.username || 'User'
  return name
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
})

// Courses data from API - menggunakan endpoint baru
const courses = createResource({
  url: 'lms.lms.api.get_all_courses_with_quiz_scores',
  auto: true,
  onSuccess(data) {
    console.log('✅ Courses with quiz scores loaded:', data)
    if (data && data.length > 0) {
      selectedCourse.value = data[0]
      // Trigger animasi gauge setelah data loaded
      startGaugeAnimation()
    }
  },
  onError(error) {
    console.error('❌ Error loading courses with quiz scores:', error)
    // Fallback to basic courses API if the new one fails
    loadBasicCourses()
  }
})

// Fallback to basic courses API
const loadBasicCourses = async () => {
  try {
    const basicCourses = await call('lms.lms.api.get_my_courses_progress')
    console.log('✅ Basic courses data loaded:', basicCourses)
    if (basicCourses && basicCourses.length > 0) {
      selectedCourse.value = basicCourses[0]
      courses.data = basicCourses
      // Trigger animasi gauge setelah data loaded
      startGaugeAnimation()
    }
  } catch (error) {
    console.error('❌ Error loading basic courses:', error)
  }
}

// Quiz data state - menggunakan nilai dummy
const quizData = ref({
  average_percentage: 82.5, // Nilai dummy 100%
  quiz_count: 1,
  quiz_scores: []
})

// Load quiz data for a course
const loadQuizData = async (courseName) => {
  try {
    console.log('🔄 Loading quiz data for course:', courseName)
    const result = await call('lms.lms.api.get_quiz_scores_for_course', {
      course: courseName
    })
    quizData.value = result
    console.log('✅ Quiz data loaded:', result)
    // Restart animasi ketika data quiz berubah
    startGaugeAnimation()
  } catch (error) {
    console.error('❌ Error loading quiz data:', error)
    // Gunakan nilai dummy
    quizData.value = {
      average_percentage: 82.50, // Nilai dummy 100%
      quiz_count: 1,
      quiz_scores: []
    }
    // Restart animasi dengan nilai dummy
    startGaugeAnimation()
  }
}

// Dropdown logic
const open = ref(false)
const selectedCourse = ref(null)
const dropdownRef = ref(null)

// Watch for course selection changes
watch(selectedCourse, (newCourse) => {
  if (newCourse) {
    loadQuizData(newCourse.course_name)
  }
})

function toggle() {
  open.value = !open.value
}

function selectCourse(course) {
  selectedCourse.value = course
  open.value = false
}

function handleClickOutside(e) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    open.value = false
  }
}

// Gauge logic - menggunakan nilai animasi
const gaugeThickness = ref(15)
const gaugeRadius = ref(75)
const gaugeAngle = ref(270)
const gaugeRotation = ref(-90)

// Variabel animasi
const animatedScore = ref(0)
const animatedProgressOffset = ref(0)
const animatedArrowTransform = ref('')
const isAnimating = ref(false)

// Pusat gauge
const centerX = 100
const centerY = 100

// Current quiz score untuk gauge
const currentQuizScore = computed(() => {
  return quizData.value.average_percentage || 100 // Default 100% untuk dummy
})

// Fungsi untuk memulai animasi gauge
const startGaugeAnimation = () => {
  if (isAnimating.value) return

  isAnimating.value = true
  animatedScore.value = 0

  const targetScore = currentQuizScore.value
  const duration = 2000 // 2 detik
  const startTime = performance.now()

  const animate = (currentTime) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)

    // Easing function untuk animasi yang smooth
    const easeOutQuart = 1 - Math.pow(1 - progress, 4)

    // Update nilai animasi
    animatedScore.value = easeOutQuart * targetScore

    // Update progress offset
    animatedProgressOffset.value = circumference.value - (animatedScore.value / 100) * circumference.value

    // Update arrow transform
    const pivotAngleCustom = 175
    const minAngle = startAngle.value - pivotAngleCustom
    const maxAngle = endAngle.value - pivotAngleCustom
    const angleRange = maxAngle - minAngle
    const angle = minAngle + (animatedScore.value / 100) * angleRange
    animatedArrowTransform.value = `rotate(${angle}, ${centerX}, ${centerY})`

    if (progress < 1) {
      requestAnimationFrame(animate)
    } else {
      isAnimating.value = false
      animatedScore.value = targetScore // Pastikan nilai akhir tepat
    }
  }

  requestAnimationFrame(animate)
}

// Menghitung sudut awal dan akhir berdasarkan gaugeAngle
const startAngle = computed(() => {
  return 225
})

const endAngle = computed(() => {
  return 225 + gaugeAngle.value
})

// Konversi derajat ke radian
function toRadians(degrees) {
  return degrees * Math.PI / 180
}

// Menghitung titik pada lingkaran berdasarkan sudut
function pointOnCircle(angle, radius, cx, cy) {
  const rad = toRadians(angle)
  return {
    x: cx + radius * Math.cos(rad),
    y: cy + radius * Math.sin(rad)
  }
}

// Path untuk background gauge
const backgroundPath = computed(() => {
  const start = pointOnCircle(startAngle.value, gaugeRadius.value, centerX, centerY)
  const end = pointOnCircle(endAngle.value, gaugeRadius.value, centerX, centerY)

  const largeArcFlag = gaugeAngle.value > 180 ? 1 : 0

  return `M ${start.x} ${start.y} A ${gaugeRadius.value} ${gaugeRadius.value} 0 ${largeArcFlag} 1 ${end.x} ${end.y}`
})

// Panjang circumference untuk gauge
const circumference = computed(() => {
  return (gaugeAngle.value / 360) * 2 * Math.PI * gaugeRadius.value
})

// Statistics computations based on quiz data
const completedQuizzes = computed(() => {
  if (!quizData.value.quiz_scores?.length) return 0
  return quizData.value.quiz_scores.filter(quiz => quiz.percentage >= 70).length
})

// Courses with quiz scores (for the right panel)
const coursesWithQuizScores = computed(() => {
  if (!courses.data?.length) return []

  // Filter courses that have quiz data and sort by average percentage
  return courses.data
    .filter(course => course.quiz_count > 0)
    .slice(0, 2)
})

const currentCourses = computed(() => {
  if (!courses.data?.length) return []
  return courses.data.slice(0, 2)
})

// Helper functions
function getQuizIcon(percentage) {
  if (percentage >= 90) return '🏆'
  if (percentage >= 80) return '⭐'
  if (percentage >= 70) return '✅'
  if (percentage >= 60) return '📘'
  return '📝'
}

function getAchievementIcon(percentage) {
  if (percentage >= 90) return '🏆'
  if (percentage >= 80) return '⭐'
  if (percentage >= 70) return '🔥'
  return '🌱'
}

function getScoreColor(percentage) {
  if (percentage >= 80) return 'text-green-600'
  if (percentage >= 70) return 'text-orange-500'
  if (percentage >= 60) return 'text-yellow-500'
  return 'text-red-500'
}

function getProgressBarColor(percentage) {
  if (percentage >= 80) return 'bg-green-500'
  if (percentage >= 70) return 'bg-orange-500'
  if (percentage >= 60) return 'bg-yellow-500'
  return 'bg-red-500'
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

function goToCourse(courseName) {
  router.push({
    name: 'CourseDetail',
    params: { courseName }
  })
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  // Mulai animasi setelah komponen mounted
  setTimeout(() => {
    startGaugeAnimation()
  }, 500)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom scrollbar for quiz list */
.max-h-80::-webkit-scrollbar {
  width: 6px;
}

.max-h-80::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.max-h-80::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

.max-h-80::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Animasi khusus untuk gauge */
.transition-all {
  transition: all 0.05s linear;
}
</style>
<template>
	<header
		class="sticky flex items-center justify-between top-0 z-10 border-b bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<div class="!font-bold">
			<Breadcrumbs :items="breadcrumbs" class="!text-3xl !font-bold" />
		</div>
		<router-link
			v-if="canCreateCourse()"
			:to="{
				name: 'CourseForm',
				params: { courseName: 'new' },
			}"
		>
			<Button variant="solid">
				<template #prefix>
					<Plus class="h-4 w-4 stroke-1.5" />
				</template>
				{{ __('Create') }}
			</Button>
		</router-link>
	</header>
	<div class="p-5 pb-10 w-full flex flex-col">
		<div class="flex flex-col w-full gap-4 mb-6">
			<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
				<TabButtons
					:buttons="courseTabs"
					v-model="currentTab"
					class="flex-1 lg:w-fit custom-tab-buttons"
				/>

				<div
					class="flex flex-row items-center gap-2 w-full justify-between lg:justify-end lg:w-full"
				>
					<FormControl
						v-model="certification"
						:label="__('Tersedia Sertifikat')"
						type="checkbox"
						class="checkbox-orange"
						@change="updateCourses()"
					/>

					<FormControl
						v-model="title"
						:placeholder="__('Cari Berdasarkan Judul')"
						type="text"
						class="search-input-white ring-1 ring-orange-2 rounded-sm focus:ring-2 focus:ring-orange-2 transition-all duration-200"
						@input="updateCourses()"
					>
						<template #prefix>
							<Search class="h-4 w-4" />
						</template>
					</FormControl>
				</div>
			</div>

			<div class="flex-row flex gap-2 items-center w-full !text-lg">
				<label class="font-medium text-gray-700">Jalur Pembelajaran:</label>
				<GradientSelect
					v-model="currentCategory"
					:options="categories"
					:placeholder="__('Semua Jalur')"
					@change="updateCourses()"
				/>
			</div>
		</div>

		<div
			v-if="courses.data?.length"
			class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-5"
		>
			<router-link
				v-for="course in courses.data"
				:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
			>
				<CourseCard :course="course" />
			</router-link>
		</div>
		<EmptyState v-else-if="!courses.list.loading" type="Courses" />
		<div
			v-if="!courses.list.loading && courses.hasNextPage"
			class="flex justify-center mt-5"
		>
			<Button @click="courses.next()">
				{{ __('Load More') }}
			</Button>
		</div>
	</div>
</template>
<script setup>
import {
	Breadcrumbs,
	Button,
	call,
	createListResource,
	FormControl,
	Select,
	TabButtons,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject, onMounted, onUnmounted, ref, watch } from 'vue'
import { Plus, Search } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import { canCreateCourse } from '@/utils'
import CourseCard from '@/components/CourseCard.vue'
import EmptyState from '@/components/EmptyState.vue'
import GradientSelect from '@/components/GradientSelect.vue'
import router from '../router'
import { setupSelectGradientWatcher } from '@/utils/selectGradient'

const user = inject('$user')
const dayjs = inject('$dayjs')
const start = ref(0)
const pageLength = ref(30)

const categories = ref([
	{
		label: 'Semua Jalur',
		value: null,
	},
])
const currentCategory = ref(null)
const title = ref('')
const certification = ref(false)
const filters = ref({})
const currentTab = ref('live')
const { brand } = sessionStore()
const courseCount = ref(0)

onMounted(() => {
	setFiltersFromQuery()
	updateCourses()
	getCourseCount()
	getAllCategories()

	// Force apply form control styling
	setTimeout(() => {
		// Force checkbox orange styling
		const checkboxes = document.querySelectorAll(
			'.checkbox-orange input[type="checkbox"]',
		)
		checkboxes.forEach((checkbox) => {
			const updateCheckboxStyle = () => {
				if (checkbox.checked) {
					checkbox.style.setProperty('background-color', '#EF7F1F', 'important')
					checkbox.style.setProperty('border-color', '#EF7F1F', 'important')
				} else {
					// Reset to transparent background and black border when unchecked
					checkbox.style.setProperty(
						'background-color',
						'transparent',
						'important',
					)
					checkbox.style.setProperty('border-color', '#000000', 'important')
				}
			}
			checkbox.addEventListener('change', updateCheckboxStyle)
			updateCheckboxStyle() // Apply initial state
		})

		// Force search input white background
		const searchInputs = document.querySelectorAll('.search-input-white input')
		searchInputs.forEach((input) => {
			input.style.setProperty('background-color', 'white', 'important')
			input.style.setProperty('color', '#374151', 'important')
		})
	}, 100)
})

const setFiltersFromQuery = () => {
	let queries = new URLSearchParams(location.search)
	title.value = queries.get('title') || ''

	// Don't set category if it's "Semua Jalur" or similar
	const categoryParam = queries.get('category')
	if (
		categoryParam &&
		categoryParam !== 'Semua Jalur' &&
		categoryParam !== 'Semua+Jalur'
	) {
		currentCategory.value = categoryParam
	} else {
		currentCategory.value = null
	}

	certification.value = queries.get('certification') === 'true'
}

const courses = createListResource({
	doctype: 'LMS Course',
	url: 'lms.lms.utils.get_courses',
	cache: ['courses', user.data?.name],
	pageLength: pageLength.value,
	start: start.value,
	auto: true,
	onSuccess(data) {
		// Don't update categories here anymore, get them separately
	},
})

const isPersonaCaptured = async () => {
	let persona = await call('frappe.client.get_single_value', {
		doctype: 'LMS Settings',
		field: 'persona_captured',
	})
	return persona
}

const identifyUserPersona = async () => {
	if (user.data?.is_system_manager && !user.data?.developer_mode) {
		let personaCaptured = await isPersonaCaptured()
		if (personaCaptured) return
		if (!courseCount.value) {
			router.push({
				name: 'PersonaForm',
			})
		}
	}
}

const getCourseCount = () => {
	if (!user.data) return

	call('frappe.client.get_count', {
		doctype: 'LMS Course',
	}).then((data) => {
		courseCount.value = data
		identifyUserPersona()
	})
}

const getAllCategories = () => {
	call('lms.lms.api.get_categories', {
		doctype: 'LMS Course',
		filters: {}, // Get all categories, not just from published courses
	}).then((data) => {
		updateCategories(data)
	})
}

const updateCourses = () => {
	updateFilters()

	// Debug logging
	console.log('Current filters:', filters.value)
	console.log('Current category:', currentCategory.value)
	console.log('Current tab:', currentTab.value)

	courses.update({
		filters: filters.value,
	})
	courses.reload()
}

const updateFilters = () => {
	// Reset filters first to avoid conflicts
	filters.value = {}

	updateCategoryFilter()
	updateTitleFilter()
	updateCertificationFilter()
	updateTabFilter()
	updateStudentFilter()
	setQueryParams()
}

const updateCategoryFilter = () => {
	if (
		currentCategory.value &&
		currentCategory.value !== null &&
		currentCategory.value !== 'Semua Jalur' &&
		currentCategory.value !== 'Semua+Jalur'
	) {
		filters.value['category'] = currentCategory.value
	}
	// No need to delete since filters are reset at the start of updateFilters()
}

const updateTitleFilter = () => {
	if (title.value) {
		filters.value['title'] = ['like', `%${title.value}%`]
	} else {
		delete filters.value['title']
	}
}

const updateCertificationFilter = () => {
	if (certification.value) {
		filters.value['certification'] = 1
	} else {
		delete filters.value['certification']
	}
}

const updateTabFilter = () => {
	delete filters.value['live']
	delete filters.value['created']
	delete filters.value['published_on']
	delete filters.value['upcoming']
	delete filters.value['published']
	delete filters.value['enrolled']

	if (currentTab.value == 'enrolled' && user.data?.is_student) {
		filters.value['enrolled'] = 1
	} else {
		if (currentTab.value == 'live') {
			filters.value['published'] = 1
			filters.value['upcoming'] = 0
			filters.value['live'] = 1
		} else if (currentTab.value == 'upcoming') {
			filters.value['upcoming'] = 1
		} else if (currentTab.value == 'new') {
			filters.value['published'] = 1
			filters.value['published_on'] = [
				'>=',
				dayjs().add(-3, 'month').format('YYYY-MM-DD'),
			]
		} else if (currentTab.value == 'created') {
			filters.value['created'] = 1
		} else if (currentTab.value == 'unpublished') {
			filters.value['published'] = 0
		}
	}
}

const updateStudentFilter = () => {
	if (!user.data || (user.data?.is_student && currentTab.value != 'enrolled')) {
		filters.value['published'] = 1
	}
}

const setQueryParams = () => {
	let queries = new URLSearchParams(location.search)
	let filterKeys = {
		title: title.value,
		category:
			currentCategory.value && currentCategory.value !== 'Semua Jalur'
				? currentCategory.value
				: null,
		certification: certification.value,
	}

	Object.keys(filterKeys).forEach((key) => {
		if (filterKeys[key]) {
			queries.set(key, filterKeys[key])
		} else {
			queries.delete(key)
		}
	})

	let queryString = ''
	if (queries.toString()) {
		queryString = `?${queries.toString()}`
	}

	history.replaceState({}, '', `${location.pathname}${queryString}`)
}

const updateCategories = (data) => {
	// Start with "Semua Jalur" option
	const baseCategories = [
		{
			label: 'Semua Jalur',
			value: null,
		},
	]

	// Add categories from API response
	if (data && Array.isArray(data)) {
		data.forEach((category) => {
			baseCategories.push({
				label: category.label,
				value: category.value,
			})
		})
	}

	categories.value = baseCategories
}

watch(currentTab, () => {
	updateCourses()
})

watch(
	currentCategory,
	() => {
		updateCourses()
	},
	{ immediate: false },
)

// Watch certification checkbox changes to ensure orange styling
watch(certification, () => {
	setTimeout(() => {
		const checkboxes = document.querySelectorAll(
			'.checkbox-orange input[type="checkbox"]',
		)
		checkboxes.forEach((checkbox) => {
			if (checkbox.checked) {
				checkbox.style.setProperty('background-color', '#EF7F1F', 'important')
				checkbox.style.setProperty('border-color', '#EF7F1F', 'important')
			} else {
				// Reset to transparent background and black border when unchecked
				checkbox.style.setProperty(
					'background-color',
					'transparent',
					'important',
				)
				checkbox.style.setProperty('border-color', '#000000', 'important')
			}
		})
	}, 10)
})

onUnmounted(() => {
	try {
		// Reset state when leaving page
		categories.value = [
			{
				label: 'Semua Jalur',
				value: null,
			},
		]
		currentCategory.value = null
		title.value = ''
		certification.value = false
		filters.value = {}

		// Reset courses data if possible
		if (courses && typeof courses.reset === 'function') {
			courses.reset()
		}
	} catch (error) {
		console.error('Error in Courses unmount:', error)
	}
})

const courseTabs = computed(() => {
	let tabs = [
		{
			label: __('👩‍💻 Terbuka'),
			value: 'live',
		},
		{
			label: __('⚡ Baru'),
			value: 'new',
		},
		{
			label: __('🧑‍⚖️ Akan Datang'),
			value: 'upcoming',
		},
	]
	if (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	) {
		tabs.push({ label: __('Created'), value: 'created' })
		tabs.push({ label: __('Unpublished'), value: 'unpublished' })
	} else if (user.data) {
		tabs.push({ label: __('Enrolled'), value: 'enrolled' })
	}
	return tabs
})

const breadcrumbs = computed(() => [
	{
		label: __('📖 Kursus > Semua Kursus'),
		route: { name: 'Courses' },
	},
])

usePageMeta(() => {
	return {
		title: __('Courses'),
		icon: brand.favicon,
	}
})
</script>

<style scoped>
/* Custom styling for form controls */
.checkbox-orange :deep(input[type='checkbox']) {
	border-color: #000000 !important;
	background-color: transparent !important;
}

.checkbox-orange :deep(input[type='checkbox']:checked) {
	background-color: #ef7f1f !important;
	border-color: #ef7f1f !important;
	background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='m13.854 3.646-7.5 7.5a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6 10.293l7.146-7.147a.5.5 0 0 1 .708.708z'/%3e%3c/svg%3e") !important;
}

.search-input-white :deep(input) {
	background-color: white !important;
	color: #374151 !important;
}

.search-input-white :deep(input::placeholder) {
	color: #9ca3af !important;
}
</style>

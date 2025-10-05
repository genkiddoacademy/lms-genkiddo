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
						class="!checked:bg-orange-2"
						@change="updateCourses()"
					/>

					<FormControl
						v-model="title"
						:placeholder="__('Cari Berdasarkan Judul')"
						type="text"
						class="ring-1 ring-orange-2 rounded-sm !bg-white !text-gray-900 !placeholder-white focus:!bg-orange-50 focus:ring-2 focus:ring-orange-300 transition-all duration-200"
						@input="updateCourses()"
					>
						<template #prefix>
							<Search class="h-4 w-4" />
						</template>
					</FormControl>
				</div>
			</div>

			<div class="flex-row flex gap-2 items-center w-full !text-lg">
				Learning Path:
				<Select
					v-model="currentCategory"
					:options="categories"
					:placeholder="__('Semua Jalur')"
					@change="updateCourses()"
					class="!min-w-36 !w-fit !text-lg !bg-orange-2 flex !h-[40px]"
					style="color: white !important; --tw-placeholder-color: white"
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
import router from '../router'

const user = inject('$user')
const dayjs = inject('$dayjs')
const start = ref(0)
const pageLength = ref(30)
const categories = ref([])
const currentCategory = ref(null)
const title = ref('')
const certification = ref(false)
const filters = ref({})
const currentTab = ref('live')
const { brand } = sessionStore()
const courseCount = ref(0)

onMounted(() => {
	// Reset state to ensure clean load
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

	// Force reload courses data
	courses.reload()
	setFiltersFromQuery()
	updateCourses()
	getCourseCount()
})

const setFiltersFromQuery = () => {
	let queries = new URLSearchParams(location.search)
	title.value = queries.get('title') || ''
	currentCategory.value = queries.get('category') || null
	certification.value = queries.get('certification') || false
}

const courses = createListResource({
	doctype: 'LMS Course',
	url: 'lms.lms.utils.get_courses',
	cache: ['courses', user.data?.name, Date.now()],
	pageLength: pageLength.value,
	start: start.value,
	auto: true,
	onSuccess(data) {
		setCategories(data)
	},
})

const setCategories = (data) => {
	let allCategories = data.map((course) => course.category)
	allCategories = allCategories.filter(
		(category, index) => allCategories.indexOf(category) === index && category,
	)
	updateCategories(data)
}

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

const updateCourses = () => {
	updateFilters()
	courses.update({
		filters: filters.value,
	})
	courses.reload()
}

const updateFilters = () => {
	updateCategoryFilter()
	updateTitleFilter()
	updateCertificationFilter()
	updateTabFilter()
	updateStudentFilter()
	setQueryParams()
}

const updateCategoryFilter = () => {
	if (currentCategory.value) {
		filters.value['category'] = currentCategory.value
	} else {
		delete filters.value['category']
	}
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

	if (currentTab.value == 'enrolled' && user.data?.is_student) {
		filters.value['enrolled'] = 1
		delete filters.value['published']
	} else {
		delete filters.value['published']
		delete filters.value['enrolled']

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
	if (!user.data || (user.data?.is_student && currentTab.value != 'Enrolled')) {
		filters.value['published'] = 1
	}
}

const setQueryParams = () => {
	let queries = new URLSearchParams(location.search)
	let filterKeys = {
		title: title.value,
		category: currentCategory.value,
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
	// Reset categories but keep 'Semua Jalur' at first position
	const baseCategories = [
		{
			label: 'Semua Jalur',
			value: null,
		},
	]

	data.forEach((course) => {
		if (
			course.category &&
			!baseCategories.find((category) => category.value === course.category)
		) {
			baseCategories.push({
				label: course.category,
				value: course.category,
			})
		}
	})

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

onUnmounted(() => {
	try {
		// Reset state when leaving page
		categories.value = []
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

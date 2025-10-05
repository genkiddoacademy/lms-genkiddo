<template>
	<header
		class="sticky flex items-center justify-between top-0 z-10 border-b bg-surface-white px-3 py-2.5 sm:px-5"
	>
		<div class="!font-bold">
			<Breadcrumbs :items="breadcrumbs" class="!text-3xl !font-bold" />
		</div>
		<router-link
			v-if="canCreateBatch()"
			:to="{
				name: 'BatchForm',
				params: { batchName: 'new' },
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
					:buttons="batchTabs"
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
						@change="updateBatches()"
					/>

					<FormControl
						v-model="title"
						:placeholder="__('Cari Berdasarkan Judul')"
						type="text"
						class="ring-1 ring-orange-2 rounded-sm !bg-white !text-gray-900 !placeholder-white focus:!bg-orange-50 focus:ring-2 focus:ring-orange-300 transition-all duration-200"
						@input="updateBatches()"
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
					v-if="categories.length"
					v-model="currentCategory"
					:options="categories"
					:placeholder="__('Category')"
					@change="updateBatches()"
					class="!min-w-36 !w-fit !text-lg !placeholder:text-white !bg-orange-2 !text-white flex !h-[40px]"
				/>
			</div>
		</div>
		<div
			v-if="batches.data?.length"
			class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-5"
		>
			<router-link
				v-for="batch in batches.data"
				:to="{ name: 'BatchDetail', params: { batchName: batch.name } }"
			>
				<BatchCard :batch="batch" />
			</router-link>
		</div>
		<EmptyState v-else-if="!batches.list.loading" type="Batches" />

		<div
			v-if="!batches.list.loading && batches.hasNextPage"
			class="flex justify-center mt-5"
		>
			<Button @click="batches.next()">
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
import { computed, inject, onMounted, ref, watch } from 'vue'
import { Plus, Search } from 'lucide-vue-next'
import { sessionStore } from '@/stores/session'
import BatchCard from '@/components/BatchCard.vue'
import EmptyState from '@/components/EmptyState.vue'

const user = inject('$user')
const dayjs = inject('$dayjs')
const { brand } = sessionStore()
const start = ref(0)
const pageLength = ref(30)
const categories = ref([])
const currentCategory = ref(null)
const title = ref('')
const certification = ref(false)
const filters = ref({})
const is_student = computed(() => user.data?.is_student)
const currentTab = ref(is_student.value ? 'All' : 'Upcoming')
const orderBy = ref('start_date')
const readOnlyMode = window.read_only_mode

onMounted(() => {
	setFiltersFromQuery()
	updateBatches()
	categories.value = [
		{
			label: '',
			value: null,
		},
	]
})

const setFiltersFromQuery = () => {
	let queries = new URLSearchParams(location.search)
	title.value = queries.get('title') || ''
	currentCategory.value = queries.get('category') || null
	certification.value = queries.get('certification') || false
}

const batches = createListResource({
	doctype: 'LMS Batch',
	url: 'lms.lms.utils.get_batches',
	cache: ['batches', user.data?.name],
	pageLength: pageLength.value,
	start: start.value,
	onSuccess(data) {
		let allCategories = data.map((batch) => batch.category)
		allCategories = allCategories.filter(
			(category, index) =>
				allCategories.indexOf(category) === index && category,
		)
		if (categories.value.length <= allCategories.length) {
			updateCategories(data)
		}
	},
})

const updateBatches = () => {
	updateFilters()
	batches.update({
		filters: filters.value,
		orderBy: orderBy.value,
	})
	batches.reload()
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
	orderBy.value = 'start_date'
	if (!user.data) {
		return
	}
	if (currentTab.value == 'Enrolled' && is_student.value) {
		filters.value['enrolled'] = 1
		delete filters.value['start_date']
		delete filters.value['published']
		orderBy.value = 'start_date desc'
	} else if (is_student.value) {
		delete filters.value['enrolled']
	} else {
		delete filters.value['start_date']
		delete filters.value['published']
		orderBy.value = 'start_date desc'
		if (currentTab.value == 'Upcoming') {
			filters.value['start_date'] = ['>=', dayjs().format('YYYY-MM-DD')]
			filters.value['published'] = 1
			orderBy.value = 'start_date'
		} else if (currentTab.value == 'Archived') {
			filters.value['start_date'] = ['<=', dayjs().format('YYYY-MM-DD')]
		} else if (currentTab.value == 'Unpublished') {
			filters.value['published'] = 0
		}
	}
}

const updateStudentFilter = () => {
	if (!user.data || (is_student.value && currentTab.value != 'Enrolled')) {
		filters.value['start_date'] = ['>=', dayjs().format('YYYY-MM-DD')]
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
	data.forEach((batch) => {
		if (
			batch.category &&
			!categories.value.find((category) => category.value === batch.category)
		)
			categories.value.push({
				label: batch.category,
				value: batch.category,
			})
	})
}

watch(currentTab, () => {
	updateBatches()
})

const batchTabs = computed(() => {
	let tabs = [
		{
			label: __('👩‍💻 Terbuka'),
			value: 'All',
		},
		{
			label: __('⚡ Akan Datang'),
			value: 'Upcoming',
		},
	]

	if (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	) {
		tabs.push({ label: __('📝 Archived'), value: 'Archived' })
		tabs.push({ label: __('🔒 Unpublished'), value: 'Unpublished' })
	} else if (user.data) {
		tabs.push({ label: __('📚 Enrolled'), value: 'Enrolled' })
	}
	return tabs
})

const canCreateBatch = () => {
	if (readOnlyMode) return false
	if (user.data?.is_moderator || user.data?.is_instructor) return true
	return false
}

const breadcrumbs = computed(() => [
	{
		label: __('🧑‍🤝‍🧑 Batch > Semua Batch'),
		route: { name: 'Batches' },
	},
])

usePageMeta(() => {
	return {
		title: __('Batches'),
		icon: brand.favicon,
	}
})
</script>

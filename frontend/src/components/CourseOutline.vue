<template>
	<div class="">
		<div
			v-if="title && (outline.data?.length || allowEdit)"
			class="flex items-center justify-between space-x-2 mb-4"
			:class="{
				'sticky top-0 z-10 bg-surface-white border-b px-3 py-2.5 sm:px-5':
					allowEdit,
			}"
		>
			<div
				class="text-3xl font-extrabold text-gradasi-1"
				:class="{ 'font-medium text-p-base': allowEdit }"
			>
				{{ __(title) }}
			</div>
			<Button size="sm" v-if="allowEdit" @click="openChapterModal()">
				{{ __('Add Chapter') }}
			</Button>
		</div>
		<div class="border rounded-md">
			<Draggable
				:list="outline.data"
				:disabled="!allowEdit"
				item-key="name"
				group="chapters"
				@end="updateChapterOrder"
			>
				<template #item="{ element: chapter, index }">
					<div class="chapter-item">
						<div class="w-full">
							<div
								class="flex items-center p-3 transition-colors duration-200 group cursor-pointer"
								:class="[
									getChapterRoundedClass(index),
									isChapterOpen(chapter.name)
										? 'bg-orange-2 text-white'
										: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
								]"
								@click="handleChapterClick(chapter)"
							>
								<ChevronRight
									:class="{
										'rotate-90 transform duration-200': isChapterOpen(
											chapter.name,
										),
										'duration-200': !isChapterOpen(chapter.name),
										hidden: chapter.is_scorm_package,
									}"
									class="h-4 w-4 mr-2"
								/>
								<div class="text-lg text-left font-bold leading-5 flex-1">
									{{ chapter.title }}
								</div>
								<div v-if="allowEdit" class="flex ml-auto space-x-2">
									<Tooltip :text="__('Edit Chapter')" placement="bottom">
										<FilePenLine
											@click.stop.prevent="openChapterModal(chapter)"
											class="h-4 w-4 opacity-75 hover:opacity-100 invisible group-hover:visible"
										/>
									</Tooltip>
									<Tooltip :text="__('Delete Chapter')" placement="bottom">
										<Trash2
											@click.stop.prevent="trashChapter(chapter.name)"
											class="h-4 w-4 text-red-300 opacity-75 hover:opacity-100 invisible group-hover:visible"
										/>
									</Tooltip>
								</div>
							</div>
							<div
								v-if="!chapter.is_scorm_package && isChapterOpen(chapter.name)"
								class="mt-2"
							>
								<div class="rounded-lg p-2">
									<Draggable
										v-if="!chapter.is_scorm_package"
										:list="chapter.lessons"
										:disabled="!allowEdit"
										item-key="name"
										group="items"
										@end="updateOutline"
										:data-chapter="chapter.name"
									>
										<template #item="{ element: lesson }">
											<div
												class="lesson-item flex items-center p-2 hover:bg-yellow-100 rounded transition-colors group"
												:class="
													isActiveLesson(lesson.number) ? 'bg-yellow-100' : ''
												"
											>
												<router-link
													:to="{
														name: allowEdit ? 'LessonForm' : 'Lesson',
														params: {
															courseName: courseName,
															chapterNumber: lesson.number.split('.')[0],
															lessonNumber: lesson.number.split('.')[1],
														},
													}"
													class="flex items-center flex-1 text-sm"
													@click="ensureChapterOpen(chapter.name)"
												>
													<div class="flex items-center flex-1">
														<!-- Lesson Icon -->
														<MonitorPlay
															v-if="lesson.icon === 'icon-youtube'"
															class="h-4 w-4 stroke-1 mr-3 text-gray-600"
														/>
														<HelpCircle
															v-else-if="lesson.icon === 'icon-quiz'"
															class="h-4 w-4 stroke-1 mr-3 text-gray-600"
														/>
														<FileText
															v-else
															class="h-4 w-4 stroke-1 mr-3 text-gray-600"
														/>

														<!-- Lesson Title -->
														<div class="lesson-title text-gray-900">
															{{ lesson.title }}
														</div>
													</div>
												</router-link>

												<!-- Completion Status -->
												<div class="completion-status flex items-center ml-2">
													<Trash2
														v-if="allowEdit"
														@click.prevent="
															trashLesson(lesson.name, chapter.name)
														"
														class="h-4 w-4 text-red-500 mr-2 opacity-0 group-hover:opacity-100 transition-opacity"
													/>
													<div class="relative">
														<Check
															v-if="lesson.is_complete"
															class="h-5 w-5 text-green-600 bg-green-100 rounded-full p-1"
														/>
														<div
															v-else-if="lesson.icon === 'icon-quiz'"
															class="h-5 w-5 bg-yellow-300 rounded-full border-2 border-yellow-500"
														></div>
														<div
															v-else
															class="h-5 w-5 bg-gray-200 rounded-full border-2 border-gray-300"
														></div>
													</div>
												</div>
											</div>
										</template>
									</Draggable>
									<div v-if="allowEdit" class="flex mt-2 mb-2 pl-8">
										<router-link
											v-if="!chapter.is_scorm_package"
											:to="{
												name: 'LessonForm',
												params: {
													courseName: courseName,
													chapterNumber: chapter.idx,
													lessonNumber: chapter.lessons.length + 1,
												},
											}"
										>
											<Button size="sm">
												{{ __('Add Lesson') }}
											</Button>
										</router-link>
									</div>
								</div>
							</div>
						</div>
					</div>
				</template>
			</Draggable>
		</div>
	</div>
	<ChapterModal
		v-if="user.data"
		v-model="showChapterModal"
		v-model:outline="outline"
		:course="courseName"
		:chapterDetail="getCurrentChapter()"
	/>
</template>
<script setup>
import { Button, createResource, Tooltip, toast } from 'frappe-ui'
import { getCurrentInstance, inject, ref, watch, onMounted } from 'vue'
import Draggable from 'vuedraggable'
import {
	Check,
	ChevronRight,
	FileText,
	FilePenLine,
	HelpCircle,
	MonitorPlay,
	Trash2,
} from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'
import ChapterModal from '@/components/Modals/ChapterModal.vue'

const route = useRoute()
const router = useRouter()
const user = inject('$user')
const showChapterModal = ref(false)
const currentChapter = ref(null)
const activeChapter = ref(null)
const app = getCurrentInstance()
const { $dialog } = app.appContext.config.globalProperties

// Function to get localStorage key for this course
const getStorageKey = () => `accordion_state_${props.courseName}`

// Function to save accordion state to localStorage
const saveAccordionState = () => {
	if (activeChapter.value) {
		localStorage.setItem(getStorageKey(), activeChapter.value)
	} else {
		localStorage.removeItem(getStorageKey())
	}
}

// Function to load accordion state from localStorage
const loadAccordionState = () => {
	const savedState = localStorage.getItem(getStorageKey())
	return savedState
}

const props = defineProps({
	courseName: {
		type: String,
		required: true,
	},
	showOutline: {
		type: Boolean,
		default: false,
	},
	title: {
		type: String,
		default: '',
	},
	allowEdit: {
		type: Boolean,
		default: false,
	},
	getProgress: {
		type: Boolean,
		default: false,
	},
})

const outline = createResource({
	url: 'lms.lms.utils.get_course_outline',
	cache: ['course_outline', props.courseName],
	makeParams() {
		return {
			course: props.courseName,
			progress: props.getProgress,
		}
	},
	auto: true,
	onSuccess(data) {
		if (data && data.length > 0) {
			// Always prioritize current route chapter when navigating to a lesson
			const currentChapterIdx = route.params.chapterNumber
			const currentLessonIdx = route.params.lessonNumber

			if (currentChapterIdx && currentLessonIdx) {
				// User is viewing a specific lesson, ensure its chapter is open
				const targetChapter = data.find(
					(chapter) => chapter.idx == currentChapterIdx,
				)
				if (targetChapter) {
					activeChapter.value = targetChapter.name
					saveAccordionState()
					return
				}
			}

			// If not viewing a specific lesson, try to restore from localStorage
			const savedState = loadAccordionState()
			if (savedState) {
				// Check if saved chapter still exists in the data
				const savedChapter = data.find((chapter) => chapter.name === savedState)
				if (savedChapter) {
					activeChapter.value = savedState
					return
				}
			}

			// If no saved state or saved chapter doesn't exist, set based on current route or default
			if (!activeChapter.value) {
				const currentChapterIdx = route.params.chapterNumber || 1
				const targetChapter = data.find(
					(chapter) => chapter.idx == currentChapterIdx,
				)
				if (targetChapter) {
					activeChapter.value = targetChapter.name
				} else {
					activeChapter.value = data[0].name // Default to first chapter
				}
			}
		}
	},
})

watch(
	() => props.courseName,
	() => {
		// Clear localStorage for old course and reset active chapter when course changes
		localStorage.removeItem(getStorageKey())
		activeChapter.value = null
		outline.reload()
	},
)

// Watch for route changes to ensure current chapter is open
watch(
	() => [route.params.chapterNumber, route.params.lessonNumber],
	([newChapterNumber, newLessonNumber]) => {
		if (newChapterNumber && outline.data) {
			const targetChapter = outline.data.find(
				(chapter) => chapter.idx == newChapterNumber,
			)
			// Always open the chapter that contains the current lesson
			if (targetChapter) {
				activeChapter.value = targetChapter.name
				saveAccordionState()
			}
		}
	},
	{ immediate: true }, // Execute immediately when watcher is created
)

// Watch activeChapter changes to save state automatically
watch(activeChapter, () => {
	saveAccordionState()
})

// Watch when outline data becomes available and ensure current lesson's chapter is open
watch(
	() => outline.data,
	(newData) => {
		if (newData && newData.length > 0) {
			const currentChapterIdx = route.params.chapterNumber
			const currentLessonIdx = route.params.lessonNumber

			// If viewing a specific lesson and no chapter is currently open
			if (currentChapterIdx && currentLessonIdx && !activeChapter.value) {
				const targetChapter = newData.find(
					(chapter) => chapter.idx == currentChapterIdx,
				)
				if (targetChapter) {
					activeChapter.value = targetChapter.name
					saveAccordionState()
				}
			}
		}
	},
	{ immediate: true },
)

// Ensure accordion is open when component mounts
onMounted(() => {
	// Double-check accordion state after component mounts
	const currentChapterIdx = route.params.chapterNumber
	const currentLessonIdx = route.params.lessonNumber

	if (currentChapterIdx && currentLessonIdx && outline.data) {
		const targetChapter = outline.data.find(
			(chapter) => chapter.idx == currentChapterIdx,
		)
		if (targetChapter && !activeChapter.value) {
			activeChapter.value = targetChapter.name
			saveAccordionState()
		}
	}
})

const deleteLesson = createResource({
	url: 'lms.lms.api.delete_lesson',
	makeParams(values) {
		return {
			lesson: values.lesson,
			chapter: values.chapter,
		}
	},
	onSuccess() {
		outline.reload()
		toast.success(__('Lesson deleted successfully'))
	},
})

const updateLessonIndex = createResource({
	url: 'lms.lms.api.update_lesson_index',
	makeParams(values) {
		return {
			lesson: values.lesson,
			sourceChapter: values.sourceChapter,
			targetChapter: values.targetChapter,
			idx: values.idx,
		}
	},
	onSuccess() {
		toast.success(__('Lesson moved successfully'))
	},
})

const updateChapterIndex = createResource({
	url: 'lms.lms.api.update_chapter_index',
	makeParams(values) {
		return {
			chapter: values.chapter,
			course: values.course,
			idx: values.idx,
		}
	},
	onSuccess() {
		toast.success(__('Chapter moved successfully'))
	},
})

const trashLesson = (lessonName, chapterName) => {
	$dialog({
		title: __('Delete this lesson?'),
		message: __(
			'Deleting this lesson will permanently remove it from the course. This action cannot be undone. Are you sure you want to continue?',
		),
		actions: [
			{
				label: __('Delete'),
				theme: 'red',
				variant: 'solid',
				onClick(close) {
					deleteLesson.submit({
						lesson: lessonName,
						chapter: chapterName,
					})
					close()
				},
			},
		],
	})
}

const openChapterDetail = (index) => {
	return index == route.params.chapterNumber || index == 1
}

const toggleChapter = (chapterName) => {
	if (activeChapter.value === chapterName) {
		activeChapter.value = null
	} else {
		activeChapter.value = chapterName
	}
	// Save state to localStorage whenever accordion is toggled
	saveAccordionState()
}

const isChapterOpen = (chapterName) => {
	return activeChapter.value === chapterName
}

const ensureChapterOpen = (chapterName) => {
	activeChapter.value = chapterName
	saveAccordionState()
}

const openChapterModal = (chapter = null) => {
	currentChapter.value = chapter
	showChapterModal.value = true
}

const getCurrentChapter = () => {
	return currentChapter.value
}

const getChapterRoundedClass = (index) => {
	if (!outline.data || outline.data.length === 0) return 'rounded-md'

	const totalChapters = outline.data.length

	if (totalChapters === 1) {
		// Jika hanya ada satu chapter, gunakan rounded penuh
		return 'rounded-md'
	} else if (index === 0) {
		// Chapter pertama: rounded atas saja
		return 'rounded-t-md'
	} else if (index === totalChapters - 1) {
		// Chapter terakhir: rounded bawah saja
		return 'rounded-b-md'
	} else {
		// Chapter tengah: tidak ada rounded
		return ''
	}
}

const updateOutline = (e) => {
	updateLessonIndex.submit({
		lesson: e.item.__draggable_context.element.name,
		sourceChapter: e.from.dataset.chapter,
		targetChapter: e.to.dataset.chapter,
		idx: e.newIndex,
	})
}

const updateChapterOrder = (e) => {
	updateChapterIndex.submit({
		chapter: e.item.__draggable_context.element.name,
		course: props.courseName,
		idx: e.newIndex,
	})
}

const deleteChapter = createResource({
	url: 'lms.lms.api.delete_chapter',
	makeParams(values) {
		return {
			chapter: values.chapter,
		}
	},
	onSuccess() {
		outline.reload()
		toast.success(__('Chapter deleted successfully'))
	},
})

const trashChapter = (chapterName) => {
	$dialog({
		title: __('Delete this chapter?'),
		message: __(
			'Deleting this chapter will also delete all its lessons and permanently remove it from the course. This action cannot be undone. Are you sure you want to continue?',
		),
		actions: [
			{
				label: __('Delete'),
				theme: 'red',
				variant: 'solid',
				onClick(close) {
					deleteChapter.submit({ chapter: chapterName })
					close()
				},
			},
		],
	})
}

const handleChapterClick = (chapter) => {
	// If it's a SCORM package, redirect to the SCORM chapter
	if (chapter.is_scorm_package) {
		redirectToChapter(chapter)
	} else {
		// Otherwise, toggle the accordion
		toggleChapter(chapter.name)
	}
}

const redirectToChapter = (chapter) => {
	if (!chapter.is_scorm_package) return
	if (props.allowEdit) return
	if (!user.data) {
		toast.success(__('Please enroll for this course to view this lesson'))
		return
	}

	router.push({
		name: 'SCORMChapter',
		params: {
			courseName: props.courseName,
			chapterName: chapter.name,
		},
	})
}

const isActiveLesson = (lessonNumber) => {
	return (
		route.params.chapterNumber == lessonNumber.split('.')[0] &&
		route.params.lessonNumber == lessonNumber.split('.')[1]
	)
}
</script>

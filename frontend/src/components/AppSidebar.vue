<template>
	<div
		class="flex h-full flex-col transition-all duration-300 ease-in-out border-r bg-surface-menu-bar overflow-hidden"
		:class="sidebarStore.isSidebarCollapsed ? 'w-20' : '!w-[260px]'"
	>
		<div
			class="flex flex-col flex-1 overflow-y-auto overflow-x-hidden h-fit px-4 scrollbar-hide"
			:class="sidebarStore.isSidebarCollapsed ? 'items-center' : ''"
		>
			<div
				class="flex items-center flex-col py-1 w-full"
				:class="
					sidebarStore.isSidebarCollapsed
						? 'justify-center space-x-1'
						: 'justify-between'
				"
			>
				<div class="flex items-center justify-center flex-1 min-w-0 pt-4">
					<Tooltip :text="__('Toggle sidebar')">
						<div
							class="flex items-center justify-center w-6 h-6 rounded hover:bg-surface-gray-2 transition-colors flex-shrink-0 cursor-pointer"
							@click="toggleSidebar()"
						>
							<Menu class="w-4 h-4 text-ink-gray-7" />
						</div>
					</Tooltip>

					<UserDropdown :isCollapsed="sidebarStore.isSidebarCollapsed" />
				</div>
			</div>
			<!-- Main Content Sections -->

			<!-- Theme Toggle and Main Links -->
			<div
				class="border-t-2 border-gray-200 flex flex-col py-2"
				v-if="sidebarSettings.data || !user"
			>
				<!-- Theme Toggle: render expanded or collapsed UI inside same parent -->
				<div
					v-if="!sidebarStore.isSidebarCollapsed"
					class="py-2 flex items-center justify-center mb-2"
				>
					<button
						type="button"
						:aria-pressed="isDarkMode ? 'true' : 'false'"
						class="relative inline-flex items-center gap-2 rounded-full px-4 py-2 select-none transition ring-1 ring-black/5 shadow-sm"
						:class="
							isDarkMode
								? 'bg-gray-200 text-gray-700'
								: 'bg-warning-100 text-white'
						"
						@click="handleThemeClick"
					>
						<span class="text-xs font-semibold tracking-wide">{{
							isDarkMode ? 'GELAP' : 'TERANG'
						}}</span>
						<Sun v-if="!isDarkMode" :size="18" class="shrink-0" />
						<Moon v-else :size="18" class="shrink-0" />
					</button>
				</div>

				<div v-else class="px-2 py-2 flex items-center justify-center mb-2">
					<button
						type="button"
						class="grid place-items-center w-9 h-9 rounded-full ring-1 shadow-sm transition"
						:class="
							isDarkMode
								? 'bg-black ring-white text-white'
								: 'bg-warning-100 ring-warning-100 text-white'
						"
						@click="handleThemeClick"
					>
						<Sun v-if="!isDarkMode" :size="18" />
						<Moon v-else :size="18" />
					</button>
				</div>

				<SidebarLink
					v-for="link in sidebarLinks"
					:key="link.to"
					:link="link"
					:isCollapsed="sidebarStore.isSidebarCollapsed"
					class="px-2 my-0.5"
				/>
			</div>

			<!-- Guest User Section -->
			<div
				v-if="!user"
				class="border-t-2 border-gray-200 py-2"
				:class="
					sidebarStore.isSidebarCollapsed
						? 'flex flex-col items-center space-y-1'
						: 'flex flex-col'
				"
			>
				<SidebarLink
					:link="{
						label: 'Halaman Utama',
						icon: 'Command',
						to: 'Home',
						activeFor: ['Home'],
						onClick: goToHome,
					}"
					:isCollapsed="sidebarStore.isSidebarCollapsed"
					:class="sidebarStore.isSidebarCollapsed ? 'w-fit' : 'px-2 my-0.5'"
				/>

				<!-- Login/Register Buttons -->
				<div
					v-if="!user"
					class="py-2 pt-4"
					:class="
						sidebarStore.isSidebarCollapsed
							? 'flex flex-col items-center space-y-2 px-2'
							: 'space-y-2 px-2'
					"
				>
					<div
						v-if="sidebarStore.isSidebarCollapsed"
						class="flex flex-col gap-1"
					>
						<Tooltip :text="'Log In'">
							<button
								@click="goToLogin"
								class="p-2 rounded ring-1 ring-orange-2 !border-orange-2 !text-orange-2 hover:!bg-orange-2/50"
							>
								<LogIn class="h-4 w-4" />
							</button>
						</Tooltip>
						<Tooltip :text="'Register'">
							<button
								@click="goToRegister"
								class="p-2 rounded !bg-orange-2 !text-white hover:!bg-orange-600"
							>
								<User class="h-4 w-4" />
							</button>
						</Tooltip>
					</div>
					<div v-else class="space-y-2">
						<Button
							variant="outline"
							class="w-full !border-orange-2 !text-orange-2 hover:!bg-orange-50"
							@click="goToLogin"
						>
							Log In
						</Button>
						<Button
							variant="solid"
							class="w-full !bg-orange-2 !text-white hover:!bg-orange-600"
							@click="goToRegister"
						>
							Register
						</Button>
					</div>
				</div>
			</div>

			<!-- User Profile and Settings Section -->
			<div
				v-if="user"
				class="border-t-2 border-gray-200 py-2"
				:class="
					sidebarStore.isSidebarCollapsed
						? 'flex flex-col items-center space-y-1'
						: 'flex flex-col'
				"
			>
				<SidebarLink
					:link="{
						label: 'Profile',
						icon: 'UserRound',
						to: 'Profile',
						activeFor: [
							'Profile',
							'ProfileAbout',
							'ProfileCertificates',
							'ProfileRoles',
							'ProfileEvaluator',
						],
						onClick: goToProfile,
					}"
					:isCollapsed="sidebarStore.isSidebarCollapsed"
					:class="sidebarStore.isSidebarCollapsed ? 'w-fit' : 'px-2 my-0.5'"
				/>
				<SidebarLink
					v-if="userResource.data?.roles?.includes('Administrator')"
					:link="{
						label: 'Pengaturan',
						icon: 'Settings',
						to: 'Settings',
						activeFor: ['Settings'],
						onClick: goToSettings,
					}"
					:isCollapsed="sidebarStore.isSidebarCollapsed"
					:class="sidebarStore.isSidebarCollapsed ? 'w-fit' : 'px-2 my-0.5'"
				/>
				<SidebarLink
					:link="{
						label: 'Bantuan',
						icon: 'HelpCircle',
						to: 'Help',
						activeFor: ['Help'],
						onClick: showHelp,
					}"
					:isCollapsed="sidebarStore.isSidebarCollapsed"
					:class="sidebarStore.isSidebarCollapsed ? 'w-fit' : 'px-2 my-0.5'"
				/>
				<SidebarLink
					:link="{
						label: 'Halaman Utama',
						icon: 'Command',
						to: 'Home',
						activeFor: ['Home'],
						onClick: goToHome,
					}"
					:isCollapsed="sidebarStore.isSidebarCollapsed"
					:class="sidebarStore.isSidebarCollapsed ? 'w-fit' : 'px-2 my-0.5'"
				/>
			</div>

			<!-- Logout Section -->
			<div
				v-if="user"
				class="border-t-2 border-gray-200 py-2"
				:class="
					sidebarStore.isSidebarCollapsed
						? 'flex flex-col items-center space-y-1'
						: 'flex flex-col'
				"
			>
				<SidebarLink
					:link="{
						label: 'Logout',
						icon: 'LogOut',
						to: null,
						onClick: handleLogout,
					}"
					:isCollapsed="sidebarStore.isSidebarCollapsed"
					:class="sidebarStore.isSidebarCollapsed ? 'w-fit' : 'px-2 my-0.5'"
				/>
			</div>
		</div>
		<!-- Web Pages Section -->
		<div
			v-if="sidebarSettings.data?.web_pages?.length"
			class="border-t-2 border-gray-200 py-2"
			:class="
				sidebarStore.isSidebarCollapsed ? 'flex flex-col items-center' : ''
			"
		>
			<div
				v-if="sidebarSettings.data?.web_pages?.length"
				class="flex flex-col"
				:class="sidebarStore.isSidebarCollapsed ? 'items-center space-y-1' : ''"
			>
				<SidebarLink
					v-for="link in sidebarSettings.data.web_pages"
					:key="link.name || link.to"
					:link="link"
					:isCollapsed="sidebarStore.isSidebarCollapsed"
					:class="sidebarStore.isSidebarCollapsed ? 'w-fit' : 'px-2 my-0.5'"
					:showControls="isModerator ? true : false"
					@openModal="openPageModal"
					@deletePage="deletePage"
				/>
			</div>
		</div>
	</div>

	<!-- Bottom Section -->
	<div class="flex-shrink-0 p-2 space-y-2">
		<div
			v-if="readOnlyMode && !sidebarStore.isSidebarCollapsed"
			class="bg-surface-modal py-2.5 px-3 text-xs text-ink-gray-7 leading-5 rounded-md"
		>
			{{
				__(
					'This site is being updated. You will not be able to make any changes. Full access will be restored shortly.',
				)
			}}
		</div>
		<TrialBanner
			v-if="
				userResource.data?.is_system_manager && userResource.data?.is_fc_site
			"
			:isSidebarCollapsed="sidebarStore.isSidebarCollapsed"
		/>
		<GettingStartedBanner
			v-if="showOnboarding && !isOnboardingStepsCompleted"
			:isSidebarCollapsed="sidebarStore.isSidebarCollapsed"
			appName="learning"
		/>

		<div
			v-if="readOnlyMode && sidebarStore.isSidebarCollapsed"
			class="flex justify-center"
		>
			<Tooltip>
				<CircleAlert class="size-4 stroke-1.5 text-ink-gray-7 cursor-pointer" />
				<template #body>
					<div
						class="max-w-[30ch] rounded bg-surface-gray-7 px-2 py-1 text-center text-p-xs text-ink-white shadow-xl"
					>
						{{
							__(
								'This site is being updated. You will not be able to make any changes. Full access will be restored shortly.',
							)
						}}
					</div>
				</template>
			</Tooltip>
		</div>
	</div>

	<!-- Modals -->
	<IntermediateStepModal
		v-model="showIntermediateModal"
		:currentStep="currentStep"
	/>
	<PageModal
		v-model="showPageModal"
		v-model:reloadSidebar="sidebarSettings"
		:page="pageToEdit"
	/>
</template>

<script setup>
const isDarkMode = ref(false)

const toggleTheme = () => {
	const newTheme = isDarkMode.value ? 'dark' : 'light'
	document.documentElement.setAttribute('data-theme', newTheme)
	localStorage.setItem('theme', newTheme)
}

function handleThemeClick() {
	isDarkMode.value = !isDarkMode.value
	toggleTheme()
}

import UserDropdown from '@/components/UserDropdown.vue'
import CollapseSidebar from '@/components/Icons/CollapseSidebar.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import {
	ref,
	onMounted,
	inject,
	watch,
	reactive,
	markRaw,
	h,
	onUnmounted,
} from 'vue'
import { getSidebarLinks } from '@/utils'
import { usersStore } from '@/stores/user'
import { sessionStore } from '@/stores/session'
import { useSidebar } from '@/stores/sidebar'
import { useSettings } from '@/stores/settings'
import { Button, createResource, Tooltip, call } from 'frappe-ui'
import PageModal from '@/components/Modals/PageModal.vue'
import { capture } from '@/telemetry'
import LMSLogo from '@/components/Icons/LMSLogo.vue'
import { useRouter } from 'vue-router'
import InviteIcon from './Icons/InviteIcon.vue'
import {
	BookOpen,
	CircleAlert,
	Plus,
	CircleHelp,
	FolderTree,
	FileText,
	UserPlus,
	Users,
	BookText,
	Zap,
	Menu,
	Sun,
	Moon,
	Command,
	LogIn,
	User,
	LogOut,
	UserRound,
	Settings,
	HelpCircle,
	LayoutDashboard
} from 'lucide-vue-next'
import {
	TrialBanner,
	HelpModal,
	GettingStartedBanner,
	useOnboarding,
	showHelpModal,
	minimize,
	IntermediateStepModal,
} from 'frappe-ui/frappe'

const { user, logout } = sessionStore()
const { userResource } = usersStore()
let sidebarStore = useSidebar()
const socket = inject('$socket')
const unreadCount = ref(0)
const sidebarLinks = ref(getSidebarLinks())
const showPageModal = ref(false)
const isModerator = ref(false)
const isInstructor = ref(false)
const pageToEdit = ref(null)
const settingsStore = useSettings()
const { sidebarSettings } = settingsStore
const showOnboarding = ref(false)
const showIntermediateModal = ref(false)
const currentStep = ref({})
const router = useRouter()
let onboardingDetails
let isOnboardingStepsCompleted = false
const readOnlyMode = window.read_only_mode
const isActive = ref(true)
const iconProps = {
	strokeWidth: 1.5,
	width: 16,
	height: 16,
}

onMounted(() => {
	if (user) {
		addNotifications()
		setSidebarLinks()
		if (userResource.data) {
			addAdminSidebar()
		}
	} else {
		addGuestSidebar()
	}
	setUpOnboarding()
	socket.on('publish_lms_notifications', (data) => {
		unreadNotifications.reload()
	})

	// Initialize theme
	const currentTheme =
		document.documentElement.getAttribute('data-theme') || 'light'
	isDarkMode.value = currentTheme === 'dark'
})

const setSidebarLinks = () => {
    if (!user) {
        return // Skip for guest users
    }
    sidebarSettings.reload(
        {},
        {
            onSuccess(data) {
                // Filter based on settings
                Object.keys(data).forEach((key) => {
                    if (!parseInt(data[key])) {
                        sidebarLinks.value = sidebarLinks.value.filter(
                            (link) => link.label.toLowerCase().split(' ').join('_') !== key,
                        )
                    }
                })

                // Filter based on user roles
                filterSidebarByRole()

                // Add Dashboard at the top if not already present
                if (!sidebarLinks.value.some((link) => link.label === 'Dashboard')) {
                    sidebarLinks.value.unshift({
                        label: 'Dashboard',
                        icon: 'LayoutDashboard',
                        to: 'Dashboard',
                        activeFor: ['Dashboard'],
                    })
                }

                // Add Chat with Kiko if not already present
                if (
                    !sidebarLinks.value.some((link) => link.label === 'Chat with Kiko')
                ) {
                    sidebarLinks.value.push({
                        label: 'Chat with Kiko',
                        icon: 'MessageCircle',
                        to: 'ChatKiko',
                        activeFor: ['ChatKiko'],
                    })
                }
            },
            onError() {
                // Handle error, keep default sidebarLinks
            },
        },
    )
}

const filterSidebarByRole = () => {
	if (!userResource.data?.roles) return

	const userRoles = userResource.data.roles
	const isAdmin = userRoles.includes('Administrator')
	const isModerator = userRoles.includes('Moderator')
	const isInstructor = userRoles.includes('Course Creator')
	const isEvaluator = userRoles.includes('Batch Evaluator')
	const isStudent = userRoles.includes('LMS Student')

	// Add Desk link for administrators
	if (isAdmin) {
		sidebarLinks.value.push({
			label: 'Desk',
			icon: 'Settings',
			to: '/app/lms',
			activeFor: [],
			onClick: () => {
				window.location.href = '/app/lms'
			},
		})
	}

	// Role-based filtering logic
	sidebarLinks.value = sidebarLinks.value.filter((link) => {
		switch (link.label) {
			case 'Statistics':
				return isAdmin || isModerator
			case 'Jobs':
				return isAdmin || isModerator
			case 'Programming Exercises':
				return true // All roles can access, but functionality differs
			case 'Certified Members':
				return true // All roles can view
			case 'Courses':
			case 'Batches':
				return true // All roles can access
			default:
				return true
		}
	})
}

const unreadNotifications = createResource({
	cache: 'Unread Notifications Count',
	url: 'frappe.client.get_count',
	makeParams(values) {
		return {
			doctype: 'Notification Log',
			filters: {
				for_user: user,
				read: 0,
			},
		}
	},
	onSuccess(data) {
		unreadCount.value = data
		sidebarLinks.value = sidebarLinks.value.map((link) => {
			if (link.label === 'Notifications') {
				link.count = data
			}
			return link
		})
	},
	auto: user ? true : false,
})

const addNotifications = () => {
	if (userResource.data?.is_system_manager || userResource.data?.is_moderator) {
		return // Admin sidebar already includes Notifications
	}
	if (user) {
		sidebarLinks.value.push({
			label: 'Notifications',
			icon: 'Bell',
			to: 'Notifications',
			activeFor: ['Notifications'],
			count: unreadCount.value,
		})
	}
}

const addQuizzes = () => {
	if (userResource.data?.is_system_manager || userResource.data?.is_moderator) {
		return // Admin sidebar already set
	}
	if (isInstructor.value || isModerator.value) {
		sidebarLinks.value.splice(4, 0, {
			label: 'Quizzes',
			icon: 'CircleHelp',
			to: 'Quizzes',
			activeFor: [
				'Quizzes',
				'QuizForm',
				'QuizSubmissionList',
				'QuizSubmission',
			],
		})
	}
}

const addAssignments = () => {
	if (userResource.data?.is_system_manager || userResource.data?.is_moderator) {
		return // Admin sidebar already set
	}
	if (isInstructor.value || isModerator.value) {
		sidebarLinks.value.splice(5, 0, {
			label: 'Assignments',
			icon: 'Pencil',
			to: 'Assignments',
			activeFor: [
				'Assignments',
				'AssignmentForm',
				'AssignmentSubmissionList',
				'AssignmentSubmission',
			],
		})
	}
}

const addAdminSidebar = () => {
	if (
		!userResource.data?.is_system_manager &&
		!userResource.data?.is_moderator
	) {
		return // Only for admin/moderator users
	}

	// For admin/moderator users, ensure all admin links are present
	const adminLinks = [
		{
			label: 'Statistics',
			icon: 'TrendingUp',
			to: 'Statistics',
			activeFor: ['Statistics'],
		},
		{
			label: 'Jobs',
			icon: 'Briefcase',
			to: 'Jobs',
			activeFor: ['Jobs', 'JobDetail'],
		},
		{
			label: 'Notifications',
			icon: 'Bell',
			to: 'Notifications',
			activeFor: ['Notifications'],
			count: unreadCount.value,
		},
	]

	// Add admin links that aren't already present
	adminLinks.forEach((adminLink) => {
		if (!sidebarLinks.value.some((link) => link.label === adminLink.label)) {
			sidebarLinks.value.push(adminLink)
		}
	})
}

const addPrograms = () => {
	if (userResource.data?.is_system_manager || userResource.data?.is_moderator) {
		return // Admin sidebar already set
	}
	let activeFor = ['Programs', 'ProgramForm']
	let index = 1
	let canAddProgram = false

	if (
		!isInstructor.value &&
		!isModerator.value &&
		settingsStore.learningPaths.data
	) {
		sidebarLinks.value = sidebarLinks.value.filter(
			(link) => link.label !== 'Courses',
		)
		activeFor.push('CourseDetail')
		activeFor.push('Lesson')
		index = 0
		canAddProgram = true
	} else if (isInstructor.value || isModerator.value) {
		canAddProgram = true
	}

	if (canAddProgram) {
		sidebarLinks.value.splice(index, 0, {
			label: 'Programs',
			icon: 'Route',
			to: 'Programs',
			activeFor: activeFor,
		})
	}
}

const addGuestSidebar = () => {
    if (!user) {
        sidebarLinks.value = [
            {
                label: 'Courses',
                icon: 'GraduationCap',
                to: 'Courses',
                activeFor: [
                    'Courses',
                    'CourseDetail',
                    'Lesson',
                    'CourseForm',
                    'LessonForm',
                ],
            },
            {
                label: 'Batches',
                icon: 'Users',
                to: 'Batches',
                activeFor: ['Batches', 'BatchDetail', 'Batch', 'BatchForm'],
            },
            {
                label: 'Chat with Kiko',
                icon: 'MessageCircle',
                to: 'ChatKiko',
                activeFor: ['ChatKiko'],
            },
        ]
    }
}

const openPageModal = (link) => {
	showPageModal.value = true
	pageToEdit.value = link
}

const deletePage = (link) => {
	createResource({
		url: 'lms.lms.api.delete_sidebar_item',
		makeParams(values) {
			return {
				webpage: link.web_page,
			}
		},
	}).submit(
		{},
		{
			onSuccess() {
				sidebarSettings.reload()
			},
		},
	)
}

const toggleSidebar = () => {
	sidebarStore.isSidebarCollapsed = !sidebarStore.isSidebarCollapsed
	localStorage.setItem(
		'isSidebarCollapsed',
		JSON.stringify(sidebarStore.isSidebarCollapsed),
	)
}

// Removed toggleWebPages (no longer needed)

const goToLogin = () => {
	window.location.href = '/login'
}

const goToRegister = () => {
	window.location.href = '/login#signup'
}

const goToHome = () => {
	// Navigate to the external Genkiddo site
	window.open('https://genkiddo.id/', '_blank')
}

const goToProfile = async () => {
	try {
		await router.push({
			name: 'Profile',
			params: {
				username: userResource.data?.username,
			},
		})
	} catch (error) {
		console.error('Navigation to profile failed:', error)
	}
}

const goToSettings = () => {
	settingsStore.isSettingsOpen = true
}

const showHelp = () => {
	showHelpModal.value = true
}

const handleLogout = () => {
	logout.submit().then(() => {
		window.location.reload()
	})
}

const getFirstCourse = async () => {
	let firstCourse = localStorage.getItem('firstCourse')
	if (firstCourse) return firstCourse
	return await call('lms.lms.onboarding.get_first_course')
}

const getFirstBatch = async () => {
	let firstBatch = localStorage.getItem('firstBatch')
	if (firstBatch) return firstBatch
	return await call('lms.lms.onboarding.get_first_batch')
}

const steps = reactive([
	{
		name: 'create_first_course',
		title: __('Create your first course'),
		icon: markRaw(h(BookOpen, iconProps)),
		completed: false,
		onClick: async () => {
			minimize.value = true
			try {
				await router.push({
					name: 'Courses',
				})
			} catch (error) {
				console.error('Navigation error:', error)
			}
		},
	},
	{
		name: 'create_first_chapter',
		title: __('Add your first chapter'),
		icon: markRaw(h(FolderTree, iconProps)),
		completed: false,
		dependsOn: 'create_first_course',
		onClick: async () => {
			minimize.value = true
			try {
				let course = await getFirstCourse()
				if (course) {
					await router.push({
						name: 'CourseForm',
						params: { courseName: course },
					})
				} else {
					await router.push({ name: 'CourseForm' })
				}
			} catch (error) {
				console.error('Navigation error:', error)
			}
		},
	},
	{
		name: 'create_first_lesson',
		title: __('Add your first lesson'),
		icon: markRaw(h(FileText, iconProps)),
		completed: false,
		dependsOn: 'create_first_chapter',
		onClick: async () => {
			minimize.value = true
			try {
				let course = await getFirstCourse()
				if (course) {
					await router.push({
						name: 'CourseForm',
						params: { courseName: course },
					})
				} else {
					await router.push({ name: 'Courses' })
				}
			} catch (error) {
				console.error('Navigation error:', error)
			}
		},
	},
	{
		name: 'create_first_quiz',
		title: __('Create your first quiz'),
		icon: markRaw(h(CircleHelp, iconProps)),
		completed: false,
		dependsOn: 'create_first_course',
		onClick: async () => {
			minimize.value = true
			try {
				await router.push({ name: 'Quizzes' })
			} catch (error) {
				console.error('Navigation error:', error)
			}
		},
	},
	{
		name: 'invite_students',
		title: __('Invite your team and students'),
		icon: markRaw(h(InviteIcon, iconProps)),
		completed: false,
		onClick: () => {
			minimize.value = true
			settingsStore.activeTab = 'Members'
			settingsStore.isSettingsOpen = true
		},
	},
	{
		name: 'create_first_batch',
		title: __('Create your first batch'),
		icon: markRaw(h(Users, iconProps)),
		completed: false,
		onClick: async () => {
			minimize.value = true
			try {
				await router.push({ name: 'Batches' })
			} catch (error) {
				console.error('Navigation error:', error)
			}
		},
	},
	{
		name: 'add_batch_student',
		title: __('Add students to your batch'),
		icon: markRaw(h(UserPlus, iconProps)),
		completed: false,
		dependsOn: 'create_first_batch',
		onClick: async () => {
			minimize.value = true
			try {
				let batch = await getFirstBatch()
				if (batch) {
					await router.push({
						name: 'Batch',
						params: {
							batchName: batch,
						},
					})
				} else {
					await router.push({ name: 'Batch' })
				}
			} catch (error) {
				console.error('Navigation error:', error)
			}
		},
	},
	{
		name: 'add_batch_course',
		title: __('Add courses to your batch'),
		icon: markRaw(h(BookText, iconProps)),
		completed: false,
		dependsOn: 'create_first_batch',
		onClick: async () => {
			minimize.value = true
			try {
				let batch = await getFirstBatch()
				if (batch) {
					await router.push({
						name: 'Batch',
						params: {
							batchName: batch,
						},
						hash: '#courses',
					})
				} else {
					await router.push({ name: 'Batch' })
				}
			} catch (error) {
				console.error('Navigation error:', error)
			}
		},
	},
])

const articles = ref([
	{
		title: __('Introduction'),
		opened: false,
		subArticles: [
			{ name: 'introduction', title: __('Introduction') },
			{ name: 'setting-up', title: __('Setting up') },
		],
	},
	{
		title: __('Creating a course'),
		opened: false,
		subArticles: [
			{ name: 'create-a-course', title: __('Create a course') },
			{ name: 'add-a-chapter', title: __('Add a chapter') },
			{ name: 'add-a-lesson', title: __('Add a lesson') },
		],
	},
	{
		title: __('Creating a batch'),
		opened: false,
		subArticles: [
			{ name: 'create-a-batch', title: __('Create a batch') },
			{ name: 'create-a-live-class', title: __('Create a live class') },
		],
	},
	{
		title: __('Assessments'),
		opened: false,
		subArticles: [
			{ name: 'quizzes', title: __('Quizzes') },
			{ name: 'assignments', title: __('Assignments') },
		],
	},
	{
		title: __('Certification'),
		opened: false,
		subArticles: [
			{ name: 'issue-a-certificate', title: __('Issue a Certificate') },
			{
				name: 'custom-certificate-templates',
				title: __('Custom Certificate Templates'),
			},
		],
	},
	{
		title: __('Monetization'),
		opened: false,
		subArticles: [
			{
				name: 'setting-up-payment-gateway',
				title: __('Setting up payment gateway'),
			},
		],
	},
	{
		title: __('Settings'),
		opened: false,
		subArticles: [{ name: 'roles', title: __('Roles') }],
	},
])

const setUpOnboarding = () => {
	if (userResource.data?.is_system_manager) {
		onboardingDetails = useOnboarding('learning')
		onboardingDetails.setUp(steps)
		isOnboardingStepsCompleted = onboardingDetails.isOnboardingStepsCompleted
		showOnboarding.value = true
	}
}

watch(userResource, () => {
	try {
		if (userResource.data) {
			isModerator.value = userResource.data.is_moderator
			isInstructor.value = userResource.data.is_instructor
			addAdminSidebar()
			addPrograms()
			addQuizzes()
			addAssignments()
			setUpOnboarding()
		}
	} catch (error) {
		console.error('Error in userResource watcher:', error)
	}
})

const redirectToWebsite = () => {
	window.open('https://frappe.io/learning', '_blank')
}

onUnmounted(() => {
	socket.off('publish_lms_notifications')
})
</script>

<style scoped>
/* Hide scrollbar for Chrome, Safari and Opera */
.scrollbar-hide::-webkit-scrollbar {
	display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.scrollbar-hide {
	-ms-overflow-style: none;  /* IE and Edge */
	scrollbar-width: none;  /* Firefox */
}
</style>
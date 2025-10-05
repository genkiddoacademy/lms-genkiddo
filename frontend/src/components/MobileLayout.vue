<template>
	<div class="flex h-full flex-col relative">
		<div class="h-full pb-20" id="scrollContainer">
			<slot />
		</div>

		<div class="relative z-20">
			<!-- Dropdown menu -->
			<div
				class="fixed bottom-20 right-2 w-[80%] rounded-md bg-surface-white text-base p-5 space-y-4 shadow-md"
				v-if="showMenu"
				ref="menu"
			>
				<div
					v-for="link in otherLinks"
					:key="link.label"
					class="flex items-center space-x-2 cursor-pointer"
					@click="handleClick(link)"
				>
					<component
						:is="icons[link.icon]"
						class="h-4 w-4 stroke-1.5 text-ink-gray-5"
					/>
					<div>{{ link.label }}</div>
				</div>
			</div>

			<!-- Fixed menu -->
			<div
				v-if="sidebarSettings.data"
				class="fixed bottom-0 left-0 w-full flex items-center justify-around border-t border-outline-gray-2 bg-surface-white standalone:pb-4 z-10"
			>
				<button
					v-for="tab in sidebarLinks"
					:key="tab.label"
					:class="isVisible(tab) ? 'block' : 'hidden'"
					class="flex flex-col items-center justify-center py-3 transition active:scale-95"
					@click="handleClick(tab)"
				>
					<component
						:is="icons[tab.icon]"
						class="h-6 w-6 stroke-1.5"
						:class="[isActive(tab) ? 'text-ink-gray-9' : 'text-ink-gray-5']"
					/>
				</button>
				<button @click="toggleMenu">
					<component
						:is="icons['List']"
						class="h-6 w-6 stroke-1.5 text-ink-gray-5"
					/>
				</button>
			</div>
		</div>
	</div>
</template>
<script setup>
import { getSidebarLinks } from '@/utils'
import { useRouter } from 'vue-router'
import { watch, ref, onMounted } from 'vue'
import { sessionStore } from '@/stores/session'
import { useSettings } from '@/stores/settings'
import { usersStore } from '@/stores/user'
import * as icons from 'lucide-vue-next'

const { logout, user } = sessionStore()
let { isLoggedIn } = sessionStore()
const { sidebarSettings, settingsStore } = useSettings()
const router = useRouter()
let { userResource } = usersStore()
const sidebarLinks = ref(getSidebarLinks())
const otherLinks = ref([])
const showMenu = ref(false)
const menu = ref(null)
const isDarkMode = ref(false)
const isModerator = ref(false)
const isInstructor = ref(false)

const toggleTheme = () => {
	const newTheme = isDarkMode.value ? 'dark' : 'light'
	document.documentElement.setAttribute('data-theme', newTheme)
	localStorage.setItem('theme', newTheme)
}

const handleThemeClick = () => {
	isDarkMode.value = !isDarkMode.value
	toggleTheme()
}

onMounted(() => {
	// Initialize theme
	const currentTheme =
		document.documentElement.getAttribute('data-theme') || 'light'
	isDarkMode.value = currentTheme === 'dark'

	if (user) {
		setSidebarLinks()
		if (userResource.data) {
			addAdminSidebar()
		}
	} else {
		addGuestSidebar()
	}
})

const setSidebarLinks = () => {
	if (!user) {
		return // Skip for guest users
	}
	sidebarSettings.reload(
		{},
		{
			onSuccess(data) {
				filterLinksToShow(data)
				addOtherLinks()
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
				limitSidebarToFour()
			},
		},
	)
}

const filterLinksToShow = (data) => {
	Object.keys(data).forEach((key) => {
		if (!parseInt(data[key])) {
			sidebarLinks.value = sidebarLinks.value.filter(
				(link) => link.label.toLowerCase().split(' ').join('_') !== key,
			)
		}
	})
}

const addOtherLinks = () => {
	if (user) {
		addNotifications()
		limitSidebarToFour()
		otherLinks.value.push({
			label: 'Profile',
			icon: 'UserRound',
		})
		otherLinks.value.push({
			label: 'Toggle Theme',
			icon: isDarkMode.value ? 'Moon' : 'Sun',
		})
		// Settings shortcut in mobile "more" menu
		// Settings shortcut in mobile "more" menu (only for admins)
		if (userResource.data?.roles?.includes('Administrator')) {
			otherLinks.value.push({
				label: 'Settings',
				icon: 'Settings',
			})
		}
		otherLinks.value.push({
			label: 'Log out',
			icon: 'LogOut',
		})
	} else {
		otherLinks.value.push({
			label: 'Log in',
			icon: 'LogIn',
		})
		otherLinks.value.push({
			label: 'Register',
			icon: 'User',
		})
		otherLinks.value.push({
			label: 'Toggle Theme',
			icon: isDarkMode.value ? 'Moon' : 'Sun',
		})
	}
}

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
		addOtherLinks()
	}
}

const limitSidebarToFour = () => {
	if (user && sidebarLinks.value.length > 4) {
		const excessLinks = sidebarLinks.value.slice(4)
		sidebarLinks.value = sidebarLinks.value.slice(0, 4)

		// Add excess links to hamburger menu
		excessLinks.forEach((link) => {
			if (!otherLinks.value.some((item) => item.label === link.label)) {
				otherLinks.value.unshift(link)
			}
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

watch(userResource, () => {
	try {
		if (userResource.data) {
			isModerator.value = userResource.data.is_moderator
			isInstructor.value = userResource.data.is_instructor
			addAdminSidebar()
			addPrograms()
			addQuizzes()
			addAssignments()
			limitSidebarToFour()
		}
	} catch (error) {
		console.error('Error in userResource watcher:', error)
	}
})

const handleOutsideClick = (e) => {
	if (menu.value && !menu.value.contains(e.target)) {
		showMenu.value = false
	}
}

watch(showMenu, (val) => {
	if (val) {
		setTimeout(() => {
			document.addEventListener('click', handleOutsideClick)
		}, 0)
	} else {
		document.removeEventListener('click', handleOutsideClick)
	}
})

watch(isDarkMode, () => {
	otherLinks.value = otherLinks.value.map((link) => {
		if (link.label === 'Toggle Theme') {
			link.icon = isDarkMode.value ? 'Moon' : 'Sun'
		}
		return link
	})
})

let isActive = (tab) => {
	return tab.activeFor?.includes(router.currentRoute.value.name)
}

const handleClick = async (tab) => {
	try {
		if (tab.label == 'Log in') window.location.href = '/login'
		else if (tab.label == 'Register') window.location.href = '/register'
		else if (tab.label == 'Toggle Theme') handleThemeClick()
		else if (tab.label == 'Settings') settingsStore.isSettingsOpen = true
		else if (tab.label == 'Log out')
			logout.submit().then(() => {
				isLoggedIn = false
			})
		else if (tab.label == 'Profile')
			await router.push({
				name: 'Profile',
				params: {
					username: userResource.data?.username,
				},
			})
		else if (tab.to) {
			await router.push({ name: tab.to })
		}
	} catch (error) {
		console.error('Navigation error in mobile layout:', error)
	}
}

const isVisible = (tab) => {
	if (tab.label == 'Log in') return !isLoggedIn
	else if (tab.label == 'Log out') return isLoggedIn
	else return true
}

const toggleMenu = () => {
	showMenu.value = !showMenu.value
}
</script>

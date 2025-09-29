<template>
	<button
		v-if="link && !link.onlyMobile"
		class="flex h-7 cursor-pointer items-center rounded text-ink-gray-8 duration-300 ease-in-out focus:outline-none focus:transition-none focus-visible:rounded focus-visible:ring-2 focus-visible:ring-outline-gray-3"
		:class="
			isActive
				? 'bg-orange-2 shadow-sm text-white font-bold'
				: 'hover:bg-surface-gray-2'
		"
		@click="handleClick"
	>
		<div v-if="isCollapsed" class="p-1">
			<Tooltip :text="link.label" placement="right">
				<slot name="icon">
					<span class="grid h-5 w-6 place-items-center">
						<component
							:is="icons[link.icon]"
							class="h-4 w-4 stroke-1.5"
							:class="isActive ? 'text-white' : 'text-ink-gray-8'"
						/>
					</span>
				</slot>
			</Tooltip>
		</div>
		<div v-else class="flex items-center w-full py-1 group">
			<slot name="icon">
				<span class="grid h-5 w-6 flex-shrink-0 place-items-center">
					<component
						:is="icons[link.icon]"
						class="h-4 w-4 stroke-1.5"
						:class="isActive ? 'text-white' : 'text-ink-gray-8'"
					/>
				</span>
			</slot>
			<span class="flex-shrink-0 text-sm ml-2">
				{{ __(link.label) }}
			</span>
			<span v-if="link.count" class="!ml-auto block text-xs text-ink-gray-5">
				{{ link.count }}
			</span>
			<div
				v-if="showControls"
				class="flex items-center space-x-2 !ml-auto text-xs text-ink-gray-5 group-hover:visible invisible"
			>
				<component
					:is="icons['Edit']"
					class="h-3 w-3 stroke-1.5 text-ink-gray-7"
					@click.stop="openModal(link)"
				/>
				<component
					:is="icons['X']"
					class="h-3 w-3 stroke-1.5 text-ink-gray-7"
					@click.stop="deletePage(link)"
				/>
			</div>
		</div>

		<!-- Count badge for collapsed state -->
		<span
			v-if="link.count && isCollapsed && link.count > 0"
			class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full h-4 w-4 flex items-center justify-center text-[10px] font-bold"
		>
			{{ link.count > 9 ? '9+' : link.count }}
		</span>
	</button>
</template>
<script setup>
import { Tooltip } from 'frappe-ui'
import { computed, watchEffect, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as icons from 'lucide-vue-next'

const router = useRouter()
const emit = defineEmits(['openModal', 'deletePage'])

const props = defineProps({
	link: {
		type: Object,
		required: true,
	},
	isCollapsed: {
		type: Boolean,
		default: false,
	},
	showControls: {
		type: Boolean,
		default: false,
	},
})

function handleClick() {
	// Check if there's a custom onClick handler
	if (props.link.onClick && typeof props.link.onClick === 'function') {
		props.link.onClick()
		return
	}

	// Default navigation behavior
	if (router.hasRoute(props.link.to)) {
		router.push({ name: props.link.to })
	} else if (props.link.to) {
		window.location.href = `/${props.link.to}`
	}
}

const isActive = computed(() => {
	// Check if there's a custom isActive property
	if (props.link?.isActive !== undefined) {
		return props.link.isActive
	}

	const currentRoute = router.currentRoute.value
	if (!currentRoute?.name) return false

	if (props.link?.activeFor) {
		return props.link.activeFor.includes(currentRoute.name)
	}
	// For web pages without activeFor, check if current route matches
	if (router.hasRoute(props.link.to)) {
		return currentRoute.name === props.link.to
	} else {
		return currentRoute.path === `/${props.link.to}`
	}
})

// Use watchEffect to ensure reactivity on mount and route changes
watchEffect(async () => {
	const currentRoute = router.currentRoute.value
	if (currentRoute) {
		await nextTick()
	}
	// This will trigger whenever currentRoute changes
})

onMounted(async () => {
	await router.isReady()
	// Ensure router is ready
})

const openModal = (link) => {
	emit('openModal', link)
}

const deletePage = (link) => {
	emit('deletePage', link)
}
</script>

<template>
	<div class="p-2" v-if="!isCollapsed">
		<div
			class="flex h-12 py-2 items-center rounded-md duration-300 ease-in-out"
			:class="isCollapsed ? 'px-1 w-8' : 'px-2'"
		>
			<img
				v-if="branding.data?.banner_image"
				:src="branding.data?.banner_image.file_url"
				class="w-8 h-8 rounded flex-shrink-0"
			/>
			<LMSLogo v-else class="w-8 h-8 rounded flex-shrink-0" />
			<div
				class="flex flex-1 flex-col text-left duration-300 ease-in-out"
				:class="
					isCollapsed
						? 'opacity-0 ml-0 w-0 overflow-hidden'
						: 'opacity-100 ml-2 w-auto'
				"
			>
				<div class="text-base font-medium text-ink-gray-9 leading-none">
					<span
						v-if="
							branding.data?.app_name && branding.data?.app_name != 'Frappe'
						"
					>
						{{ branding.data?.app_name }}
					</span>
					<span v-else class="!font-bold !text-lg"> GenKiddo LMS </span>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import LMSLogo from '@/components/Icons/LMSLogo.vue'
import { sessionStore } from '@/stores/session'
import { convertToTitleCase } from '@/utils'
import { usersStore } from '@/stores/user'
import { useSettings } from '@/stores/settings'
import { ref, onMounted } from 'vue'

const { branding } = sessionStore()
let { userResource } = usersStore()
const settingsStore = useSettings()
const theme = ref('light')

const props = defineProps({
	isCollapsed: {
		type: Boolean,
		default: false,
	},
})

onMounted(() => {
	theme.value = localStorage.getItem('theme') || 'light'
	if (['light', 'dark'].includes(theme.value)) {
		document.documentElement.setAttribute('data-theme', theme.value)
	}
})
</script>

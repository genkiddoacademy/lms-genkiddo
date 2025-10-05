<template>
	<NoPermission v-if="!$user.data" />
	<div v-else-if="profile.data">
		<header
			class="sticky top-0 z-10 flex flex-col md:flex-row md:items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5"
		>
			<Breadcrumbs class="h-7" :items="breadcrumbs" />
		</header>
		<div class="group relative h-[130px] w-full">
			<img
				v-if="profile.data.cover_image"
				:src="profile.data.cover_image"
				class="h-[130px] w-full object-cover object-center"
			/>
			<div
				v-else
				:class="{ 'bg-surface-gray-2': !profile.data.cover_image }"
				class="h-[130px] w-full"
			></div>
			<div
				class="absolute bottom-0 left-1/2 mb-4 flex -translate-x-1/2 space-x-2 opacity-0 transition-opacity focus-within:opacity-100 group-hover:opacity-100"
				v-if="isSessionUser()"
			>
				<EditCoverImage
					@select="(imageUrl) => coverImage.submit({ url: imageUrl })"
				>
					<template v-slot="{ togglePopover }">
						<Button
							v-if="!readOnlyMode"
							variant="outline"
							@click="togglePopover()"
						>
							<template #prefix>
								<Edit class="w-4 h-4 stroke-1.5 text-ink-gray-7" />
							</template>
							{{ __('Edit') }}
						</Button>
					</template>
				</EditCoverImage>
			</div>
		</div>
		<div class="mx-auto -mt-10 md:-mt-4 max-w-4xl translate-x-0 px-5">
			<div class="flex flex-col md:flex-row items-center">
				<div>
					<img
						v-if="profile.data.user_image"
						:src="profile.data.user_image"
						class="object-cover h-[100px] w-[100px] rounded-full border-4 border-white"
					/>
					<UserAvatar
						v-else
						:user="profile.data"
						class="h-[100px] w-[100px] rounded-full border-4 border-white object-cover"
					/>
				</div>
				<div class="ml-6">
					<h2 class="mt-2 text-3xl font-bold text-gradasi-1">
						{{ profile.data.full_name }}
					</h2>
					<div class="mt-2 text-base text-ink-gray-7">
						{{ profile.data.headline }}
					</div>
				</div>
				<Button
					v-if="isSessionUser() && !readOnlyMode"
					class="mt-3 sm:mt-0 md:ml-auto !bg-orange-2 text-white"
					@click="editProfile()"
				>
					<template #prefix>
						<Edit class="w-4 h-4 stroke-1.5 text-white" />
					</template>
					{{ __('Edit Profile') }}
				</Button>
			</div>

			<!-- About Section -->
			<div class="mt-7 mb-10">
				<h2 class="mb-3 text-lg font-semibold text-ink-gray-9">
					{{ __('About') }}
				</h2>
				<div
					v-if="profile.data.bio"
					v-html="profile.data.bio"
					class="ProseMirror prose prose-table:table-fixed prose-td:p-2 prose-th:p-2 prose-td:border prose-th:border prose-td:border-outline-gray-2 prose-th:border-outline-gray-2 prose-td:relative prose-th:relative prose-th:bg-surface-gray-2 prose-sm max-w-none !whitespace-normal"
				></div>
				<div v-else class="text-ink-gray-7 text-sm italic">
					{{ __('No introduction') }}
				</div>
			</div>

			<!-- Achievements Section -->
			<div class="mt-7 mb-10" v-if="badges.data?.length">
				<h2 class="mb-3 text-lg font-semibold text-ink-gray-9">
					{{ __('Achievements') }}
				</h2>
				<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
					<div v-for="badge in badges.data" :key="badge.name">
						<Popover trigger="hover" :leaveDelay="Number(0.01)">
							<template #target>
								<div class="relative">
									<img
										:src="badge.badge_image"
										:alt="badge.badge"
										class="h-[80px]"
									/>
									<div
										v-if="badge.count > 1"
										class="flex items-end bg-surface-gray-2 p-2 text-xs font-semibold rounded-full absolute right-0 bottom-0"
									>
										<span>
											<X class="w-3 h-3" />
										</span>
										{{ badge.count }}
									</div>
								</div>
							</template>
							<template #body-main>
								<div class="w-[250px] text-base">
									<img
										:src="badge.badge_image"
										:alt="badge.badge"
										class="bg-surface-gray-2 rounded-t-md h-[200px] mx-auto"
									/>
									<div class="p-5">
										<div class="text-2xl font-semibold mb-2">
											{{ badge.badge }}
										</div>
										<div class="text-ink-gray-7 mb-3">
											{{ badge.description }}
										</div>
										<div class="text-ink-gray-7">
											<span class="font-semibold">
												{{ __('Earned:') }}
											</span>
											{{ dayjs(badge.creation).format('DD MMM YYYY') }}
										</div>
									</div>
								</div>
							</template>
						</Popover>
					</div>
				</div>
			</div>

			<!-- Certificates Section -->
			<div class="mt-7 mb-10">
				<h2 class="mb-3 text-lg font-semibold text-ink-gray-9">
					{{ __('Certificates') }}
				</h2>
				<div
					v-if="certificates.data?.length"
					class="grid grod-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
				>
					<div
						v-for="certificate in certificates.data"
						:key="certificate.name"
						class="flex flex-col bg-surface-white border rounded-lg p-3 cursor-pointer hover:bg-surface-menu-bar"
						@click="openCertificate(certificate)"
					>
						<div class="font-medium leading-5 mb-2 text-ink-gray-9">
							{{ certificate.course_title || certificate.batch_title }}
						</div>
						<div class="text-sm text-ink-gray-7 font-medium mt-auto">
							<span> {{ __('Issued on') }}: </span>
							{{ dayjs(certificate.issue_date).format('DD MMM YYYY') }}
						</div>
					</div>
				</div>
				<div v-else class="text-ink-gray-7 text-sm italic">
					{{ __('Tidak ada sertifikat') }}
				</div>
			</div>
		</div>
	</div>
	<EditProfile
		v-model="showProfileModal"
		v-model:reloadProfile="profile"
		:profile="profile"
	/>
</template>
<script setup>
import {
	Breadcrumbs,
	createResource,
	createListResource,
	Button,
	Popover,
	usePageMeta,
} from 'frappe-ui'
import { computed, inject, watch, ref, onMounted, watchEffect } from 'vue'
import { sessionStore } from '@/stores/session'
import { Edit, X } from 'lucide-vue-next'
import UserAvatar from '@/components/UserAvatar.vue'
import { useRoute, useRouter } from 'vue-router'
import NoPermission from '@/components/NoPermission.vue'
import { convertToTitleCase } from '@/utils'
import EditProfile from '@/components/Modals/EditProfile.vue'
import EditCoverImage from '@/components/Modals/EditCoverImage.vue'

const { user, brand } = sessionStore()
const $user = inject('$user')
const dayjs = inject('$dayjs')
const route = useRoute()
const router = useRouter()
const showProfileModal = ref(false)
const readOnlyMode = window.read_only_mode

const props = defineProps({
	username: {
		type: String,
		required: true,
	},
})

onMounted(() => {
	if ($user.data) {
		profile.reload()
		badges.reload()
		certificates.reload()
	}
})

const profile = createResource({
	url: 'frappe.client.get',
	makeParams(values) {
		return {
			doctype: 'User',
			filters: {
				username: props.username,
			},
		}
	},
})

const coverImage = createResource({
	url: 'frappe.client.set_value',
	makeParams(values) {
		return {
			doctype: 'User',
			name: profile.data?.name,
			fieldname: 'cover_image',
			value: values.url,
		}
	},
	onSuccess() {
		profile.reload()
	},
})

const badges = createListResource({
	doctype: 'LMS Badge Assignment',
	filters: {
		user: () => profile.data?.name,
	},
	fields: [
		'name',
		'badge',
		'badge_image',
		'description',
		'creation',
		'count(name) as count',
	],
	groupBy: 'badge',
	cache: ['badges', () => profile.data?.name],
})

const certificates = createListResource({
	doctype: 'LMS Certificate',
	filters: {
		member: () => profile.data?.name,
	},
	fields: ['name', 'course_title', 'batch_title', 'issue_date', 'template'],
	cache: ['certificates', () => profile.data?.name],
})

watch(
	() => props.username,
	() => {
		profile.reload()
		badges.reload()
		certificates.reload()
	},
)

watch(
	() => profile.data?.name,
	() => {
		if (profile.data?.name) {
			badges.reload()
			certificates.reload()
		}
	},
)

const editProfile = () => {
	showProfileModal.value = true
}

const isSessionUser = () => {
	return $user.data?.email === profile.data?.email
}

const openCertificate = (certificate) => {
	window.open(
		`/api/method/lms.lms.utils.get_certificate_pdf/${certificate.name}`,
		'_blank',
	)
}

const breadcrumbs = computed(() => {
	let crumbs = [
		{
			label: 'People',
		},
		{
			label: profile.data?.full_name,
			route: {
				name: 'Profile',
				params: {
					username: user.doc?.username,
				},
			},
		},
	]
	return crumbs
})

usePageMeta(() => {
	return {
		title: profile.data?.full_name,
		icon: brand.favicon,
	}
})
</script>

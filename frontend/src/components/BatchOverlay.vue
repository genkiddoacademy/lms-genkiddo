<template>
	<div v-if="batch.data" class="mt-4 w-full flex flex-row justify-between">
		<div class="flex flex-row gap-8">
			<div class="flex flex-col h-fit">
				<div
					v-if="batch.data.amount"
					class="text-lg font-semibold text-ink-gray-9"
				>
					{{ formatNumberIntoCurrency(batch.data.amount, batch.data.currency) }}
				</div>

				<DateRange
					:startDate="batch.data.start_date"
					:endDate="batch.data.end_date"
					class=""
				/>

				<div class="flex items-center text-ink-gray-7">
					<Clock class="h-4 w-4 stroke-1.5 mr-2" />
					<span
						>Pukul: {{ formatTime(batch.data.start_time) }} -
						{{ formatTime(batch.data.end_time) }}
						{{ batch.data.timezone }}
					</span>
				</div>
			</div>

			<div class="flex flex-col h-fit">
				<div
					v-if="batch.data.courses.length"
					class="flex items-center text-ink-gray-7 pb-2"
				>
					<BookOpen class="h-4 w-4 stroke-1.5 mr-2" />
					<span
						>Jumlah Course: {{ batch.data.courses.length }} {{ __('Courses') }}
					</span>
				</div>

				<div class="flex avatar-group">
					<Users class="h-4 w-4 stroke-1.5 mr-2 text-ink-gray-7" />
					<div
						class="h-6 mr-1 text-ink-gray-7"
						:class="{
							'avatar-group overlap': batch.data.instructors.length > 1,
						}"
					>
						Oleh:
						<UserAvatar
							v-for="instructor in batch.data.instructors"
							:user="instructor"
						/>
					</div>
					<CourseInstructors :instructors="batch.data.instructors" />
				</div>
			</div>
		</div>
		<div v-if="!readOnlyMode" class="flex flex-col gap-2">
			<router-link
				v-if="isModerator || isStudent"
				:to="{
					name: 'Batch',
					params: {
						batchName: batch.data.name,
					},
				}"
			>
				<Button variant="solid" class="w-48 !text-white !p-4 !bg-orange-2">
					<template #prefix>
						<Settings v-if="isModerator" class="size-4 stroke-1.5" />
						<LogIn v-else class="size-4 stroke-1.5" />
					</template>
					<span>
						{{ isModerator ? __('Manage Batch') : __('Visit Batch') }}
					</span>
				</Button>
			</router-link>
			<router-link
				:to="{
					name: 'Billing',
					params: {
						type: 'batch',
						name: batch.data.name,
					},
				}"
				v-else-if="
					batch.data.paid_batch &&
					batch.data.seats_left > 0 &&
					batch.data.accept_enrollments
				"
			>
				<Button
					v-if="!isStudent"
					class="w-48 !p-4"
					variant="solid !bg-orange-2"
				>
					<template #prefix>
						<CreditCard class="size-4 stroke-1.5" />
					</template>
					<span>
						{{ __('Mulai Belajar') }}
					</span>
				</Button>
			</router-link>
			<Button
				variant="solid"
				class="w-48 !p-4 !bg-orange-2"
				v-else-if="
					batch.data.allow_self_enrollment &&
					batch.data.seats_left &&
					batch.data.accept_enrollments
				"
				@click="enrollInBatch()"
			>
				<template #prefix>
					<GraduationCap class="size-4 stroke-1.5" />
				</template>
				{{ __('Mulai Belajar') }}
			</Button>
			<router-link
				v-if="isModerator"
				:to="{
					name: 'BatchForm',
					params: {
						batchName: batch.data.name,
					},
				}"
			>
				<Button class="w-48 !p-4">
					<template #prefix>
						<Pencil class="size-4 stroke-1.5" />
					</template>
					<span>
						{{ __('Edit') }}
					</span>
				</Button>
			</router-link>
		</div>
	</div>
</template>
<script setup>
import { inject, computed } from 'vue'
import { Button, createResource, toast } from 'frappe-ui'
import {
	BookOpen,
	Clock,
	CreditCard,
	Users,
	GraduationCap,
	LogIn,
	Pencil,
	Settings,
} from 'lucide-vue-next'
import { formatNumberIntoCurrency, formatTime } from '@/utils'
import DateRange from '@/components/Common/DateRange.vue'
import CourseInstructors from '@/components/CourseInstructors.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = inject('$user')
const readOnlyMode = window.read_only_mode

const props = defineProps({
	batch: {
		type: Object,
		default: null,
	},
})

const enroll = createResource({
	url: 'lms.lms.utils.enroll_in_batch',
	makeParams(values) {
		return {
			batch: props.batch.data.name,
		}
	},
})

const enrollInBatch = () => {
	if (!user.data) {
		window.location.href = `/login?redirect-to=/batches/details/${props.batch.data.name}`
	}
	enroll.submit(
		{},
		{
			onSuccess(data) {
				toast.success(__('You have been enrolled in this batch'))
				router.push({
					name: 'Batch',
					params: {
						batchName: props.batch.data.name,
					},
				})
			},
		},
	)
}

const seats_left = computed(() => {
	if (props.batch.data?.seat_count) {
		return props.batch.data?.seat_count - props.batch.data?.students?.length
	}
	return null
})

const isStudent = computed(() => {
	return props.batch.data?.students?.includes(user.data?.name)
})

const isModerator = computed(() => {
	return user.data?.is_moderator || user.data?.is_system_manager
})
</script>

<style>
.avatar-group {
	display: inline-flex;
	align-items: center;
}

.avatar-group .avatar {
	transition: margin 0.1s ease-in-out;
}

.avatar-group.overlap .avatar + .avatar {
	margin-left: calc(-8px);
}
</style>

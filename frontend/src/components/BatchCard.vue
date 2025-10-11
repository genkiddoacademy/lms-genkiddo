<template>
	<div
		class="flex flex-row border hover:border-outline-gray-3 rounded-md overflow-hidden h-full relative"
		style="min-height: 230px"
	>
		<div
			class="batch-image flex-shrink-0 relative"
			:class="{ 'default-image': !batch.meta_image }"
			:style="{
				backgroundImage: batch.meta_image
					? 'url(\'' + encodeURI(batch.meta_image) + '\')'
					: 'none',
			}"
		>
			<!-- Seats Left overlay -->
			<div
				v-if="batch.seat_count"
				class="absolute top-3 left-3 text-sm px-3 py-1.5 rounded-md font-medium"
				:class="
					batch.seats_left > 0
						? 'bg-green-100 text-green-700'
						: 'bg-red-100 text-red-700'
				"
			>
				<span v-if="batch.seats_left > 0">
					{{ batch.seats_left }} Slot Tersedia
				</span>
				<span v-else>
					{{ __('Sold Out') }}
				</span>
			</div>
			<div v-if="!batch.meta_image" class="image-placeholder">
				{{ batch.title[0] }}
			</div>
		</div>
		<div class="flex flex-col flex-auto p-4">
			<div class="text-lg leading-5 font-semibold mb-2 text-ink-gray-9">
				{{ batch.title }}
			</div>
			<div class="short-introduction text-sm text-ink-gray-7 mb-3">
				{{ batch.description }}
			</div>
			<div v-if="batch.amount" class="font-semibold text-ink-gray-9 mb-3">
				{{ batch.price }}
			</div>
			<div class="flex flex-col space-y-2 mt-auto">
				<div
					v-if="
						batch.students_count !== undefined && batch.students_count !== null
					"
					class="flex items-center text-sm text-ink-gray-7"
				>
					<Users class="h-4 w-4 stroke-1.5 mr-2 text-ink-gray-7" />
					<span> {{ batch.students_count || 0 }} {{ __('Enrolled') }} </span>
				</div>
				<DateRange
					:startDate="batch.start_date"
					:endDate="batch.end_date"
					class="text-sm text-ink-gray-7"
				/>
				<div class="flex items-center text-sm text-ink-gray-7">
					<Clock class="h-4 w-4 stroke-1.5 mr-2 text-ink-gray-7" />
					<span>
						{{ formatTime(batch.start_time) }} -
						{{ formatTime(batch.end_time) }}
					</span>
				</div>
				<div
					v-if="batch.timezone"
					class="flex items-center text-sm text-ink-gray-7"
				>
					<Globe class="h-4 w-4 stroke-1.5 mr-2 text-ink-gray-5" />
					<span>
						{{ batch.timezone }}
					</span>
				</div>
			</div>
			<div
				v-if="batch.instructors?.length"
				class="flex avatar-group overlap mt-4"
			>
				<div
					class="h-6 mr-1"
					:class="{ 'avatar-group overlap': batch.instructors.length > 1 }"
				>
					<UserAvatar
						v-for="instructor in batch.instructors"
						:user="instructor"
					/>
				</div>
				<CourseInstructors :instructors="batch.instructors" />
			</div>
		</div>
	</div>
</template>
<script setup>
import { formatTime } from '@/utils'
import { Clock, Globe, Users } from 'lucide-vue-next'
import DateRange from '@/components/Common/DateRange.vue'
import CourseInstructors from '@/components/CourseInstructors.vue'
import UserAvatar from '@/components/UserAvatar.vue'

const props = defineProps({
	batch: {
		type: Object,
		default: null,
	},
})
</script>
<style>
.batch-image {
	width: 390px;
	height: 230px;
	background-size: cover;
	background-position: center;
	background-repeat: no-repeat;
}

.default-image {
	display: flex;
	flex-direction: column;
	align-items: center;
	background-color: theme('colors.blue.100');
	color: theme('colors.blue.600');
}

.image-placeholder {
	display: flex;
	align-items: center;
	flex: 1;
	font-size: 3rem;
	color: theme('colors.gray.700');
	font-weight: 600;
}

.short-introduction {
	display: -webkit-box;
	-webkit-line-clamp: 2;
	line-clamp: 2;
	-webkit-box-orient: vertical;
	text-overflow: ellipsis;
	width: 100%;
	overflow: hidden;
	margin: 0.25rem 0 1rem;
	line-height: 1.5;
}

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

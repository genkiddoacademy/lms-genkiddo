<template>
	<Dialog
		v-model="show"
		:options="{
			title: __('Add an assessment'),
			size: 'sm',
			actions: [
				{
					label: __('Submit'),
					variant: 'solid',
					loading: assessmentResource.loading,
					disabled:
						!assessmentType || !assessment || assessmentResource.loading,
					onClick: (close) => addAssessment(close),
				},
			],
		}"
	>
		<template #body-content>
			<div class="space-y-4">
				<FormControl
					type="select"
					:options="assessmentTypes"
					v-model="assessmentType"
					:label="__('Type')"
				/>
				<Link
					v-if="assessmentType"
					v-model="assessment"
					:doctype="assessmentType"
					:label="__('Assessment')"
					:placeholder="__('Select an assessment...')"
					:onCreate="
						(value, close) => {
							close()
							if (assessmentType === 'LMS Quiz') {
								router.push({
									name: 'QuizForm',
									params: {
										quizID: 'new',
									},
								})
							} else if (assessmentType === 'LMS Assignment') {
								router.push({
									name: 'Assignments',
								})
							}
						}
					"
				/>
				<div v-else class="text-sm text-gray-500">
					{{ __('Please select an assessment type first') }}
				</div>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import { Dialog, FormControl, createResource, toast } from 'frappe-ui'
import Link from '@/components/Controls/Link.vue'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const show = defineModel()
const assessmentType = ref(null)
const assessment = ref(null)
const assessments = defineModel('assessments')
const router = useRouter()

const props = defineProps({
	batch: {
		type: String,
		default: null,
	},
})

const assessmentResource = createResource({
	url: 'frappe.client.insert',
	makeParams(values) {
		return {
			doc: {
				doctype: 'LMS Assessment',
				parent: props.batch,
				parenttype: 'LMS Batch',
				parentfield: 'assessment',
				assessment_type: assessmentType.value,
				assessment_name: assessment.value,
			},
		}
	},
})

const addAssessment = (close) => {
	// Validate required fields
	if (!assessmentType.value) {
		toast.error(__('Please select an assessment type'))
		return
	}

	if (!assessment.value) {
		toast.error(__('Please select an assessment'))
		return
	}

	console.log('Adding assessment:', {
		batch: props.batch,
		assessmentType: assessmentType.value,
		assessment: assessment.value,
	})

	assessmentResource.submit(
		{},
		{
			onSuccess(data) {
				assessments.value.reload()
				toast.success(__('Assessment added successfully'))
				assessmentType.value = null
				assessment.value = null
				close()
			},
			onError(err) {
				console.error('Error adding assessment:', err)
				const errorMessage =
					err?.messages?.[0] ||
					err?.message ||
					err ||
					__('Failed to add assessment')
				toast.error(errorMessage)
			},
		},
	)
}

// Watch for assessment type changes and reset assessment selection
watch(assessmentType, (newValue, oldValue) => {
	if (newValue !== oldValue) {
		assessment.value = null
	}
})

const assessmentTypes = computed(() => {
	return [
		{ label: 'Quiz', value: 'LMS Quiz' },
		{ label: 'Assignment', value: 'LMS Assignment' },
		{ label: 'Programming Exercise', value: 'LMS Programming Exercise' },
	]
})
</script>

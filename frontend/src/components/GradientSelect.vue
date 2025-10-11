<template>
	<div class="gradient-select-custom" @click="toggleDropdown" ref="selectRef">
		<button
			type="button"
			class="gradient-select-button"
			:class="{ 'gradient-select-button--open': isOpen }"
		>
			<span class="gradient-select-text">
				{{ selectedOption?.label || placeholder }}
			</span>
			<svg
				class="gradient-select-icon"
				:class="{ 'gradient-select-icon--rotated': isOpen }"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M19 9l-7 7-7-7"
				/>
			</svg>
		</button>

		<div v-if="isOpen" class="gradient-select-dropdown" @click.stop>
			<div
				v-for="option in options"
				:key="option.value"
				class="gradient-select-option"
				:class="{
					'gradient-select-option--selected': option.value === modelValue,
				}"
				@click="selectOption(option)"
			>
				{{ option.label }}
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
	modelValue: {
		type: [String, Number],
		default: null,
	},
	options: {
		type: Array,
		default: () => [],
	},
	placeholder: {
		type: String,
		default: 'Select option',
	},
})

const emit = defineEmits(['update:modelValue', 'change'])

const isOpen = ref(false)
const selectRef = ref(null)

const selectedOption = computed(() => {
	return props.options.find((option) => option.value === props.modelValue)
})

const toggleDropdown = () => {
	isOpen.value = !isOpen.value
}

const selectOption = (option) => {
	emit('update:modelValue', option.value)
	emit('change', option.value)
	isOpen.value = false
}

const closeDropdown = (event) => {
	if (selectRef.value && !selectRef.value.contains(event.target)) {
		isOpen.value = false
	}
}

onMounted(() => {
	document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
	document.removeEventListener('click', closeDropdown)
})
</script>

<style scoped>
.gradient-select-custom {
	position: relative;
	display: inline-block;
	min-width: 12rem;
	width: fit-content;
}

.gradient-select-button {
	background: linear-gradient(90deg, #f86300 0%, #dd3a3a 100%);
	color: white;
	border: none;
	border-radius: 6px;
	padding: 8px 16px;
	font-weight: 500;
	font-size: 1rem;
	width: 100%;
	display: flex;
	align-items: center;
	justify-content: space-between;
	cursor: pointer;
	transition: all 0.2s ease;
}

.gradient-select-button:hover {
	background: linear-gradient(90deg, #e55a00 0%, #c23030 100%);
	transform: translateY(-1px);
	box-shadow: 0 4px 12px rgba(248, 99, 0, 0.3);
}

.gradient-select-text {
	color: white;
	font-weight: 500;
}

.gradient-select-icon {
	width: 20px;
	height: 20px;
	color: white;
	stroke: white;
	transition: transform 0.2s ease;
}

.gradient-select-icon--rotated {
	transform: rotate(180deg);
}

.gradient-select-dropdown {
	position: absolute;
	top: 100%;
	left: 0;
	right: 0;
	background: white;
	border: 1px solid #e2e8f0;
	border-radius: 8px;
	box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
	z-index: 1000;
	margin-top: 4px;
	max-height: 200px;
	overflow-y: auto;
}

.gradient-select-option {
	padding: 10px 16px;
	cursor: pointer;
	color: #374151;
	transition: all 0.2s ease;
}

.gradient-select-option:hover {
	background: linear-gradient(90deg, #fff5f0 0%, #ffeee6 100%);
	color: #f86300;
}

.gradient-select-option--selected {
	background: linear-gradient(90deg, #f86300 0%, #dd3a3a 100%);
	color: white;
}

.gradient-select-option--selected:hover {
	background: linear-gradient(90deg, #f86300 0%, #dd3a3a 100%);
	color: white;
}
</style>

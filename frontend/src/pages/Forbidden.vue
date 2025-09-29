<template>
	<div class="min-h-screen flex items-center justify-center bg-gray-50">
		<div class="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
			<div class="mb-6">
				<svg
					class="mx-auto h-16 w-16 text-red-500"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
					/>
				</svg>
			</div>
			<h1 class="text-2xl font-bold text-gray-900 mb-4">Akses Ditolak</h1>
			<p class="text-gray-600 mb-6">
				Halaman ini memerlukan login untuk dapat diakses. Silakan login terlebih
				dahulu untuk melanjutkan.
			</p>
			<div class="space-y-3">
				<button
					@click="goToLogin"
					class="w-full bg-orange-500 hover:bg-orange-600 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
				>
					Login
				</button>
				<button
					@click="goToHome"
					class="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-lg transition duration-200"
				>
					Kembali ke Beranda
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import { sessionStore } from '@/stores/session'

export default {
	name: 'Forbidden',
	methods: {
		goToLogin() {
			const { login } = sessionStore()
			login()
		},
		goToHome() {
			window.open('https://genkiddo.id/', '_blank')
		},
	},
}
</script>

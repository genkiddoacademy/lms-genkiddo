<template>
	<div class="bg-gray-50 h-screen flex flex-col">
		<!-- Header -->
		<header class="border-b border-gray-200 p-4 flex items-center space-x-2">
			<img src="https://kiko.genkiddo.id/static/images/kiko-icon.png" alt="Kiko" class="w-8 h-8 rounded-full" />
			<h1 class="text-lg font-semibold text-gray-800">Chat with Kiko</h1>
		</header>

		<!-- Chat container -->
		<main id="chat-container" ref="chatContainer" class="flex-1 overflow-y-auto px-4 py-6 space-y-4">
			<div v-if="showWelcome"
				class="flex flex-col items-start md:items-center text-left md:text-center space-y-4 w-full">
				<img src="https://kiko.genkiddo.id/static/images/kiko-icon.png" alt="Kiko"
					class="w-20 h-20 rounded-full shadow mx-auto md:mx-0" />
				<h2 class="text-2xl font-semibold text-gray-800">Halo, Aku Kiko!</h2>
				<p class="text-gray-600">Apa ada yang bisa kubantu, nggak ya?</p>

				<!-- Input awal -->
				<div id="initial-input" class="mt-6 w-full max-w-2xl">
					<form @submit.prevent="handleSubmit('messageInput')"
						class="flex items-center space-x-2 bg-white p-3 rounded-2xl shadow-md">
						<textarea id="messageInput" v-model="inputMessage" rows="1"
							placeholder="Tanyakan ke kiko sesuatu..."
							class="flex-1 px-4 py-3 border-none rounded-xl resize-none min-h-[80px] focus:outline-none focus:ring-0 focus:border-transparent"
							style="max-height: 200px" @input="autoResize($event)"
							@keydown.enter.prevent="handleSubmit('messageInput')"></textarea>
						<button type="submit"
							class="md:w-12 md:h-12 w-14 h-14 bg-orange-500 text-white rounded-full flex items-center justify-center transition hover:bg-orange-600 active:scale-95">
							<svg xmlns="http://www.w3.org/2000/svg" class="md:w-5 md:h-5 w-6 h-6"
								viewBox="0 0 20 20" fill="currentColor">
								<path fill-rule="evenodd"
									d="M10 3a1 1 0 01.894.553l5 10a1 1 0 01-1.788.894L10 5.618 5.894 14.447a1 1 0 11-1.788-.894l5-10A1 1 0 0110 3z"
									clip-rule="evenodd" />
							</svg>
						</button>

					</form>
					<p class="text-xs text-gray-400 mt-2 text-center">
						Kiko bisa saja salah, periksa jawaban sebelum percaya 100%.
					</p>
				</div>

				<!-- Quick questions -->
				<div class="mt-6 space-y-2 w-full max-w-md">
					<button v-for="q in quickQuestions" :key="q" @click="sendQuickQuestion(q)"
						class="block w-full text-left md:text-center text-gray-700 hover:text-orange-600 transition">
						{{ q }}
					</button>
				</div>
			</div>

			<!-- Chat Messages -->
			<template v-for="(msg, index) in messages" :key="index">
				<div class="flex items-start space-x-3 chat-message" :class="msg.role === 'user' ? 'justify-end' : ''">
					<template v-if="msg.role === 'user'">
						<div class="bg-orange-100 p-3 rounded-lg text-gray-800 max-w-lg whitespace-pre-wrap">
							{{ msg.content }}
						</div>
						<div
							class="min-w-8 min-h-8 rounded-full bg-orange-500 text-white flex items-center justify-center">
							U
						</div>
					</template>
					<template v-else>
						<img src="https://kiko.genkiddo.id/static/images/kiko-icon.png" alt="Kiko"
							class="w-8 h-8 rounded-full" />
						<div class="bg-white p-3 rounded-lg shadow text-gray-800 max-w-lg whitespace-pre-wrap"
							v-html="msg.content"></div>
					</template>
				</div>
			</template>

			<!-- Typing indicator -->
			<div v-if="isTyping" class="flex items-start space-x-3 chat-message">
				<img src="https://kiko.genkiddo.id/static/images/kiko-icon.png" class="w-8 h-8 rounded-full" />
				<div class="bg-white p-3 rounded-lg shadow text-gray-500">
					Kiko sedang mengetik...
				</div>
			</div>
		</main>

		<!-- Input footer -->
		<footer id="chat-footer" v-if="!showWelcome" class="border-t border-gray-200 p-4">
			<form @submit.prevent="handleSubmit('messageInputFooter')" class="flex items-center space-x-2">
				<textarea id="messageInputFooter" v-model="inputMessage" rows="1"
					placeholder="Tanyakan ke kiko sesuatu..."
					class="flex-1 px-4 py-2 border border-gray-300 rounded-lg resize-none shadow-sm focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
					style="min-height: 44px; max-height: 150px" @input="autoResize($event)"
					@keydown.enter.prevent="handleSubmit('messageInputFooter')"></textarea>
				<button type="submit"
					class="md:w-12 md:h-12 w-14 h-14 bg-orange-500 text-white rounded-full flex items-center justify-center transition hover:bg-orange-600 active:scale-95">
					<svg xmlns="http://www.w3.org/2000/svg" class="md:w-5 md:h-5 w-6 h-6" viewBox="0 0 20 20"
						fill="currentColor">
						<path fill-rule="evenodd"
							d="M10 3a1 1 0 01.894.553l5 10a1 1 0 01-1.788.894L10 5.618 5.894 14.447a1 1 0 11-1.788-.894l5-10A1 1 0 0110 3z"
							clip-rule="evenodd" />
					</svg>
				</button>


			</form>
			<p class="text-xs text-gray-400 mt-2 text-center">
				Kiko bisa saja salah, periksa jawaban sebelum percaya 100%.
			</p>
		</footer>
	</div>
</template>

<script>
export default {
	name: "ChatKiko",
	data() {
		return {
			showWelcome: true,
			inputMessage: "",
			messages: [],
			isTyping: false,
			quickQuestions: [
				"Apa itu GenKiddo Academy?",
				"Apa yang membuat GenKiddo Academy berbeda dari kursus lain?",
				"Apa saja program kelas yang tersedia?",
				"Apa saja pilihan paket belajarnya?",
				"Apakah saya bisa mencoba kelas terlebih dahulu sebelum mendaftar?",
			],
		};
	},
	methods: {
		autoResize(e) {
			e.target.style.height = "auto";
			e.target.style.height = e.target.scrollHeight + "px";
		},
		handleSubmit(inputId) {
			const text = this.inputMessage.trim();
			if (!text) return;
			this.sendMessage(text);
			this.inputMessage = "";
		},
		sendQuickQuestion(q) {
			this.sendMessage(q);
		},
		async sendMessage(text) {
			if (this.showWelcome) this.showWelcome = false;

			this.messages.push({ role: "user", content: text });
			this.scrollToBottom();

			this.isTyping = true;

			try {
				const res = await fetch("https://kiko.genkiddo.id/chat", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({ message: text }),
				});

				const data = await res.json();
				this.isTyping = false;

				this.typeWriterEffect(data.reply);
			} catch {
				this.isTyping = false;
				this.messages.push({
					role: "ai",
					content: "⚠️ Error: gagal terhubung ke server.",
				});
			}
		},
		typeWriterEffect(text) {
			let i = 0;
			let buffer = "";
			const speed = 20;

			const interval = setInterval(() => {
				if (i < text.length) {
					buffer += text.charAt(i);
					i++;
					this.$set(this.messages, this.messages.length, {
						role: "ai",
						content: buffer,
					});
					this.scrollToBottom();
				} else {
					clearInterval(interval);
				}
			}, speed);
		},
		scrollToBottom() {
			this.$nextTick(() => {
				const el = this.$refs.chatContainer;
				el.scrollTop = el.scrollHeight;
			});
		},
	},
};
</script>

<style scoped>
.chat-message {
	animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
	from {
		opacity: 0;
		transform: translateY(10px);
	}

	to {
		opacity: 1;
		transform: translateY(0);
	}
}
</style>

import frappeUIPreset from 'frappe-ui/src/tailwind/preset'

export default {
	presets: [frappeUIPreset],
	content: [
		'./index.html',
		'./src/**/*.{vue,js,ts,jsx,tsx}',
		'./node_modules/frappe-ui/src/**/*.{vue,js,ts,jsx,tsx}',
		'../node_modules/frappe-ui/src/**/*.{vue,js,ts,jsx,tsx}',
		'./node_modules/frappe-ui/frappe/**/*.{vue,js,ts,jsx,tsx}',
		'../node_modules/frappe-ui/frappe/**/*.{vue,js,ts,jsx,tsx}',
	],
	theme: {
		extend: {
			fontSize: {
				xs: '0.75rem', // 12px
				sm: '1rem', // 16px
				base: '1.25rem', // 20px
				lg: '1.5rem', // 24px
				xl: '1.75rem', // 28px
				'2xl': '2rem', // 32px
				'3xl': '2.25rem', // 36px
				'4xl': '2.5rem', // 40px
				'5xl': '2.75rem', // 44px
				'6xl': '3rem', // 48px
				'7xl': '3.25rem', // 52px
				'8xl': '3.5rem', // 56px
				'9xl': '3.75rem', // 60px
			},
			spacing: {
				0: '0',
				px: '1px',
				0.5: '0.125rem', // 2px
				1: '0.25rem', // 4px
				1.5: '0.375rem', // 6px
				2: '0.5rem', // 8px
				2.5: '0.625rem', // 10px
				3: '0.75rem', // 12px
				3.5: '0.875rem', // 14px
				4: '1rem', // 16px
				5: '1.25rem', // 20px
				6: '1.5rem', // 24px
				7: '1.75rem', // 28px
				8: '2rem', // 32px
				9: '2.25rem', // 36px
				10: '2.5rem', // 40px
				11: '2.75rem', // 44px
				12: '3rem', // 48px
				14: '3.5rem', // 56px
				16: '4rem', // 64px
				20: '5rem', // 80px
				24: '6rem', // 96px
				28: '7rem', // 112px
				32: '8rem', // 128px
				36: '9rem', // 144px
				40: '10rem', // 160px
				44: '11rem', // 176px
				48: '12rem', // 192px
				52: '13rem', // 208px
				56: '14rem', // 224px
				60: '15rem', // 240px
				64: '16rem', // 256px
				72: '18rem', // 288px
				80: '20rem', // 320px
				96: '24rem', // 384px
			},
			colors: {
				'orange-2': '#EF7F1F',
				'warning-100': '#F5B704',
				'gradasi-1': {
					0: '#F86300',
					100: '#DD3A3A',
				},
			},

			backgroundImage: {
				'gradasi-1': 'linear-gradient(90deg, #F86300 0%, #DD3A3A 100%)',
			},

			strokeWidth: {
				1.5: '1.5',
			},
			screens: {
				'2xl': '1600px',
				'3xl': '1920px',
			},
		},
	},
	plugins: [
		function ({ addUtilities }) {
			addUtilities({
				'.text-gradasi-1': {
					background:
						'linear-gradient(90deg, #F86300 0%, #DD3A3A 100%)',
					'-webkit-background-clip': 'text',
					'background-clip': 'text',
					'-webkit-text-fill-color': 'transparent',
					color: 'transparent',
				},
			})
		},
	],
}

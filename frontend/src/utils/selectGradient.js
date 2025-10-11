// Utility function untuk force apply gradient styling pada Select components

export const applyGradientToSelect = (
	selector = '.gradient-select-wrapper button[type="button"]',
) => {
	const selectButtons = document.querySelectorAll(selector)

	selectButtons.forEach((button) => {
		// Apply comprehensive gradient styling
		const gradientStyles = {
			background: 'linear-gradient(90deg, #F86300 0%, #DD3A3A 100%)',
			'background-image':
				'linear-gradient(90deg, #F86300 0%, #DD3A3A 100%)',
			'background-color': '#F86300',
			color: 'white',
			border: 'none',
			width: '100%',
			'background-size': '100% 100%',
			'background-repeat': 'no-repeat',
			'background-attachment': 'scroll',
			'background-clip': 'border-box',
			'background-origin': 'padding-box',
		}

		// Apply styles to button
		Object.entries(gradientStyles).forEach(([property, value]) => {
			button.style.setProperty(property, value, 'important')
		})

		// Remove conflicting styles from all child elements
		const allChildren = button.querySelectorAll('*')
		allChildren.forEach((child) => {
			child.style.setProperty('background', 'transparent', 'important')
			child.style.setProperty(
				'background-color',
				'transparent',
				'important',
			)
			child.style.setProperty('background-image', 'none', 'important')
			child.style.setProperty('color', 'white', 'important')
		})

		// Ensure text elements are white
		const textElements = button.querySelectorAll('span, div, p')
		textElements.forEach((el) => {
			el.style.setProperty('color', 'white', 'important')
		})

		// Ensure SVG icons are white
		const svgElements = button.querySelectorAll('svg, path')
		svgElements.forEach((svg) => {
			svg.style.setProperty('color', 'white', 'important')
			svg.style.setProperty('stroke', 'white', 'important')
			svg.style.setProperty('fill', 'white', 'important')
		})
	})
}

export const setupSelectGradientWatcher = () => {
	// Initial apply
	setTimeout(() => applyGradientToSelect(), 100)

	// Watch for DOM changes and reapply
	const observer = new MutationObserver(() => {
		setTimeout(() => {
			applyGradientToSelect()
		}, 50)
	})

	observer.observe(document.body, {
		childList: true,
		subtree: true,
		attributes: true,
		attributeFilter: ['class', 'style'],
	})

	return observer
}

// Export default untuk backward compatibility
export default {
	applyGradientToSelect,
	setupSelectGradientWatcher,
}

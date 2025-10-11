import { Code, Zap, Leaf, Award, Crown } from 'lucide-vue-next'

// Tag mapping with icons and colors
export const tagMapping = {
	'Programmer Kecil': { icon: Code, color: 'bg-orange-200 text-orange-800' },
	'Programmer Muda': { icon: Zap, color: 'bg-blue-200 text-blue-800' },
	Beginner: { icon: Leaf, color: 'bg-green-200 text-green-800' },
	Intermediate: { icon: Award, color: 'bg-yellow-200 text-yellow-800' },
	Advance: { icon: Crown, color: 'bg-purple-200 text-purple-800' },
}

export const getTagIcon = (tag) => {
	return tagMapping[tag]?.icon || Code
}

export const getTagClasses = (tag) => {
	return tagMapping[tag]?.color || 'bg-gray-200 text-gray-800'
}

export const getDisplayTag = (tag) => {
	// Return the tag as is if it exists in our mapping, otherwise return the original tag
	return tagMapping[tag] ? tag : tag
}

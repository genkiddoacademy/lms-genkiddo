export interface BreadcrumbItem {
	label: string
	route?: any
	onClick?: () => void
}

export interface BreadcrumbsProps {
	items: BreadcrumbItem[]
}

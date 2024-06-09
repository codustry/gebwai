/** @type {import('tailwindcss').Config} */

import daisyui from "daisyui"
import defaultTheme from 'tailwindcss/defaultTheme'

// https://designsystem.line.me/LDSM/foundation/color/line-color-guide-ex-en

export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				LINE: "#06C755",
			},
			fontFamily: {
				sans: ['Prompt', ...defaultTheme.fontFamily.sans],
			},
		},
	},
	plugins: [
		daisyui,
	],
	daisyui: {
		themes: ["lofi", "dark"],
	},
}

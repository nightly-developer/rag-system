import { defineConfig } from 'vite'

export default defineConfig({
	resolve: {
		alias: {
			// You can add aliases if needed
		}
	},
	build: {
		// Ensure that it's built properly for the browser
		target: 'esnext'
	}
})

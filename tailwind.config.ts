import type {Config} from 'tailwindcss'

// @ts-ignore
export default {
    content: ["./market/**/*.{html,js}", "./users/**/*.{html,js}", "./cart/**/*.{html,js}", "./order/**/*.{html,js}"],
    theme: {
        extend: {},
    },
    plugins: [],
} satisfies Config

module.exports = {
    plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
        require('@tailwindcss/forms'),
    ]
}



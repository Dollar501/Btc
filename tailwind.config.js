/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./*.js",
    "./src/**/*.{html,js}",
    "./script.js",
    "./languages.js"
  ],
  safelist: [
    'bg-gradient-to-br',
    'from-blue-900',
    'via-purple-900',
    'to-indigo-900',
    'text-white',
    'min-h-screen',
    'flex',
    'flex-col',
    'items-center',
    'justify-center',
    'p-4',
    'bg-black',
    'bg-opacity-50',
    'backdrop-blur-sm',
    'rounded-xl',
    'shadow-2xl',
    'border',
    'border-gray-700',
    'animate-pulse',
    'text-yellow-400',
    'text-blue-400',
    'text-green-400',
    'text-red-400',
    'hover:bg-blue-600',
    'hover:bg-green-600',
    'hover:bg-purple-600',
    'transition-all',
    'duration-300',
    'transform',
    'hover:scale-105',
    {
      pattern: /bg-(blue|green|purple|yellow|red|gray)-(100|200|300|400|500|600|700|800|900)/,
    },
    {
      pattern: /text-(blue|green|purple|yellow|red|gray|white)-(100|200|300|400|500|600|700|800|900)/,
    },
    {
      pattern: /border-(blue|green|purple|yellow|red|gray)-(100|200|300|400|500|600|700|800|900)/,
    }
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
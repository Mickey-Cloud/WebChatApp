/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin')

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      height: {
        main: "calc(100vh - 144px)",
      },
      maxHeight: {
        main: "calc(100vh - 128px)",
        chat: "80vh"
      },
      fontSize: {
        xxs: ["10px", "14px"], // [font-size, line-height]
      },
      colors: {
        lgrn: "#dcfce7",
        grn: "#4ade80",
      },
    },
  },
  plugins: [
    plugin(function({ addBase, theme }) {
      addBase({
        'h1': { fontSize: theme('fontSize.2xl') },
        'h2': { fontSize: theme('fontSize.xl') },
        'h3': { fontSize: theme('fontSize.lg') },
      })
    })
  ]
}


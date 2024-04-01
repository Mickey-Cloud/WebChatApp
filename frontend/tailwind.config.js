/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      height: {
        main: "calc(100vh - 128px)",
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
  plugins: [],
}


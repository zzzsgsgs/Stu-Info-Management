/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // support manual dark mode toggle
  theme: {
    extend: {
      colors: {
        primary: 'var(--el-color-primary)',
        success: 'var(--el-color-success)',
        warning: 'var(--el-color-warning)',
        danger: 'var(--el-color-danger)',
        info: 'var(--el-color-info)',
      }
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false, // Prevent Tailwind from overriding Element Plus styles heavily
  }
}

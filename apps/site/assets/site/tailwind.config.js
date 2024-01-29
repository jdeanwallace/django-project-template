/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["apps/site/templates/**/*.{html,}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

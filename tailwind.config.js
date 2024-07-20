/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html"],
  theme: {
    extend: {
      colors:{
        "text": "#eeeeee",
        "background": "#212121",
        "primary": "#91a276",
        "accent": "#76875b"
      },
      fontFamily: {
        'sharetechmono': ['Share Tech Mono', 'sans-serif'],
      },
    },
  },
  plugins: [],
}


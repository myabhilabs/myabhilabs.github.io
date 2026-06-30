/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*.html',
    './about/**/*.html',
    './apps/**/*.html',
    './privacy/**/*.html',
    './contact/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'system-ui', 'sans-serif'],
      },
      animation: {
        'orb-slow': 'orb 8s ease-in-out infinite',
        'orb-slower': 'orb 12s ease-in-out infinite reverse',
      },
      keyframes: {
        orb: {
          '0%, 100%': { transform: 'translate(0, 0) scale(1)' },
          '33%': { transform: 'translate(30px, -20px) scale(1.05)' },
          '66%': { transform: 'translate(-20px, 10px) scale(0.95)' },
        },
      },
    },
  },
  plugins: [],
};

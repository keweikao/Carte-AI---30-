import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['var(--font-display)'],
        body: ['var(--font-body)'],
        handwriting: ['var(--font-handwriting)'],
        serif: ['Cormorant Garamond', 'Georgia', 'serif'],
      },
      colors: {
        cream: {
          50: '#F9F6F0',  // Main background - matches color guide
          100: '#F3EDE3',
          200: '#FFF0E0',
        },
        caramel: {
          50: '#FAF6F0',
          100: '#F5EDE1',
          DEFAULT: '#D4A574',  // Primary accent
          600: '#B8874F',
          700: '#9C6D3E',
        },
        terracotta: {
          50: '#F9EDE9',
          100: '#E8C5C2',
          DEFAULT: '#C77B5F',  // Multi-select tags - matches color guide
          600: '#A85F46',
          700: '#B04E48',
        },
        sage: {
          50: '#F0F2EF',
          100: '#D8DDD5',
          DEFAULT: '#8B9D83',
          700: '#6F7D68',
          900: '#4A5145',
        },
        charcoal: {
          50: '#F7F7F7',
          100: '#E3E3E3',
          DEFAULT: '#2C2C2C',  // Primary selections - matches color guide
          700: '#1F1F1F',
          900: '#0A0A0A',
        },
      },
      borderRadius: {
        button: 'var(--radius-button)',
        card: 'var(--radius-card)',
        input: 'var(--radius-input)',
      },
      boxShadow: {
        card: '0 4px 20px rgba(212, 165, 116, 0.15)',
        floating: '0 25px 50px -12px rgba(44, 44, 44, 0.15)',  // Main card shadow
      },
    },
  },
  plugins: [],
};
export default config;

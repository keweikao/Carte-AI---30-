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
      },
      colors: {
        cream: {
          50: '#FFFCF7',
          100: '#FFF8F0',
          200: '#FFF0E0',
        },
        caramel: {
          50: '#F5E6D3',
          100: '#E8D4B8',
          DEFAULT: '#D4A574',
          700: '#B8915F',
          900: '#8A6B47',
        },
        terracotta: {
          50: '#F5E1E0',
          100: '#E8C5C2',
          DEFAULT: '#C85A54',
          700: '#B04E48',
          900: '#8A3D39',
        },
        sage: {
          50: '#F0F2EF',
          100: '#D8DDD5',
          DEFAULT: '#8B9D83',
          700: '#6F7D68',
          900: '#4A5145',
        },
        charcoal: {
          50: '#F5F5F5',
          100: '#E0E0E0',
          DEFAULT: '#2D2D2D',
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
        floating: '0 12px 40px rgba(45, 45, 45, 0.25)',
      },
    },
  },
  plugins: [],
};
export default config;

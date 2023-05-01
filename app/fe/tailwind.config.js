/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
    colors: {
      // Custom color palette based on the figma
      primary: {
        text: "#000000", // black
        background: "#f4f4f1", // white
      },
      active: {
        text: "#f4f4f1", // white
        button: "#2f57fc", // blue
      },
      black: "#000000",
      white: "#f4f4f1",
      green: "#6dfe5d",
      yellow: "#e8ff1f",
      red: "#ff3c3c",
      blue: "#2f57fc",
      gray: {
        1: "#e0e0de",
        2: "#d2d2d2",
        3: "#535353",
      },
    }
  },
  plugins: [],
}


import type { Config } from "tailwindcss";
export default { content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"], theme: { extend: { colors: { ink: "#17212b", brand: { DEFAULT: "#2a7de1", dark: "#1767c4", pale: "#eaf4ff" } }, boxShadow: { soft: "0 8px 30px rgba(23,33,43,.08)" } } }, plugins: [] } satisfies Config;


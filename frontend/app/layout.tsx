import "./globals.css";

export const metadata = {
  title: "NR Fiscal Intelligence",
  description: "Inteligência fiscal, contábil e financeira",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}

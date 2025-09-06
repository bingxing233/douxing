import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: '中小微企业智能招聘助手',
  description: '基于NVIDIA NeMo Agent Toolkit的智能招聘助手',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
        <div className="min-h-screen flex flex-col">
          {children}
        </div>
      </body>
    </html>
  );
}
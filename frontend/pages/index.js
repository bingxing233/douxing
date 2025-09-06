// frontend/pages/index.js
import { useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [activeTab, setActiveTab] = useState('job-parser');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              中小微企业智能招聘助手
            </h1>
            <nav className="flex space-x-1">
              <Link 
                href="/job-parser" 
                className="px-4 py-2 rounded-lg text-gray-600 hover:text-blue-600 hover:bg-blue-50 font-medium transition-all duration-200"
              >
                岗位解析
              </Link>
              <Link 
                href="/resume-screener" 
                className="px-4 py-2 rounded-lg text-gray-600 hover:text-blue-600 hover:bg-blue-50 font-medium transition-all duration-200"
              >
                简历筛选
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-16 mt-8">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">智能招聘助手</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            基于 NVIDIA NeMo Agent Toolkit 构建的智能招聘助手，用于自动化完成招聘前期流程，
            减少重复性的招聘工作，提升招聘效率和准确率。
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden max-w-4xl mx-auto card-hover">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('job-parser')}
                className={`flex-1 py-5 px-6 text-center border-b-2 font-medium text-sm transition-all duration-200 ${
                  activeTab === 'job-parser'
                    ? 'border-blue-500 text-blue-600 bg-blue-50'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center justify-center space-x-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  <span>岗位需求解析</span>
                </div>
              </button>
              <button
                onClick={() => setActiveTab('resume-screener')}
                className={`flex-1 py-5 px-6 text-center border-b-2 font-medium text-sm transition-all duration-200 ${
                  activeTab === 'resume-screener'
                    ? 'border-green-500 text-green-600 bg-green-50'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center justify-center space-x-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>简历自动筛选</span>
                </div>
              </button>
            </nav>
          </div>

          <div className="p-8">
            {activeTab === 'job-parser' ? (
              <div className="text-center py-12 fade-in">
                <div className="max-w-md mx-auto">
                  <div className="bg-gradient-to-br from-blue-100 to-blue-200 rounded-full p-5 w-20 h-20 flex items-center justify-center mx-auto mb-6 shadow-md">
                    <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">岗位需求解析</h3>
                  <p className="text-gray-600 mb-8 text-lg">
                    将模糊的岗位描述转换为标准化职位描述（JD）
                  </p>
                  <Link href="/job-parser">
                    <button className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium py-3 px-8 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl btn-primary">
                      开始使用
                    </button>
                  </Link>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 fade-in">
                <div className="max-w-md mx-auto">
                  <div className="bg-gradient-to-br from-green-100 to-green-200 rounded-full p-5 w-20 h-20 flex items-center justify-center mx-auto mb-6 shadow-md">
                    <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-3">简历自动筛选</h3>
                  <p className="text-gray-600 mb-8 text-lg">
                    自动解析简历并与岗位需求匹配
                  </p>
                  <Link href="/resume-screener">
                    <button className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-medium py-3 px-8 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl btn-primary">
                      开始使用
                    </button>
                  </Link>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Features section */}
        <div className="mt-20">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">核心功能</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              通过AI技术自动化招聘流程，提升招聘效率
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-7 rounded-2xl shadow-lg card-hover">
              <div className="bg-gradient-to-br from-blue-100 to-blue-200 rounded-full p-4 w-16 h-16 flex items-center justify-center mb-5 shadow-md">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">岗位需求理解</h3>
              <p className="text-gray-600">
                将模糊的岗位描述转换为标准化职位描述（JD）
              </p>
            </div>
            
            <div className="bg-white p-7 rounded-2xl shadow-lg card-hover">
              <div className="bg-gradient-to-br from-green-100 to-green-200 rounded-full p-4 w-16 h-16 flex items-center justify-center mb-5 shadow-md">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">简历自动筛选</h3>
              <p className="text-gray-600">
                自动解析简历并与岗位需求匹配，提高筛选效率
              </p>
            </div>
            
            <div className="bg-white p-7 rounded-2xl shadow-lg card-hover">
              <div className="bg-gradient-to-br from-purple-100 to-purple-200 rounded-full p-4 w-16 h-16 flex items-center justify-center mb-5 shadow-md">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">初轮沟通自动化</h3>
              <p className="text-gray-600">
                通过AI进行初步候选人沟通，节省人力资源
              </p>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-white/80 backdrop-blur-sm border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-gray-600">
              © {new Date().getFullYear()} 中小微企业智能招聘助手
            </p>
            <p className="text-gray-500 text-sm mt-2">
              基于 NVIDIA NeMo Agent Toolkit 构建
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
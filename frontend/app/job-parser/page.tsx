// frontend/app/job-parser/page.tsx
'use client';
import { useState } from 'react';
import axios from 'axios';
import Link from 'next/link';

interface JobParseResult {
  status?: string;
  data?: {
    position?: string;
    company?: string;
    location?: string;
    salary_range?: string;
    experience_required?: string;
    education_required?: string;
    skills?: string[];
    responsibilities?: string[];
    requirements?: string[];
    benefits?: string[];
    employment_type?: string;
    industry?: string;
  };
  message?: string;
  error_detail?: string;
  raw_response?: string;
  error?: string;
}

export default function JobParserPage() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState<JobParseResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleParse = async () => {
    setLoading(true);
    try {
      const res = await axios.post('/api/parse-job', {
        description: input
      });
      
      // 根据新的API响应格式处理结果
      if (res.data.status === 'success' && res.data.data) {
        setResult(res.data);
      } else if (res.data.status === 'partial_success') {
        // 处理部分成功的情况
        setResult({
          raw_response: res.data.raw_response,
          message: res.data.message
        });
      } else {
        // 处理错误情况
        setResult({
          error: res.data.message || '解析失败',
          error_detail: res.data.error_detail
        });
      }
    } catch (err: any) {
      console.error('解析失败', err);
      setResult({
        error: '网络错误或服务器异常',
        error_detail: err.message
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              中小微企业智能招聘助手
            </Link>
            <nav className="flex space-x-1">
              <Link 
                href="/job-parser" 
                className="px-4 py-2 rounded-lg text-blue-600 bg-blue-50 font-medium transition-all duration-200"
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

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold text-gray-900 mb-3">岗位需求解析</h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            将模糊的岗位描述转换为标准化职位描述（JD）
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden max-w-4xl mx-auto card-hover">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-6">
            <h2 className="text-2xl font-bold text-white">输入岗位描述</h2>
            <p className="text-blue-100 mt-2">请输入您需要标准化的岗位描述</p>
          </div>
          
          <div className="p-6">
            <div className="mb-6">
              <label htmlFor="jobDescription" className="block text-sm font-medium text-gray-700 mb-2">
                岗位描述
              </label>
              <textarea
                id="jobDescription"
                placeholder="例如：招会做Excel的行政"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all input-focus"
                rows={5}
              />
              <button 
                onClick={handleParse}
                disabled={loading || !input.trim()}
                className={`mt-4 w-full py-3 px-4 rounded-xl font-medium text-white transition-all flex items-center justify-center ${
                  loading || !input.trim() 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 shadow-lg hover:shadow-xl btn-primary'
                }`}
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    生成中...
                  </>
                ) : (
                  <>
                    <svg className="icon-xs mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    </svg>
                    生成标准化岗位需求
                  </>
                )}
              </button>
            </div>

            {result && (
              <div className="mt-8 border border-gray-200 rounded-xl overflow-hidden transition-all duration-300 fade-in">
                <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                  <h2 className="text-xl font-semibold text-gray-800 flex items-center">
                    <svg className="icon-xs mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    解析结果
                  </h2>
                </div>
                <div className="p-6 space-y-6">
                  {result.error ? (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-5">
                      <div className="flex">
                        <svg className="icon-xs text-red-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <div>
                          <h3 className="text-lg font-medium text-red-800">错误信息</h3>
                          <p className="mt-1 text-red-600">{result.error}</p>
                          {result.error_detail && (
                            <p className="mt-2 text-sm text-red-500">{result.error_detail}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  ) : result.raw_response ? (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-5">
                      <div className="flex">
                        <svg className="icon-xs text-yellow-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                        </svg>
                        <div>
                          <h3 className="text-lg font-medium text-yellow-800">部分成功</h3>
                          <p className="mt-1 text-yellow-600">{result.message}</p>
                          <div className="mt-3">
                            <h4 className="font-medium text-yellow-700">原始响应:</h4>
                            <pre className="mt-2 text-sm text-yellow-600 bg-yellow-100 p-3 rounded overflow-x-auto">
                              {result.raw_response}
                            </pre>
                          </div>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <>
                      <div className="flex items-start">
                        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center mt-1">
                          <span className="text-blue-800 text-sm font-bold">1</span>
                        </div>
                        <div className="ml-4 flex-1">
                          <h3 className="text-lg font-medium text-gray-900">岗位名称</h3>
                          <p className="mt-1 text-gray-600">{result.data?.position || '未指定'}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start">
                        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center mt-1">
                          <span className="text-blue-800 text-sm font-bold">2</span>
                        </div>
                        <div className="ml-4 flex-1">
                          <h3 className="text-lg font-medium text-gray-900">工作地点</h3>
                          <p className="mt-1 text-gray-600">{result.data?.location || '未指定'}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start">
                        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center mt-1">
                          <span className="text-blue-800 text-sm font-bold">3</span>
                        </div>
                        <div className="ml-4 flex-1">
                          <h3 className="text-lg font-medium text-gray-900">薪资范围</h3>
                          <p className="mt-1 text-gray-600">{result.data?.salary_range || '未指定'}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-start">
                        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center mt-1">
                          <span className="text-blue-800 text-sm font-bold">4</span>
                        </div>
                        <div className="ml-4 flex-1">
                          <h3 className="text-lg font-medium text-gray-900">核心职责</h3>
                          {result.data?.responsibilities && Array.isArray(result.data.responsibilities) ? (
                            <ul className="mt-1 space-y-1">
                              {result.data.responsibilities.map((item, index) => (
                                <li key={index} className="text-gray-600 flex items-start">
                                  <span className="mr-2 mt-1">•</span>
                                  <span>{item}</span>
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <p className="mt-1 text-gray-600">{result.data?.responsibilities || '未指定'}</p>
                          )}
                        </div>
                      </div>
                      
                      <div className="flex items-start">
                        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center mt-1">
                          <span className="text-blue-800 text-sm font-bold">5</span>
                        </div>
                        <div className="ml-4 flex-1">
                          <h3 className="text-lg font-medium text-gray-900">任职要求</h3>
                          <div className="mt-2 space-y-3">
                            <div className="flex">
                              <span className="text-gray-600 w-24 font-medium">学历要求：</span>
                              <span className="text-gray-900">{result.data?.education_required || '未指定'}</span>
                            </div>
                            <div className="flex">
                              <span className="text-gray-600 w-24 font-medium">工作经验：</span>
                              <span className="text-gray-900">{result.data?.experience_required || '未指定'}</span>
                            </div>
                            <div>
                              <span className="text-gray-600 font-medium">专业技能：</span>
                              <div className="mt-1">
                                {result.data?.skills && Array.isArray(result.data.skills) && result.data.skills.length > 0 ? (
                                  <div className="flex flex-wrap gap-2">
                                    {result.data.skills.map((skill, index) => (
                                      <span key={index} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                                        {skill}
                                      </span>
                                    ))}
                                  </div>
                                ) : (
                                  <span className="text-gray-900">未指定</span>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-start">
                        <div className="flex-shrink-0 h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center mt-1">
                          <span className="text-blue-800 text-sm font-bold">6</span>
                        </div>
                        <div className="ml-4 flex-1">
                          <h3 className="text-lg font-medium text-gray-900">公司福利</h3>
                          {result.data?.benefits && Array.isArray(result.data.benefits) ? (
                            <ul className="mt-1 space-y-1">
                              {result.data.benefits.map((item, index) => (
                                <li key={index} className="text-gray-600 flex items-start">
                                  <span className="mr-2 mt-1">✓</span>
                                  <span>{item}</span>
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <p className="mt-1 text-gray-600">{result.data?.benefits || '未指定'}</p>
                          )}
                        </div>
                      </div>
                    </>
                  )}
                </div>
              </div>
            )}
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
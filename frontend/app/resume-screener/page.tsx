// frontend/app/resume-screener/page.tsx
'use client';
import { useState } from 'react';
import axios from 'axios';
import Link from 'next/link';

interface ResumeScreenResult {
  status?: string;
  data?: {
    match_score?: number;
    skills_match?: {
      matched_skills?: string[];
      missing_skills?: string[];
      additional_skills?: string[];
    };
    experience_match?: string;
    education_match?: string;
    strengths?: string[];
    weaknesses?: string[];
    recommendations?: string[];
    overall_assessment?: string;
  };
  message?: string;
  error_detail?: string;
  error?: string;
  resume_index?: number;
}

export default function ResumeScreenerPage() {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeText, setResumeText] = useState('');
  const [result, setResult] = useState<ResumeScreenResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleScreen = async () => {
    if (!jobDescription || !resumeText) {
      alert('请填写岗位描述和简历内容');
      return;
    }
    
    setLoading(true);
    try {
      // 修改API调用以匹配新的后端接口
      const res = await axios.post('/api/screen-resumes', {
        resume_texts: [resumeText],
        job_requirements: { description: jobDescription }
      });
      
      // 根据新的API响应格式处理结果
      if (res.data.status === 'success' && res.data.results) {
        setResult(res.data.results[0]); // 只处理第一个简历的结果
      } else {
        // 处理错误情况
        setResult({
          error: res.data.message || '筛选失败',
          error_detail: res.data.error_detail
        });
      }
      setLoading(false);
    } catch (err: any) {
      console.error('筛选失败', err);
      setResult({
        error: '网络错误或服务器异常',
        error_detail: err.message
      });
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-teal-50">
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
                className="px-4 py-2 rounded-lg text-gray-600 hover:text-blue-600 hover:bg-blue-50 font-medium transition-all duration-200"
              >
                岗位解析
              </Link>
              <Link 
                href="/resume-screener" 
                className="px-4 py-2 rounded-lg text-green-600 bg-green-50 font-medium transition-all duration-200"
              >
                简历筛选
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold text-gray-900 mb-3">简历筛选</h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            自动解析简历并与岗位需求匹配
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden card-hover">
          <div className="bg-gradient-to-r from-green-600 to-teal-700 p-6">
            <h2 className="text-2xl font-bold text-white">输入信息</h2>
            <p className="text-green-100 mt-2">请输入岗位描述和简历内容进行匹配分析</p>
          </div>
          
          <div className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <div className="bg-gray-50 rounded-xl p-6">
                <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <svg className="icon-xs mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                  </svg>
                  岗位描述
                </h2>
                <textarea
                  placeholder="请输入标准化的岗位描述"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all input-focus"
                  rows={10}
                />
              </div>
              
              <div className="bg-gray-50 rounded-xl p-6">
                <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <svg className="icon-xs mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  简历内容
                </h2>
                <textarea
                  placeholder="请输入简历内容"
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all input-focus"
                  rows={10}
                />
              </div>
            </div>
            
            <div className="flex justify-center">
              <button 
                onClick={handleScreen}
                disabled={loading || !jobDescription.trim() || !resumeText.trim()}
                className={`py-3 px-8 rounded-xl font-medium text-white transition-all flex items-center justify-center ${
                  loading || !jobDescription.trim() || !resumeText.trim()
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 shadow-lg hover:shadow-xl btn-primary'
                }`}
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    筛选中...
                  </>
                ) : (
                  <>
                    <svg className="icon-xs mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    </svg>
                    开始筛选
                  </>
                )}
              </button>
            </div>

            {result && (
              <div className="mt-8 border border-gray-200 rounded-xl overflow-hidden transition-all duration-300 fade-in">
                <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                  <h2 className="text-xl font-semibold text-gray-800 flex items-center">
                    <svg className="icon-xs mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    筛选结果
                  </h2>
                </div>
                <div className="p-6">
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
                  ) : (
                    <>
                      <div className="flex items-center justify-center mb-8">
                        <div className="relative">
                          <div className="flex-shrink-0 h-24 w-24 rounded-full bg-gradient-to-r from-green-500 to-teal-500 flex items-center justify-center">
                            <span className="text-white text-3xl font-bold">
                              {result.data?.match_score || 'N/A'}
                            </span>
                          </div>
                          <div className="absolute -bottom-2 -right-2 bg-white rounded-full p-1 shadow-md">
                            <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                          </div>
                        </div>
                        <div className="ml-6">
                          <h3 className="text-xl font-medium text-gray-900">匹配度评分</h3>
                          <p className="text-gray-600">满分100分</p>
                        </div>
                      </div>
                      
                      <div className="space-y-8">
                        <div>
                          <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                            <svg className="w-5 h-5 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                            技能匹配
                          </h3>
                          {result.data?.skills_match ? (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                              <div className="bg-green-50 p-5 rounded-xl border border-green-100">
                                <h4 className="font-medium text-green-800 mb-3 flex items-center">
                                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                                  </svg>
                                  匹配技能
                                </h4>
                                <ul className="space-y-2">
                                  {result.data.skills_match.matched_skills?.map((skill, index) => (
                                    <li key={index} className="text-green-700 flex items-start">
                                      <span className="mr-2 mt-1">✓</span>
                                      <span>{skill}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                              
                              <div className="bg-yellow-50 p-5 rounded-xl border border-yellow-100">
                                <h4 className="font-medium text-yellow-800 mb-3 flex items-center">
                                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                                  </svg>
                                  缺少技能
                                </h4>
                                <ul className="space-y-2">
                                  {result.data.skills_match.missing_skills?.map((skill, index) => (
                                    <li key={index} className="text-yellow-700 flex items-start">
                                      <span className="mr-2 mt-1">-</span>
                                      <span>{skill}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                              
                              <div className="bg-blue-50 p-5 rounded-xl border border-blue-100">
                                <h4 className="font-medium text-blue-800 mb-3 flex items-center">
                                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                  </svg>
                                  额外技能
                                </h4>
                                <ul className="space-y-2">
                                  {result.data.skills_match.additional_skills?.map((skill, index) => (
                                    <li key={index} className="text-blue-700 flex items-start">
                                      <span className="mr-2 mt-1">+</span>
                                      <span>{skill}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                          ) : (
                            <p className="text-gray-600 bg-gray-50 p-5 rounded-xl">暂无技能匹配信息</p>
                          )}
                        </div>
                        
                        <div>
                          <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                            <svg className="w-5 h-5 mr-2 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                            </svg>
                            经验与学历匹配
                          </h3>
                          <div className="bg-gray-50 p-5 rounded-xl space-y-4">
                            <div>
                              <h4 className="font-medium text-gray-700">工作经验匹配：</h4>
                              <p className="text-gray-600 mt-1 bg-white p-3 rounded-lg">{result.data?.experience_match || '暂无信息'}</p>
                            </div>
                            <div>
                              <h4 className="font-medium text-gray-700">学历匹配：</h4>
                              <p className="text-gray-600 mt-1 bg-white p-3 rounded-lg">{result.data?.education_match || '暂无信息'}</p>
                            </div>
                          </div>
                        </div>
                        
                        <div>
                          <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                            <svg className="w-5 h-5 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                            </svg>
                            综合评估
                          </h3>
                          <div className="bg-gray-50 p-5 rounded-xl space-y-5">
                            <div>
                              <h4 className="font-medium text-gray-700 flex items-center">
                                <svg className="w-4 h-4 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                                </svg>
                                优势：
                              </h4>
                              {result.data?.strengths && Array.isArray(result.data.strengths) ? (
                                <ul className="mt-2 space-y-2">
                                  {result.data.strengths.map((strength, index) => (
                                    <li key={index} className="text-gray-600 flex items-start bg-white p-3 rounded-lg">
                                      <span className="mr-2 mt-1">•</span>
                                      <span>{strength}</span>
                                    </li>
                                  ))}
                                </ul>
                              ) : (
                                <p className="text-gray-600 bg-white p-3 rounded-lg">暂无信息</p>
                              )}
                            </div>
                            
                            <div>
                              <h4 className="font-medium text-gray-700 flex items-center">
                                <svg className="w-4 h-4 mr-2 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                                </svg>
                                不足：
                              </h4>
                              {result.data?.weaknesses && Array.isArray(result.data.weaknesses) ? (
                                <ul className="mt-2 space-y-2">
                                  {result.data.weaknesses.map((weakness, index) => (
                                    <li key={index} className="text-gray-600 flex items-start bg-white p-3 rounded-lg">
                                      <span className="mr-2 mt-1">•</span>
                                      <span>{weakness}</span>
                                    </li>
                                  ))}
                                </ul>
                              ) : (
                                <p className="text-gray-600 bg-white p-3 rounded-lg">暂无信息</p>
                              )}
                            </div>
                            
                            <div>
                              <h4 className="font-medium text-gray-700 flex items-center">
                                <svg className="w-4 h-4 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                建议：
                              </h4>
                              {result.data?.recommendations && Array.isArray(result.data.recommendations) ? (
                                <ul className="mt-2 space-y-2">
                                  {result.data.recommendations.map((recommendation, index) => (
                                    <li key={index} className="text-gray-600 flex items-start bg-white p-3 rounded-lg">
                                      <span className="mr-2 mt-1">•</span>
                                      <span>{recommendation}</span>
                                    </li>
                                  ))}
                                </ul>
                              ) : (
                                <p className="text-gray-600 bg-white p-3 rounded-lg">暂无信息</p>
                              )}
                            </div>
                            
                            <div>
                              <h4 className="font-medium text-gray-700 flex items-center">
                                <svg className="w-4 h-4 mr-2 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                                </svg>
                                总体评价：
                              </h4>
                              <p className="text-gray-600 mt-2 bg-white p-3 rounded-lg">{result.data?.overall_assessment || '暂无评价'}</p>
                            </div>
                          </div>
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
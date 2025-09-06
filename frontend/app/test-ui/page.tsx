'use client';
import { useState } from 'react';

export default function TestUIPage() {
  const [uiAvailable, setUiAvailable] = useState(false);
  const [error, setError] = useState('');

  const testImport = async () => {
    try {
      const module = await import('@nvidia/nemo-agent-ui');
      setUiAvailable(!!module);
    } catch (err) {
      setError(err.message || 'Unknown error');
      console.error(err);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">UI组件测试</h1>
      
      <button 
        onClick={testImport}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        测试 @nvidia/nemo-agent-ui 导入
      </button>

      <div className="mt-6">
        {uiAvailable && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
            成功导入 @nvidia/nemo-agent-ui 组件库
          </div>
        )}
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            导入失败: {error}
          </div>
        )}
      </div>
    </div>
  );
}
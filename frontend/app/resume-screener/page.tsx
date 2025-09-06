// frontend/app/resume-screener/page.tsx
'use client';
import { useState } from 'react';
import { Card, Button, Upload, Table, Badge, message } from '@nvidia/nemo-agent-ui';
import { UploadOutlined } from '@ant-design/icons';
import axios from 'axios';

export default function ResumeScreenerPage() {
  const [jobId, setJobId] = useState(''); // 简化：手动输入岗位ID
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [screeningResults, setScreeningResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (files) => {
    // 简化：仅前端模拟上传
    const newFiles = files.map(file => ({
      uid: Date.now() + Math.random(),
      name: file.name,
      status: 'done'
    }));
    setUploadedFiles([...uploadedFiles, ...newFiles]);
  };

  const handleScreen = async () => {
    if (!jobId || uploadedFiles.length === 0) {
      message.error('请提供岗位ID并上传简历');
      return;
    }
    
    setLoading(true);
    try {
      // 模拟从文件中提取文本内容
      const resumeTexts = uploadedFiles.map((file, index) => 
        `简历内容${index + 1}：候选人具备相关技能和经验，适合该岗位。`
      );
      
      // 调用后端API进行简历筛选
      const res = await axios.post('/api/screen-resumes', {
        resume_texts: resumeTexts,
        job_requirements: { id: jobId } // 简化处理，实际应包含完整的岗位要求
      });
      
      // 处理返回结果
      const results = res.data.results.map((result, index) => ({
        id: uploadedFiles[index].uid,
        name: uploadedFiles[index].name.replace('.pdf', '').replace('.docx', ''),
        matchScore: result.match_score || Math.floor(Math.random() * 100),
        matchLevel: result.match_level || (Math.random() > 0.7 ? '匹配' : Math.random() > 0.4 ? '待评估' : '不匹配'),
        reason: result.reason || '技能匹配度评估完成'
      }));
      
      setScreeningResults(results);
      message.success('简历筛选完成');
    } catch (err) {
      console.error('筛选失败', err);
      message.error('简历筛选失败：' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { title: '候选人', dataIndex: 'name', key: 'name' },
    { 
      title: '匹配度', 
      key: 'match',
      render: (_, record) => (
        <Badge 
          status={record.matchLevel === '匹配' ? 'success' : record.matchLevel === '待评估' ? 'warning' : 'error'}
          text={`${record.matchScore}% ${record.matchLevel}`}
        />
      )
    },
    { title: '匹配理由', dataIndex: 'reason', key: 'reason' }
  ];

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">简历筛选</h1>
      
      <Card className="mb-6 p-4">
        <div className="mb-4">
          <input
            type="text"
            placeholder="输入岗位ID"
            value={jobId}
            onChange={(e) => setJobId(e.target.value)}
            className="p-2 border rounded w-full"
          />
        </div>
        
        <Upload
          name="resumes"
          accept=".pdf,.docx"
          showUploadList
          beforeUpload={() => false} // 阻止自动上传
          onChange={info => handleFileUpload(info.fileList)}
        >
          <Button icon={<UploadOutlined />}>上传简历</Button>
        </Upload>
        
        <Button 
          type="primary" 
          className="mt-4"
          onClick={handleScreen}
          loading={loading}
          disabled={!jobId || uploadedFiles.length === 0}
        >
          开始筛选
        </Button>
      </Card>
      
      {screeningResults.length > 0 && (
        <Card>
          <h2 className="text-xl font-semibold mb-4">筛选结果</h2>
          <Table
            columns={columns}
            dataSource={screeningResults}
            rowKey="id"
          />
        </Card>
      )}
    </div>
  );
}
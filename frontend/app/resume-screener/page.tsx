// frontend/app/resume-screener/page.tsx
'use client';
import { useState } from 'react';
import { Card, Button, Upload, Table, Badge } from '@nvidia/nemo-agent-ui';
import { UploadOutlined } from '@ant-design/icons';

export default function ResumeScreenerPage() {
  const [jobId, setJobId] = useState(''); // 简化：手动输入岗位ID
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [screeningResults, setScreeningResults] = useState([]);

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
    // 简化：模拟筛选过程
    const mockResults = uploadedFiles.map(file => ({
      id: file.uid,
      name: file.name.replace('.pdf', '').replace('.docx', ''), // 模拟候选人姓名
      matchScore: Math.floor(Math.random() * 100),
      matchLevel: Math.random() > 0.7 ? '匹配' : Math.random() > 0.4 ? '待评估' : '不匹配',
      reason: '技能匹配度70%，经验要求部分满足' // 模拟理由
    }));
    setScreeningResults(mockResults);
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
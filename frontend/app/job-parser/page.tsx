// frontend/app/job-parser/page.tsx
'use client';
import { useState } from 'react';
import { Button, Input, Card, Form, Divider } from '@nvidia/nemo-agent-ui';
import axios from 'axios';

export default function JobParserPage() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleParse = async () => {
    setLoading(true);
    try {
      const res = await axios.post('/api/parse-job', {
        description: input
      });
      setResult(res.data);
    } catch (err) {
      console.error('解析失败', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">岗位需求解析</h1>
      
      <Form onSubmit={(e) => { e.preventDefault(); handleParse(); }}>
        <Input
          placeholder="请输入岗位描述（例如：招会做Excel的行政）"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          multiline
          rows={4}
          className="mb-4"
        />
        <Button type="primary" loading={loading} onClick={handleParse}>
          生成标准化岗位需求
        </Button>
      </Form>

      {result && (
        <Card className="mt-6 p-4">
          <h2 className="text-xl font-semibold mb-4">解析结果</h2>
          <Divider />
          <div className="space-y-4">
            <div>
              <h3 className="font-medium">岗位名称：{result.title}</h3>
            </div>
            <div>
              <h3 className="font-medium">核心职责：</h3>
              <p>{result.responsibilities}</p>
            </div>
            <div>
              <h3 className="font-medium">任职要求：</h3>
              <ul className="list-disc pl-5">
                <li>学历要求：{result.requirements.education}</li>
                <li>工作经验：{result.requirements.experience}</li>
                <li>专业技能：{result.requirements.skills.join(', ')}</li>
              </ul>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}
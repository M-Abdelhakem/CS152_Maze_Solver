import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  try {
    const targetUrl = `http://http://3.147.27.202:8000${req.url?.replace('/api/proxy', '') || ''}`;
    
    const response = await fetch(targetUrl, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: req.method !== 'GET' && req.method !== 'HEAD' && req.body ? 
        JSON.stringify(req.body) : undefined
    });
    
    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    return res.status(500).json({ error: 'Failed to fetch from backend' });
  }
}
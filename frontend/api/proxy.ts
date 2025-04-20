import type { VercelRequest, VercelResponse } from '@vercel/node';

// Define the API URL directly since I only use it for deployment on vercel
const BACKEND_URL = 'http://3.147.27.202:8000';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  try {
    // Log the incoming request details
    console.log('Incoming request URL:', req.url);
    console.log('Incoming request method:', req.method);
    
    const targetUrl = `${BACKEND_URL}${req.url?.replace('/api/proxy', '') || ''}`;
    console.log('Forwarding to:', targetUrl);
    
    const response = await fetch(targetUrl, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: req.method !== 'GET' && req.method !== 'HEAD' && req.body ? 
        JSON.stringify(req.body) : undefined
    });
    
    console.log('Backend response status:', response.status);
    
    // If we get a 404 from the backend, provide a more specific error
    if (response.status === 404) {
      return res.status(404).json({ 
        error: 'Backend endpoint not found',
        url: targetUrl
      });
    }
    
    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    // Return more detailed error information
    return res.status(500).json({ 
      error: 'Failed to fetch from backend', 
      message: error.message,
      stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
}
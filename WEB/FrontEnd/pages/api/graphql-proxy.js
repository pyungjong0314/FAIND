export default async function handler(req, res) {
    const response = await fetch("http://223.194.45.67:8003", {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(req.body)
    });
  
    const data = await response.json();
    res.status(200).json(data);
  }
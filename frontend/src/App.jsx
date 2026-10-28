import { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetching from our local FastAPI backend
        const backendUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const response = await fetch(`${backendUrl}/api/analysis`)
        if (!response.ok) throw new Error('Failed to fetch data')
        const result = await response.json()
        
        // Format dates for better chart readability
        const formattedData = result.time_series.map(item => ({
          ...item,
          displayTime: new Date(item.startTime).toLocaleString([], {
            month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
          })
        }))

        setData({ metrics: result.metrics, time_series: formattedData })
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading wind generation data...</div>
  if (error) return <div style={{ padding: '2rem', color: 'red' }}>Error: {error}</div>
  if (!data) return null

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '0.5rem' }}>UK Day-Ahead Wind Generation Analysis</h1>
      <p style={{ color: '#666', marginBottom: '2rem' }}>Evaluating forecast accuracy for January 2026 trading decisions.</p>
      
      {/* KPI Cards */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        <div style={{ padding: '1.5rem', backgroundColor: '#f3f4f6', borderRadius: '8px', flex: 1 }}>
          <h3 style={{ margin: 0, color: '#4b5563', fontSize: '0.9rem' }}>Mean Absolute Error (MAE)</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: '0.5rem 0 0 0' }}>{data.metrics.mean_absolute_error_mw} MW</p>
        </div>
        <div style={{ padding: '1.5rem', backgroundColor: '#f3f4f6', borderRadius: '8px', flex: 1 }}>
          <h3 style={{ margin: 0, color: '#4b5563', fontSize: '0.9rem' }}>Root Mean Square Error (RMSE)</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: '0.5rem 0 0 0' }}>{data.metrics.root_mean_square_error_mw} MW</p>
        </div>
        <div style={{ padding: '1.5rem', backgroundColor: '#f3f4f6', borderRadius: '8px', flex: 1 }}>
          <h3 style={{ margin: 0, color: '#4b5563', fontSize: '0.9rem' }}>Settlement Periods</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', margin: '0.5rem 0 0 0' }}>{data.metrics.total_settlement_periods}</p>
        </div>
      </div>

      {/* Line Chart: Actual vs Forecast */}
      <div style={{ marginBottom: '3rem', height: '400px' }}>
        <h2 style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>Actual vs Forecasted Generation (MW)</h2>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data.time_series}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
            <XAxis dataKey="displayTime" minTickGap={50} tick={{fontSize: 12}} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="actual_generation" name="Actual Generation" stroke="#2563eb" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="forecast_generation" name="Day-Ahead Forecast" stroke="#ea580c" strokeWidth={2} strokeDasharray="5 5" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Bar Chart: Error Margin */}
      <div style={{ height: '300px' }}>
        <h2 style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>Absolute Forecast Error (MW)</h2>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data.time_series}>
            <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
            <XAxis dataKey="displayTime" minTickGap={50} tick={{fontSize: 12}} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="absolute_error_mw" name="Absolute Error (MW)" fill="#ef4444" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default App
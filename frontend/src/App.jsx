import { useState } from 'react'
import './App.css'

export default function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  async function handleSearch(e) {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    setQuery('')
    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`)
    const data = await res.json()
    setResults(data.results)
    setLoading(false)
  }

  return (
    <div className="app">
      <h1>Gutenberg Search</h1>
      <form className="search-form" onSubmit={handleSearch}>
        <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search..." />
        <button type="submit">Search</button>
      </form>
      {loading && <p>Loading...</p>}
      <ul className="results">
        {results.map(r => (
          <li key={r.id}>{r.title} — {r.author}</li>
        ))}
      </ul>
    </div>
  )
}

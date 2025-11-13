import { useEffect, useState } from 'react'

const API = '/api' // goes through Vite proxy to FastAPI

export default function App() {
  const [token, setToken] = useState(null)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [items, setItems] = useState([])
  const [name, setName] = useState('')
  const [price, setPrice] = useState('')

  async function fetchItems() {
    const res = await fetch(`${API}/items`)
    const data = await res.json()
    setItems(data)
  }

  async function handleLogin(e) {
    e.preventDefault()
    const res = await fetch(`${API}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    if (res.ok) {
      const data = await res.json()
      setToken(data.token)
      setUsername('')
      setPassword('')
      await fetchItems()
    } else {
      alert('Login failed')
    }
  }

  async function handleAddItem(e) {
    e.preventDefault()
    const p = parseFloat(price)
    if (!name || Number.isNaN(p)) return
    const res = await fetch(`${API}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, price: p }),
    })
    if (res.ok) {
      setName('')
      setPrice('')
      await fetchItems()
    } else {
      alert('Create failed')
    }
  }

  useEffect(() => { fetchItems() }, [])

  return (
    <div style={{ maxWidth: 720, margin: '2rem auto', fontFamily: 'system-ui' }}>
      <h1>E2E Mini App (React)</h1>

      {!token ? (
        <form onSubmit={handleLogin} id="login-form" data-testid="login-form" style={{ display: 'grid', gap: '0.5rem', maxWidth: 360 }}>
          <label>
            Username
            <input id="username" data-testid="username" value={username} onChange={e => setUsername(e.target.value)} />
          </label>
          <label>
            Password
            <input id="password" data-testid="password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
          </label>
          <button id="login-btn" data-testid="login-btn" type="submit">Login</button>
          <small>Tip: admin / fakepass</small>
        </form>
      ) : (
        <>
          <div id="logged-in" data-testid="logged-in" style={{ marginBottom: '1rem' }}>Logged in ✔</div>

          <form onSubmit={handleAddItem} id="add-form" data-testid="add-form" style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
            <input id="item-name" data-testid="item-name" placeholder="Notebook" value={name} onChange={e => setName(e.target.value)} />
            <input id="item-price" data-testid="item-price" type="number" step="0.01" placeholder="10.50" value={price} onChange={e => setPrice(e.target.value)} />
            <button id="add-btn" data-testid="add-btn" type="submit">Add</button>
          </form>

          <ul id="items" data-testid="items">
            {items.map(it => (
              <li key={it.id} data-testid={`item-${it.id}`}>
                {it.id} - {it.name} (${it.price})
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  )
}

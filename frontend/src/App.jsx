import { useEffect, useState } from 'react'
import { Navigate, Route, Routes, useNavigate } from 'react-router-dom'
import './App.css'

const SESSION_TOKEN_KEY = 'session_token'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const BEARER_PREFIX = 'Bearer '

function hasToken() {
  return Boolean(sessionStorage.getItem(SESSION_TOKEN_KEY))
}

function ProtectedRoute({ children }) {
  if (!hasToken()) {
    return <Navigate to="/login" replace />
  }

  return children
}

function LoginPage() {
  const navigate = useNavigate()
  const [usuario, setUsuario] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ usuario, password }),
      })

      if (!response.ok) {
        throw new Error('Credenciales inválidas')
      }

      const body = await response.json()
      sessionStorage.setItem(SESSION_TOKEN_KEY, body.access_token)
      navigate('/welcome', { replace: true })
    } catch {
      setError('No se pudo iniciar sesión. Verifica tus datos e intenta nuevamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="page-layout">
      <section className="panel">
        <h1 className="title">Iniciar sesión</h1>
        <p className="subtitle">Ingresa tus credenciales para acceder a la plataforma.</p>
        <form className="form" onSubmit={handleSubmit}>
          <label htmlFor="usuario">Usuario</label>
          <input
            id="usuario"
            type="text"
            value={usuario}
            onChange={(event) => setUsuario(event.target.value)}
            required
          />

          <label htmlFor="password">Contraseña</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />

          {error ? <p className="error">{error}</p> : null}

          <button type="submit" disabled={loading}>
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>
      </section>
    </main>
  )
}

function WelcomePage() {
  const navigate = useNavigate()
  const [usuario, setUsuario] = useState('')

  useEffect(() => {
    const token = sessionStorage.getItem(SESSION_TOKEN_KEY)
    if (!token) {
      navigate('/login', { replace: true })
      return
    }

    fetch(`${API_BASE_URL}/api/me`, {
      headers: {
        Authorization: BEARER_PREFIX + token,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Token inválido')
        }
        return response.json()
      })
      .then((body) => setUsuario(body.usuario))
      .catch(() => {
        sessionStorage.removeItem(SESSION_TOKEN_KEY)
        navigate('/login', { replace: true })
      })
  }, [navigate])

  const onLogout = () => {
    sessionStorage.removeItem(SESSION_TOKEN_KEY)
    navigate('/login', { replace: true })
  }

  return (
    <main className="page-layout">
      <section className="panel">
        <h1 className="title">Bienvenido</h1>
        <p className="subtitle">Hola {usuario || 'usuario'}, iniciaste sesión correctamente.</p>
        <button type="button" onClick={onLogout}>
          Cerrar sesión
        </button>
      </section>
    </main>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/welcome"
        element={
          <ProtectedRoute>
            <WelcomePage />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}

export default App

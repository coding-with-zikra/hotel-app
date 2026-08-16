import axios from 'axios'

const axiosClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
})

// Runs before every outgoing request -- attaches the JWT from
// localStorage automatically, so individual API calls never need
// to manually add the Authorization header themselves.
axiosClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Runs on every response -- if the backend ever says the token is
// invalid/expired (401), clear it and send the user back to login
// instead of silently failing on every subsequent request.
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default axiosClient
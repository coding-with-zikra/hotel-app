import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="bg-slate-800 text-white px-6 py-4 flex items-center justify-between">
      <Link to="/" className="text-xl font-bold">
        Hotel
      </Link>
      <div className="flex gap-6">
        <Link to="/rooms" className="hover:text-slate-300">Rooms</Link>
        <Link to="/dashboard" className="hover:text-slate-300">Dashboard</Link>
        <Link to="/login" className="hover:text-slate-300">Login</Link>
      </div>
    </nav>
  )
}

export default Navbar
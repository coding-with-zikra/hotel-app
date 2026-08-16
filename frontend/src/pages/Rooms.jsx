import { useState, useEffect } from 'react'
import axiosClient from '../api/axiosClient'
import RoomCard from '../components/RoomCard'

function Rooms() {
  const [rooms, setRooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Filter state -- controlled inputs, kept as strings since that's
  // what <input> elements give us; converted/omitted when building
  // the query params sent to the backend.
  const [checkIn, setCheckIn] = useState('')
  const [checkOut, setCheckOut] = useState('')
  const [guests, setGuests] = useState('')
  const [minPrice, setMinPrice] = useState('')
  const [maxPrice, setMaxPrice] = useState('')

  const fetchRooms = async () => {
    setLoading(true)
    setError(null)
    try {
      // Only include params that are actually set -- an empty string
      // filter would otherwise reach the backend as "?guests=" which
      // FastAPI would reject (it expects a valid int or nothing).
      const params = {}
      if (checkIn) params.check_in = checkIn
      if (checkOut) params.check_out = checkOut
      if (guests) params.guests = guests
      if (minPrice) params.min_price = minPrice
      if (maxPrice) params.max_price = maxPrice

      const response = await axiosClient.get('/rooms', { params })
      setRooms(response.data)
    } catch (err) {
      setError('Failed to load rooms. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  // Fetch once on initial page load, with no filters applied.
  useEffect(() => {
    fetchRooms()
  }, [])

  const handleFilterSubmit = (e) => {
    e.preventDefault()
    fetchRooms()
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">Rooms</h1>

      <form
        onSubmit={handleFilterSubmit}
        className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8 bg-slate-800 p-4 rounded-lg"
      >
        <div>
          <label className="text-xs text-slate-400">Check In</label>
          <input
            type="date"
            value={checkIn}
            onChange={(e) => setCheckIn(e.target.value)}
            className="w-full bg-slate-700 rounded px-2 py-1"
          />
        </div>
        <div>
          <label className="text-xs text-slate-400">Check Out</label>
          <input
            type="date"
            value={checkOut}
            onChange={(e) => setCheckOut(e.target.value)}
            className="w-full bg-slate-700 rounded px-2 py-1"
          />
        </div>
        <div>
          <label className="text-xs text-slate-400">Guests</label>
          <input
            type="number"
            min="1"
            value={guests}
            onChange={(e) => setGuests(e.target.value)}
            className="w-full bg-slate-700 rounded px-2 py-1"
          />
        </div>
        <div>
          <label className="text-xs text-slate-400">Min Price</label>
          <input
            type="number"
            min="0"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
            className="w-full bg-slate-700 rounded px-2 py-1"
          />
        </div>
        <div>
          <label className="text-xs text-slate-400">Max Price</label>
          <input
            type="number"
            min="0"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            className="w-full bg-slate-700 rounded px-2 py-1"
          />
        </div>
        <button
          type="submit"
          className="col-span-2 md:col-span-5 bg-blue-600 hover:bg-blue-500 rounded py-2 mt-2"
        >
          Search
        </button>
      </form>

      {loading && <p className="text-slate-400">Loading rooms...</p>}
      {error && <p className="text-red-400">{error}</p>}

      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {rooms.map((room) => (
            <RoomCard key={room.id} room={room} />
          ))}
        </div>
      )}

      {!loading && !error && rooms.length === 0 && (
        <p className="text-slate-400">No rooms found for the selected filters.</p>
      )}
    </div>
  )
}

export default Rooms
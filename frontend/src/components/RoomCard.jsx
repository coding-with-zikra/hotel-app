import { Link } from 'react-router-dom'

function RoomCard({ room }) {
  return (
    <div className="bg-slate-800 rounded-lg overflow-hidden flex flex-col">
      <div className="p-4 flex-1 flex flex-col">
        <h3 className="text-lg font-semibold text-white">{room.name}</h3>
        <p className="text-slate-400 text-sm mt-1 flex-1">{room.description}</p>
        <div className="flex items-center justify-between mt-4">
          <span className="text-white font-bold">₹{room.price_per_night}/night</span>
          <span className="text-slate-400 text-sm">Up to {room.capacity} guests</span>
        </div>
        <Link
          to={`/rooms/${room.id}`}
          className="mt-4 bg-blue-600 hover:bg-blue-500 text-white text-center py-2 rounded"
        >
          View Details
        </Link>
      </div>
    </div>
  )
}

export default RoomCard
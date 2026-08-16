import { useParams } from 'react-router-dom'

function RoomDetail() {
  const { id } = useParams()

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <h1 className="text-3xl font-bold">Room Detail</h1>
      <p className="text-slate-400 mt-2">Room ID: {id}</p>
    </div>
  )
}

export default RoomDetail
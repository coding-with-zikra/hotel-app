import { useCart } from '../context/CartContext'

function MenuCard({ item }) {
  const { addItem } = useCart()

  return (
    <div className="bg-slate-800 rounded-lg p-4 flex flex-col min-h-[140px]">
      <h3 className="text-white font-semibold">{item.name}</h3>
      <p className="text-slate-400 text-sm mt-1 flex-1">{item.description}</p>
      <div className="flex items-center justify-between mt-4">
        <span className="text-white font-bold">₹{item.price}</span>
        <button
          onClick={() => addItem(item)}
          disabled={!item.is_available}
          className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white text-sm px-4 py-1.5 rounded"
        >
          {item.is_available ? 'Add' : 'Unavailable'}
        </button>
      </div>
    </div>
  )
}

export default MenuCard
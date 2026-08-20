import { useState, useEffect } from 'react'
import axiosClient from '../api/axiosClient'
import MenuCard from '../components/MenuCard'
import { useCart } from '../context/CartContext'

function Menu() {
  const [categories, setCategories] = useState([])
  const [activeCategoryId, setActiveCategoryId] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const { cartItems, totalItems, totalPrice, decrementItem, addItem } = useCart()

  useEffect(() => {
    const fetchMenu = async () => {
      try {
        const response = await axiosClient.get('/menu')
        setCategories(response.data)
        // Default to the first category's tab once data arrives.
        if (response.data.length > 0) {
          setActiveCategoryId(response.data[0].id)
        }
      } catch (err) {
        setError('Failed to load menu. Please try again.')
      } finally {
        setLoading(false)
      }
    }
    fetchMenu()
  }, [])

  const activeCategory = categories.find((c) => c.id === activeCategoryId)

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">Menu</h1>

      {loading && <p className="text-slate-400">Loading menu...</p>}
      {error && <p className="text-red-400">{error}</p>}

      {!loading && !error && (
        <div className="flex gap-8">
          <div className="flex-1">
            {/* Category tabs */}
            <div className="flex gap-2 overflow-x-auto pb-4 mb-6 border-b border-slate-700">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setActiveCategoryId(category.id)}
                  className={`whitespace-nowrap px-4 py-2 rounded-t-lg text-sm font-medium ${
                    category.id === activeCategoryId
                      ? 'bg-slate-800 text-white'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {category.name}
                </button>
              ))}
            </div>

            {/* Items in the active category */}
            {activeCategory && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {activeCategory.items.map((item) => (
                  <MenuCard key={item.id} item={item} />
                ))}
              </div>
            )}
          </div>

          {/* Cart summary sidebar */}
          <div className="w-72 shrink-0">
            <div className="bg-slate-800 rounded-lg p-4 sticky top-4">
              <h2 className="font-semibold mb-4">Your Cart ({totalItems})</h2>
              {cartItems.length === 0 && (
                <p className="text-slate-400 text-sm">Your cart is empty.</p>
              )}
              {cartItems.map(({ menuItem, quantity }) => (
                <div key={menuItem.id} className="flex items-center justify-between mb-3 text-sm">
                  <div>
                    <p className="text-white">{menuItem.name}</p>
                    <p className="text-slate-400">₹{menuItem.price} × {quantity}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => decrementItem(menuItem.id)}
                      className="bg-slate-700 hover:bg-slate-600 w-6 h-6 rounded"
                    >
                      −
                    </button>
                    <span>{quantity}</span>
                    <button
                      onClick={() => addItem(menuItem)}
                      className="bg-slate-700 hover:bg-slate-600 w-6 h-6 rounded"
                    >
                      +
                    </button>
                  </div>
                </div>
              ))}
              {cartItems.length > 0 && (
                <div className="border-t border-slate-700 mt-4 pt-4 flex items-center justify-between font-semibold">
                  <span>Total</span>
                  <span>₹{totalPrice.toFixed(2)}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Menu
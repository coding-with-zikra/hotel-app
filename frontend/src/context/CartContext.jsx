import { createContext, useContext, useState } from 'react'

const CartContext = createContext(null)

export function CartProvider({ children }) {
  // Cart items keyed by menu item id, so adding the same dish twice
  // increments quantity instead of creating duplicate entries.
  const [items, setItems] = useState({})

  const addItem = (menuItem) => {
    setItems((prev) => {
      const existing = prev[menuItem.id]
      return {
        ...prev,
        [menuItem.id]: {
          menuItem,
          quantity: existing ? existing.quantity + 1 : 1,
        },
      }
    })
  }

  const removeItem = (menuItemId) => {
    setItems((prev) => {
      const updated = { ...prev }
      delete updated[menuItemId]
      return updated
    })
  }

  const decrementItem = (menuItemId) => {
    setItems((prev) => {
      const existing = prev[menuItemId]
      if (!existing) return prev
      if (existing.quantity <= 1) {
        const updated = { ...prev }
        delete updated[menuItemId]
        return updated
      }
      return {
        ...prev,
        [menuItemId]: { ...existing, quantity: existing.quantity - 1 },
      }
    })
  }

  const clearCart = () => setItems({})

  const cartItems = Object.values(items)
  const totalItems = cartItems.reduce((sum, i) => sum + i.quantity, 0)
  const totalPrice = cartItems.reduce(
    (sum, i) => sum + i.quantity * Number(i.menuItem.price),
    0
  )

  return (
    <CartContext.Provider
      value={{ cartItems, addItem, removeItem, decrementItem, clearCart, totalItems, totalPrice }}
    >
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}
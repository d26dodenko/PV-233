import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const signup = async (userData: { fullName: string; email: string; password: string }) => {
    return await api.post("/users/register", userData);
  };

export const login = async (credentials: { email: string; password: string }) => {
  return await api.post("/users/login", credentials);
};

export const getProducts = async () => {
  return await api.get("/products");
};


export const getProductById = async (id: string) => {
  return await api.get(`/products/${id}`);
};

export const addToCart = async (cartItems: { productId: string; quantity: number; size: string }) => {
  return await api.post("/cart/add", cartItems);
};

export const getCartItems = async () => {
  return await api.get("/cart");
};

export const deleteCartItem = async (itemId: string) => {
  return await api.delete(`/cart/remove/${itemId}`);
};



export const createOrder = async (orderData: { shippingAddress: string }) => {
  return await api.post("/orders/create", orderData);
};

export const getOrder = async () => {
  return await api.get("/orders/get");
};


export default api;
export const logout = () => api.post("/users/logout");

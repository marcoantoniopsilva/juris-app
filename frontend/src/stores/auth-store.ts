import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  units: Array<{
    unitId: string;
    role: string;
    isAdmin: boolean;
  }>;
}

interface AuthState {
  user: User | null;
  token: string | null;
  currentUnit: string | null;
  login: (user: User, token: string) => void;
  logout: () => void;
  setCurrentUnit: (unitId: string) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      currentUnit: null,
      
      login: (user, token) => set({ user, token }),
      
      logout: () => set({ user: null, token: null, currentUnit: null }),
      
      setCurrentUnit: (unitId) => set({ currentUnit: unitId }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
"use client";

import { Navigation } from '@/components/Navigation';
import { useAuth } from '@/contexts/AuthContext';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function Layout({ children }: { children: React.ReactNode }) {
  const { session, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && !session) {
      navigate('/login');
    }
  }, [session, loading, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <main>
        {children}
      </main>
    </div>
  );
}
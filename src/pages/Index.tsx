"use client";

import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { MadeWithDyad } from '@/components/made-with-dyad';

const Index = () => {
  const { session, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    console.log("Index page loaded");
    console.log("Session:", session);
    console.log("Loading:", loading);
    
    if (!loading) {
      if (session) {
        console.log("User is logged in, redirecting to dashboard");
        navigate('/dashboard');
      } else {
        console.log("User is not logged in, redirecting to login");
        navigate('/login');
      }
    }
  }, [session, loading, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Redirecionando...</h1>
        <p className="text-xl text-gray-600">
          Por favor, aguarde enquanto você é redirecionado.
        </p>
      </div>
      <MadeWithDyad />
    </div>
  );
};

export default Index;
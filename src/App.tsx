import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Documentos from "./pages/Documentos";
import Jurisprudencia from "./pages/Jurisprudencia";
import Minutas from "./pages/Minutas";
import { AuthProvider } from "./contexts/AuthContext";
import { Layout } from "./components/Layout";

const queryClient = new QueryClient();

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  return <Layout>{children}</Layout>;
};

const PublicRoute = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};

const App = () => (
  <QueryClientProvider client={queryClient}>
    <AuthProvider>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/login" element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } />
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/documentos" element={
              <ProtectedRoute>
                <Documentos />
              </ProtectedRoute>
            } />
            <Route path="/jurisprudencia" element={
              <ProtectedRoute>
                <Jurisprudencia />
              </ProtectedRoute>
            } />
            <Route path="/minutas" element={
              <ProtectedRoute>
                <Minutas />
              </ProtectedRoute>
            } />
            {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </AuthProvider>
  </QueryClientProvider>
);

export default App;
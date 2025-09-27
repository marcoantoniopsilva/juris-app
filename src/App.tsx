import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { AppProviders } from "@/providers/AppProviders";
import { Layout } from "@/components/Layout";
import Index from "./pages/Index";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Documentos from "./pages/Documentos";
import Jurisprudencia from "./pages/Jurisprudencia";
import Minutas from "./pages/Minutas";
import NotFound from "./pages/NotFound";

const App = () => (
  <AppProviders>
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/login" element={<Login />} />
          <Route element={<Layout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/documentos" element={<Documentos />} />
            <Route path="/jurisprudencia" element={<Jurisprudencia />} />
            <Route path="/minutas" element={<Minutas />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </AppProviders>
);

export default App;
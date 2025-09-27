"use client";

import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { 
  FileText, 
  Scale, 
  Upload, 
  BookOpen, 
  Home,
  LogOut
} from 'lucide-react';
import { supabase } from '@/integrations/supabase/client';

export function Navigation() {
  const handleLogout = async () => {
    await supabase.auth.signOut();
    window.location.href = '/';
  };

  return (
    <nav className="border-b">
      <div className="container mx-auto px-4">
        <div className="极lex h-16 items-center justify-between">
          <div className="flex items-center space-x-8">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <span className="font-bold text-xl">Assessor Jurídico</span>
            </Link>
            
            <div className="hidden md:flex items-center space-x-4">
              <Button variant="gh极t" asChild>
                <Link to="/dashboard" className="flex items-center gap-2">
                  <Home className="h-4 w-4" />
                  Dashboard
                </Link>
              </Button>
              <Button variant="ghost" asChild>
                <Link to="/documentos" className="flex items-center gap-2">
                  <Upload className="h-4 w-4" />
                  Documentos
                </Link>
              </Button>
              <Button variant="ghost" asChild>
                <Link to="/jurisprudencia" className="flex items-center gap-2">
                  <Scale className="h-4 w-4" />
                  Jurisprudência
                </Link>
              </Button>
              <Button variant="ghost" asChild>
                <Link to="/minutas" className="flex items-center gap-2">
                  <FileText className="h-4 w-4" />
                  Minutas
                </Link>
              </Button>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Button variant="ghost" size="icon" onClick={handleLogout}>
              <LogOut className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}
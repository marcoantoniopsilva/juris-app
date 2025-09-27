"use client";

import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText, Scale, Users, BookOpen, Upload } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="container mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-muted-foreground">
          Bem-vindo, {user?.email} 
        </p>
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card 
          className="hover:shadow-md transition-shadow cursor-pointer"
          onClick={() => navigate('/documentos')}
        >
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-6 w-6" />
              Documentos
            </CardTitle>
            <CardDescription>Envie e gerencie documentos</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">0</p>
            <Button variant="outline" size="sm" className="mt-2">
              Ver Documentos
            </Button>
          </CardContent>
        </Card>

        <Card 
          className="hover:shadow-md transition-shadow cursor-pointer"
          onClick={() => navigate('/jurisprudencia')}
        >
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Scale className="h-6 w-6" />
              Jurisprudência
            </CardTitle>
            <CardDescription>Pesquise decisões judiciais</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">0</p>
            <Button variant="outline" size="sm" className="mt-2">
              Buscar Decisões
            </Button>
          </CardContent>
        </Card>

        <Card 
          className="hover:shadow-md transition-shadow cursor-pointer"
          onClick={() => navigate('/minutas')}
        >
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-6 w-6" />
              Minutas
            </CardTitle>
            <CardDescription>Crie minutas jurídicas</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">0</p>
            <Button variant="outline" size="sm" className="mt-2">
              Gerar Minuta
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-6 w-6" />
              Perfil
            </CardTitle>
            <CardDescription>Configurações da conta</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              {user?.email}
            </p>
            <Button variant="outline" size="sm" className="mt-2">
              Editar Perfil
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Ações Rápidas</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Button 
            className="flex items-center gap-2"
            onClick={() => navigate('/minutas')}
          >
            <FileText className="h-4 w-4" />
            Nova Minuta
          </Button>
          <Button 
            variant="outline" 
            className="flex items-center gap-2"
            onClick={() => navigate('/documentos')}
          >
            <Upload className="h-4 w-4" />
            Upload Documento
          </Button>
          <Button 
            variant="outline" 
            className="flex items-center gap-2"
            onClick={() => navigate('/jurisprudencia')}
          >
            <Scale className="h-4 w-4" />
            Buscar Jurisprudência
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
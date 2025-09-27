"use client";

import { useAuthStore } from '@/stores/auth-store';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText, Scale, Users, BookOpen } from 'lucide-react';

export default function HomePage() {
  const { user } = useAuthStore();

  if (user) {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto p-6">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-4">Assessor Jurídico</h1>
            <p className="text-xl text-muted-foreground">
              Sistema de geração de minutas para o Poder Judiciário
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-6 w-6" />
                  Minutas
                </CardTitle>
                <CardDescription>
                  Crie e gerencie suas minutas jurídicas
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button>Ver Minutas</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Scale className="h-6 w-6" />
                  Jurisprudência
                </CardTitle>
                <CardDescription>
                  Busque jurisprudência dos tribunais
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button>Buscar Jurisprudência</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-6 w-6" />
                  Unidades
                </CardTitle>
                <CardDescription>
                  Gerencie unidades judiciais
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button>Ver Unidades</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BookOpen className="h-6 w-6" />
                  Modelos
                </CardTitle>
                <CardDescription>
                  Modelos de documentos da unidade
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button>Ver Modelos</Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Assessor Jurídico</h1>
        <p className="text-xl text-muted-foreground mb-8">
          Sistema de geração de minutas para o Poder Judiciário
        </p>
        <div className="space-x-4">
          <Button size="lg">Fazer Login</Button>
          <Button variant="outline" size="lg">Cadastrar</Button>
        </div>
      </div>
    </div>
  );
}
"use client";

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { MinutaGenerator } from '@/components/MinutaGenerator';
import { CaseList } from '@/components/CaseList';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { FileText, List, Plus } from 'lucide-react';
import { useCases } from '@/hooks/useCases';
import { useCaseMinutas } from '@/hooks/useCases';

const Minutas = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('processos');
  const [selectedCase, setSelectedCase] = useState<string | null>(null);
  const { data: cases } = useCases('UNIT_ID');
  const { data: minutas } = useCaseMinutas(selectedCase || undefined);

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Minutas</h1>
        <极 className="text-muted-foreground">
          Crie e gerencie suas minutas jurídicas
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList>
          <TabsTrigger value="processos" className="flex items-center gap-2">
            <List className="h-4 w-4" />
            Processos
          </TabsTrigger>
          <TabsTrigger value="nova-minuta" className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            Nova Minuta
          </TabsTrigger>
          {selectedCase && (
            <TabsTrigger value="minutas-processo" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Minutas do Processo
            </TabsTrigger>
          )}
        </TabsList>

        <TabsContent value="processos">
          <CaseList unitId="UNIT_ID" />
        </TabsContent>

        <TabsContent value="nova-minuta">
          {selectedCase ? (
            <MinutaGenerator 
              caseId={selectedCase} 
              unitId="UNIT_ID"
              onMinutaCreated={() => setActiveTab('minutas-processo')}
            />
          ) : (
            <Card>
              <CardHeader>
                <CardTitle>Selecione um Processo</极Title>
                <CardDescription>
                  Escolha um processo para criar uma minuta
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {cases && cases.length > 0 ? (
                    cases.map((caseItem) => (
                      <div 
                        key={caseItem.id} 
                        className="border rounded-lg p-4 hover:bg-muted/50 transition-colors cursor-pointer"
                        onClick={() => {
                          setSelectedCase(caseItem.id);
                          setActiveTab('nova-minuta');
                        }}
                      >
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="font-semibold">{caseItem.numero}</h3>
                            <p className="text-sm text-muted-foreground">{caseItem.classe || 'Classe não informada'}</p>
                            <p className="text-sm text-muted-foreground">{caseItem.assunto || 'Assunto não informado'}</p>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      Nenhum processo encontrado. Crie um processo primeiro.
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="minutas-processo">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle>Minutas do Processo</CardTitle>
                  <CardDescription>
                    Minutas criadas para este processo
                  </CardDescription>
                </div>
                <Button onClick={() => setActiveTab('nova-minuta')}>
                  <Plus className="mr-2 h-4 w-4" />
                  Nova Minuta
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {minutas && minutas.length > 0 ? (
                <div className="space-y-4">
                  {minutas.map((minuta) => (
                    <div key={minuta.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-semibold">
                            {minuta.tipo_ato.charAt(0).toUpperCase() + minuta.tipo_ato.slice(1)}
                          </h3>
                          <p className="text-sm text-muted-foreground line-clamp-2">
                            {minuta.content_md.substring(0, 100)}...
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-muted-foreground">
                            Criado por {minuta.profiles?.first_name || 'Usuário'} {minuta.profiles?.last_name || ''}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            em {new Date(minuta.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text极uted-foreground">
                  Nenhuma minuta criada para este processo.
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Minutas;
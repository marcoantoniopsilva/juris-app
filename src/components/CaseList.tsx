"use client";

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useCases } from '@/hooks/useCases';
import { useCreateCase } from '@/hooks/useCases';
import { useToast } from '@/hooks/use-toast';
import { Plus, Search } from 'lucide-react';

interface CaseListProps {
  unitId: string;
}

export function CaseList({ unitId }: CaseListProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newCase, setNewCase] = useState({
    numero: '',
    classe: '',
    assunto: '',
  });
  
  const { data: cases, isLoading } = useCases(unitId);
  const { mutate: createCase, isPending } = useCreateCase();
  const { toast } = useToast();

  const filteredCases = cases?.filter(c => 
    c.numero.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.classe?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.assunto?.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  const handleCreateCase = () => {
    if (!newCase.numero.trim()) {
      toast({
        title: "Erro",
        description: "O número do processo é obrigatório.",
        variant: "destructive",
      });
      return;
    }

    createCase(
      {
        unit_id: unitId,
        ...newCase,
      },
      {
        onSuccess: () => {
          toast({
            title: "Sucesso",
            description: "Processo criado com sucesso!",
          });
          setNewCase({ numero: '', classe: '', assunto: '' });
          setShowCreateForm(false);
        },
        onError: (error) => {
          toast({
            title: "Erro",
            description: `Falha ao criar processo: ${error.message}`,
            variant: "destructive",
          });
        },
      }
    );
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>Processos</CardTitle>
              <CardDescription>
                Lista de processos da unidade
              </CardDescription>
            </div>
            <Button onClick={() => setShowCreateForm(!showCreateForm)}>
              <Plus className="mr-2 h-4 w-4" />
              Novo Processo
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {showCreateForm && (
            <div className="border rounded-lg p-4 space-y-4">
              <h3 className="font-medium">Criar Novo Processo</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="numero">Número do Processo *</Label>
                  <Input
                    id="numero"
                    placeholder="Ex: 1234567-89.2023.4.01.0000"
                    value={newCase.numero}
                    onChange={(e) => setNewCase({...newCase, numero: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="classe">Classe</Label>
                  <Input
                    id="classe"
                    placeholder="Ex: Ação Civil Pública"
                    value={newCase.classe}
                    onChange={(e) => setNewCase({...newCase, classe: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="assunto">Assunto</Label>
                  <Input
                    id="assunto"
                    placeholder="Ex: Meio Ambiente"
                    value={newCase.assunto}
                    onChange={(e) => setNewCase({...newCase, assunto: e.target.value})}
                  />
                </div>
              </div>
              <div className="flex space-x-2">
                <Button onClick={handleCreateCase} disabled={isPending}>
                  {isPending ? "Criando..." : "Criar Processo"}
                </Button>
                <Button variant="outline" onClick={() => setShowCreateForm(false)}>
                  Cancelar
                </Button>
              </div>
            </div>
          )}
          
          <div className="flex space-x-2">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Buscar processos..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8"
              />
            </div>
          </div>
          
          {isLoading ? (
            <div className="flex justify-center p-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            </div>
          ) : filteredCases.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              {searchTerm ? 'Nenhum processo encontrado.' : 'Nenhum processo cadastrado.'}
            </div>
          ) : (
            <div className="space-y-2">
              {filteredCases.map((caseItem) => (
                <div key={caseItem.id} className="border rounded-lg p-4 hover:bg-muted/50 transition-colors">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold">{caseItem.numero}</h3>
                      <p className="text-sm text-muted-foreground">{caseItem.classe || 'Classe não informada'}</p>
                      <p className="text-sm text-muted-foreground">{caseItem.assunto || 'Assunto não informado'}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-muted-foreground">
                        Criado em {new Date(caseItem.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
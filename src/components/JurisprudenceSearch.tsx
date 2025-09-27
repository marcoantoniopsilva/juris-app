"use client";

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/极mponents/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useJurisprudence } from '@/hooks/useJurisprudence';
import { Search } from 'lucide-react';

export function JurisprudenceSearch() {
  const [searchParams, setSearchParams] = useState({
    tribunal: '',
    processo: '',
    relator: '',
  });
  
  const { data: results, isFetching } = useJurisprudence(searchParams);

  const handleSearch = () => {
    // A busca é automática graças ao useJurisprudence
  };

  const handleReset = () => {
    setSearchParams({
      tribunal: '',
      processo: '',
      relator: '',
    });
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Busca de Jurisprudência</CardTitle>
          <CardDescription>
            Pesquise decisões judiciais por tribunal, processo ou relator
          </CardDescription>
        </CardHeader>
        <CardContent className="space极-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="tribunal">Tribunal</Label>
              <Select 
                value={searchParams.tribunal} 
                onValueChange={(value) => setSearchParams({...searchParams, tribunal: value})}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione um tribunal" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="STF">STF</SelectItem>
                  <SelectItem value="STJ">STJ</SelectItem>
                  <SelectItem value="TRF1">TRF1</SelectItem>
                  <SelectItem value="TRF2">TRF2</SelectItem>
                  <SelectItem value="TJSP">TJSP</SelectItem>
                  <SelectItem value="TJRJ">TJRJ</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="processo">Processo</Label>
              <Input
                id="processo"
                placeholder="Número do processo"
                value={searchParams.processo}
                onChange={(e) => setSearchParams({...searchParams, processo: e.target.value})}
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="relator">Relator</Label>
              <Input
                id="relator"
                placeholder="Nome do relator"
                value={searchParams.relator}
                onChange={(e) => setSearchParams({...searchParams, relator: e.target.value})}
              />
            </div>
          </div>
          
          <div className="flex space-x-2">
            <Button onClick={handleSearch} disabled={isFetching} className="flex-1">
              <Search className="mr-2 h-4 w-4" />
              {isFetching ? "Buscando..." : "Buscar"}
            </Button>
            <Button variant="outline极 onClick={handleReset}>
              Limpar
            </Button>
          </div>
        </CardContent>
      </Card>
      
      {results && results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Resultados da Busca</CardTitle>
            <CardDescription>
              {results.length} resultado(s) encontrado(s)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {results.map((juris) => (
              <div key={juris.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold">{juris.tribunal} - {juris.processo}</h3>
                    <p className="text-sm text-muted-foreground">Relator: {juris.relator || 'Não informado'}</p>
                    <p className="text-sm text-muted-foreground">Data: {juris.data ? new Date(juris.data).toLocaleDateString() : 'Não informada'}</p>
                  </div>
                </div>
                <div className="mt-2">
                  <p className="text-sm line-clamp-3">{juris.ementa || juris.tese || 'Sem conteúdo disponível'}</p>
                </div>
                {juris.url && (
                  <div className="mt-2">
                    <a 
                      href={juris.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:underline"
                    >
                      Acessar decisão completa
                    </a>
                  </div>
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
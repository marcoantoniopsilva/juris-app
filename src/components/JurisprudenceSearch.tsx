"use client";

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { jurisAPI } from '@/lib/api';
import { Search } from 'lucide-react';

interface JurisSearchProps {
  onSearchComplete?: (results: any[]) => void;
}

export function JurisprudenceSearch({ onSearchComplete }: JurisSearchProps) {
  const [searchParams, setSearchParams] = useState({
    query: '',
    tribunais: [] as string[],
    classes: [] as string[],
    assuntos: [] as string[],
    dataInicio: '',
    dataFim: ''
  });
  const [loading, setLoading] = useState(false);
  const [availableTribunals, setAvailableTribunals] = useState<string[]>([]);
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await jurisAPI.search(searchParams);
      const searchResults = response.data;
      setResults(searchResults);
      onSearchComplete?.(searchResults);
    } catch (error) {
      console.error('Erro na busca:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadTribunals = async () => {
    try {
      const response = await jurisAPI.getTribunals();
      setAvailableTribunals(response.data);
    } catch (error) {
      console.error('Erro ao carregar tribunais:', error);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Busca de Jurisprudência</CardTitle>
          <CardDescription>
            Busque jurisprudência nos tribunais brasileiros
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Input
              placeholder="Termos de busca..."
              value={searchParams.query}
              onChange={(e) => setSearchParams(prev => ({ ...prev, query: e.target.value }))}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select
              onValueChange={(value) => setSearchParams(prev => ({ 
                ...prev, 
                tribunais: value ? [value] : [] 
              }))}
              onOpenChange={loadTribunals}
            >
              <SelectTrigger>
                <SelectValue placeholder="Selecione o tribunal" />
              </SelectTrigger>
              <SelectContent>
                {availableTribunals.map(tribunal => (
                  <SelectItem key={tribunal} value={tribunal}>
                    {tribunal}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Input
              type="date"
              placeholder="Data início"
              value={searchParams.dataInicio}
              onChange={(e) => setSearchParams(prev => ({ ...prev, dataInicio: e.target.value }))}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              placeholder="Classes processuais"
              value={searchParams.classes.join(', ')}
              onChange={(e) => setSearchParams(prev => ({ 
                ...prev, 
                classes: e.target.value.split(',').map(c => c.trim()).filter(Boolean)
              }))}
            />

            <Input
              type="date"
              placeholder="Data fim"
              value={searchParams.dataFim}
              onChange={(e) => setSearchParams(prev => ({ ...prev, dataFim: e.target.value }))}
            />
          </div>

          <Button 
            onClick={handleSearch} 
            disabled={loading || !searchParams.query}
            className="w-full"
          >
            {loading ? 'Buscando...' : 'Buscar Jurisprudência'}
          </Button>
        </CardContent>
      </Card>

      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Resultados da Busca</CardTitle>
            <CardDescription>
              {results.length} resultado(s) encontrado(s)
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {results.slice(0, 5).map((juris) => (
              <div key={juris.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-semibold">{juris.tribunal} - {juris.processo}</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                      {juris.ementa}
                    </p>
                    <p className="text-xs text-muted-foreground mt-2">
                      Relator: {juris.relator} • Data: {juris.data}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
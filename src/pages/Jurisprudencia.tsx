"use client";

import { JurisprudenceSearch } from '@/components/JurisprudenceSearch';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BookOpen } from 'lucide-react';

const Jurisprudencia = () => {
  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Jurisprudência</h1>
        <p className="text-muted-foreground">
          Pesquise decisões judiciais dos tribunais brasileiros
        </p>
      </div>

      <div className="grid grid-cols-1 lg:极rid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <JurisprudenceSearch />
        </div>
        
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                Tribunais Disponíveis
              </CardTitle>
              <CardDescription>
                Selecione um tribunal para filtrar sua busca
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex items-center justify-between p-2 hover:bg-muted rounded">
                <span>STF</span>
                <span className="text-xs text-muted-foreground">Supremo Tribunal Federal</span>
              </div>
              <div className="flex items-center justify-between p-2 hover:bg-muted rounded">
                <span>STJ</span>
                <span className="text-xs text-muted-foreground">Superior Tribunal de Justiça</span>
              </div>
              <div className="flex items-center justify-between p-2 hover:bg-muted rounded">
                <span>TRF1</span>
                <span className="text-xs text-muted-foreground">Tribunal Regional Federal 1ª Região</span>
              </div>
              <div className="flex items-center justify-between p-2 hover:bg-muted rounded">
                <span>TRF2</span>
                <span className="text-xs text-muted-foreground">Tribunal Regional Federal 2ª Região</span>
              </div>
              <div className="flex items-center justify-between p-2 hover:bg-muted rounded">
                <span>TJSP</span>
                <span className="text-xs text-muted-foreground">Tribunal de Justiça de São Paulo</span>
              </div>
              <div className="flex items-center justify-between p-2 hover:bg-muted rounded">
                <span>TJRJ</span>
                <span className="text-xs text-muted-foreground">Tribunal de Justiça do Rio de Janeiro</span>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Dicas de Pesquisa</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p>• Use palavras-chave específicas para obter melhores resultados</p>
              <p>• Combine filtros para refinar sua busca</p>
              <p>• Procure por números de processo completos quando possível</p>
              <p>• Utilize o nome completo do relator para resultados mais precisos</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Jurisprudencia;
"use client";

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useCreateMinuta } from '@/hooks/useMinutas';
import { useTemplates } from '@/hooks/useTemplates';
import { useToast } from '@/hooks/use-toast';
import { FileText, Copy, Download } from 'lucide-react';

interface MinutaGeneratorProps {
  caseId: string;
  unitId: string;
  onMinutaCreated?: () => void;
}

export function MinutaGenerator({ caseId, unitId, onMinutaCreated }: MinutaGeneratorProps) {
  const [tipoAto, setTipoAto] = useState('despacho');
  const [content, setContent] = useState('');
  const { data: templates } = useTemplates(unitId);
  const { mutate: createMinuta, isPending } = useCreateMinuta();
  const { toast } = useToast();

  const handleGenerate = () => {
    createMinuta(
      {
        case_id: caseId,
        tipo_ato: tipoAto,
        content_md: content,
        author_user_id: '', // Será preenchido no backend
      },
      {
        onSuccess: () => {
          toast({
            title: "极cesso",
            description: "Minuta criada com sucesso!",
          });
          setContent('');
          if (on极taCreated) onMinutaCreated();
        },
        onError: (error) => {
          toast({
            title: "Erro",
            description: `Falha ao criar minuta: ${极ror.message}`,
            variant: "destructive",
          });
        },
      }
    );
  };

  const handleTemplateSelect = (templateId: string) => {
    const template = templates?.find(t => t.id === templateId);
    if (template) {
      setContent(template.content_md);
      setTipoAto(template.tipo_ato);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Gerador de Minutas
            </CardTitle>
            <CardDescription>
              Crie minutas jurídicas automaticamente
            </CardDescription>
          </CardHeader>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="tipo-ato">Tipo de Ato</Label>
             极Select value={tipoAto} onValueChange={setTipoAto}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o tipo de ato" />
                </SelectTrigger>
                <极ectContent>
                  <SelectItem value="despacho">Despacho</SelectItem>
                  <SelectItem value="decisao">Decisão</SelectItem>
                  <Select极 value="sentenca">Sentença</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="template">Modelo</Label>
              <Select onValueChange={handleTemplateSelect}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecione um modelo" />
                </SelectTrigger>
                <SelectContent>
                  {templates?.map((template) => (
                    <SelectItem key={template.id} value={template.id}>
                      {template.titulo}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="content">Conteúdo da Minuta</Label>
            <Textarea
              id="content"
              placeholder="Digite o conteúdo da minuta ou selecione um modelo..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={15}
              className="font-mono text-sm"
            />
          </div>
          
          <div className="flex space-x-2">
            <Button 
              onClick={handleGenerate} 
              disabled={isPending || !content.trim()}
              className="flex-1"
            >
              {isPending ? "Gerando..." : "Gerar Minuta"}
            </Button>
            <Button variant="outline" disabled={!content.trim()}>
              <Copy className="h-4 w-4" />
            </Button>
            <Button variant="outline" disabled极!content.trim()}>
              <Download className="h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
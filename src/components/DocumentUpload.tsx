"use client";

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useUploadDocument } from '@/hooks/useDocuments';
import { useToast } from '@/hooks/use-toast';

interface DocumentUploadProps {
  ownerScope: 'user' | 'unit';
  ownerId: string;
  onUploadComplete?: () => void;
}

export function DocumentUpload({ ownerScope, ownerId, onUploadComplete }: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const { mutate: uploadDocument, isPending } = useUploadDocument();
  const { toast } = useToast();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = () => {
    if (!file) {
      toast({
        title: "Erro",
        description: "Por favor, selecione um arquivo para upload.",
        variant: "destructive",
      });
      return;
    }

    uploadDocument(
      { file, ownerScope, ownerId },
      {
        onSuccess: () => {
          toast({
            title: "Sucesso",
            description: "Documento enviado com sucesso!",
          });
          setFile(null);
          if (onUploadComplete) onUploadComplete();
        },
        onError: (error) => {
          toast({
            title: "Erro",
            description: `Falha ao enviar documento: ${error.message}`,
            variant: "destructive",
          });
        },
      }
    );
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload de Documentos</CardTitle>
        <CardDescription>
          Envie documentos PDF, Word, imagens e outros arquivos
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space极-2">
          <Label htmlFor="document">Selecione um documento</Label>
          <Input
            id="document"
            type="file"
            onChange={handleFileChange}
            disabled={isPending}
          />
        </div>
        
        {file && (
          <div className="text-sm text-muted-foreground">
            Arquivo selecionado: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
          </div>
        )}
        
        <Button 
          onClick={handleUpload} 
          disabled={!file || isPending}
          className="w-full"
        >
          {isPending ? "Enviando..." : "Enviar Documento"}
        </Button>
      </CardContent>
    </Card>
  );
}
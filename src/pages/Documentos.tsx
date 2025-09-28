"use client";

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { DocumentUpload } from '@/components/DocumentUpload';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { FileText, User, Building } from 'lucide-react';
import { useDocuments } from '@/hooks/useDocuments';

const Documentos = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('meus-documentos');
  const { data: userDocuments, isLoading: userDocsLoading } = useDocuments('user', user?.id || '');
  const { data: unitDocuments, isLoading: unitDocsLoading } = useDocuments('unit', 'UNIT_ID'); // Substituir por ID real da unidade

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Documentos</h1>
        <p className="text-muted-foreground">
          Gerencie seus documentos e os da sua unidade
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList>
          <TabsTrigger value="meus-documentos" className="flex items-center gap-2">
            <User className="h-4 w-4" />
            Meus Documentos
          </TabsTrigger>
          <TabsTrigger value="documentos-unidade" className="flex items-center gap-2">
            <Building className="h-4 w-4" />
            Documentos da Unidade
          </TabsTrigger>
          <TabsTrigger value="upload" className="flex items-center gap-2">
            <FileText className="h-4 w-4" />
            Upload
          </TabsTrigger>
        </TabsList>

        <TabsContent value="meus-documentos">
          <Card>
            <CardHeader>
              <CardTitle>Meus Documentos</CardTitle>
              <CardDescription>
                Documentos enviados por você
              </CardDescription>
            </CardHeader>
            <CardContent>
              {userDocsLoading ? (
                <div className="flex justify-center p-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                </div>
              ) : userDocuments && userDocuments.length > 0 ? (
                <div className="space-y-4">
                  {userDocuments.map((doc) => (
                    <div key={doc.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-semibold">{doc.filename}</h3>
                          <p className="text-sm text-muted-foreground">
                            Tipo: {doc.content_type} | Tamanho: {doc.metadata?.size ? `${(doc.metadata.size / 1024 / 1024).toFixed(2)} MB` : 'N/A'}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-muted-foreground">
                            Enviado em {new Date(doc.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  Nenhum documento encontrado.
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="documentos-unidade">
          <Card>
            <CardHeader>
              <CardTitle>Documentos da Unidade</CardTitle>
              <CardDescription>
                Documentos compartilhados com sua unidade
              </CardDescription>
            </CardHeader>
            <CardContent>
              {unitDocsLoading ? (
                <div className="flex justify-center p-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                </div>
              ) : unitDocuments && unitDocuments.length > 0 ? (
                <div className="space-y-4">
                  {unitDocuments.map((doc) => (
                    <div key={doc.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-semibold">{doc.filename}</h3>
                          <p className="text-sm text-muted-foreground">
                            Tipo: {doc.content_type} | Tamanho: {doc.metadata?.size ? `${(doc.metadata.size / 1024 / 1024).toFixed(2)} MB` : 'N/A'}
                          </极>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-muted-foreground">
                            Enviado em {new Date(doc.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  Nenhum documento encontrado.
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="upload">
          <DocumentUpload 
            ownerScope="user" 
            ownerId={user?.id || ''} 
            onUploadComplete={() => {
              // Refresh documents
            }} 
          />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Documentos;
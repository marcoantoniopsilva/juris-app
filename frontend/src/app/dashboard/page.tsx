"use client";

import { useState, useEffect } from 'react'
import { useAuthStore } from '@/stores/auth-store'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { DocumentUpload } from '@/components/document-upload'
import { JurisSearch } from '@/components/juris-search'
import { MinutaGenerator } from '@/components/minuta-generator'
import { FileText, Scale, Users, BookOpen, Upload } from 'lucide-react'

export default function DashboardPage() {
  const { user, currentUnit } = useAuthStore()
  const [activeTab, setActiveTab] = useState('overview')
  const [jurisResults, setJurisResults] = useState<any[]>([])
  const [generatedMinuta, setGeneratedMinuta] = useState<any>(null)

  if (!user) {
    return <div>Carregando...</div>
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
          <p className="text-muted-foreground">
            Bem-vindo, {user.name} ({user.role})
          </p>
        </div>

        <div className="flex space-x-4 mb-6">
          <Button
            variant={activeTab === 'overview' ? 'default' : 'outline'}
            onClick={() => setActiveTab('overview')}
          >
            Visão Geral
          </Button>
          <Button
            variant={activeTab === 'upload' ? 'default' : 'outline'}
            onClick={() => setActiveTab('upload')}
          >
            Upload
          </Button>
          <Button
            variant={activeTab === 'juris' ? 'default' : 'outline'}
            onClick={() => setActiveTab('juris')}
          >
            Jurisprudência
          </Button>
          <Button
            variant={activeTab === 'minutas' ? 'default' : 'outline'}
            onClick={() => setActiveTab('minutas')}
          >
            Minutas
          </Button>
        </div>

        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="h-6 w-6" />
                  Uploads
                </CardTitle>
                <CardDescription>Documentos enviados</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold">0</p>
                <Button variant="outline" size="sm" className="mt-2">
                  Ver Uploads
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Scale className="h-6 w-6" />
                  Jurisprudência
                </CardTitle>
                <CardDescription>Precedentes encontrados</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold">0</p>
                <Button variant="outline" size="sm" className="mt-2">
                  Buscar
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-6 w-6" />
                  Minutas
                </CardTitle>
                <CardDescription>Minutas geradas</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-bold">0</p>
                <Button variant="outline" size="sm" className="mt-2">
                  Gerar
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-6 w-6" />
                  Unidade
                </CardTitle>
                <CardDescription>Unidade atual</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  {currentUnit || 'Nenhuma unidade selecionada'}
                </p>
                <Button variant="outline" size="sm" className="mt-2">
                  Gerenciar
                </Button>
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'upload' && (
          <div className="grid grid-cols-1 gap-6">
            <DocumentUpload
              ownerScope="user"
              ownerId={user.id}
              onUploadComplete={() => console.log('Upload completo')}
            />
          </div>
        )}

        {activeTab === 'juris' && (
          <div className="grid grid-cols-1 gap-6">
            <JurisSearch onSearchComplete={setJurisResults} />
            
            {jurisResults.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Resultados da Busca</CardTitle>
                  <CardDescription>
                    {jurisResults.length} resultado(s) encontrado(s)
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {jurisResults.slice(0, 5).map((result, index) => (
                      <div key={index} className="border rounded-md p-4">
                        <h4 className="font-semibold">{result.tribunal} - {result.processo}</h4>
                        <p className="text-sm text-muted-foreground mt-1">
                          {result.ementa}
                        </p>
                        <p className="text-xs text-muted-foreground mt-2">
                          Relator: {result.relator} • Data: {result.data}
                        </p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {activeTab === 'minutas' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <MinutaGenerator
              caseId="exemplo-case-id"
              onGenerationComplete={setGeneratedMinuta}
            />
            
            {generatedMinuta && (
              <Card>
                <CardHeader>
                  <CardTitle>Minuta Gerada</CardTitle>
                  <CardDescription>
                    Visualize e edite a minuta gerada
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-sm max-w-none">
                    <pre className="whitespace-pre-wrap text-sm">
                      {generatedMinuta.content_md}
                    </pre>
                  </div>
                  <Button className="mt-4">Exportar DOCX</Button>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
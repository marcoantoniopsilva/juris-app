"use client";

import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Upload, FileText, X } from 'lucide-react'
import { documentsAPI } from '@/lib/api'

interface DocumentUploadProps {
  ownerScope: 'user' | 'unit'
  ownerId: string
  onUploadComplete?: () => void
}

export function DocumentUpload({ ownerScope, ownerId, onUploadComplete }: DocumentUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [files, setFiles] = useState<File[]>([])

  const onDrop = (acceptedFiles: File[]) => {
    setFiles(prev => [...prev, ...acceptedFiles])
  }

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index))
  }

  const uploadFiles = async () => {
    setUploading(true)
    setProgress(0)

    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      try {
        await documentsAPI.upload(file, ownerScope, ownerId)
        setProgress(((i + 1) / files.length) * 100)
      } catch (error) {
        console.error('Erro ao fazer upload:', error)
      }
    }

    setUploading(false)
    setFiles([])
    setProgress(0)
    onUploadComplete?.()
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: true,
    disabled: uploading
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload de Documentos</CardTitle>
        <CardDescription>
          Faça upload de PDFs, documentos Word, planilhas e outros arquivos
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive ? 'border-primary bg-primary/10' : 'border-muted-foreground/25'
          } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <input {...getInputProps()} />
          <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <p className="text-sm text-muted-foreground mb-2">
            {isDragActive ? 'Solte os arquivos aqui...' : 'Arraste arquivos ou clique para selecionar'}
          </p>
          <p className="text-xs text-muted-foreground">
            PDF, DOCX, TXT, XLSX, imagens, áudio e vídeo
          </p>
        </div>

        {files.length > 0 && (
          <div className="mt-6">
            <h4 className="text-sm font-medium mb-2">Arquivos selecionados:</h4>
            <div className="space-y-2">
              {files.map((file, index) => (
                <div key={index} className="flex items-center justify-between p-3 border rounded-md">
                  <div className="flex items-center">
                    <FileText className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span className="text-sm">{file.name}</span>
                    <span className="text-xs text-muted-foreground ml-2">
                      ({(file.size / 1024 / 1024).toFixed(2)} MB)
                    </span>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeFile(index)}
                    disabled={uploading}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>

            {uploading && (
              <div className="mt-4">
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Upload em progresso: {Math.round(progress)}%
                </p>
              </div>
            )}

            <Button
              className="mt-4 w-full"
              onClick={uploadFiles}
              disabled={uploading || files.length === 0}
            >
              {uploading ? 'Fazendo upload...' : `Upload de ${files.length} arquivo(s)`}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
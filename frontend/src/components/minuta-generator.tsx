"use client";

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { draftsAPI } from '@/lib/api'

interface MinutaGeneratorProps {
  caseId: string
  onGenerationComplete?: (minuta: any) => void
}

export function MinutaGenerator({ caseId, onGenerationComplete }: MinutaGeneratorProps) {
  const [generationParams, setGenerationParams] = useState({
    tipo_ato: 'despacho' as 'despacho' | 'decisao' | 'sentenca',
    instrucoes: '',
    usar_modelos_unidade: true,
    buscar_jurisprudencia: true
  })
  const [generating, setGenerating] = useState(false)

  const handleGenerate = async () => {
    setGenerating(true)
    try {
      const response = await draftsAPI.generate({
        case_id: caseId,
        ...generationParams
      })
      onGenerationComplete?.(response.data)
    } catch (error) {
      console.error('Erro na geração:', error)
    } finally {
      setGenerating(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Gerar Minuta</CardTitle>
        <CardDescription>
          Gere minutas jurídicas automaticamente
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Select
            value={generationParams.tipo_ato}
            onValueChange={(value: any) => setGenerationParams(prev => ({ 
              ...prev, 
              tipo_ato: value 
            }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="Tipo de ato" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="despacho">Despacho</SelectItem>
              <SelectItem value="decisao">Decisão</SelectItem>
              <SelectItem value="sentenca">Sentença</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <textarea
            placeholder="Instruções específicas (opcional)"
            value={generationParams.instrucoes}
            onChange={(e) => setGenerationParams(prev => ({ 
              ...prev, 
              instrucoes: e.target.value 
            }))}
            className="w-full p-3 border rounded-md text-sm"
            rows={3}
          />
        </div>

        <div className="space-y-2">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={generationParams.usar_modelos_unidade}
              onChange={(e) => setGenerationParams(prev => ({ 
                ...prev, 
                usar_modelos_unidade: e.target.checked 
              }))}
              className="mr-2"
            />
            Usar modelos da unidade
          </label>
          
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={generationParams.buscar_jurisprudencia}
              onChange={(e) => setGenerationParams(prev => ({ 
                ...prev, 
                buscar_jurisprudencia: e.target.checked 
              }))}
              className="mr-2"
            />
            Buscar jurisprudência
          </label>
        </div>

        <Button 
          onClick={handleGenerate} 
          disabled={generating}
          className="w-full"
        >
          {generating ? 'Gerando...' : 'Gerar Minuta'}
        </Button>
      </CardContent>
    </Card>
  )
}
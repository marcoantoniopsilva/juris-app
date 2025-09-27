"use client";

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { jurisAPI } from '@/lib/api'

interface JurisSearchProps {
  onSearchComplete?: (results: any[]) => void
}

export function JurisSearch({ onSearchComplete }: JurisSearchProps) {
  const [searchParams, setSearchParams] = useState({
    query: '',
    tribunais: [] as string[],
    classes: [] as string[],
    assuntos: [] as string[],
    dataInicio: '',
    dataFim: ''
  })
  const [loading, setLoading] = useState(false)
  const [availableTribunals, setAvailableTribunals] = useState<string[]>([])

  const handleSearch = async () => {
    setLoading(true)
    try {
      const response = await jurisAPI.search(searchParams)
      onSearchComplete?.(response.data)
    } catch (error) {
      console.error('Erro na busca:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadTribunals = async () => {
    try {
      const response = await jurisAPI.getTribunals()
      setAvailableTribunals(response.data)
    } catch (error) {
      console.error('Erro ao carregar tribunais:', error)
    }
  }

  return (
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
  )
}
#!/bin/bash

echo "🚀 Iniciando aplicação Jurídico..."

# Verificar se as dependências estão instaladas
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências..."
    
    # Tentar instalar com npm
    if command -v npm &> /dev/null; then
        npm install
    else
        echo "❌ npm não encontrado. Por favor, instale o Node.js primeiro."
        echo "💡 Execute: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs npm"
        exit 1
    fi
fi

echo "✅ Dependências instaladas"
echo "🌐 Iniciando servidor de desenvolvimento..."

# Iniciar o servidor Vite
if command -v npm &> /dev/null; then
    npm run dev
else
    echo "❌ npm não encontrado. Não foi possível iniciar a aplicação."
    exit 1
fi
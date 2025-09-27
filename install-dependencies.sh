#!/bin/bash

# Script para instalar Node.js e dependências do projeto

echo "🚀 Iniciando instalação do Node.js e dependências..."

# Verificar se o Node.js já está instalado
if ! command -v node &> /dev/null; then
    echo "📦 Instalando Node.js..."
    
    # Instalar Node.js (método universal)
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    
    echo "✅ Node.js instalado"
else
    echo "✅ Node.js já está instalado: $(node --version)"
fi

# Verificar se npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado. Instalando..."
    sudo apt-get install -y npm
    echo "✅ npm instalado"
else
    echo "✅ npm já está instalado: $(npm --version)"
fi

# Instalar dependências do projeto
echo "📦 Instalando dependências do projeto..."
npm install

echo "✅ Todas as dependências instaladas com sucesso!"
echo "🎉 Agora você pode executar: npm run dev"
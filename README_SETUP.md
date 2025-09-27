# 🚀 Setup da Aplicação Jurídico

## Pré-requisitos
- Sistema Linux/Unix (Ubuntu, Debian, etc.)
- Acesso sudo para instalação de pacotes

## 📋 Passo a Passo

### 1. Instalar Node.js e npm (se não tiver)
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verificar instalação
node --version
npm --version
```

### 2. Instalar dependências do projeto
```bash
# Dar permissão e executar script de instalação
chmod +x install-dependencies.sh
./install-dependencies.sh

# Ou instalar manualmente
npm install
```

### 3. Iniciar a aplicação
```bash
# Método 1: Usando npm diretamente
npm run dev

# Método 2: Usando script alternativo
chmod +x start-app.sh
./start-app.sh
```

### 4. Acessar a aplicação
Abra seu navegador e vá para: http://localhost:5173

## 🐛 Solução de Problemas

### Se npm não for encontrado:
```bash
# Instalar npm separadamente
sudo apt install -y npm
```

### Se houver erro de permissão:
```bash
# Corrigir permissões do npm
sudo chown -R $USER:$USER ~/.npm
sudo chown -R $USER:$USER node_modules
```

### Se a porta 5173 estiver ocupada:
Edite o arquivo `vite.config.ts` e mude a porta:
```ts
server: {
    host: "0.0.0.0",
    port: 3000,  // ou outra porta disponível
},
```

## 📦 Estrutura do Projeto
```
juridico-app/
├── src/                 # Código fonte
├── node_modules/        # Dependências (gerado automaticamente)
├── package.json         # Configuração do projeto
├── vite.config.ts       # Configuração do Vite
├── tailwind.config.js   # Configuração do Tailwind
└── index.html          # Página principal
```

## 🆘 Suporte
Se encontrar problemas, verifique:
1. Node.js versão 18+ está instalado
2. npm está disponível no PATH
3. Todas as dependências foram instaladas
4. Não há conflitos de porta

Execute `node --version` e `npm --version` para verificar as instalações.
# 🛒 Achadinhos da Shopee - Arquitetura Serverless & Edge Database

## 📌 Visão Geral
Plataforma de catálogo de ofertas e afiliados da Shopee, projetada para escalar para milhões de produtos sem sobrecarregar o hardware local. A arquitetura foi migrada de um servidor monolítico local (Termux/SQLite) para uma arquitetura Cloud-Native (Serverless + Edge Database), garantindo alta disponibilidade, resiliência e baixa latência.

## 🏗️ Arquitetura e Stack Tecnológico
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (hospedagem estática).
- **Backend/API:** Node.js com Express.
- **Banco de Dados:** Turso (LibSQL/SQLite na nuvem) com 10+ milhões de registros.
- **Hospedagem Backend:** Render (Serverless).
- **Infraestrutura Local de Desenvolvimento (Legado):** Termux/Android, Nginx, Cloudflare Tunnel.

## ⚙️ Principais Soluções de Engenharia Implementadas
1. **Migração de Banco de Dados (Edge Computing):** Transição de um arquivo JSON/SQLite local (que estourava a RAM do dispositivo) para o Turso Cloud. A API agora realiza consultas HTTP otimizadas diretamente na borda da AWS.
2. **Proteção contra OOM (Out of Memory):** O servidor Node.js não carrega mais o catálogo inteiro na memória. O uso de SQL com `LIMIT` e `OFFSET` reduziu o consumo de RAM do servidor para menos de 50MB.
3. **SEO Técnico e Redirecionamento 301:** Implementação de regras de redirecionamento permanente (301) via Nginx e Middleware no Node.js. Links antigos estáticos (`/ofertas/nome-do-produto-ID.html`) são automaticamente convertidos para a nova rota dinâmica (`/produto.html?id=ID`), salvando a autoridade do domínio e evitando erros 404.
4. **Segurança (AppSec):**
   - Implementação de `.gitignore` rigoroso para não expor arquivos `.env`.
   - Configuração no Nginx para bloquear *scanners de vulnerabilidade* (tentativas de acesso a `.env`, `.git`, `.aws`, credenciais de nuvem).
   - Uso de `rel="sponsored noopener"` em todos os links de afiliados, em conformidade com as diretrizes do Google.

## 🚀 Como Executar o Projeto (Ambiente de Desenvolvimento)
1. Clone o repositório.
2. Instale as dependências: `npm install` (dentro da pasta `backend`).
3. Crie um arquivo `.env` na raiz do backend e adicione suas credenciais (conforme `.env.example`).
4. Inicie o servidor: `node server.js` (ou `npm start`).

## ☁️ Deploy em Produção (Render)
- **Root Directory:** `backend`
- **Build Command:** `npm install`
- **Start Command:** `node server.js`
- As variáveis de ambiente (`TURSO_DATABASE_URL` e `TURSO_AUTH_TOKEN`) devem ser configuradas diretamente no painel do Render.

## 🛡️ Segurança e Boas Práticas
- **Nunca** suba o arquivo `.env` para o controle de versão.
- O banco de dados conta com autenticação via Token Bearer (Turso).
- Frontend otimizado para não expor a chave de API do banco.

---
*Documentação gerada por Ana Caroline Lamas - Arquiteta de Soluções Cloud & IA.*

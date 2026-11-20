<p align="center"><img src="assets/banner.svg" alt="Loja da Shopee — catálogo afiliado com Node.js, Turso e scripts de dados" width="100%"></p>

# Loja da Shopee — catálogo de ofertas afiliadas com Node.js, Turso e scripts de dados

Versão de deploy do site **Os Achadinhos da Shopee**, migrada de um servidor local (Termux + SQLite) para uma arquitetura em nuvem: front-end estático, API em **Node.js (Express)** hospedada no **Render** e banco **Turso** (libSQL/SQLite). Inclui também os **scripts Python** usados para coletar, converter e processar o catálogo de produtos.

## Recursos

- **API do catálogo** com consultas paginadas (`LIMIT`/`OFFSET`), sem carregar o catálogo inteiro na memória: `/api/catalogo`, `/api/produto/:id` e `/api/admin/stats`.
- **Sitemaps dinâmicos** e **redirecionamentos 301** de URLs antigas (`/ofertas/...-ID.html` → `/produto.html?id=ID`), no Node.js e no Nginx.
- **Front-end**: início, recomendações, produto, painel, termos, privacidade e cookies, com `rel="sponsored noopener"` nos links de afiliado.
- **Nginx** (`config/nginx.conf`) com bloqueio de varreduras por `.env`, `.git`, `.aws` e credenciais.
- **Pipeline de dados** em `backend/`:
  - coleta por categoria na API de afiliados (`worker-categorias.js`, `loop_garimpo_33min.py`);
  - criação e conversão de banco (`criar_banco.py`, `converter_sqlite.py`, `converter_real.py`) e divisão em partes (`fatiar_banco.py`);
  - enriquecimento de títulos e hashtags por sinônimos (`enriquecer_produtos.py`);
  - scripts `multiplicar_*.py`, que geram variações de título (sufixos como "Promoção" ou "Frete Grátis") com IDs `_V1…_Vn` a partir da base de cerca de 63 mil produtos.
- **Arquivos de dados** versionados: base do catálogo (`catalogo_63k_original.json`, `produtos_base.json`), backups e lotes de coleta.

## Instalação

Requisitos: **Node.js 20+**, **Python 3** (para os scripts) e um banco **Turso**.

```bash
git clone https://github.com/ticarollamas-arch/loja-da-shopee-deploy.git
cd loja-da-shopee-deploy/backend
npm install
cp .env.example .env      # TURSO_DATABASE_URL e TURSO_AUTH_TOKEN
```

## Como usar

```bash
npm start                         # API Express
python3 criar_banco.py            # exemplo: gera o banco SQLite local a partir do JSON
```

**Deploy no Render**: *Root Directory* `backend`, build `npm install`, start `node server.js`, com `TURSO_DATABASE_URL` e `TURSO_AUTH_TOKEN` configurados no painel.

## Observações

- Variações de título geradas a partir do mesmo produto tendem a ser tratadas pelos buscadores como **conteúdo duplicado**. Avalie o impacto em SEO antes de indexar o catálogo multiplicado.
- Os JSONs de catálogo somam dezenas de MB no repositório.
- `backend/limpar_celular.sh` é um utilitário à parte, para remover aplicativos pré-instalados de um celular Samsung via `rish`, sem relação com o site.
- Na raiz há um `package.json` e uma pasta `src/` de exemplo (Vite), que não fazem parte do deploy.

## Tecnologias

Node.js · Express · Turso (libSQL) · Python 3 · SQLite · HTML/CSS/JavaScript · Nginx · Render · Termux · Cloudflare Tunnel

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE). Marcas citadas pertencem aos seus titulares.

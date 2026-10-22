require('dotenv').config();
const express = require('express');
const { createClient } = require('@tursodatabase/serverless/compat');
const app = express();
const PORT = process.env.PORT || 3001;

const db = createClient({
  url: process.env.TURSO_DATABASE_URL,
  authToken: process.env.TURSO_AUTH_TOKEN,
});

app.use((req, res, next) => {
    res.setHeader('Cache-Control', 'no-store');
    next();
});

app.get('/api/catalogo', async (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const offset = (page - 1) * limit;
    const cat = req.query.cat;
    const q = req.query.q;

    let query = 'SELECT * FROM produtos';
    let params = [];
    let conditions = [];

    if (cat && cat !== 'Todos') { conditions.push('categoria = ?'); params.push(cat); }
    if (q) { conditions.push('titulo LIKE ?'); params.push(`%${q}%`); }
    if (conditions.length > 0) { query += ' WHERE ' + conditions.join(' AND '); }
    
    query += ' LIMIT ? OFFSET ?';
    params.push(limit, offset);

    try {
        const result = await db.execute({ sql: query, args: params });
        const formatado = result.rows.map(p => ({
            itemId: p.id, titulo: p.titulo, preco: p.preco, imagem: p.imagem, link_afiliado: p.link, categoria: p.categoria, hashtags: p.hashtags
        }));
        res.json(formatado);
    } catch (e) { res.status(500).json({ error: e.message }); }
});

app.get('/api/produto/:id', async (req, res) => {
    try {
        const result = await db.execute({
            sql: 'SELECT * FROM produtos WHERE id = ?',
            args: [req.params.id]
        });
        const p = result.rows[0];
        if (p) res.json({ itemId: p.id, titulo: p.titulo, preco: p.preco, imagem: p.imagem, link_afiliado: p.link, categoria: p.categoria, hashtags: p.hashtags });
        else res.status(404).json({ error: "Produto não encontrado" });
    } catch (e) { res.status(500).json({ error: e.message }); }
});

app.get('/api/admin/stats', async (req, res) => {
    try {
        const result = await db.execute('SELECT count(*) as total FROM produtos');
        res.json({ total: result.rows[0].total });
    } catch (e) { res.status(500).json({ error: e.message }); }
});

app.listen(PORT, () => console.log(`🚀 API Nuvem (Turso Serverless) rodando na porta ${PORT}!`));

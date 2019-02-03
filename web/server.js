const Q = require('q');
const express = require('express');
	const bodyParser = require('body-parser');
const { Pool } = require('pg');
	const pool = new Pool({
		host: 'localhost',
		user: 'nl',
		password: null,
		database: 'logbase'
	});

app = express();
app.use(bodyParser.json());

app.get('/', (req, res, next) => {
	pool.connect().then(psql => psql.query('SELECT name, date FROM documents;').then(({ rows }) => res.send(rows[0].name)));
})
app.get('/:docid(\\d+)', (req, res, next) => {
	pool.connect().then(psql => {
		psql.query('SELECT string_agg(s.body, ". ") AS body FROM sentences s INNER JOIN documents d ON d.id = $1;', [req.params.docid])
		    .then(({ rows }) => res.send(rows[0].body))
	});
});
app.post('/', (req, res, next) => {
	pool.connect().then(psql => {
		(req.query.docid != null ?
			psql.query('SELECT id FROM documents WHERE id = $1;', [req.query.docid]) :
			Q(null)
		).then(id => {
			if(id == null)
				return psql.query('INSERT INTO documents (name) VALUES ($1) RETURNING id;', [req.query.name]).then(({ rows }) => rows[0].name);
			else
				return id;
		})
			.then(id => psql.query('SELECT body, pos FROM sentences s WHERE parent = $1 ORDER BY s.pos ASC;', [id]))
			.then(({ rows }) => {
				const sentences = req.query.body.split(/[^\w]*\.\.?[^\w]*/);
				const matches = [];
				for(let row_id = 0; row_id < rows.length; row_id++) {
					for(const sid = 0; sid < sentences.length; sid++) {
						if(rows[row_id] === sentences[sid])
							matches.push([sid, row_id]);
					}
				}
				let midx = 0;
				for(let i = 0; i < sentences.length; i++) {
					while(matches.length > midx && matches[midx][0] < i)
						midx++;
					if(matches.length === midx)
						pos = rows[matches[midx][0]].pos + i - matches[midx][1];
					psql.query('INSERT INTO ')
				}
			});
	});
});
app.post('/search', (req, res, next) => {
	
})
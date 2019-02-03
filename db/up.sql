CREATE TABLE documents (
	id SERIAL PRIMARY KEY,
	d TIMESTAMP DEFAULT NOW()
);
CREATE TABLE sentences (
	id SERIAL PRIMARY KEY,
	parent INT,
	FOREIGN KEY ("parent") REFERENCES documents("id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX ON sentences("parent");
CREATE TABLE concepts ( id SERIAL PRIMARY KEY,
	parent INT NOT NULL,
	FOREIGN KEY ("parent") REFERENCES documents("id") ON UPDATE CASCADE ON DELETE CASCADE );
CREATE INDEX ON concepts("parent");
CREATE TABLE concept_graph ( a INT, b INT,
	FOREIGN KEY ("a") REFERENCES concepts("id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY ("b") REFERENCES concepts("id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX ON concept_graph("a");
CREATE INDEX ON concept_graph("b");
CREATE TABLE entities (
	id SERIAL PRIMARY KEY,
	doc_parent INT NOT NULL,
	entity_parent INT,
	concept INT,
	FOREIGN KEY ("doc_parent") REFERENCES documents("id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY ("entity_parent") REFERENCES entities("id") ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY ("concept") REFERENCES concepts("id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE relation ( subj INT, rel INT, obj INT,
	FOREIGN KEY ("subj") REFERENCES entities("id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY ("rel") REFERENCES entities("id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY ("obj") REFERENCES entities("id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE INDEX ON entities("doc_parent");
CREATE INDEX ON entities("entity_parent");
DROP TABLE plain;
CREATE TABLE plain (
	id SERIAL PRIMARY KEY,
	sentence INT NOT NULL,
	parent INT,
	word VARCHAR(64),
	entity INT,
	label VARCHAR(10),
	FOREIGN KEY ("parent") REFERENCES plain("id") ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY ("sentence") REFERENCES sentences("id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY ("entity") REFERENCES entities("id") ON UPDATE CASCADE ON DELETE SET NULL,
	UNIQUE (id, parent)
);
CREATE INDEX ON plain ("entity");
CREATE INDEX ON plain ("parent");

DROP TABLE test.rdoc;
CREATE TABLE test.rdoc (doc INT NOT NULL, rid VARCHAR(20), FOREIGN KEY ("doc") REFERENCES public.documents("id") ON UPDATE CASCADE ON DELETE CASCADE);
DROP TABLE test.rsentence;
CREATE TABLE test.rsentence (sentence INT NOT NULL, r_cid VARCHAR(20), body TEXT, FOREIGN KEY ("sentence") REFERENCES public.sentences("id") ON UPDATE CASCADE ON DELETE CASCADE);
CREATE INDEX ON test.rsentence("r_cid");
CREATE INDEX ON test.rsentence("sentence")
DROP TABLE test.rtree;
CREATE TABLE test.rtree (root VARCHAR(20), parent VARCHAR(20), child VARCHAR(20));
CREATE INDEX ON test.rtree("parent");
CREATE INDEX ON test.rtree("child");
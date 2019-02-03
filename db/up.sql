CREATE TABLE documents ( id SERIAL PRIMARY KEY,
	d TIMESTAMP DEFAULT NOW() );
CREATE TABLE sentences ( id SERIAL PRIMARY KEY,
	parent INT,
	FOREIGN KEY ("parent") REFERENCES documents("id") ON UPDATE CASCADE ON DELETE CASCADE );
CREATE TABLE concepts ( id SERIAL PRIMARY KEY,
	parent INT NOT NULL,
	FOREIGN KEY ("parent") REFERENCES documents("id") ON UPDATE CASCADE ON DELETE CASCADE );
CREATE TABLE concept_graph ( a INT, b INT,
	FOREIGN KEY ("a") REFERENCES concepts("id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY ("b") REFERENCES concepts("id") ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE entities (
	id SERIAL PRIMARY KEY,
	doc_parent INT NOT NULL,
	entity_parent INT,
	concept INT,
	FOREIGN KEY ("parent") REFERENCES documents("id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY ("entity_parent") REFERENCES entities("id") ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY ("concept") REFERENCES concepts("id") ON UPDATE CASCADE ON DELETE CASCADE
);
DROP TABLE plain;
CREATE TABLE plain (
	id SERIAL PRIMARY KEY,
	parent INT NOT NULL,
	word VARCHAR(64) NOT NULL,
	entity INT,
	FOREIGN KEY ("parent") REFERENCES sentences("id") ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY ("entity") REFERENCES entities("id") ON UPDATE CASCADE ON DELETE SET NULL,
	UNIQUE (id, parent)
);
CREATE INDEX ON plain ("entity");
CREATE INDEX ON plain ("parent");
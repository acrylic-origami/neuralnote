import psycopg2

if __name__ == '__main__':
	with psycopg2.connect('dbname=nl user=nl password=logbase') as conn:
		cur = conn.cursor()
		cur.execute('SELECT body FROM documents;')
		for row in cur:
			print(row[0])
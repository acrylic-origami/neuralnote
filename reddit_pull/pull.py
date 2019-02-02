import sys
import praw
import psycopg2
import unicodecsv as csv
import re
import traceback
from datetime import datetime

# 'announcements', 
SUBS = [ 'funny', 'AskReddit', 'todayilearned', 'science', 'worldnews', 'pics', 'IAmA', 'gaming', 'videos', 'movies', 'aww', 'Music', 'blog', 'gifs', 'news', 'explainlikeimfive', 'askscience', 'EarthPorn', 'books', 'television', 'mildlyinteresting', 'LifeProTips', 'Showerthoughts', 'space', 'DIY', 'Jokes', 'gadgets', 'nottheonion', 'sports', 'tifu', 'food', 'photoshopbattles', 'Documentaries', 'Futurology', 'history', 'InternetIsBeautiful', 'dataisbeautiful', 'UpliftingNews', 'listentothis', 'GetMotivated', 'personalfinance', 'OldSchoolCool', 'philosophy', 'Art', 'nosleep', 'WritingPrompts', 'creepy' ] # 'TwoXChromosomes', 'Fitness', 'technology', 'WTF', 'bestof', 'AdviceAnimals', 'politics', 'atheism', 'interestingasfuck', 'europe', 'woahdude', 'BlackPeopleTwitter', 'oddlysatisfying', 'gonewild', 'leagueoflegends', 'pcmasterrace', 'reactiongifs', 'gameofthrones', 'wholesomememes', 'Unexpected', 'Overwatch', 'facepalm', 'trees', 'Android', 'lifehacks', 'me_irl', 'relationships', 'Games', 'nba', 'programming', 'tattoos', 'NatureIsFuckingLit', 'Whatcouldgowrong', 'CrappyDesign', 'dankmemes', 'nsfw', 'cringepics', '4chan', 'soccer', 'comics', 'sex', 'pokemon', 'malefashionadvice', 'NSFW_GIF', 'StarWars', 'Frugal', 'HistoryPorn', 'AnimalsBeingJerks', 'RealGirls', 'travel', 'buildapc', 'OutOfTheLoop'

COMMENT_LIMIT = 300

if __name__ == '__main__':
	r = praw.Reddit(client_id='WToYeaZlhp2ocQ', client_secret='md7SrJ6w_w59EU1iQ6CPeWP6924', user_agent='XProfiler/0.1 by concaten8')
	posts = []
	conn = psycopg2.connect('dbname=nl user=nl password=logbase')
	
	cur = conn.cursor()
	
	static_fields = [
		# dates
		('approved_at_utc', 'approved'),
		('created_utc', 'created'),
		('banned_at_utc', 'banned'),
		
		# meta
		('post_hint',None),
		('id',None)
	]
	dynamic_fields = [
		# activity
		('locked',None),
		('downs',None),
		('ups',None),
		('score',None),
		('likes',None),
		('view_count',None),
		('num_comments',None),
		('num_crossposts',None),
		('spoiler',None),
		('pinned',None), # identical?
		('stickied',None), # identical?

		# meta
		('gilded',None),
		('title',None),
		('permalink',None),
		('domain',None),
		('edited',None),
		('post_categories',None),
		('over_18',None),
		('can_gild',None),
		('distinguished',None)
	]
	
	for sub in SUBS:
		i = 0
		e = 0
		print(sub)
		li = list(r.subreddit(sub).new(limit=None))
		
		for pidx, p in enumerate(li):
			try:
				j = 0
				def recurse(R, parent):
					global j, pidx, p
					j = j + 1
					if j > COMMENT_LIMIT:
						return
						
					sys.stdout.write('\r%d|%d' % (pidx, j))
					for c in R:
						if isinstance(c, praw.models.MoreComments):
							recurse(c.comments(), parent)
						else:
							try:
								cur.execute('INSERT INTO documents (rid, rparent, body) VALUES (%s, %s, %s) RETURNING id;', (c.id, p.id, c.body))
								
								doc_id = cur.fetchone()
								cur.execute('INSERT INTO concepts(parent) VALUES (%s) RETURNING id;', (doc_id,))
								concept_id = cur.fetchone()[0]
								if parent != None:
									cur.execute('INSERT INTO concept_graph (a, b) VALUES (%s, %s);', (parent, concept_id))
								for sentence in c.body.split('.'):
									cur.execute('INSERT INTO sentences (parent) VALUES (%s) RETURNING id;', (doc_id,))
									sentence_id = cur.fetchone()[0]
									for tok in re.split('[^\w]', sentence, flags=re.U):
										cur.execute('INSERT INTO plain (parent, word, entity) VALUES (%s, %s, NULL)', (sentence_id, tok))
										# w_dynamic = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
								conn.commit()
								recurse(c.replies, concept_id)
							except (KeyboardInterrupt, SystemExit):
								raise
							except:
								conn.rollback()
								print(traceback.print_exc())
				recurse(p.comments, None)
			except (KeyboardInterrupt, SystemExit):
				raise
			except:
				conn.rollback()
				print(traceback.print_exc())
					
		# with open('/tmp/static.csv', 'w') as f_static, open('/tmp/dynamic.csv', 'w') as f_dynamic:
		# 	w_static = csv.writer(f_static, quoting=csv.QUOTE_MINIMAL)
		# 	# w_static.writerow([(f[1] or f[0]) for f in static_fields])
		# 	for row in statics:
		# 		w_static.writerow(row)
			
		# 	w_dynamic = csv.writer(f_dynamic, quoting=csv.QUOTE_MINIMAL)
		# 	# w_dynamic.writerow([(f[1] or f[0]) for f in dynamic_fields] + ['d', 'id'])
		# 	for row in dynamics:
		# 		w_dynamic.writerow(row)
		# 	# print('COPY dynamic (%s) FROM \'/tmp/dynamic.csv\' CSV ENCODING \'utf8\';' % ','.join([(f[1] or f[0]) for f in dynamic_fields] + ['d', 'id']))
		# cur.execute('CREATE TEMP TABLE static_tmp (LIKE static INCLUDING defaults INCLUDING constraints INCLUDING indexes) ON COMMIT DROP;')
		# cur.execute('COPY static_tmp (%s) FROM \'/tmp/static.csv\' CSV ENCODING \'utf8\';' % ','.join((f[1] or f[0]) for f in static_fields))
		# cur.execute('INSERT INTO static SELECT * FROM static_tmp ON CONFLICT DO NOTHING;')
		# cur.execute('COPY dynamic (%s) FROM \'/tmp/dynamic.csv\' CSV NULL \'\' ENCODING \'utf8\';' % ','.join([(f[1] or f[0]) for f in dynamic_fields] + ['d', 'id']))
		# conn.commit()
			
		# # 	i += 1
		# # sys.exit(0)
		# # print('%s: %d, %d' % (sub, i, e))
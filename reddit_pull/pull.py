import sys
import praw
import psycopg2
import unicodecsv as csv
import re
import traceback
import nltk
from nltk.parse import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk import Tree
from datetime import datetime

# 'announcements', 
# 'funny', 
SUBS = [ 'AskReddit', 'todayilearned', 'science', 'worldnews', 'pics', 'IAmA', 'gaming', 'videos', 'movies', 'aww', 'Music', 'blog', 'gifs', 'news', 'explainlikeimfive', 'askscience', 'EarthPorn', 'books', 'television', 'mildlyinteresting', 'LifeProTips', 'Showerthoughts', 'space', 'DIY', 'Jokes', 'gadgets', 'nottheonion', 'sports', 'tifu', 'food', 'photoshopbattles', 'Documentaries', 'Futurology', 'history', 'InternetIsBeautiful', 'dataisbeautiful', 'UpliftingNews', 'listentothis', 'GetMotivated', 'personalfinance', 'OldSchoolCool', 'philosophy', 'Art', 'nosleep', 'WritingPrompts', 'creepy' ] # 'TwoXChromosomes', 'Fitness', 'technology', 'WTF', 'bestof', 'AdviceAnimals', 'politics', 'atheism', 'interestingasfuck', 'europe', 'woahdude', 'BlackPeopleTwitter', 'oddlysatisfying', 'gonewild', 'leagueoflegends', 'pcmasterrace', 'reactiongifs', 'gameofthrones', 'wholesomememes', 'Unexpected', 'Overwatch', 'facepalm', 'trees', 'Android', 'lifehacks', 'me_irl', 'relationships', 'Games', 'nba', 'programming', 'tattoos', 'NatureIsFuckingLit', 'Whatcouldgowrong', 'CrappyDesign', 'dankmemes', 'nsfw', 'cringepics', '4chan', 'soccer', 'comics', 'sex', 'pokemon', 'malefashionadvice', 'NSFW_GIF', 'StarWars', 'Frugal', 'HistoryPorn', 'AnimalsBeingJerks', 'RealGirls', 'travel', 'buildapc', 'OutOfTheLoop'

COMMENT_LIMIT = 300
POST_LIMIT = 100

if __name__ == '__main__':
	r = praw.Reddit(client_id='WToYeaZlhp2ocQ', client_secret='md7SrJ6w_w59EU1iQ6CPeWP6924', user_agent='XProfiler/0.1 by concaten8')
	parser = CoreNLPParser(url='http://localhost:9000')
	with psycopg2.connect('dbname=nl user=nl password=logbase') as conn:
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
			
			for pidx, p in enumerate(li[0:POST_LIMIT]):
				cur.execute('INSERT INTO documents VALUES (DEFAULT) RETURNING id;')
				doc_id = cur.fetchone()[0]
				cur.execute('INSERT INTO test.rdoc (doc, rid) VALUES (%s, %s);', (doc_id, p.id))
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
									cur.execute('INSERT INTO test.rtree (root, parent, child) VALUES (%s, %s, %s)', (p.id, parent.id if parent != None else None, c.id))
									# cur.execute('INSERT INTO concepts(parent) VALUES (%s) RETURNING id;', (doc_id,))
									# concept_id = cur.fetchone()[0]
									# if parent != None:
									# 	cur.execute('INSERT INTO concept_graph (a, b) VALUES (%s, %s);', (parent, concept_id))
									
									for sentence in c.body.split('.'):
										cur.execute('INSERT INTO sentences (parent) VALUES (%s) RETURNING id;', (doc_id,))
										sentence_id = cur.fetchone()[0]
										cur.execute('INSERT INTO test.rsentence (sentence, r_cid, body) VALUES (%s, %s, %s);', (sentence_id, c.id, c.body))
										if not re.match('^[^\\w]*$', sentence):
											R = parser.raw_parse(sentence)
											def tree_recurse(parent, parent_id):
												for child in parent:
													if isinstance(child, nltk.Tree):
														cur.execute('INSERT INTO plain (sentence, parent, label) VALUES (%s, %s, %s) RETURNING id;', (sentence_id, parent_id, child.label()))
														plain_id = cur.fetchone()[0]
														tree_recurse(child, plain_id)
													else:
														cur.execute('INSERT INTO plain (sentence, parent, word, label) VALUES (%s, %s, %s, %s)', (sentence_id, parent_id, child, parent.label()))
											tree_recurse(list(R)[0], None)

										# for tok in nltk.word_tokenize(sentence):
										# 	cur.execute('INSERT INTO plain (parent, word, entity) VALUES (%s, %s, NULL)', (sentence_id, tok))
											# w_dynamic = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
									conn.commit()
									recurse(c.replies, c)
								except (KeyboardInterrupt, SystemExit):
									raise
								except:
									# raise
									conn.rollback()
									print(traceback.print_exc())
					recurse(p.comments, None)
				except (KeyboardInterrupt, SystemExit):
					raise
				except:
					# raise
					conn.rollback()
					print(traceback.print_exc())
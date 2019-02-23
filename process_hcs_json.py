import json, sys
total = 0
tks = 0

fmt = 'conllu'
fs = []
if sys.argv[1] != 'conllu' and sys.argv[1] != 'cg3':
	fs = sys.argv[1:]	
else:
	fmt = sys.argv[1]
	fs = sys.argv[2:]

for f in fs:
	s_no = 0
	fd = open(f, 'r')
	doc = json.load(fd)
	for s in doc['kwic']:
		idx = 1
		ws = []
		sent = ''
		for w in s['tokens']:
#			print(w)
			#{'word': 'Mapenzi', 'gloss': 'Favourite', 'pos': 'N', 'syntax': '@<NH', 'lemma': 'penzi', 'msdextra': '_', 'lex': '|penzi..nn.1|', 'msd': '5/6-PL'}
			
			misc = '_'
			if 'lex' in w:
				misc = 'Lex=' + w['lex']
				if 'gloss' in w and type(w['gloss']) != type(None):
					misc = misc + '|Gloss=' + w['gloss']

			tag = w['pos'] 
			msd = w['msd'].title()
			tag = tag.strip('|').replace('|_', '').replace(' ','|')
			msd = msd.strip('|').replace('|_', '').replace(' ','|')
			ws.append((idx, w['word'], w['lemma'], '_', tag.strip('|'), msd.strip('|'), '_', w['syntax'], '_', '_'))
			sent = sent + w['word'] + ' '
			idx += 1
			tks += 1
		print('# sent_id = %s:%d' % (f, s_no))
		print('# text = %s' % (sent))
		for w in ws:
			if fmt == 'cg3':
				print('"<%s>"\n\t"%s" %s %s #%d->%d' % (w[1], w[2], w[4].replace('|', ' '), w[7], w[0], w[0]))
			else:
	                        print('%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % w)
		print()
		s_no += 1
		total += 1

print(tks, total, file=sys.stderr)

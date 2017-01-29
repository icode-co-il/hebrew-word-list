# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from collections import Counter
from progressbar import ProgressBar
import re, os
import time

INVALID_FILENAME_PATTERN = re.compile(ur'\.(jpg|png)\.html$|שיחת_משתמש|תמונה')
PARAGRAPHS_PATTERN = re.compile(r"<p>(.*?)</p>")
CHARS_PATTERN = re.compile(ur"""[^אבגדהוזחטיכלמנסעפצקרשתןףץםך'\-\s"]""")

all_files = []
for root, _, filenames in os.walk(u'wikipedia-he-html'):
	for filename in filenames:
		if INVALID_FILENAME_PATTERN.search(filename):
			continue
		all_files.append(os.path.join(root, filename))

freq = Counter()

with ProgressBar(max_value = len(all_files)) as progress:
	for i, file_path in enumerate(all_files):
		progress.update(i)

		try:
			html = open(file_path, "rb").read().decode('utf8')
		except UnicodeDecodeError:
			continue

		if '<meta http-equiv="Refresh"' in html: # HTML redirect
			continue

		for p_html in PARAGRAPHS_PATTERN.findall(html):
			p_text = BeautifulSoup(p_html, 'html.parser').get_text()
			p_text = CHARS_PATTERN.sub('', p_text)
			for word in p_text.split():
				word = word.strip('="')
				if len(word) > 1:
					freq[word] += 1

print "Total words: ", len(freq)
open('words.txt', "wb").write(
	u"\n".join("%s, %s" % x for x in freq.most_common()).encode('utf8'))

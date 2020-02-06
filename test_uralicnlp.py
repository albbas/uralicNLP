#encoding: utf-8
from uralicNLP import uralicApi
from uralicNLP.cg3 import Cg3
from uralicNLP.translate import *
from uralicNLP import dependency
import re

#print(uralicApi.supported_languages())

#uralicApi.download("fin")
"""
print(uralicApi.analyze("voita", "fin"))
print(uralicApi.analyze("voita", "fin", descrpitive=False))
print(uralicApi.analyze("voita", "fin"))
print(uralicApi.analyze("voita", "fin", descrpitive=False))



print(uralicApi.generate("käsi+N+Sg+Par", "fin"))
print(uralicApi.generate("käsi+N+Sg+Par", "fin"))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", descrpitive=True))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", descrpitive=True))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", dictionary_forms=False))
print(uralicApi.generate("käsi+N+Sg+Par", "fin", dictionary_forms=False))

print(uralicApi.generate("käsi+N+Sg+Par", "deu"))

#print(uralicApi.dictionary_search("car", "sms"))

print(uralicApi.lemmatize("voita", "fin", descrpitive=True))


#uralicApi.download("kpv")

"""
"""
cg = Cg3("fin")
print(cg.disambiguate(["Kissa","voi","nauraa", "."], descrpitive=True))


cg = Cg3("kpv")
print(cg.disambiguate("театрӧ пыран абонемент".split(" ")))
"""

#print (uralicApi.lemmatize("livsmedel", "swe",force_local=True, word_boundaries=True))

"""
print("كتاب")

print(uralicApi.analyze("كتاب","ara"))
print(uralicApi.generate("+noun+humanكاتب+masc+pl@","ara"))

print(uralicApi.lemmatize("كتاب","ara"))

str = "+noun+humanكاتب+masc+pl@"
print(re.findall(r"[ء-ي]+", str))

"""

print(uralicApi.analyze("cats", "eng"))
print(uralicApi.generate("cat[N]+N+PL", "eng"))
print(uralicApi.lemmatize("cats", "eng"))

"""

translator = ApertiumGiellateknoTranslator()
print(translator.translate("kissa juoksee kovaa", "fin","sme"))


translator = ApertiumStableTranslator()
print(translator.translate("el gato corre rápido", "spa","cat"))
"""
"""
ud = dependency.parse_text("kissa nauroi kovaa\nLehmä lauloi ainiaan", "fin",url="http://localhost:9877")
for sentence in ud:
	for word in sentence:
		print word.pos, word.lemma, word.get_attribute("deprel")
	print "---"
"""
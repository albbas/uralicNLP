#encoding: utf-8
import re
from copy import copy
import codecs

class UD_collection():
	"""docstring for UD_collection"""
	def __init__(self, file_handle):
		sentence = []
		self.sentences = []
		for line in file_handle:
			if line == "\n":
				self.sentences.append(parse_sentence(sentence))
				sentence = []
			else:
				sentence.append(line.replace("\n", ""))

	def find_sentences(self, query={}, head_query={}, match_range_tokens = False, match_empty_nodes = False, enhanced_dependencies=False, return_root= False):
		results = []
		for sentence in self.sentences:
			r = sentence.find(query, head_query, match_range_tokens, match_empty_nodes, enhanced_dependencies)
			if return_root and len(r) > 0:
				results.append(sentence)
			else:
				results.extend(r)
		return results
		
class UD_sentence():
	def __init__(self):
		self.comments = ""
		self.id = "0"
		self.children = []
		self.secondary_children = []

	def set_root(self, root):
		self.root =root
		self.find = root.find

	def __repr__(self):
		children = self.find()
		children.sort()
		representation = self.comments
		for child in children:
			representation = representation + unicode(child) + u"\n"
		return representation

class UD_relation():
	"""docstring for UD_relation"""
	def __init__(self, node, relation, head, primary=True):
		self.node = node
		self.head = head
		self.relation = relation
		if primary:
			if head is not None:
				head.children.append(self)
			node.head = self
		else:
			head.secondary_children.append(self)
			node.heads.append(self)
		self.primary = primary

	def __repr__(self):
		return self.head.id + ":" + self.relation

	def __eq__(self, other):
		return repr(self) == repr(other)

	def __lt__(self, other):
		s_dash = False
		if "-" in self.node.id:
			s_dash = True
			s_id = (int(self.node.id.split("-")[0]))
		else:
			s_id = int(self.node.id)
		o_dash = False
		if "-" in other.node.id:
			o_dash = True
			o_id = (int(other.node.id.split("-")[0]))
		else:
			o_id = int(other.node.id)
		if o_id == s_id:
			if s_dash:
				return True
			return False
		else:
			return s_id < o_id
		

class UD_node():
	"""docstring for UD_node"""
	def __init__(self, id, form, lemma, upostag, xpostag, feats, misc):
		self.id = id
		self.form = form 
		self.lemma = lemma
		self.upostag = upostag
		self.xpostag = xpostag
		self.feats = feats
		self.misc = misc
		self.head = None
		self.children = []
		self.heads = []
		self.secondary_children = []

	def find(self, query={}, head_query={}, match_range_tokens = False, match_empty_nodes = False, enhanced_dependencies=False):
		results = []
		passed = True
		if (not match_range_tokens and "-" in self.id) or (not match_empty_nodes and "." in self.id):
			passed = False
		else:
			for key in query:
				if key == "deprel":
					if self.head is None:
						attr = "root"
					else:
						attr = self.head.relation
				else:
					attr = getattr(self, key)
				v = query[key]
				if isinstance(v, re._pattern_type):
					if v.match(attr) is None:
						passed = False
						break
				else:
					if v != attr:
						passed = False
						break
		
			head = self.head
			if head is not None and passed:
				if enhanced_dependencies:
					heads = self.heads + head
				else:
					heads = [head]
				head_pass = True
				for head in heads:
					head_pass = True
					for key in head_query:
						if key == "deprel":
							if self.head is None:
								attr = "root"
							else:
								attr = self.head.relation
						else:
							attr = getattr(self, key)
						v = head_query[key]
						if isinstance(v, re._pattern_type):
							if v.match(attr) is None:
								head_pass = False
								break
						else:
							if v != attr:
								head_pass = False
								break
					if head_pass:
						break
				passed = head_pass
					

			elif head is None and len(head_query.keys()) >0:
				passed = False
		if passed:
			results.append(self)
		for child in self.children:
			r = child.node.find(query, head_query, match_range_tokens, match_empty_nodes, enhanced_dependencies)
			results.extend(r)
		return results


	def __repr__(self):
		head_repr = "0\troot"
		if self.head is not None:
			head_repr = self.head.head.id + "\t" + self.head.relation
		if len(self.heads) == 0:
			deps = "_"
		else:
			rels = copy(self.heads)
			rels = [x for x in rels if x.head != self]
			if self.head is not None:
				rels.append(self.head)
			rels.sort()
			deps = "|".join(str(x) for x in rels)
			if deps == "":
				deps = "_"
		return self.id + "\t" + self.form + "\t" + self.lemma + "\t" + self.upostag + "\t" + self.xpostag + "\t" + self.feats + "\t" + head_repr + "\t" + deps + "\t" + self.misc
	
	def __eq__(self, other):
		return repr(self) == repr(other)

	def __lt__(self, other):
		s_dash = False
		if "-" in self.id:
			s_dash = True
			s_id = (int(self.id.split("-")[0]))
		else:
			s_id = int(self.id)
		o_dash = False
		if "-" in other.id:
			o_dash = True
			o_id = (int(other.id.split("-")[0]))
		else:
			o_id = int(other.id)
		if o_id == s_id:
			if s_dash:
				return True
			return False
		else:
			return s_id < o_id

def parse_sentence(conll_u_sentence):
	if type(conll_u_sentence) == str or type(conll_u_sentence) == unicode:
		conll_u_sentence = conll_u_sentence.split("\n")
	nodes = {}
	relations = {}
	ud_sentence = UD_sentence()
	comments = ""
	for annotation in conll_u_sentence:
		if annotation == "":
			continue
		if annotation.startswith("#"):
			comments = comments + annotation + "\n"
			continue
		parts = annotation.split("\t")
		node = UD_node(parts[0],parts[1],parts[2],parts[3],parts[4],parts[5],parts[9])
		nodes[parts[0]] = node
		relations[parts[0]] = [parts[6],parts[7],parts[8]]
	ud_sentence.comments = comments
	root = None
	nodes["0"] = ud_sentence
	for id in relations:
		relation = relations[id]
		head_id = relation[0]
		if head_id == "0":
			root = nodes[id]
		head_relation = UD_relation(nodes[id], relation[1], nodes[head_id])
		o_rel = relation[2]
		if o_rel == u"_":
			other_relations = []
		else:
			other_relations = o_rel.split("|")
		head_rel = head_id + ":" + relation[1]
		for other_relation in other_relations:
			if other_relation == head_rel:
				continue
			other_parts = other_relation.split(":")
			r = UD_relation(nodes[id], other_parts[1], nodes[other_parts[0]], False)
	ud_sentence.set_root(root)
	return ud_sentence


root = parse_sentence(codecs.open("/Users/mikahama/Desktop/fi_test.conllu", "r", encoding="utf-8").read())
#print unicode(root)

nodes = root.find({"upostag":"NOUN", "deprel": "obl"})
for node in nodes:
	print unicode(node)

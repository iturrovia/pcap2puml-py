"""
The purpose of this module is to parse data formatted as tabbed tree

"""

import itertools
from tabtree import parser

class TestParser(object):
	"""
	Class to test functions in parser module
	"""

	LINES = [
		'item 0', 
		'\titem 0 0', 
		'\titem 0 1',
		'\t\titem 0 1 0',
		'\t\titem 0 1 1',
		'\titem 0 2', 
		'',
		'item 1', 
		' item 1 0', 
		' item 1 1',
		' \titem 1 1 0',
		'\t item 1 1 1',
		'\titem 1 2', 
		''
	]
	DTS = [
		(0, 'item 0'),
		(1, 'item 0 0'),
		(1, 'item 0 1'),
		(2, 'item 0 1 0'),
		(2, 'item 0 1 1'),
		(1, 'item 0 2'),
		(0, ''),
		(0, 'item 1'),
		(1, 'item 1 0'),
		(1, 'item 1 1'),
		(2, 'item 1 1 0'),
		(2, 'item 1 1 1'),
		(1, 'item 1 2'),
		(0, '')
	]
	DC_NODE_TREES = [
		{'data': 'item 0', 'children': [
			{'data': 'item 0 0', 'children': []},
			{'data': 'item 0 1', 'children': [
				{'data': 'item 0 1 0', 'children': []},
				{'data': 'item 0 1 1', 'children': []}
			]},
			{'data': 'item 0 2', 'children': []}
		]},
		{'data': 'item 1', 'children': [
			{'data': 'item 1 0', 'children': []},
			{'data': 'item 1 1', 'children': [
				{'data': 'item 1 1 0', 'children': []},
				{'data': 'item 1 1 1', 'children': []}
			]},
			{'data': 'item 1 2', 'children': []}
		]}
	]

	def test_line_to_depth_and_text(self):
		# Testing for all the lines and DTs in this test class
		for (line, dt) in zip(self.LINES, self.DTS):
			assert parser.line_to_depth_and_text(line) == dt

	def test_lines_to_dts(self):
		dts = list( parser.lines_to_dts(self.LINES) )
		assert len(dts) == len(self.DTS)
		for (dt1, dt2) in zip(dts, self.DTS):
			assert dt1 == dt2

	def test_dts_to_node_trees(self):

		def text_to_dc_node(text):
			return {'data': text, 'children': []}

		def compare_dc_nodes(dc1, dc2):
			if(dc1['data'] != dc2['data']):
				return False
			elif(len(dc1['children']) != len(dc2['children'])):
				return False
			else:
				for (child1, child2) in zip(dc1['children'], dc2['children']):
					if(not compare_dc_nodes(child1, child2)):
						return False
			return True

		node_trees = list( parser.dts_to_node_trees(self.DTS, text_to_node=text_to_dc_node, node_children_key='children') )
		assert len(node_trees) == len(self.DC_NODE_TREES)
		for (dc1, dc2) in zip(node_trees, self.DC_NODE_TREES):
			assert compare_dc_nodes(dc1, dc2)

	def test_lines_to_node_trees(self):

		def text_to_dc_node(text):
			return {'data': text, 'children': []}

		def compare_dc_nodes(dc1, dc2):
			if(dc1['data'] != dc2['data']):
				return False
			elif(len(dc1['children']) != len(dc2['children'])):
				return False
			else:
				for (child1, child2) in zip(dc1['children'], dc2['children']):
					if(not compare_dc_nodes(child1, child2)):
						return False
			return True

		node_trees = list( parser.lines_to_node_trees(self.LINES, text_to_node=text_to_dc_node, node_children_key='children') )
		assert len(node_trees) == len(self.DC_NODE_TREES)
		for (dc1, dc2) in zip(node_trees, self.DC_NODE_TREES):
			assert compare_dc_nodes(dc1, dc2)

	def test_spaces_to_tabs(self):
		assert parser.spaces_to_tabs('        abcd', 8) == '\tabcd'
		assert parser.spaces_to_tabs('                abcd', 8) == '\t\tabcd'
		assert parser.spaces_to_tabs('        \tabcd', 8) == '\t\tabcd'
		assert parser.spaces_to_tabs('\t        abcd', 8) == '\t\tabcd'

	def test_text_to_dc_node(self):
		dc_node = parser.text_to_dc_node('abcd')
		assert dc_node['data'] == 'abcd'
		assert tuple(dc_node['children']) == tuple([])
	

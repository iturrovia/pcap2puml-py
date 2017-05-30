"""
The purpose of this module is to create puml.SeqDiag objects out of PCAP files
To do so, it provides templates to ease such task:
	- VoipTemplate class: creates a puml.SeqDiag object out of a list of PCAP packets as parsed by pyshark

"""
from __future__ import print_function
try:
	import itertools.ifilter as filter
except ImportError:
	pass
try:
	import itertools.imap as map
except ImportError:
	pass
from pcap2puml import puml

def has_layer(packet, layer_name):
    return layer_name in map(lambda layer: layer._layer_name, packet.layers)

class VoipTemplate(object):
	'''
	This is a template to create ,
	which we can use to create a a puml.SeqDiag object out of a list of PCAP packets as parsed by pyshark
	'''
	def __init__(self, nodealiases={}):
		self.__call_ids = {}
		self.nodealiases = nodealiases

	CALL_ID_COLORS = ['red', 'blue', 'green', 'purple', 'brown', 'magenta', 'aqua', 'orange']

	def get_message_color(self, packet):
		call_id = packet.sip.get_field('call_id')
		call_id_index = self.__call_ids.get(call_id)
		if(call_id_index == None):
			call_id_index = len(self.__call_ids)
			self.__call_ids[call_id] = call_id_index
		return VoipTemplate.CALL_ID_COLORS[call_id_index % len(VoipTemplate.CALL_ID_COLORS)]

	def participantid_to_participantname(self, participantid):
		participantname = self.nodealiases.get(participantid)
		if(participantname == None):
			participantname = participantid
		return participantname

	def get_transport_ports(self, packet):
		if(has_layer(packet, 'udp')):
			t_layer = packet.udp
		elif (has_layer(packet, 'tcp')):
			t_layer = packet.tcp
		elif (has_layer(packet, 'sctp')):
			t_layer = packet.sctp
		else:
			raise ValueError('packet contains no transport layer')
		return (t_layer.srcport, t_layer.dstport)
	
	def get_participant_ids(self, packet):
		src_ip = packet.ip.src
		dst_ip = packet.ip.dst
		return (src_ip, dst_ip)

	def get_participants(self, packet):
		(src_id, dst_id) = self.get_participant_ids(packet)
		src = {'name': '"{}"'.format(self.participantid_to_participantname(src_id))}
		dst = {'name': '"{}"'.format(self.participantid_to_participantname(dst_id))}
		return (src, dst)

	def get_arrow(self, packet):
		arrow = {'head': '>', 'shaft': '-', 'color': self.get_message_color(packet)}
		return arrow

	def get_sequence_number(self, packet):
		return {'number': packet.number}

	def get_timestamp(self, packet):
		return packet.sniff_timestamp

	def get_message_lines(self, packet):
		sip = packet.sip
		if(sip.get_field('status_code') == None):
			main_line = {'text': sip.get_field('request_line'), 'color': self.get_message_color(packet)}
		else:
			 main_line = {'text': sip.get_field('status_line'), 'color': self.get_message_color(packet)}
		message_lines = [main_line]
		sip_fields = ['call_id', 'from_user', 'to_user', 'p_asserted_identity', 'sdp_connection_info', 'sdp_media']
		for sip_field in sip_fields:
			field_value = sip.get_field(sip_field)
			if(field_value != None):
				line_text = '{}: {}'.format(sip_field, field_value)
				message_lines.append({'text': line_text})
		sdp_media_attrs = sip.get_field('sdp_media_attr')
		if(sdp_media_attrs != None):
			for sdp_media_attr in sdp_media_attrs.all_fields:
				if(sdp_media_attr.showname_value in ['sendrecv', 'sendonly', 'recvonly', 'inactive']):
					line_text = sdp_media_attr.showname
					message_lines.append({'text': line_text})
		return message_lines

	def packet_to_seqevents(self, packet):
		seqevent = puml.SeqEvent(
			self.get_participants(packet),
			self.get_message_lines(packet),
			arrow=self.get_arrow (packet),
			timestamp=self.get_timestamp(packet),
			sequence_number=self.get_sequence_number(packet),
			notes=None,
			event_type=puml.SEQEVENT_TYPE_MESSAGE)
		return [seqevent]

	def packets_to_seqevents(self, packets):
		seqevents = []
		supported_packets = filter(lambda packet: has_layer(packet, 'sip'), packets)
		for packet in supported_packets:
			for seqevent in self.packet_to_seqevents(packet):
				seqevents.append(seqevent)
		return seqevents

	def create_puml_seq_diagram(self, packets):
		seqevents = self.packets_to_seqevents(packets)
		participants = None
		return puml.SeqDiagram(seqevents, participants=participants)

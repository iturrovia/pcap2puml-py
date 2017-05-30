## pcap2puml - Creating PlantUML diagrams from PCAP files

1. pcap2puml is a tiny package to create PlantUML diagrams from PCAP files.
2. The API is designed to make PlantUML diagrams out of any network packets, but templates for VoIP (SIP-RTP+DNS+Diameter) are provided.

## How to use pcap2puml?

1. Load the package from any Python script/program
2. Create a packet_to_seqevent function (or use one from the templates)
3. Use the packet_to_seqevent as input parameter to create a PumlWriter object, and feed it with a PCAP file.

This is best done with from a Jupyter Notebook, so you can interactively tune the packet_to_seqevents and see the result in the output diagram). Jupyter notebook can be great to comment on traces too.

```
from pcap2puml import core
from pcap2puml.templates import sip_template

p2se = sip_template.default_sip_packet_to_seqevents
seqevents = core.create_seqevents(p2se, packets, context=None)
puml_lines = core.create_puml(seqevents)
with open('test.puml', 'w') ad puml_file:
	puml_file.write('\n'.join(puml_lines))

[TODO]  Add code example
```

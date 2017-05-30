## pcap2puml - Creating PlantUML Sequence Diagrams from PCAP files

1. pcap2puml is a tiny package to create PlantUML diagrams from PCAP files.
2. It contains two modules:
	- puml: defines SeqDiag object, to represent and create PlantUML Sequence Diagrams (http://plantuml.com/sequence-diagram)
	- pcap: defines templates to create SeqDiag objects out of PCAP files. Main template is for VoIP (SIP) traffic. The templates are objects with many methods that can be easily overridden.

## How to use pcap2puml?

See example at pcap2puml-example.ipynb (https://github.com/fran-ovia/pcap2puml-py/blob/master/pcap2puml-example.ipynb)

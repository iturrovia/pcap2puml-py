import pydoc
import shutil

import pcap2puml
pydoc.writedoc(pcap2puml)
shutil.move('pcap2puml.html', 'doc/pcap2puml.html')
import pcap2puml.puml
pydoc.writedoc(pcap2puml.puml)
shutil.move('pcap2puml.puml.html', 'doc/pcap2puml.puml.html')
pydoc.writedoc(pcap2puml.pcap)
shutil.move('pcap2puml.pcap.html', 'doc/pcap2puml.pcap.html')

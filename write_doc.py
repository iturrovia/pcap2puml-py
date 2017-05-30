import pydoc
import shutil

import tabtree
pydoc.writedoc(tabtree)
shutil.move('tabtree.html', 'doc/tabtree.html')
import tabtree.parser
pydoc.writedoc(tabtree.parser)
shutil.move('tabtree.parser.html', 'doc/tabtree.parser.html')

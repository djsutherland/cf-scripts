import networkx as nx

from conda_forge_tick.migrators import Compiler
from conda_forge_tick.utils import convert_dict_to_nt

g = nx.read_gpickle('../cf-graph/graph.pkl')

# Migrate the PRed versions
for node, attrs in g.nodes:
    if 'PRed' in attrs:
        attrs['PRed'] = {convert_dict_to_nt({'class_name': 'Version',
                                             'class_version': 0,
                                             'version': attrs['PRed']})}

# Don't migrate already done Compilers (double commits cause problems)
m = Compiler()
compiler_migrations = []
for node, attrs in g.nodes:
    if m.filter(attrs):
        continue
    compiler_migrations.append(node)

last_compiler_pr = 'cxxopts'
last_compiler_index = compiler_migrations.index(last_compiler_pr)
for i in range(last_compiler_index):
    g.nodes[compiler_migrations[i]]['PRed'] = {convert_dict_to_nt({
        'class_name': 'Compiler', 'class_version': 0})}

nx.write_gpickle(g, '../cf-graph/graph.pkl')

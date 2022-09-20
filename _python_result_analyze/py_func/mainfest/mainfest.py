from pglast import parse_sql, ast, Node
import os, fnmatch
from dataclasses import dataclass, field
from typing import Dict
import re

@dataclass
class ManifestNode:
    unique_id: str = field(default_factory= str)
    node_path: str = field(default_factory= str)
    node_name: str = field(default_factory= str)
    node_deps: str = field(default_factory= str)
    resource_type: str = field(default= None)
    materialized: str = field(default= None)
    node_status: str = field(default= None)
    node_started_at: str = field(default= None)
    node_finished_at: str = field(default= None)

    # {'node_path': 'cookbook2/agetbl.sql', 'node_name': 'agetbl', 'unique_id': 'model.mimic.agetbl', 'resource_type': 'model', 'materialized': 'table', 'node_status': 'started', 'node_started_at': '2022-09-14T01:49:34.536011', 'node_finished_at': None}


@dataclass
class Manifest:
    nodes: Dict = field(default_factory = dict)
    source: Dict= field (default_factory = dict)
    query: Dict = field (default_factory = dict)
    files: Dict = field(default_factory=dict)
    file_path: Dict = field(default_factory=dict)
    refs: Dict = field(default_factory=dict)

    def expect(self, unique_id: str):
        if unique_id in self.nodes:
            return self.nodes[unique_id]
        elif unique_id in self.source:
            return self.source[unique_id]
        else:
            raise Exception(f"Expected node {unique_id} not found in manifest")
    
    def print_manifest(self):
        for node, v in self.nodes.items():
            print(v)

class ManifestTask:
    def __init__(self, model_dir, extension, prefix = 'model.mimic.') -> None:
        self.model_dir = model_dir
        self.extension = extension
        self.prefix = prefix
        self._load_manifest()

    def _load_manifest(self):
        nodes = {}
        files = {}
        source = {}
        query = {}
        ref = {}
        regex_config = re.compile(r"\{\{\n*\s*config\s*\(\n*\s*.*\n*\s*\)\n*\s*\}\}", re.IGNORECASE)
        regex = re.compile(r"""(\{\{\s*ref\s*\(\')(.*)(\'\s*\)\s*\}\})""", re.IGNORECASE)
        for root, dirnames, filenames in os.walk(self.model_dir):
            for filename in fnmatch.filter(filenames, self.extension):
                node_name = os.path.splitext(filename)[0]
                unique_id = '{}{}'.format(self.prefix,node_name)
                file_path = os.path.join(root, filename)

                with open(file_path) as f:
                    src = f.read()
                    source[unique_id] = src
                    refs= regex.findall(src)
                    # refs = re.search(regex, src)
                    # src = re.sub(regex_config, '', src)
                    # src = re.sub(regex, lambda m: m.group(2) + ' ', src)
                    query[unique_id]  = regex.sub(lambda m: m.group(2) + ' ', regex_config.sub('', src))
                    ref[unique_id] = [r[1] for r in refs] if refs else None    
                
                nodes[unique_id] = ManifestNode(unique_id= unique_id, node_path= file_path, node_name= node_name, node_deps = ref[unique_id])
                files[unique_id] = file_path

        self.manifest = Manifest(nodes= nodes, source= source, file_path= file_path, query= query, refs = ref)



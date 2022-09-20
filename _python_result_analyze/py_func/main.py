# from mainfest.mainfest import ManifestTask

from mainfest import ParseGraphTask

if __name__ == '__main__':
    man = ParseGraphTask('/Users/chenchunyu/Documents/workspace/Experiment/mimic/mimic-dbt/models/cookbook', '*.sql') #example
    # man.manifest.print_manifest()
    man._init_graph()
    # man.vis_graph()
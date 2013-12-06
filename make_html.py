from collections import OrderedDict, defaultdict
import json
import jinja2
import copy

def group_files(d):
    out = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for k,v in d.items():
        for k2,v2 in v.items():
            if type(v2) == list:
                for listitem in v2:
                    publisher = listitem.split('-', 1)[0]
                    out[k][k2][publisher].append(listitem)
            else:
                out[k][k2] = v2
    return out
            

current_stats = {
    'aggregated': json.load(open('./stats-calculated/current/aggregated.json'), object_pairs_hook=OrderedDict),
    'inverted_file': json.load(open('./stats-calculated/current/inverted-file.json'), object_pairs_hook=OrderedDict)
}
current_stats['inverted_file_grouped'] = group_files(current_stats['inverted_file'])
ckan = json.load(open('./ckan.json'), object_pairs_hook=OrderedDict)

def iati_stats_page(template, **kwargs):
    def f(jinja_env):
        validation_template = jinja_env.get_template(template)
        return validation_template.render(current_stats=current_stats, ckan=ckan, **kwargs)
    return f



import github.web
urls = {
    'index.html': iati_stats_page('index.html'),
    'validation.html': iati_stats_page('validation.html', validation=True),
    'github.html': github.web.main
}

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
jinja_env.filters['url_to_filename'] = lambda x: x.split('/')[-1]

for url, f in urls.items():
    with open('out/'+url, 'w') as fp:
        fp.write(f(jinja_env).encode('utf-8'))
import yaml
from jinja2 import Environment, FileSystemLoader
from urllib.parse import quote_plus


TARGET_DIR = 'web'


def entry_to_url(entry):
    # word = quote_plus(entry['word'])
    word = entry['word']
    trans = entry['trans'].lower()
    trans = trans.replace(' ', '-').replace(';', '-').replace('(', '').replace(')', '')
    trans = trans.replace(',', '').replace('--', '-')
    return f'{word}-{trans}-in-chinese.html'


def create_entry_file(entry, env, prev_entry=None, next_entry=None):
    page_data = dict(entry)  # shallow copy
    page_data['prev_entry'] = prev_entry
    page_data['next_entry'] = next_entry

    template = env.get_template('entry.html')
    with open(f'{TARGET_DIR}/{entry["url"]}', mode='w') as f:
        f.write(template.render(**page_data))


def create_index_file(data, env):
    template = env.get_template('index.html')
    with open(f'{TARGET_DIR}/index.html', mode='w') as f:
        f.write(template.render(data=data))


def main():
    env = Environment(loader=FileSystemLoader('templates'))

    with open('szdict.yml') as f:
        data = yaml.load(f)

        for entry in data:
            entry['url'] = entry_to_url(entry)

        create_index_file(data, env)

        for i, entry in enumerate(data):
            prev_entry = data[i-1] if i > 0 else None
            next_entry = data[i+1] if i < len(data) - 1 else None
            create_entry_file(entry, env, prev_entry=prev_entry, next_entry=next_entry)


if __name__ == '__main__':
    main()

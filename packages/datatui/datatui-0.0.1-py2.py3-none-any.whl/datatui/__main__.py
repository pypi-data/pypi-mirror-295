import json
import srsly
import click 
from diskcache import Cache
from .app import datatui


@click.group()
def cli():
    pass

@click.command()
@click.argument('examples-path')
@click.option('--cache', default="annotations", help='Cache path')
@click.option('--collection', default="default", help='Subset a collection')
@click.option('--descr', default=None, help='Add a description')
def annotate(examples_path, cache, collection, descr):
    """Annotate and put some examples into the cache."""
    examples = list(srsly.read_jsonl(examples_path))
    datatui(cache, examples, collection, pbar=True, description=descr)

@click.command()
@click.option('--collection', default=None, help='Subset a collection')
@click.option('--cache', default="annotations", help='Cache path')
@click.option('--file-out', default=None, help='Output file path')
def export(collection, cache, file_out):
    """Export annotations from the cache."""
    cache = Cache(cache)
    relevant = (cache[k] for k in cache.iterkeys() 
                if collection is None or collection == cache[k]['collection'])
    if not file_out:
        for item in relevant:
            print(json.dumps(item))
    else:
        srsly.write_jsonl(file_out, relevant)

cli.add_command(annotate)
cli.add_command(export)

if __name__ == "__main__":
    cli()

from boxsdk import OAuth2, Client
import click
import yaml
import os


class Auth(object):
    def __init__(self, client_id, client_secret, access_token, config_fp):
        config = yaml.load(open(config_fp))
        oauth = OAuth2(
            client_id = client_id or config['oauth']['client_id'],
            client_secret = client_secret or config['oauth']['client_secret'],
            access_token = access_token or config['oauth']['access_token']
        )
        self.client = Client(oauth)


@click.group()
@click.option('--client_id', default=None)
@click.option('--client_secret', default=None)
@click.option('--access_token', default=None)
@click.option('--config_fp', default='config.yaml')
@click.pass_context
def cli(ctx, client_id, client_secret, access_token, config_fp):
    ctx.obj = Auth(client_id, client_secret, access_token, config_fp)


@cli.command()
@click.argument('dirpath', required=False)
@click.option('--folder_id', '-i', required=False)
@click.pass_context
@click.pass_obj
def lsdir(auth, ctx, dirpath, folder_id):
    """ Lists items in directory path """
    folder_id = folder_id or '0'

    folder = auth.client.folder(folder_id=folder_id).get()
    print folder['name']

    next_folder = None
    if dirpath: next_folder = dirpath.split('/')[0]
        
    for item in auth.client.folder(folder_id=folder_id).get_items(limit=1000, offset=0):
        if type(item) == type(folder):
            item = auth.client.folder(folder_id=item['id']).get()
            if item['name'] == next_folder:
                ctx.invoke(lsdir, dirpath='/'.join(dirpath.split('/')[1:]), folder_id=item['id'])
        else:
            item = auth.client.file(file_id=item['id']).get()
        if not next_folder: # only print if at end of given path
            print '{}\t{}\t{}'.format(item['owned_by']['login'], item['size'], item['name']).expandtabs(25)


@cli.command('download')
@click.argument('path', required=True)
@click.option('--folder_id', '-i', required=False)
@click.option('--output', '-o', default='.')
@click.pass_context
@click.pass_obj
def download(auth, ctx, path, folder_id, output):
    if not os.path.exists(output): os.makedirs(output)
    folder_id = folder_id or '0'

    folder = auth.client.folder(folder_id=folder_id).get()

    next_folder = None
    if path: next_folder = path.split('/')[0]
    print '{} -> {}'.format(folder['name'], next_folder)
    for item in auth.client.folder(folder_id=folder_id).get_items(limit=1000, offset=0):
        if type(item) == type(folder):
            item = auth.client.folder(folder_id=item['id']).get()
            if item['name'] == next_folder:
                ctx.invoke(download, path='/'.join(path.split('/')[1:]), folder_id=item['id'], output=output)
        else:
            item = auth.client.file(file_id=item['id']).get()
            if item['name'] == next_folder and len(path.split('/')) == 1:
                print 'downloading {}'.format(item['name'])
                with open(os.path.join(output, item['name']), 'w+') as output_file:
                    item.download_to(output_file)
                return
        if not next_folder: # only print if at end of given path
            print 'downloading {}'.format(item['name'])
            with open(os.path.join(output, item['name']), 'w+') as output_file:
                    item.download_to(output_file)


if __name__ == "__main__":
    cli()

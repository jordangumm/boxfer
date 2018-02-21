from boxsdk import OAuth2, Client
import click
import yaml


class Auth(object):
    def __init__(self, client_id, client_secret, access_token, config_fp):
        config = yaml.load(open(config_fp))
        print config
        
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
@click.argument('path', required=False)
@click.pass_obj
def ls(auth, path):
    print auth.client.folder(folder_id='0')


if __name__ == "__main__":
    cli()

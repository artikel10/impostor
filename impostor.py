#!/usr/bin/env python3

import click
import requests


SUMMARY_URL = 'https://onionoo.torproject.org/summary'
DETAILS_URL = 'https://onionoo.torproject.org/details'

METRICS_URL = 'https://metrics.torproject.org/rs.html#details/'


@click.command()
@click.argument('myfamily')
@click.option('--contact',
              help='Find relays with this string in the ContactInfo.',
              multiple=True)
@click.option('--nickname',
              help='Find relays with this string in the Nickname.',
              multiple=True)
def main(myfamily, contact, nickname):
    """Find Tor relays imitating your own relays.

    Invalid relays must:

    \b
    - Not be linked to a given MyFamily fingerprint.
    - Use a given ContactInfo or Nickname.
    - Be running.
    """
    valid_fingerprints = get_effective_family(myfamily)

    found_relays = {}
    for c in contact:
        relays = get_relays({'contact': c})
        found_relays.update({r['fingerprint']: r for r in relays})
    for n in nickname:
        relays = get_relays({'search': n})
        found_relays.update({r['fingerprint']: r for r in relays})
    found_fingerprints = set(found_relays.keys())

    invalid_fingerprints = found_fingerprints - valid_fingerprints
    invalid_relays = [found_relays[fp] for fp in invalid_fingerprints]
    invalid_relays = [r for r in invalid_relays if r['running']]

    if invalid_relays:
        click.echo('Impostors found:')
        for r in invalid_relays:
            click.echo(f'- {METRICS_URL}{r["fingerprint"]} {r["nickname"]}')
        click.get_current_context().exit(1)


def get_effective_family(fingerprint):
    """Return the effective family fingerprints."""
    headers = {'Accept-Encoding': 'gzip'}
    params = {'family': fingerprint}
    res = requests.get(SUMMARY_URL, headers=headers, params=params)
    res.raise_for_status()
    relays = res.json().get('relays', [])
    return {r['f'] for r in relays}


def get_relays(parameters):
    """Return the matching relay details."""
    headers = {'Accept-Encoding': 'gzip'}
    res = requests.get(DETAILS_URL, headers=headers, params=parameters)
    res.raise_for_status()
    return res.json().get('relays', [])


if __name__ == '__main__':
    main()

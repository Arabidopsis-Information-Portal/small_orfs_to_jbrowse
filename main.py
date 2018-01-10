import json
import os.path as op

import gff_utils as utils
import tools


def fail(message):
    # This is a simple failure message generator for generic ADAMA adapters
    # It will eventually be replaced with a system-wide fail function
    return 'text/plaintext; charset=ISO-8859-1', message


def search(args):
    q = args['q']
    chrom = args['chr']
    start = args['start']
    end = args['end']
    if start >= end:
        fail('End coordinate must be greater than start')
    strand = None if 'strand' not in args \
            else args['strand']
    featuretype = 'mRNA' if 'featuretype' not in args \
            else args['featuretype']
    level = 1 if 'level' not in args \
            else args['level']
    completely_within = False if 'completely_within' not in args \
            else args['completely_within']
    interbase = True if 'interbase' not in args \
            else args['interbase']

    if q == 'features':
        data = utils.parse_gff(chrom=chrom, start=start, \
            end=end, strand=strand, featuretype=featuretype, level=level, \
            completely_within=completely_within, interbase=interbase)


        if not data:
            return fail('Failed to parse gff')
    elif q == 'globalStats':
        data = { 'scoreMin': -1, 'scoreMax': 1 }
    elif q == 'regionStats':
        raise Exception('Not implemented yet')
    elif q == 'regionFeatureDensities':
        raise Exception('Not implemented yet')

    return 'application/json', tools.send_to_jbrowse(data)


def list(args):
    q = args['q']

    if q == 'listChromosomes':
        _url, token = args['_url'], args['_token']

        url = op.join(_url, 'aip', 'get_sequence_by_coordinate_v0.3', 'list')
        data = tools.do_request(url, token)
    elif q == 'makeTrackListJson':
        _url, namespace, adapter = args['_url'], args['_namespace'], args['_adapter']

        url = op.join(_url, namespace, adapter)
        data = {
            'plugins' : { 'Araport' : { 'location' : './plugins/Araport' } },
            'tracks' : utils.generate_config(url)
        }

    return 'application/json', json.dumps(data)

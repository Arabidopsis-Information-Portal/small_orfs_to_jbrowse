import os.path as op


SMALL_ORFS_GFF_FILE = op.join(op.dirname(__file__), 'data', 'pnas.1614788113_SupplementalDS1.gff3')


def read_index(gff_file, inmemory=False):
    """
    Read in a gffutils index for fast retrieval of features.
    """
    import gffutils
    from subprocess import call

    gff_file = SMALL_ORFS_GFF_FILE
    gff_file_db = "{0}.db".format(gff_file)
    gff_file_db_gz = "{0}.gz".format(gff_file_db)

    if inmemory:
        return gffutils.create_db(gff_file, ':memory:')

    if op.exists(gff_file_db_gz):
        call('gunzip {0}'.format(gff_file_db_gz), \
            shell=True, executable='/bin/bash')

    if op.exists(gff_file_db):
        return gffutils.FeatureDB(gff_file_db)

    return gffutils.create_db(gff_file, gff_file_db)


def parse_gff(chrom, start, end, strand, featuretype, level, completely_within, interbase):
    """Parse GFF and return JSON."""

    gff_file = SMALL_ORFS_GFF_FILE
    gffutils_db = read_index(gff_file)

    response_body = { 'features' : [] }
    region = "{0}:{1}-{2}".format(chrom, start, end)
    for parent in gffutils_db.region(region=region, strand=strand, featuretype=featuretype, \
        completely_within=completely_within):
        _strand = 1 if parent.strand == '+' else \
            (-1 if parent.strand == '-' else 0)
        pfeat = {
            'start' : (parent.start - 1) if interbase else parent.start,
            'end' : parent.end,
            'strand' : _strand,
            'uniqueID' : parent.id,
            'name' : parent.attributes.get('Name', [parent.id])[0],
            'description' : parent.attributes.get('Note', [None])[0],
            'peptide_sequence': parent.attributes.get('peptide_sequence', [None])[0],
            'expressed_in': parent.attributes.get('expressed_in', [None])[0],
            'type' : featuretype,
            'score' : parent.score if (isinstance(parent.score, (int, float))) else 0,
        }

        cfeats = dict()
        for _level in xrange(level, 0, -1):
            for child in gffutils_db.children(parent, order_by=('start'), level=_level):
                _strand = 1 if child.strand == '+' else \
                    (-1 if child.strand == '-' else 0)
                _parent = child.attributes.get('Parent')[0]
                if _parent not in cfeats: cfeats[_parent] = []
                cfeat = {
                    'start' : (child.start - 1) if interbase else child.start,
                    'end' : child.end,
                    'strand' : _strand,
                    'type' : child.featuretype,
                    'score' : child.score if (isinstance(child.score, (int, float))) else 0
                }
                if child.featuretype.endswith('codon') or child.featuretype == 'CDS':
                    cfeat['phase'] = child.frame
                if child.id in cfeats:
                    cfeat['subfeatures'] = cfeats[child.id]
                cfeats[_parent].append(cfeat)

        if parent.id in cfeats:
            pfeat['subfeatures'] = cfeats[parent.id]

        response_body['features'].append(pfeat)

    return response_body


def generate_config(api_url):
    """Generate the required trackList.json config stanzas for JBrowse"""

    config_template = {
        "style" : {
            "color" : "plum",
            "description" : "function( fObj, varName, gObj, tObj ) { return 'Expressed in ' + fObj.get('expressed_in'); }"
        },
        "key" : "Translated small ORFs (Hsu et al. 2016)",
        "storeClass" : "Araport/Store/SeqFeature/REST",
        "baseUrl" : "%(api_url)s",
        "type" : "JBrowse/View/Track/CanvasFeatures",
        "category" : "Community Data / Genomic Elements",
        "metadata" : {
            "Description" : "Super-resolution ribosome profiling reveals unannotated translation events in Arabidopsis",
            "Source" : "Hsu et al. 2016 (PNAS)",
            "URL" : "http://www.pnas.org/content/113/45/E7126.full"
        },
        "glyph" : "JBrowse/View/FeatureGlyph/Gene",
        "label" : "translated_small_ORFs_Hsu_et_al"
    }

    config = []
    config.append(replace_in_dict(config_template, { 'api_url' : api_url }))

    return config


def replace_in_dict(input, variables):
    """
    Method to replace placeholders in dict
    source: http://stackoverflow.com/questions/33046828/string-replace-format-placeholder-values-in-a-nested-python-dictionary
    """
    result = {}
    for key, value in input.iteritems():
        if isinstance(value, dict):
            result[key] = replace_in_dict(value, variables)
        else:
            result[key] = value % variables
    return result

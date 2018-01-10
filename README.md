Translated small ORFs to JBrowse web services
===

**Objective**: Build a simple web service which parses a standalone GFF3 file containing translated small ORFs reported in Hsu et al. (PNAS 2016), and returns this data in JBrowse compatible JSON format.

The adapter utilizes [gffutils](http://pythonhosted.org/gffutils/contents.html) to process the input GFF3 file, creating an intermediary sqlite database for fast data retrieval.

**Reference**:  
Hsu, Polly Yingshan, Lorenzo Calviello, Hsin-Yen Larry Wu, Fay-Wei Li, Carl J. Rothfels, Uwe Ohler, and Philip N. Benfey. **Super-resolution ribosome profiling reveals unannotated translation events in Arabidopsis**. *Proceedings of the National Academy of Sciences* 113, no. 45 (2016): E7126-E7135. doi:[10.1073/pnas.1614788113](http://www.pnas.org/content/113/45/E7126.full)

**Requirements**:
* Enable the following plugin in JBrowse within `tracks.conf`:
  * [Araport REST](https://github.com/Arabidopsis-Information-Portal/jbrowse/blob/stable/plugins/Araport/js/Store/SeqFeature/REST.js) with bindings to ADAMA
```
[plugins]
Araport.location = ./plugins/Araport
```

* This adapter relies on storing the GFF3 file corresponding to the annotated small ORFs in the `data/` sub-directory.
```
data/pnas.1614788113_SupplementalDS1.gff3
```
* Ensure that the [small_orfs_to_jbrowse](https://github.com/Arabidopsis-Information-Portal/small_orfs_to_jbrowse) adapter is registered and accessible via ADAMA. See [metadata.yml](metadata.yml) for adapter configuration (list of dependency modules and REST endpoints described using swagger.io spec).

* Set up the following track configuration in JBrowse within `trackList.json`:
```
{
  "style" : {
    "color" : "plum"
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
```

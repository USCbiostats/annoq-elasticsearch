import time
from elasticsearch import helpers, Elasticsearch
import json
import os
import sys
import pprint
from setup_es import es, ES_INDEX
#run python3 index_es_json test_input_json

def load_json(directory):
    
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            if name.endswith('.json'):
                print(os.path.join(root, name))
                with open(os.path.join(root, name), 'r') as open_file:
                    yield json.load(open_file) #not working
                    #but return works


def load_data_temp(a):
    return [{
        "_index": "vs-index",
        "_id": "X:60014T>C",
        "_source": {
            "chr": "X",
            "pos": 60014,
            "ref": "T",
            "alt": "C",
            "ANNOVAR_ensembl_Effect": "intergenic",
            "ANNOVAR_ensembl_Closest_gene(intergenic_only)": "NONE:NONE(dist=NONE),ENSG00000228572:ENST00000431238(dist=110396)",
            "ANNOVAR_ensembl_summary": ".(0):intergenic(1)",
            "SnpEff_ensembl_Effect": "intergenic_region",
            "SnpEff_ensembl_Effect_impact": "MODIFIER",
            "SnpEff_ensembl_Gene_name": "CHR_START-LL0YNC03-29C1.1",
            "SnpEff_ensembl_Gene_ID": "CHR_START-ENSG00000228572",
            "SnpEff_ensembl_HGVSc": "n.60014T>C",
            "SnpEff_ensembl_summary": "CHR_START-LL0YNC03-29C1.1(1):intergenic_region(1)",
            "VEP_ensembl_Consequence": "intergenic_variant",
            "VEP_ensembl_summary": ".(0):intergenic_variant(1)",
            "ANNOVAR_refseq_Effect": "intergenic",
            "ANNOVAR_refseq_Closest_gene(intergenic_only)": "NONE:NONE(dist=NONE),NONE:NONE:NONE(dist=NONE)",
            "ANNOVAR_refseq_summary": ".(0):intergenic(1)",
            "SnpEff_refseq_Effect": "intergenic_region",
            "SnpEff_refseq_Effect_impact": "MODIFIER",
            "SnpEff_refseq_Gene_name": "CHR_START-PLCXD1",
            "SnpEff_refseq_Gene_ID": "CHR_START-PLCXD1",
            "SnpEff_refseq_HGVSc": "n.60014T>C",
            "SnpEff_refseq_summary": "CHR_START-PLCXD1(1):intergenic_region(1)",
            "VEP_refseq_Consequence": "intergenic_variant",
            "VEP_refseq_summary": ".(0):intergenic_variant(1)",
            "ANNOVAR_ucsc_Effect": "intergenic",
            "ANNOVAR_ucsc_Closest_gene(intergenic_only)": "NONE:NONE(dist=NONE),NONE:NONE:NONE(dist=NONE)",
            "ANNOVAR_ucsc_summary": ".(0):intergenic(1)",
            "RegulomeDB_motif": "Motifs|PWM|TRF1",
            "RegulomeDB_score": "6",
            "CADD_raw": 0.204739,
            "CADD_phred": 5.912,
            "CADD_raw_rankscore": 0.74219,
            "fathmm-MKL_coding_score": 0.45077,
            "fathmm-MKL_coding_rankscore": 0.95953,
            "fathmm-MKL_coding_pred": "N",
            "fathmm-MKL_coding_group": "FI",
            "FANTOM5_enhancer_permissive": "N",
            "FANTOM5_enhancer_robust": "N",
            "FANTOM5_CAGE_peak_permissive": "N",
            "FANTOM5_CAGE_peak_robust": "N",
            "Ensembl_Regulatory_Build_feature_type": "TF_binding_site",
            "Ensembl_Regulatory_Build_ID": "ENSR00000420094",
            "Aloft_Confidenceflanking_0_GO_molecular_function_complete_list": ".."
        }
    }]

# pprint.pprint(list(load_json(sys.argv[1])))


start_time = time.time()
helpers.bulk(es, load_json( sys.argv[1]), index=ES_INDEX, chunk_size=1000, request_timeout=200)
print("--- %s seconds ---" % (time.time() - start_time))
load_json(sys.argv[1])

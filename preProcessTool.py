from BM25 import BM25Okapi
import helper
class preProcessTool():
    def __init__(self, model_AllenNLP_SRL,model_STANFORD, isGhaithOntology):
        from ontology_reader import Ontology_Separated
        self.ontology_list = Ontology_Separated()
        self.ttp_df = helper.create_mitre_TTP_dictionary()
        self.verb_dict, self.verb_list = helper.create_dictionary_from_file(filename='ontology/verb_list.txt')
        self.cyber_dict, self.cyber_list = helper.create_dictionary_from_file(filename='ontology/cyber_object_list.txt')

        if isGhaithOntology:
            self.prepare_ghaith_ontology()
        else:
            self.prepapre_ontology()

    def prepare_ghaith_ontology(self):
        from ontology_reader import ParseGhaithOntology
        ontology = ParseGhaithOntology()
        ontology_dict = ontology.read_csv()
        self.bm25_what_where_list, self.bm25_what_where_map = ontology.parse_ontology(ontology_dict)
        print(self.bm25_what_where_list)
        self.bm25_what_where = BM25Okapi(self.bm25_what_where_list)
        return

    def prepapre_ontology(self):
        from ontology_reader import Ontology_Separated
        from ontology_reader import utilities

        self.preprocessed_ontology = list()
        util = utilities()
        for i in self.ontology_list.df_list:
            self.preprocessed_ontology.append(util.lemmatize_and_stemm_whole_list(__list__=i, key_vector='', isLemmatize=True, isStem=True))
            # self.preprocessed_ontology.append(util.lemmatize_and_stemm_whole_list(__list__=i, key_vector='what', isLemmatize=True, isStem=True))
            # self.preprocessed_ontology.append(util.lemmatize_and_stemm_whole_list(__list__=i, key_vector='where', isLemmatize=True, isStem=True))
            # break
        self.bm25_how = BM25Okapi(self.preprocessed_ontology[0][1])
        self.bm25_why = BM25Okapi(self.preprocessed_ontology[1][1])
        self.bm25_what_where = BM25Okapi(self.preprocessed_ontology[2][1])

        self.bm25_how_map = self.preprocessed_ontology[0][0]
        self.bm25_why_map = self.preprocessed_ontology[1][0]
        self.bm25_what_where_map = self.preprocessed_ontology[2][0]

        # self.bm25_how = BM25Okapi(self.preprocessed_ontology[0][1])
        # self.bm25_how_where = BM25Okapi(self.preprocessed_ontology[1][1])
        # self.bm25_why = BM25Okapi(self.preprocessed_ontology[2][1])
        # self.bm25_why_where = BM25Okapi(self.preprocessed_ontology[3][1])
        # self.bm25_what_where = BM25Okapi(self.preprocessed_ontology[4][1])
        # self.bm25_what_where_where = BM25Okapi(self.preprocessed_ontology[5][1])
        #
        # self.bm25_how_map = self.preprocessed_ontology[0][0]
        # self.bm25_how_map_where = self.preprocessed_ontology[1][0]
        # self.bm25_why_map = self.preprocessed_ontology[2][0]
        # self.bm25_why_map_where = self.preprocessed_ontology[3][0]
        # self.bm25_what_where_map = self.preprocessed_ontology[4][0]
        # self.bm25_what_where_map_where = self.preprocessed_ontology[5][0]

        return


if __name__=='__main__':
    # preProcessTool()
    pass
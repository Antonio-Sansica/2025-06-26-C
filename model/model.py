from database.DAO import DAO
import networkx as nx
from model.constructor import Piazzamento


class Model:
    def __init__(self):
        self.mappa_nodi = {}
        self.grafo = nx.Graph()
        self.popola_mappa()


    def popola_mappa(self):
        # La chiami all'avvio o prima di fare il grafo
        lista_nodi = DAO.getAllNodi()
        for nodo in lista_nodi:
            self.mappa_nodi[nodo.constructorId] = nodo

    def get_oggetto_da_cache(self, id_cercato):
        return self.mappa_nodi.get(int(id_cercato), None)


    def get_years(self):
        return DAO.getAllYears()

    # Sostituisci il build_graph:
    def build_graph(self, anno1, anno2):
        self.grafo.clear()
        self.mappa_nodi = {}

        # STEP 1: Prendo tutti i costruttori
        lista_nodi = DAO.getAllNodi()

        # STEP 2: Riempio il dizionario per ogni costruttore
        for nodo in lista_nodi:
            # Chiamo il DAO per questo specifico nodo
            risultati = DAO.getRisultati(anno1, anno2, nodo.constructorId)

            for row in risultati:
                anno = row['year']
                p = Piazzamento(row['raceId'], row['driverId'], row['position'])

                # Se l'anno non c'è nel dizionario, lo inizializzo con lista vuota
                if anno not in nodo.risultati_per_anno:
                    nodo.risultati_per_anno[anno] = []

                # Aggiungo il piazzamento
                nodo.risultati_per_anno[anno].append(p)

            # Ora che il nodo è stato riempito, lo metto nella mappa e nel grafo
            self.mappa_nodi[nodo.constructorId] = nodo
            self.grafo.add_node(nodo)

        # PASSO 4: Collega (Avevi messo anno1, anno2, anno1, anno2... occhio alla traccia degli archi)
        archi_grezzi = DAO.get_archi_grafo_pesato(anno1, anno2, anno1, anno2)
        for id_1, id_2, peso in archi_grezzi:
            if id_1 in self.mappa_nodi and id_2 in self.mappa_nodi:
                n1 = self.mappa_nodi[id_1]
                n2 = self.mappa_nodi[id_2]
                self.grafo.add_edge(n1, n2, weight=peso)


    def get_dettagli_grafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()


    def get_componente_connessa_maggiore(self):
        # 1. Quante sono in totale?
        num_componenti = nx.number_connected_components(self.grafo)

        # 2. Ottengo una lista di "set" (insiemi) contenenti i nodi di ciascuna componente connessa
        componenti = list(nx.connected_components(self.grafo))

        # 3. Trovo quella più grande usando len() come chiave per la ricerca del massimo
        if not componenti:
            return 0, []
        comp_maggiore = max(componenti, key=len)

        return num_componenti, list(comp_maggiore)

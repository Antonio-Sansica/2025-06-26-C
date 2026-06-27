import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def populate_dd_iniziali(self):
        self._view._ddYear1.options.clear()
        self._view._ddYear2.options.clear()
        dati = self._model.get_years()
        for dato in dati:
            anno = dato
            self._view._ddYear1.options.append(ft.dropdown.Option(str(anno)))
            self._view._ddYear2.options.append(ft.dropdown.Option(str(anno)))
        self._view.update_page()

    def handleBuildGraph(self, e):
        # 1. LETTURA INPUT E CONTROLLO ERRORI
        valore_str = self._view._ddYear1.value
        valore2_str = self._view._ddYear2.value
        try:
            parametro_utente = int(valore_str)
            parametro2_utente = int(valore2_str)

        except ValueError:
            self._view.create_alert("Attenzione: Inserisci un numero valido!")
            return

        if parametro_utente > parametro2_utente:
            self._view.create_alert("Attenzione: il secondo numero deve essere maggiore del primo")
            return


        # 2. CHIAMATA AL MODEL
        self._model.build_graph(parametro_utente, parametro2_utente)

        # 3. PULIZIA SCHERMO E VERIFICA
        self._view._txt_result.controls.clear()

        if self._model.grafo.number_of_nodes() == 0:
            self._view._txt_result.controls.append(ft.Text("Nessun grafo creato con questi parametri."))
            self._view.update_page()
            return

        # 4. STAMPA DELLE RISPOSTE STANDARD
        nodi, archi = self._model.get_dettagli_grafo()
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con successo!", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Numero Nodi: {nodi}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero Archi: {archi}"))


        self._view.update_page()



    def handlePrintDetails(self, e):
        # b) Numero componenti connesse e componente maggiore
        num_comp, comp_maggiore = self._model.get_componente_connessa_maggiore()
        self._view._txt_result.controls.append(
            ft.Text(f"Componente più grande ({len(comp_maggiore)} nodi):", color="red"))

        # Stampa i nodi della componente maggiore (puoi stamparli come preferisci)
        # 1. Creiamo una funzione di supporto (o una funzione lambda) per calcolare il peso massimo di un nodo
        def get_peso_massimo_nodo(nodo):
            # Prendiamo tutti gli archi collegati a questo nodo
            archi_incidenti = self._model.grafo.edges(nodo, data=True)

            # Se il nodo è isolato (non ha archi), il suo peso massimo è 0
            if not archi_incidenti:
                return 0

            # Estraiamo il valore 'weight' da ogni arco e cerchiamo il massimo
            # (data_arco[2] contiene il dizionario degli attributi dell'arco, ad esempio {'weight': 45})
            pesi = [data_arco[2].get('weight', 0) for data_arco in archi_incidenti]
            return max(pesi)

        # 2. Ordiniamo la lista 'comp_maggiore' usando la nostra funzione come chiave di ordinamento
        # Usiamo reverse=True perché la traccia chiede l'ordine DECRESCENTE (dal più grande al più piccolo)
        comp_maggiore_ordinata = sorted(comp_maggiore, key=get_peso_massimo_nodo, reverse=True)

        # 3. Stampiamo i nodi ormai ordinati (ricordati di usare i campi corretti del tuo Constructor!)
        for nodo in comp_maggiore_ordinata:
            # Calcoliamo il peso massimo solo per poterlo stampare a schermo (utile per verificare se è giusto!)
            peso_max = get_peso_massimo_nodo(nodo)

            # Sostituito surname/driver_id/dob con i campi reali dell'oggetto Constructor (name, nationality)
            self._view._txt_result.controls.append(
                ft.Text(f"{nodo.name} ({nodo.nationality}) -- Peso Max Arco: {peso_max}")
            )
        self._view.update_page()

    def handleCercaTeamSfortunati(self, e):
        pass

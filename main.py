import json
import os
import sys

# Forzature grafiche stabili per il tuo PC
os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"
os.environ["KIVY_GRAPHICS"] = "gles"

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

NOME_FILE_JSON = "libreria.json"


class AppLibreriaAvanzata(App):

    def on_start(self):

        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        Window.bind(on_request_close=self.chiusura_pulita)

    def chiusura_pulita(self, *args):
        self.stop()
        sys.exit(0)

    def build(self):
        self.libro_selezionato_index = None
        self.ordine_corrente = {"colonna": "titolo", "inverso": False}

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # ---------------- 1. BARRA DI RICERCA + PULSANTE RESET ----------------
        barra_ricerca = BoxLayout(size_hint_y=None, height=40, spacing=5)
        lbl_cerca = Label(
            text="Cerca:", color=(0, 0, 0, 1), size_hint_x=None, width=50
        )
        self.input_ricerca = TextInput(
            hint_text="Digita per filtrare...", multiline=False
        )
        self.input_ricerca.bind(text=self.aggiorna_tabella)
        
        # Nuovo pulsante per uscire dalla ricerca / svuotare il campo
        btn_reset_cerca = Button(
            text="X",
            size_hint_x=None,
            width=40,
            background_color=(0.7, 0.2, 0.2, 1),
            background_normal="",
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_reset_cerca.bind(on_press=self.annulla_ricerca)
        
        barra_ricerca.add_widget(lbl_cerca)
        barra_ricerca.add_widget(self.input_ricerca)
        barra_ricerca.add_widget(btn_reset_cerca)
        root.add_widget(barra_ricerca)

        # ---------------- 2. DETTAGLI INSERIMENTO (CAMPI) ----------------
        campi_layout = GridLayout(cols=2, spacing=8, size_hint_y=None, height=160)

        campi_layout.add_widget(Label(text="Titolo:", color=(0, 0, 0, 1)))
        self.in_titolo = TextInput(multiline=False)
        campi_layout.add_widget(self.in_titolo)

        campi_layout.add_widget(Label(text="Autore:", color=(0, 0, 0, 1)))
        self.in_autore = TextInput(multiline=False)
        campi_layout.add_widget(self.in_autore)

        campi_layout.add_widget(Label(text="Genere:", color=(0, 0, 0, 1)))
        self.in_tipologia = TextInput(multiline=False)
        campi_layout.add_widget(self.in_tipologia)

        campi_layout.add_widget(Label(text="Posizione:", color=(0, 0, 0, 1)))
        self.in_posizione = TextInput(multiline=False)
        campi_layout.add_widget(self.in_posizione)

        root.add_widget(campi_layout)

        note_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=40, spacing=10
        )
        note_layout.add_widget(
            Label(text="Note:", color=(0, 0, 0, 1), size_hint_x=None, width=65)
        )
        self.in_note = TextInput(multiline=False)
        note_layout.add_widget(self.in_note)
        root.add_widget(note_layout)

        # ---------------- 3. PULSANTI COLORATI (CON TESTO SEMPRE LEGGIBILE) ----------------
        barra_pulsanti = BoxLayout(size_hint_y=None, height=45, spacing=10)

        btn_aggiungi = Button(
            text="Aggiungi libro",
            background_color=(0.18, 0.66, 0.35, 1),
            background_normal="",
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_aggiungi.bind(on_press=self.aggiungi_libro)

        # Fix colori: testo bianco forzato sia attivo che spento (opacità ridotta per lo stato disabilitato)
        self.btn_modifica = Button(
            text="Modifica libro",
            background_color=(0.9, 0.6, 0.1, 1),
            background_normal="",
            disabled=True,
            color=(1, 1, 1, 1),
            disabled_color=(1, 1, 1, 0.5), 
            background_disabled_normal="",
            bold=True
        )
        self.btn_modifica.bind(on_press=self.modifica_libro)

        self.btn_elimina = Button(
            text="Elimina libro",
            background_color=(0.82, 0.2, 0.2, 1),
            background_normal="",
            disabled=True,
            color=(1, 1, 1, 1),
            disabled_color=(1, 1, 1, 0.5),
            background_disabled_normal="",
            bold=True
        )
        self.btn_elimina.bind(on_press=self.elimina_libro)

        barra_pulsanti.add_widget(btn_aggiungi)
        barra_pulsanti.add_widget(self.btn_modifica)
        barra_pulsanti.add_widget(self.btn_elimina)
        root.add_widget(barra_pulsanti)

        # ---------------- 4. INTESTAZIONI COLONNE ORDINABILI ----------------
        intestazioni = BoxLayout(size_hint_y=None, height=35, spacing=2)
        colonne = ["Titolo", "Autore", "Genere", "Posizione", "Note"]

        for col in colonne:
            btn_col = Button(
                text=col,
                background_color=(0.2, 0.2, 0.2, 1),
                background_normal="",
                bold=True,
                color=(1, 1, 1, 1)
            )
            btn_col.bind(
                on_press=lambda instance, c=col.lower(): self.ordina_per(c)
            )
            intestazioni.add_widget(btn_col)
        root.add_widget(intestazioni)

        # ---------------- 5. TABELLA DEI DATI CON SCROLLBAR ----------------
        scroll = ScrollView(
            size_hint=(1, 1),
            bar_width="14dp",
            bar_color=[0.12, 0.53, 0.9, 0.9],
            bar_inactive_color=[0.12, 0.53, 0.9, 0.4],
            scroll_type=["bars", "content"],
        )

        self.griglia_dati = GridLayout(cols=5, spacing=2, size_hint_y=None)
        self.griglia_dati.bind(
            minimum_height=self.griglia_dati.setter("height")
        )
        scroll.add_widget(self.griglia_dati)
        root.add_widget(scroll)

        self.libri = self.carica_dati_json()
        self.aggiorna_tabella()

        return root

    # ---- AZIONE RESET CERCA ----
    def annulla_ricerca(self, instance):
        """Svuota la barra di ricerca ripristinando la lista completa."""
        self.input_ricerca.text = ""

    # ---- LOGICA DATI JSON ----
    def ottieni_percorso_json(self):
        # Rileva automaticamente se sei su PC o su Smartphone e sceglie la cartella corretta
        cartella_sicura = self.user_data_dir
        return os.path.join(cartella_sicura, NOME_FILE_JSON)

    def carica_dati_json(self):
        percorso = self.ottieni_percorso_json()
        if os.path.exists(percorso):
            try:
                with open(percorso, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def salva_dati_json(self):
        percorso = self.ottieni_percorso_json()
        with open(percorso, "w", encoding="utf-8") as f:
            json.dump(self.libri, f, indent=4, ensure_ascii=False)
        self.aggiorna_tabella()

    # ---- VISUALIZZAZIONE TABELLA ----
    def aggiorna_tabella(self, *args):
        self.griglia_dati.clear_widgets()
        testo_ricerca = self.input_ricerca.text.lower()

        libri_filtrati = []
        for idx, libro in enumerate(self.libri):
            # Cambia i valori sotto se le chiavi del tuo JSON hanno nomi o maiuscole differenti
            titolo = str(libro.get("titolo", libro.get("Titolo", "")))
            autore = str(libro.get("autore", libro.get("Autore", "")))
            tipologia = str(libro.get("tipologia", libro.get("Genere", "")))
            posizione = str(libro.get("posizione", libro.get("Posizione", "")))
            note = str(libro.get("note", libro.get("Note", "")))

            if (
                testo_ricerca in titolo.lower()
                or testo_ricerca in autore.lower()
                or testo_ricerca in tipologia.lower()
            ):
                libri_filtrati.append(
                    {
                        "originale_idx": idx,
                        "titolo": titolo,
                        "autore": autore,
                        "tipologia": tipologia,
                        "posizione": posizione,
                        "note": note,
                    }
                )

        col = self.ordine_corrente["colonna"]
        inv = self.ordine_corrente["inverso"]
        libri_filtrati.sort(key=lambda x: x[col].lower(), reverse=inv)

        for item in libri_filtrati:
            originale_idx = item["originale_idx"]
            campi_libro = [
                item["titolo"],
                item["autore"],
                item["tipologia"],
                item["posizione"],
                item["note"],
            ]

            sfondo_riga = (
                (0.7, 0.85, 1, 1)
                if self.libro_selezionato_index == originale_idx
                else (1, 1, 1, 1)
            )

            for campo in campi_libro:
                btn_cella = Button(
                    text=campo,
                    background_color=sfondo_riga,
                    background_normal="",
                    color=(0, 0, 0, 1),
                    halign="left",
                    valign="middle",
                    size_hint_y=None,
                    height=35,
                )
                btn_cella.bind(size=btn_cella.setter("text_size"))
                btn_cella.bind(
                    on_press=lambda instance, idx=originale_idx: self.seleziona_riga(
                        idx
                    )
                )
                self.griglia_dati.add_widget(btn_cella)

    def seleziona_riga(self, idx):
        self.libro_selezionato_index = idx
        libro = self.libri[idx]

        # REGOLE DI CARICAMENTO CORRETTE (Senza sovrascrivere gli oggetti Kivy)
        self.in_titolo.text = str(libro.get("titolo", libro.get("Titolo", "")))
        self.in_autore.text = str(libro.get("autore", libro.get("Autore", "")))
        self.in_tipologia.text = str(libro.get("tipologia", libro.get("Genere", "")))
        
        # FIX: Prima c'era self.in_posizione = str(...), che rompeva tutto!
        self.in_posizione.text = str(libro.get("posizione", libro.get("Posizione", "")))
        
        self.in_note.text = str(libro.get("note", libro.get("Note", "")))

        self.btn_modifica.disabled = False
        self.btn_elimina.disabled = False
        self.aggiorna_tabella()


        self.btn_modifica.disabled = False
        self.btn_elimina.disabled = False
        self.aggiorna_tabella()
    def svuota_campi(self):
        self.in_titolo.text = ""
        self.in_autore.text = ""
        self.in_tipologia.text = ""
        self.in_posizione.text = ""
        self.in_note.text = ""
        self.libro_selezionato_index = None
        self.btn_modifica.disabled = True
        self.btn_elimina.disabled = True
    def ordina_per(self, colonna):
        if self.ordine_corrente["colonna"] == colonna:
            self.ordine_corrente["inverso"] = not self.ordine_corrente["inverso"]
        else:
            self.ordine_corrente["colonna"] = colonna
            self.ordine_corrente["inverso"] = False
            self.aggiorna_tabella()
    def aggiungi_libro(self, instance):
        if self.in_titolo.text.strip() and self.in_autore.text.strip():
            nuovo = {
            "titolo": self.in_titolo.text.strip(),
            "autore": self.in_autore.text.strip(),
            "tipologia": self.in_tipologia.text.strip(),
            "posizione": self.in_posizione.text.strip(),
            "note": self.in_note.text.strip(),
            }
            self.libri.append(nuovo)
            self.svuota_campi()
            self.salva_dati_json()
    def modifica_libro(self, instance):
        if (
            self.libro_selezionato_index is not None
            and self.in_titolo.text.strip()
            and self.in_autore.text.strip()
            ):
            self.libri[self.libro_selezionato_index] = {
            "titolo": self.in_titolo.text.strip(),
            "autore": self.in_autore.text.strip(),
            "tipologia": self.in_tipologia.text.strip(),
            "posizione": self.in_posizione.text.strip(),
            "note": self.in_note.text.strip(),
            }
            self.svuota_campi()
            self.salva_dati_json()
    def elimina_libro(self, instance):
        if self.libro_selezionato_index is not None:
            self.libri.pop(self.libro_selezionato_index)
            self.svuota_campi()
            self.salva_dati_json()
if __name__ == "__main__":
    AppLibreriaAvanzata().run()

#il campo Genere nel database ha nome tipologia
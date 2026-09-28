import { useEffect, useState } from "react";
import styles from "./App.module.css";

function FicheIntervention({ intervention, titre }) {
  return (
    <div className={styles.interventionCard}>
      <h2 className={styles.resultTitle}>{titre}</h2>
      <dl className={styles.detailGrid}>
        <div className={styles.detailItem}>
          <dt>Client</dt>
          <dd>{intervention.client}</dd>
        </div>
        <div className={styles.detailItem}>
          <dt>Ville</dt>
          <dd>{intervention.ville}</dd>
        </div>
        <div className={styles.detailItem}>
          <dt>Type</dt>
          <dd>{intervention.type}</dd>
        </div>
        <div className={styles.detailItem}>
          <dt>Durée</dt>
          <dd>{intervention.duree} minutes</dd>
        </div>
        <div className={styles.detailItem}>
          <dt>Priorité</dt>
          <dd>
            <span className={styles.priority}>{intervention.priorite}</span>
          </dd>
        </div>
        <div className={`${styles.detailItem} ${styles.wideDetailItem}`}>
          <dt>Problème</dt>
          <dd>{intervention.probleme}</dd>
        </div>
        <div className={`${styles.detailItem} ${styles.wideDetailItem}`}>
          <dt>Action réalisée</dt>
          <dd>{intervention.action}</dd>
        </div>
      </dl>
    </div>
  );
}

function App() {
  const [rapport, setRapport] = useState("");
  const [resultat, setResultat] = useState(null);
  const [chargement, setChargement] = useState(false);
  const [historique, setHistorique] = useState([]);
  const [pageCourante, setPageCourante] = useState(1);
  const [interventionSelectionnee, setInterventionSelectionnee] =
    useState(null);
  const [erreur, setErreur] = useState("");

  async function chargerHistorique() {
    const response = await fetch("http://localhost:8000/historique");

    if (!response.ok) {
      throw new Error("Impossible de charger l'historique des interventions.");
    }

    const data = await response.json();
    setHistorique(data);
    setPageCourante(1);
  }

  async function chargerIntervention(id) {
    setErreur("");

    try {
      const response = await fetch(`http://localhost:8000/historique/${id}`);

      if (!response.ok) {
        throw new Error("Intervention introuvable.");
      }

      const data = await response.json();
      setInterventionSelectionnee(data);
    } catch (error) {
      setErreur(error.message);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setChargement(true);
    setErreur("");

    try {
      const response = await fetch("http://localhost:8000/analyser", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          rapport: rapport,
        }),
      });

      if (!response.ok) {
        throw new Error("Erreur lors de l'analyse du rapport.");
      }

      const data = await response.json();
      setResultat(data);
      await chargerHistorique();
    } catch (error) {
      setErreur(error.message);
    } finally {
      setChargement(false);
    }
  }

  useEffect(() => {
    fetch("http://localhost:8000/historique")
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            "Impossible de charger l'historique des interventions.",
          );
        }

        return response.json();
      })
      .then((data) => setHistorique(data))
      .catch((error) => setErreur(error.message));
  }, []);

  const interventionsParPage = 6;
  const nombrePages = Math.ceil(historique.length / interventionsParPage);
  const indexDebut = (pageCourante - 1) * interventionsParPage;
  const historiqueVisible = historique.slice(
    indexDebut,
    indexDebut + interventionsParPage,
  );

  return (
    <main className={styles.container}>
      <div className={styles.shell}>
        <header className={styles.header}>
          <p className={styles.eyebrow}>Assistant opérations</p>
          <h1 className={styles.title}>
            Analyse tes rapports d'intervention avec l'IA.
          </h1>
          <p className={styles.subtitle}>
            Transforme un compte rendu libre en intervention structurée et
            retrouve les analyses précédentes.
          </p>
        </header>

        <div className={styles.grid}>
          <section className={styles.panel}>
            <h2 className={styles.panelTitle}>Nouveau rapport</h2>
            <form className={styles.form} onSubmit={handleSubmit}>
              <label className={styles.label} htmlFor="rapport">
                Compte rendu de l'intervention
              </label>
              <textarea
                id="rapport"
                className={styles.textarea}
                value={rapport}
                onChange={(event) => setRapport(event.target.value)}
                placeholder="Décris le problème rencontré..."
                required
              />

              <button
                className={styles.button}
                type="submit"
                disabled={chargement}
              >
                {chargement ? "Analyse en cours..." : "Analyser le rapport"}
              </button>
            </form>

            {erreur && <p className={styles.error}>{erreur}</p>}

            {resultat && (
              <div className={styles.result}>
                <FicheIntervention
                  intervention={resultat}
                  titre="Résultat de l'analyse"
                />
              </div>
            )}
          </section>

          <section className={styles.panel}>
            <h2 className={styles.panelTitle}>Historique</h2>
            <ul className={styles.historyList}>
              {historiqueVisible.map((intervention) => (
                <li key={intervention.id}>
                  <button
                    className={styles.historyButton}
                    onClick={() => chargerIntervention(intervention.id)}
                  >
                    {intervention.client} - {intervention.type} -{" "}
                    {intervention.priorite}
                  </button>
                </li>
              ))}
            </ul>
            {nombrePages > 1 && (
              <div className={styles.pagination}>
                <button
                  className={styles.pageButton}
                  onClick={() => setPageCourante((page) => page - 1)}
                  disabled={pageCourante === 1}
                >
                  Précédent
                </button>
                <span className={styles.pageInfo}>
                  Page {pageCourante} sur {nombrePages}
                </span>
                <button
                  className={styles.pageButton}
                  onClick={() => setPageCourante((page) => page + 1)}
                  disabled={pageCourante === nombrePages}
                >
                  Suivant
                </button>
              </div>
            )}
            <button
              className={`${styles.button} ${styles.secondaryButton}`}
              onClick={chargerHistorique}
            >
              Actualiser l'historique
            </button>

            {interventionSelectionnee && (
              <div className={styles.detail}>
                <FicheIntervention
                  intervention={interventionSelectionnee}
                  titre="Détail de l'intervention"
                />
              </div>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}
export default App;

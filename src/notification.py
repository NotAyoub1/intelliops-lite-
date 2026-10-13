from src.contrat import Analyse, Evenement, Notification
def choisir_canal(criticite: str) -> str:
    if criticite in ("CRITICAL", "HIGH"):
        return "TEAMS"
    if criticite == "MEDIUM":
        return "EMAIL"
    if criticite == "LOW":
        return "DASHBOARD"
    raise ValueError(f"Criticité inconnue : {criticite}")
def rediger(evt: Evenement, analyse: Analyse) -> str:
    lignes = [
        f"[{analyse.criticite}] Service : {evt.component}",
        f"Incident : {evt.message}",
        f"Cause probable : {analyse.cause_probable}",
        f"Action : {analyse.action_recommandee}",
        f"Sources : {', '.join(analyse.sources)}",
    ]
    return "\n".join(lignes)
def notifier(evt: Evenement, analyse: Analyse, journal: list) -> Notification:
    raise NotImplementedError
def demander_validation(analyse: Analyse, reponse: str) -> bool:
    if not analyse.sensible:
        return True
    return reponse.strip().lower() in {"o", "oui", "y", "yes"}
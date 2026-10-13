import re 
from src.contrat import Analyse, Evenement
def est_doublon(evt: Evenement, deja_vus: set) -> bool:
    cle = (evt.source, evt.component, evt.event_type, evt.message)
    if cle in deja_vus:
        return True
    deja_vus.add(cle)
    return False
def rechercher_runbook(evt: Evenement, base: dict):
    message = evt.message.lower()
    for mot_cle, procedure in base.items():
        if mot_cle.lower() in message:
            return procedure
    return None
def _nombre_redemarrages(message: str) -> int:
    m = re.search(r"restarts=(\d+)", message)
    return int(m.group(1)) if m else 0


def classer(evt: Evenement) -> str:
    if evt.event_type == "CONTAINER_RESTART":
        return "CRITICAL" if _nombre_redemarrages(evt.message) > 100 else "MEDIUM"
    if evt.event_type == "VULNERABILITY" and evt.severity == "CRITICAL":
        return "HIGH"
    return evt.severity
def analyser(evt: Evenement, base: dict) -> Analyse:
    criticite = classer(evt)
    cause = rechercher_runbook(evt, base) or "Cause inconnue : analyse manuelle requise"
    if evt.event_type == "CONTAINER_RESTART":
        action = f"Redémarrer {evt.component}"
    elif evt.event_type == "VULNERABILITY":
        action = "Mettre à jour la dépendance"
    else:
        action = "Consulter les logs"
    evt.status = "ANALYSED"
    return Analyse(evt.id, criticite, cause, action,
                   criticite in ("HIGH", "CRITICAL"), [evt.source])
import logging
from client import SeekApiClient
from typing import List, Dict


def test_seek_api_client():
    # Remplace par ta clé API réelle ou une clé de test appropriée
    api_key = "WVpjSU41RUJFVDR2U1lGcmpLRmI6c3Y1dmNISF9RMC1UX2JlQjg5blFFZw=="

    # Crée une instance du client
    client = SeekApiClient(api_key)

    # Exemple de chaîne de recherche
    search_string = "playzou"

    # Effectue une recherche
    documents = client.search_documents(search_string, display_filename=True, size=10)

    # Affiche les documents trouvés
    logging.info(f"Documents found: {documents}")

    # Extrait les informations des documents
    extracted_info = client.extracted_search(documents)

    # Affiche les informations extraites
    logging.info(f"Extracted information: {extracted_info}")

    assert isinstance(extracted_info.emails, list), "Emails should be a list"
    assert isinstance(extracted_info.phones, list), "Phones should be a list"
    assert isinstance(
        extracted_info.fivem_licenses, list
    ), "FiveM licenses should be a list"
    assert isinstance(extracted_info.steam_ids, list), "Steam IDs should be a list"

    # Affiche les informations extraites
    logging.info(f"Emails: {extracted_info.emails}")
    logging.info(f"Phones: {extracted_info.phones}")
    logging.info(f"FiveM Licenses: {extracted_info.fivem_licenses}")
    logging.info(f"Steam IDs: {extracted_info.steam_ids}")


if __name__ == "__main__":
    # Configure le niveau de logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Exécute le test
    test_seek_api_client()

# SeekApiClient

## Introduction

Le package `Seekbaseapi` est conçu pour interagir avec l'API SeekBASE, permettant de rechercher et d'extraire des informations spécifiques (comme les emails, numéros de téléphone, licences FiveM et identifiants Steam) à partir de documents. Ce package est particulièrement utile pour analyser des contenus textuels à grande échelle.

## Installation

Pour installer ce package, assurez-vous d'avoir Python 3.7+ et utilisez pip:

```bash
pip install seekbaseapi
```

## Utilisation

### Initialisation du client

Pour commencer à utiliser `SeekApiClient`, vous devez initialiser le client avec une clé API valide.

```python
from seekbaseapi import SeekApiClient

api_key = "api_key"
client = SeekApiClient(api_key)
```

### Recherche de documents

Vous pouvez rechercher des documents dans la base de données SeekBASE en utilisant la méthode `search_documents`. Cette méthode prend en paramètre une chaîne de recherche, un booléen pour afficher le nom du fichier, et la taille des résultats à retourner.

```python
search_string = "votre_chaine_de_recherche"
documents = client.search_documents(search_string, display_filename=True, size=10000)
```

### Extraction d'informations

Après avoir obtenu les documents, vous pouvez extraire les informations spécifiques telles que les e-mails, numéros de téléphone, licences FiveM et identifiants Steam en utilisant la méthode `extracted_search`.

```python
extracted_info = client.extracted_search(documents)

print("Emails:", extracted_info.emails)
print("Phones:", extracted_info.phones)
print("FiveM Licenses:", extracted_info.fivem_licenses)
print("Steam IDs:", extracted_info.steam_ids)
```

## Classe et Méthodes

### `SeekApiClient`

- **`__init__(api_key: str)`**

  - Initialise le client SeekBASE avec la clé API fournie.
  - **Paramètres**:
    - `api_key` (str): La clé API pour accéder à SeekBASE.

- **`search_documents(search_string: str, display_filename: bool = False, size: int = 10000) -> List[Dict[str, Any]]`**

  - Recherche des documents dans SeekBASE en fonction de la chaîne de recherche fournie.
  - **Paramètres**:
    - `search_string` (str): La chaîne de recherche à utiliser dans la requête.
    - `display_filename` (bool): Affiche le nom du fichier si True.
    - `size` (int): Le nombre de résultats à retourner.
  - **Retourne**:
    - Liste de dictionnaires représentant les documents trouvés.

- **`extracted_search(documents: List[Dict[str, Any]]) -> ExtractedInfo`**
  - Traite les résultats de la recherche pour extraire les informations spécifiques.
  - **Paramètres**:
    - `documents` (List[Dict[str, Any]]): Liste des documents trouvés.
  - **Retourne**:
    - Un objet `ExtractedInfo` contenant les e-mails, numéros de téléphone, licences FiveM et identifiants Steam trouvés.

### `ExtractedInfo`

- **Attributs**:
  - `emails` (List[str]): Liste des e-mails extraits.
  - `phones` (List[str]): Liste des numéros de téléphone extraits.
  - `fivem_licenses` (List[str]): Liste des licences FiveM extraites.
  - `steam_ids` (List[str]): Liste des identifiants Steam extraits.

## Exemples

```python
from seekbaseapi import SeekApiClient

api_key = "api_key"
client = SeekApiClient(api_key)

search_string = "votre_chaine_de_recherche"
documents = client.search_documents(search_string, display_filename=True, size=10000)

extracted_info = client.extracted_search(documents)

print("Emails:", extracted_info.emails)
print("Phones:", extracted_info.phones)
print("FiveM Licenses:", extracted_info.fivem_licenses)
print("Steam IDs:", extracted_info.steam_ids)
```

Formatage des Numeros de Telephone
Les numeros de telephone sont formates dans le format (XXX) XXX-XXXX pour une meilleure lisibilite.

## Gestion des Erreurs

Le package gere plusieurs types d'erreurs :

RequestError : Erreurs liees aux requetes SEEKBASE.
JSONDecodeError : Erreurs de decodage JSON lorsque le contenu ne peut pas etre transforme en JSON.
TypeError : Erreurs liees aux types de donnees lors du traitement du contenu.
Les erreurs sont signalees avec des messages clairs pour faciliter le debogage.

## Assistance

Pour toute aide ou question, veuillez rejoindre notre serveur Discord : https://discord.gg/6jAaqjpJ3x

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

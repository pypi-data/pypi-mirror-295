import re
import json
import urllib3
import logging
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
from typing import List, Dict, Set, Any
from tenacity import retry, wait_fixed, stop_after_attempt
from pydantic import BaseModel, EmailStr

__all__ = ["SeekApiClient"]

urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ExtractedInfo(BaseModel):
    emails: Set[EmailStr]
    phones: Set[str]
    fivem_licenses: Set[str]
    steam_ids: Set[str]
    ips: Set[str]
    fivem_ids: Set[str]
    xbl: Set[str]


class SeekApiClient:
    def __init__(self, api_key: str):
        """
        Initialise le client SeekBase avec la clé API.

        :param api_key: La clé API pour accéder à SeekBase.
        """
        self._host = "api.seekbase.shop"
        self._api_key = api_key
        self.client = self._create_client()

    def _create_client(self) -> Elasticsearch:
        """
        Crée une instance du client SeekBase.

        :return: Instance du client SeekBase.
        :raises ValueError: Si la clé API n'est pas fournie.
        """
        if not self._api_key:
            raise ValueError("Please provide an API key!")
        return Elasticsearch(
            [f"https://{self._host}:9200"],
            api_key=self._api_key,
            verify_certs=False,
        )

    @staticmethod
    def _filter_infos(
        response: Dict[str, Any], include_filename: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Filtre les résultats de la requête API en fonction des éléments de la BLACKLIST et
        inclut ou non le nom du fichier selon le paramètre `include_filename`.

        :param response: Résultat de la requête SeekBase.
        :param include_filename: Booléen pour indiquer si le nom du fichier doit être inclus.
        :return: La liste des résultats filtrés sous forme de dictionnaires.
        """

        results: List[Dict[str, Any]] = []

        for result in response.get("hits", {}).get("hits", []):
            source = result.get("_source", {})
            content = source.get("content", "")
            filename = source.get("filename", "")

            result_dict = {"content": content}
            if include_filename:
                result_dict["filename"] = filename

            results.append(result_dict)

        return results

    @retry(wait=wait_fixed(10), stop=stop_after_attempt(5))
    def search_documents(
        self, search_string: str, display_filename: bool = False, size: int = 10000
    ) -> List[Dict[str, Any]]:
        """
        Recherche des documents dans SeekBase en fonction de la chaîne de recherche fournie.

        :param search_string: La chaîne de recherche à utiliser dans la requête.
        :param display_filename: Affiche le nom du fichier si True.
        :param size: Le nombre de résultats à retourner.
        :return: Liste des documents trouvés.
        """
        search_query = {
            "size": size,
            "query": {
                "bool": {
                    "must": {"match_phrase": {"content": search_string}},
                    "must_not": [
                        {"match_phrase": {"content": "</code>"}},
                        {"match_phrase": {"content": "</script>"}},
                    ],
                }
            },
        }

        if display_filename:
            search_query["_source"] = ["filename", "content"]

        try:
            response = self.client.search(index="searcher", body=search_query)
            return self._filter_infos(response, include_filename=display_filename)
        except RequestError as e:
            logging.error(f"Request error: {e.info}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        return []

    @staticmethod
    def _format_phone_number(number: str) -> str:
        """
        Formate un numéro de téléphone au format (XXX) XXX-XXXX.

        :param number: Le numéro de téléphone à formater.
        :return: Le numéro de téléphone formaté.
        """
        digits = re.sub(r"\D", "", number)
        if len(digits) != 10:
            return number
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

    @staticmethod
    def _is_local_ip(ip: str) -> bool:
        octets = list(map(int, ip.split(".")))
        if (
            octets[0] == 127
            or octets[0] == 10
            or (octets[0] == 192 and octets[1] == 168)
            or (octets[0] == 172 and 16 <= octets[1] <= 31)
        ):
            return True
        return False

    def extracted_search(self, documents: List[Dict[str, Any]]) -> ExtractedInfo:
        """
        Traite les résultats de la recherche pour extraire les informations spécifiques.

        :param documents: Liste des documents trouvés, chaque document contenant le contenu et le nom de fichier.
        :return: Dictionnaire contenant les e-mails, numéros de téléphone, identifiants Steam, licences FiveM, et adresses IP trouvés.
        """

        text = str([doc.get("content", "") for doc in documents])

        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        phone_pattern = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
        ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
        steam_pattern = r"steam:([A-Za-z0-9]+)"
        license_pattern = r"license\d*:(\w{32,})"
        fiveid_pattern = r"fivem:[0-9]+"
        xbl_pattern = r"xbl:[0-9]+"

        emails = set(re.findall(email_pattern, text))
        phones = set(re.findall(phone_pattern, text))
        ips = set(
            [ip for ip in re.findall(ip_pattern, text) if not self._is_local_ip(ip)]
        )
        steam_ids = set(re.findall(steam_pattern, text))
        fivem_licenses = set(re.findall(license_pattern, text))
        fivem_ids = set(re.findall(fiveid_pattern, text))
        xbl = set(re.findall(xbl_pattern, text))

        formatted_phones = set([self._format_phone_number(phone) for phone in phones])

        return ExtractedInfo(
            emails=emails,
            phones=formatted_phones,
            fivem_licenses=fivem_licenses,
            steam_ids=steam_ids,
            ips=ips,
            fivem_ids=fivem_ids,
            xbl=xbl,
        )

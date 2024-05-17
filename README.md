 # Toolbox PROJDEN

## Description du Projet

Ce projet est un outil d'audit de sécurité réseau conçu pour effectuer diverses tâches de reconnaissance et d'analyse de vulnérabilités sur une cible spécifiée (adresse IP ou nom de domaine). Les fonctionnalités incluent la résolution de noms de domaine, la recherche des serveurs de noms, le scan de ports avec Nmap, l'analyse de vulnérabilités, et l'attaque par force brute avec Hydra.

## Fonctionnalités

- **Résolution de noms de domaine :** Conversion d'un nom de domaine en adresse IP et recherche des serveurs de noms.
- **Résolution d'adresses IP :** Conversion d'une adresse IP en nom d'hôte.
- **Scan de ports avec Nmap :** Identification des ports ouverts et des services associés.
- **Analyse de vulnérabilités :** Utilisation de Nmap avec le script Vulners pour identifier les vulnérabilités sur les 
                                  ports ouverts.
- **Attaque par force brute :** Utilisation d'Hydra pour effectuer des attaques par force brute sur les services SSH, FTP et 
  Telnet.
- **Génération de rapports :** Création de rapports détaillés en PDF résumant les résultats de l'audit.

La Toolbox PROJDEN offre une suite complète de fonctionnalités permettant d'identifier les ports ouverts et les services associés, de résoudre les noms de domaine en adresses IP, de détecter les vulnérabilités à l'aide du script Vulners, d'exécuter des attaques par force brute sur les services SSH et FTP, et de compiler ces résultats dans un rapport PDF détaillé.

## Instructions
- **Type d'audit :** Vous serez invité à choisir entre un audit sur une adresse IP ou un nom de domaine.
- **Entrée cible :** Entrez l'adresse IP ou le nom de domaine cible.
- **Résultats du scan :** Les résultats du scan de ports et de l'analyse de vulnérabilités seront affichés.
- **Attaque par force brute :** Vous pouvez choisir de lancer des attaques par force brute sur les services détectés.
- **Génération de rapport :** Vous aurez l'option de générer un rapport en PDF des résultats de l'audit.



## Prérequis

**Voici les prérequis pour ce projet :**

Python 3.x : Assurez-vous d'avoir Python 3.x installé sur votre système pour exécuter le script.

Modules Python : Les modules suivants doivent être installés pour garantir le bon fonctionnement du projet :
- nmap
- socket
- subprocess
- re
- prettytable
- reportlab
- pexpect
- json
- dns (dns.resolver)

Ces modules fournissent les fonctionnalités nécessaires pour effectuer des scans de ports, analyser les résultats, générer des rapports, et bien plus encore. Vous pouvez installer ces modules via pip avec la commande suivante :

**Pour installer les modules requis, vous pouvez utiliser la commande suivante:**
```sh
pip install nmap prettytable reportlab pexpect dns
```

## Scripts et Fonctions

- **resolve_hostname(hostname):** Résout un nom de domaine en adresse IP et trouve les serveurs de noms.
- **get_hostname(ip_address):** Résout une adresse IP en un nom d'hôte et trouve les serveurs de noms.
- **perform_basic_nmap_scan(target):** Effectue un scan Nmap basique pour identifier les ports ouverts et les services.
- **parse_basic_nmap_results(raw_data):** Analyse les résultats bruts du scan Nmap en données structurées.
- **scan_vulnerabilities(target):** Scanne les vulnérabilités sur les ports ouverts en utilisant le script Vulners.
- **extract_vulners_data(raw_data):** Extrait les données pertinentes de la sortie Nmap Vulners pour l'affichage.
- **format_results_to_table(basic_results, port_cve_mapping):** Formate et affiche les résultats dans une table.
- **run_hydra(target, port, service):** Exécute Hydra pour effectuer une attaque par force brute et capture les résultats.
- **parse_hydra_results(hydra_output):** Analyse la sortie d'Hydra pour extraire les connexions réussies.
- **check_and_bruteforce(basic_results, target):** Vérifie les ports SSH ou FTP ouverts et propose une attaque par force brute.
- **main():** Fonction principale qui orchestre l'exécution du script selon les choix de l'utilisateur.

## Génération de Rapports
Si vous choisissez de générer un rapport PDF, les résultats du scan seront sauvegardés dans un fichier report_data.json. Ensuite, un script externe generate_report.py sera exécuté pour créer le rapport PDF.

**Pour générer le rapport PDF manuellement, exécutez:**
```sh
python3 generate_report.py
```
## generate_report.py
Ce script utilise les données sauvegardées dans report_data.json pour générer un rapport PDF structuré avec les résultats de l'audit.

## Notes
**Sécurité:** L'utilisation de cet outil doit être autorisée par le propriétaire du réseau ou du domaine. Une utilisation non autorisée est illégale.
**Précautions:** Soyez prudent lors de l'exécution des attaques par force brute, car elles peuvent être détectées comme des comportements malveillants par les systèmes de sécurité réseau.




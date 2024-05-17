 # Toolbox PROJDEN

## Description du Projet

La Toolbox PROJDEN est un outil complet d'audit de sécurité réseau qui permet de scanner les vulnérabilités, d'effectuer des tests de force brute sur les services SSH et FTP, et de générer des rapports détaillés en format PDF. Cet outil est conçu pour aider les administrateurs réseau et les professionnels de la sécurité à identifier et à atténuer les vulnérabilités potentielles dans leur infrastructure.

## Fonctionnalités

- **Scan de ports ouverts**: Identifie les ports ouverts sur la cible et les services qui y sont associés.
- **Résolution DNS**: Convertit les noms de domaine en adresses IP et trouve les serveurs de noms.
- **Scan des vulnérabilités**: Utilise le script Vulners pour détecter les vulnérabilités associées aux ports ouverts.
- **Attaque par force brute**: Exécute des attaques par force brute sur les services SSH et FTP pour identifier les identifiants valides.
- **Génération de rapport PDF**: Compile les résultats du scan et les détails des vulnérabilités dans un rapport PDF complet.

La Toolbox PROJDEN offre une suite complète de fonctionnalités permettant d'identifier les ports ouverts et les services associés, de résoudre les noms de domaine en adresses IP, de détecter les vulnérabilités à l'aide du script Vulners, d'exécuter des attaques par force brute sur les services SSH et FTP, et de compiler ces résultats dans un rapport PDF détaillé.

## Prérequis

- Python 3.x
- Modules Python:
  - nmap
  - socket
  - subprocess
  - re
  - prettytable
  - reportlab
  - pexpect
  - json
  - dns

**Pour installer les modules requis, vous pouvez utiliser la commande suivante:**
```sh
pip install python-nmap prettytable reportlab pexpect dnspython
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




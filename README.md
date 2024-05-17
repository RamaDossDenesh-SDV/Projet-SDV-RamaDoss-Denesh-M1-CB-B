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

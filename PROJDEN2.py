#!/usr/bin/python3

import nmap
import socket
import subprocess
import re
from prettytable import PrettyTable
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pexpect
import json
import time
import dns.resolver

# Configuration des styles de texte pour le rapport PDF
styles = getSampleStyleSheet()

# Définition des couleurs pour les messages console
class Colors:
    HEADER = '\033[95m'  # Violet
    OKBLUE = '\033[94m'  # Bleu
    OKGREEN = '\033[92m'  # Vert
    WARNING = '\033[93m'  # Jaune
    ORANGE = '\033[38;5;208m'
    FAIL = '\033[91m'  # Rouge
    ENDC = '\033[0m'  # Réinitialiser la couleur
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(Colors.OKGREEN + """
###########################################################################################
▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░░▌      ▐░▌
▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀▀█░█▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌░▌     ▐░▌
▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌      ▐░▌    ▐░▌       ▐░▌▐░▌          ▐░▌▐░▌    ▐░▌
▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌      ▐░▌    ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌ ▐░▌   ▐░▌
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌      ▐░▌    ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀█░█▀▀ ▐░▌       ▐░▌      ▐░▌    ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌   ▐░▌ ▐░▌
▐░▌          ▐░▌     ▐░▌  ▐░▌       ▐░▌      ▐░▌    ▐░▌       ▐░▌▐░▌          ▐░▌    ▐░▌▐░▌
▐░▌          ▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄█░▌    ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌     ▐░▐░▌
▐░▌          ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░▌    ▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░▌      ▐░░▌
 ▀            ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀      ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀ 
###########################################################################################
===========================Bienvenue sur la Toolbox PROJDEN==============================
###########################################################################################
Cette outil vous permettre d'effectuer une audit complète des vulnérabilités present sur votre réseau ou site internet.

Données que vous pouvez avoir avec cette outils : 

           - Les ports ouverts sur le réseau

           - Trouver le nom de domaine correspondant au IP ou l'IP correspondant au nom de domaine

           - CVE (Une liste publique de failles de sécurité informatique)

           - Possibilité d'effectuer une attaque Brute force sur le port SSH, FTP et Telnet

           - Générer un rapport complet au format PDF
""" + Colors.ENDC)


def resolve_hostname(hostname):
    """Résoudre le nom de domaine en une adresse IP et trouver les serveurs de noms."""
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"{Colors.ORANGE}>>> L'adresse IP pour {hostname} est {ip_address}{Colors.ENDC}")
        
        # Recherche des serveurs de noms
        try:
            answers = dns.resolver.resolve(hostname, 'NS')
            name_servers = [str(rdata) for rdata in answers]
            print(f"{Colors.FAIL}>>> Les serveurs de noms pour {hostname} sont : {', '.join(name_servers)}{Colors.ENDC}")
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            print(f"{Colors.FAIL}>>> Nom de serveur non trouvé pour {hostname}.{Colors.ENDC}")

        return ip_address
    except socket.gaierror:
        print(f"{Colors.OKBLUE}>>> Erreur de résolution de nom. Veuillez vérifier le nom de domaine entré.{Colors.ENDC}")
        return None

def get_hostname(ip_address):
    """Résoudre l'adresse IP en un nom d'hôte et trouver les serveurs de noms."""
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        print(f"{Colors.OKBLUE}>>> Le nom de la machine pour l'adresse IP {ip_address} est {hostname}{Colors.ENDC}")

        # Recherche des serveurs de noms
        try:
            answers = dns.resolver.resolve(hostname, 'NS')
            name_servers = [str(rdata) for rdata in answers]
            print(f"{Colors.ORANGE}>>> Les serveurs de noms pour {hostname} sont : {', '.join(name_servers)}{Colors.ENDC}")
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            print(f"{Colors.OKBLUE}>>> Nom de serveur non trouvé pour {hostname}.{Colors.ENDC}")

        return hostname
    except socket.herror:
        print(f"{Colors.HEADER}>>> Erreur de résolution du nom de la machine. Aucune correspondance trouvée pour l'adresse IP {ip_address}.{Colors.ENDC}")
        print(f"{Colors.HEADER}>>> Nous allons poursuivre avec la partie Scan Nmap{ip_address}.{Colors.ENDC}")
        return None

def perform_basic_nmap_scan(target):
    """Effectuer un scan Nmap basique pour identifier les ports ouverts et les services."""
    basic_scan = f"nmap -Pn -sV {target}"
    result = subprocess.run(basic_scan, shell=True, text=True, capture_output=True)
    return result.stdout

def parse_basic_nmap_results(raw_data):
    """Analyser les résultats bruts du scan Nmap en données structurées."""
    lines = raw_data.split('\n')
    results = []
    for line in lines:
        if 'open' in line and 'tcp' in line:
            parts = line.split()
            port_info = parts[0]
            state = parts[1]
            service = parts[2] if len(parts) > 2 else ''
            version = ' '.join(parts[3:]) if len(parts) > 3 else ''
            results.append([port_info, state, service, version])
    return results

def scan_vulnerabilities(target):
    """Scanner les vulnérabilités sur les ports ouverts en utilisant le script Vulners."""
    vulners_scan = f"nmap -Pn -sV --script vulners --script-args mincvss=5.0 {target}"
    result = subprocess.run(vulners_scan, shell=True, text=True, capture_output=True)
    return result.stdout

def extract_vulners_data(raw_data):
    """Extraire les données pertinentes de la sortie Nmap Vulners pour l'affichage."""
    lines = raw_data.split('\n')
    port_cve_mapping = {}
    current_port = None

    for line in lines:
        if 'tcp' in line and 'open' in line:
            parts = line.split()
            current_port = parts[0].split('/')[0]  # Extraire le numéro de port
        elif 'CVE' in line and current_port:
            if current_port not in port_cve_mapping:
                port_cve_mapping[current_port] = []
            port_cve_mapping[current_port].append(line.strip())

    return port_cve_mapping

def format_results_to_table(basic_results, port_cve_mapping):
    """Formater et afficher les résultats dans une table, et afficher les CVE séparément."""
    table = PrettyTable()
    table.field_names = ["Port", "State", "Service", "Version"]

    for result in basic_results:
        table.add_row(result)

    print("\n" + Colors.ORANGE + "[-] Résultats du scan Nmap de base :" + Colors.ENDC)
    print(table)

    print("\n" + Colors.ORANGE + "[-] Résultats détaillés des CVE :" + Colors.ENDC)
    for port, cves in port_cve_mapping.items():
        print(f"\nPort {port}")
        for cve in cves:
            print(f"|       {cve}")

    return table.get_string(), port_cve_mapping

def run_hydra(target, port, service):
    """Exécuter Hydra pour effectuer une attaque par force brute et capturer les résultats."""
    hydra_command = f"hydra -L identifiant.txt -P mdp.txt {target} -s {port} {service}"
    result = subprocess.run(hydra_command, shell=True, text=True, capture_output=True)
    return result.stdout

def parse_hydra_results(hydra_output):
    """Analyser la sortie d'Hydra pour extraire les connexions réussies."""
    results = []
    lines = hydra_output.split('\n')
    for line in lines:
        if "login:" in line and "password:" in line:
            parts = line.split()
            try:
                login_index = parts.index("login:") + 1
                password_index = parts.index("password:") + 1
                login = parts[login_index]
                password = parts[password_index]
                results.append((login, password))
            except (ValueError, IndexError):
                continue
    return results

def check_and_bruteforce(basic_results, target):
    """Vérifier les ports SSH, FTP ou Telnet ouverts et proposer une attaque par force brute."""
    services_open = {"SSH": None, "FTP": None, "Telnet": None}
    brute_force_results = {"SSH": [], "FTP": [], "Telnet": []}

    for result in basic_results:
        port, _, service, _ = result
        if service == "ssh":
            services_open["SSH"] = port.split('/')[0]
        elif service == "ftp":
            services_open["FTP"] = port.split('/')[0]
        elif service == "telnet":
            services_open["Telnet"] = port.split('/')[0]

    # Lister les services ouverts
    open_services = [f"{service} (port {port})" for service, port in services_open.items() if port]
    
    if open_services:
        user_choice = input(f"{Colors.ORANGE}Voici les ports ouverts : {', '.join(open_services)}. Voulez-vous effectuer une brute force sur ces ports ? (Oui/Non): {Colors.ENDC}").strip().lower()
        if user_choice == 'oui':
            for service, port in services_open.items():
                if port:
                    specific_choice = input(f"{Colors.ORANGE}Voulez-vous effectuer une brute force sur le port {port} pour le service {service}? (Oui/Non): {Colors.ENDC}").strip().lower()
                    if specific_choice == 'oui':
                        hydra_output = run_hydra(target, port, service.lower())
                        results = parse_hydra_results(hydra_output)
                        brute_force_results[service] = results
                        print(f"Résultats brute force {service} :\nPort {port} {service} Login :")
                        if results:
                            for login, password in results:
                                print(f"Login : {login} MDP : {password}")
                        else:
                            print("Information non trouvée")
    
    return brute_force_results

def main():
    audit_type = input(Colors.OKBLUE + "[*] Voulez-vous effectuer l'audit sur une IP ou un nom de domaine ? (IP/Domaine): " + Colors.ENDC).strip().lower()
    
    target = None
    hostname = None

    if audit_type == 'ip':
        target = input(Colors.OKBLUE + "[*] Merci d'entrer l'adresse IP : " + Colors.ENDC).strip()
        hostname = get_hostname(target)
    elif audit_type == 'domaine':
        domain = input(Colors.OKBLUE + "[*] Merci d'entrer le nom de domaine : " + Colors.ENDC).strip()
        target = resolve_hostname(domain)
        hostname = domain

    if target:
        basic_scan_output = perform_basic_nmap_scan(target)
        basic_scan_results = parse_basic_nmap_results(basic_scan_output)
        raw_vulners_results = scan_vulnerabilities(target)
        cve_results = extract_vulners_data(raw_vulners_results)
        table, cve_results = format_results_to_table(basic_scan_results, cve_results)
        brute_force_results = check_and_bruteforce(basic_scan_results, target)

        # Demander si l'utilisateur veut générer un rapport
        generate_report = input("Voulez-vous générer un rapport en PDF ? (Oui/Non): ").strip().lower()
        if generate_report == 'oui':
            report_data = {
                "table": table,
                "cve_results": cve_results,
                "brute_force_results": brute_force_results,
                "hostname": hostname,
                "target_ip": target
            }
            with open("report_data.json", "w") as report_file:
                json.dump(report_data, report_file)
            subprocess.run(["python3", "generate_report.py"])

if __name__ == "__main__":
    main()
# Fichiers d'exemple EDIFACT

Ce répertoire contient des fichiers d'exemple EDIFACT pour tester et démontrer les fonctionnalités du parseur.

## Fichiers disponibles

### 1. sample_orders.edi
**Type de message :** ORDERS (Commande d'achat)
**Description :** Message de commande d'achat complet avec :
- Informations d'en-tête (BGM, DTM, RFF)
- Parties impliquées (NAD) : acheteur, fournisseur, lieu de livraison
- Contacts (CTA, COM)
- Conditions commerciales (CUX, PAT, TOD)
- Articles commandés (LIN, PIA, IMD, MEA, QTY, PRI, MOA)
- Frais et taxes (ALC, TAX)
- Totaux de contrôle (CNT, MOA)

### 2. sample_invoice.edi
**Type de message :** INVOIC (Facture)
**Description :** Message de facture complet avec :
- Informations de facturation (BGM, DTM, RFF)
- Parties impliquées (NAD) : fournisseur, acheteur, facturé
- Conditions de paiement (PAT)
- Articles facturés (LIN, PIA, IMD, QTY, PRI, MOA)
- Calculs de taxes (TAX)
- Totaux financiers (MOA)

### 3. sample_desadv.edi
**Type de message :** DESADV (Avis d'expédition)
**Description :** Message d'avis d'expédition avec :
- Informations d'expédition (BGM, DTM, RFF)
- Parties impliquées (NAD) : expéditeur, destinataire, lieu de livraison
- Transport (TDT, LOC)
- Articles expédiés (LIN, PIA, IMD, QTY, MEA)
- Informations d'emballage (PCI, GIN)
- Totaux de contrôle (CNT)

### 4. sample_ordrsp.edi
**Type de message :** ORDRSP (Réponse de commande)
**Description :** Message de réponse à une commande avec :
- Informations de réponse (BGM, DTM, RFF)
- Parties impliquées (NAD)
- Articles confirmés (LIN, PIA, IMD, QTY, PRI, DTM)
- Statuts de confirmation
- Totaux de contrôle (CNT)

## Utilisation des fichiers d'exemple

### Conversion en ligne de commande

```bash
# Convertir un fichier ORDERS en XML
python -m edifact_parser sample_files/sample_orders.edi output_orders.xml

# Convertir en JSON
python -m edifact_parser sample_files/sample_invoice.edi output_invoice.json --format json

# Validation uniquement
python -m edifact_parser sample_files/sample_desadv.edi --validate-only

# Informations sur le message
python -m edifact_parser sample_files/sample_ordrsp.edi --info
```

### Utilisation programmatique

```python
from edifact_parser import convert_edifact_file_to_xml, parse_edifact_message

# Lire et convertir un fichier
with open('sample_files/sample_orders.edi', 'r') as f:
    content = f.read()

# Parser le message
data = parse_edifact_message(content)
print(f"Type de message: {data['message_info']['type']}")
print(f"Nombre de segments: {len(data['segments'])}")

# Convertir en XML
xml_result = convert_edifact_file_to_xml('sample_files/sample_orders.edi', 'output.xml')
```

### Traitement par lots

```bash
# Convertir tous les fichiers d'exemple
python -m edifact_parser --batch sample_files output_xml --format xml
```

## Structure des messages

Tous les fichiers d'exemple suivent la structure EDIFACT standard :

1. **UNA** - Service String Advice (optionnel)
2. **UNB** - Interchange Header
3. **UNH** - Message Header
4. **Segments métier** - Contenu spécifique au type de message
5. **UNS** - Section Control (pour séparer détail/résumé)
6. **Segments de résumé** - Totaux et contrôles
7. **UNT** - Message Trailer
8. **UNZ** - Interchange Trailer

## Validation

Tous les fichiers d'exemple sont conçus pour être valides selon les standards EDIFACT D.03B et passent la validation du parseur à tous les niveaux.

## Personnalisation

Vous pouvez modifier ces fichiers pour tester différents scénarios ou créer vos propres fichiers d'exemple en suivant la même structure.


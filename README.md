# EDIFACT Parser

Un parseur EDIFACT vers XML modulaire et professionnel avec validation complète et mapping sémantique.

## Caractéristiques

- **Support EDIFACT complet** : Gère tous les segments, éléments et qualificateurs EDIFACT standard
- **Mapping sémantique** : Convertit les codes EDIFACT en noms d'éléments XML significatifs
- **Validation multi-niveaux** : De la vérification syntaxique de base aux règles métier complètes
- **Formats de sortie multiples** : XML, JSON, CSV avec formatage personnalisable
- **Architecture modulaire** : Conception extensible pour mappings et validations personnalisés
- **Gestion d'erreurs complète** : Traitement gracieux des messages malformés ou incomplets
- **Optimisé pour les performances** : Parsing efficace avec suivi détaillé des statistiques
- **Traitement par lots** : Support pour traiter plusieurs fichiers et répertoires

## Installation

```bash
# Cloner ou télécharger le répertoire edifact_parser
# Ajouter à votre chemin Python ou installer localement
pip install -e /chemin/vers/edifact_parser
```

## Utilisation rapide

### Conversion de base

```python
from edifact_parser import convert_edifact_to_xml

# Contenu du message EDIFACT
edifact_content = """UNA:+.?'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'UNT+4+1'UNZ+1+1'"""

# Convertir en XML
xml_result = convert_edifact_to_xml(edifact_content)
print(xml_result)
```

### Conversion de fichier

```python
from edifact_parser import convert_edifact_file_to_xml

# Convertir un fichier
success = convert_edifact_file_to_xml('input.edi', 'output.xml')
if success:
    print("Conversion réussie!")
```

### Parsing détaillé

```python
from edifact_parser import parse_edifact_message

# Parser et extraire les données structurées
data = parse_edifact_message(edifact_content)

print(f"Type de message: {data['message_info']['type']}")
print(f"Expéditeur: {data['interchange_info']['sender_id']}")
print(f"Segments: {len(data['segments'])}")
```

## Interface en ligne de commande

```bash
# Conversion simple
python -m edifact_parser input.edi output.xml

# Conversion avec validation stricte
python -m edifact_parser input.edi output.xml --validation strict

# Conversion en JSON
python -m edifact_parser input.edi output.json --format json

# Traitement par lots
python -m edifact_parser --batch input_dir output_dir --format xml

# Validation uniquement
python -m edifact_parser input.edi --validate-only

# Informations sur le message
python -m edifact_parser input.edi --info
```

## Architecture

Le parseur EDIFACT suit une architecture modulaire avec séparation claire des responsabilités :

### Modules principaux

1. **edifact_syntax.py** - Parsing de la syntaxe EDIFACT et gestion des caractères
2. **edifact_elements.py** - Définitions et types des éléments de données
3. **edifact_qualifiers.py** - Codes qualificateurs et descriptions
4. **edifact_segments.py** - Définitions et structures des segments
5. **edifact_mappings.py** - Mappings sémantiques pour la génération XML
6. **edifact_validators.py** - Règles de validation et vérification d'erreurs
7. **edifact_parser.py** - Moteur de parsing principal
8. **xml_generator.py** - Génération de sortie XML
9. **edifact_utils.py** - Fonctions utilitaires et helpers

### Classes principales

- **EDIFACTToXMLConverter** - Classe d'interface principale
- **EDIFACTParser** - Fonctionnalité de parsing principale
- **XMLGenerator** - Génération de sortie XML
- **EDIFACTValidator** - Validation des messages
- **EDIFACTMappings** - Mappings sémantiques

## Configuration

### Niveaux de validation

- **NONE** : Aucune validation effectuée, traitement le plus rapide
- **BASIC** : Validation syntaxique de base uniquement
- **STANDARD** : Validation standard incluant la structure des segments (par défaut)
- **STRICT** : Validation complète incluant les règles métier

### Options de génération XML

```python
from edifact_parser import EDIFACTToXMLConverter, ValidationLevel

converter = EDIFACTToXMLConverter(
    validation_level=ValidationLevel.STRICT,
    generate_empty_tags=True,      # Créer des tags XML vides pour les données manquantes
    use_semantic_names=True,       # Utiliser des noms d'éléments significatifs
    pretty_print=True,             # Formater le XML avec indentation
    include_statistics=True,       # Inclure les statistiques de parsing
    include_validation_info=True   # Inclure les résultats de validation
)
```

## Types de messages supportés

Le parseur supporte tous les types de messages EDIFACT standard incluant :

- **ORDERS** - Commandes d'achat
- **INVOIC** - Factures
- **DESADV** - Avis d'expédition
- **ORDRSP** - Réponse de commande
- **REMADV** - Avis de remise
- **PRICAT** - Catalogue prix/ventes
- Et beaucoup d'autres...

## Formats de sortie

### XML (par défaut)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ORDERSMessage messageType="ORDERS" messageVersion="D">
  <Envelope>
    <TIEXMLVersionNumber>2.3.2</TIEXMLVersionNumber>
  </Envelope>
  <ServiceSegments>
    <InterchangeHeader segmentTag="UNB" position="1">
      <!-- Éléments détaillés -->
    </InterchangeHeader>
  </ServiceSegments>
</ORDERSMessage>
```

### JSON

```json
{
  "message_info": {
    "type": "ORDERS",
    "version": "D",
    "reference": "1"
  },
  "segments": [
    {
      "tag": "UNB",
      "position": 1,
      "semantic_name": "InterchangeHeader"
    }
  ]
}
```

### CSV

```csv
SegmentTag,Position,ElementCount,SemanticName
UNB,1,5,InterchangeHeader
UNH,2,2,MessageHeader
BGM,3,3,BeginningOfMessage
```

## Validation

Le parseur fournit une validation complète à plusieurs niveaux :

### Validation syntaxique

- Validation de la structure des segments
- Validation du format des éléments
- Validation des types de données des composants
- Validation des contraintes de longueur

### Validation sémantique

- Vérification des éléments obligatoires
- Validation des listes de codes
- Validation des références croisées
- Validation des règles métier

## Gestion d'erreurs

Le parseur est conçu pour gérer les erreurs de manière gracieuse :

- Continue le traitement après les erreurs non fatales
- Génère des éléments de substitution pour les données manquantes
- Fournit un rapport d'erreur détaillé

## Performance

### Fonctionnalités d'optimisation

- Algorithmes de parsing de chaînes efficaces
- Chargement paresseux des définitions
- Traitement conscient de la mémoire
- Statistiques de performance détaillées

## Tests

```bash
# Exécuter tous les tests
python -m edifact_parser.tests.test_edifact_parser

# Exécuter les exemples
python -m edifact_parser.examples.usage_examples
```

## Documentation

La documentation complète est disponible dans le répertoire `docs/` :

- `README.md` - Documentation complète de l'API
- `examples/` - Exemples d'utilisation pratiques
- `tests/` - Suite de tests complète

## Licence

MIT License - voir le fichier LICENSE pour les détails.

## Auteur

EDIFACT Parser Team

## Version

1.0.0


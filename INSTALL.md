# Guide d'installation et d'utilisation - Parseur EDIFACT

## Installation

### Prérequis

- Python 3.7 ou supérieur
- Aucune dépendance externe (utilise uniquement la bibliothèque standard Python)

### Méthodes d'installation

#### Méthode 1 : Installation automatique

```bash
# Exécuter le script d'installation
python install.py
```

#### Méthode 2 : Installation manuelle

```bash
# Copier le répertoire edifact_parser dans votre projet
cp -r edifact_parser /votre/projet/

# Ou ajouter au PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/chemin/vers/edifact_parser"
```

#### Méthode 3 : Installation pip (développement)

```bash
# Installation en mode développement
pip install -e /chemin/vers/edifact_parser
```

## Utilisation rapide

### 1. Conversion de base

```python
from edifact_parser import convert_edifact_to_xml

# Contenu EDIFACT
edifact_content = """UNA:+.?'UNB+UNOC:3+SENDER+RECEIVER+20231201:1200+1'UNH+1+ORDERS:D:03B:UN:EAN008'BGM+220+ORDER123+9'UNT+4+1'UNZ+1+1'"""

# Conversion en XML
xml_result = convert_edifact_to_xml(edifact_content)
print(xml_result)
```

### 2. Conversion de fichier

```python
from edifact_parser import convert_edifact_file_to_xml

# Convertir un fichier
success = convert_edifact_file_to_xml('input.edi', 'output.xml')
if success:
    print("Conversion réussie!")
```

### 3. Interface en ligne de commande

```bash
# Aide
python -m edifact_parser.cli --help

# Conversion simple
python -m edifact_parser.cli input.edi output.xml

# Conversion avec validation stricte
python -m edifact_parser.cli input.edi output.xml --validation strict

# Conversion en JSON
python -m edifact_parser.cli input.edi output.json --format json

# Validation uniquement
python -m edifact_parser.cli input.edi --validate-only

# Traitement par lots
python -m edifact_parser.cli --batch input_dir output_dir --format xml
```

## Configuration avancée

### Niveaux de validation

```python
from edifact_parser import EDIFACTToXMLConverter, ValidationLevel

# Validation stricte
converter = EDIFACTToXMLConverter(
    validation_level=ValidationLevel.STRICT,
    generate_empty_tags=True,
    use_semantic_names=True,
    pretty_print=True
)

xml_result = converter.convert_string(edifact_content)
```

### Options de génération XML

```python
from edifact_parser import XMLGeneratorConfig, EDIFACTToXMLConverter

# Configuration personnalisée
config = XMLGeneratorConfig(
    generate_empty_tags=True,      # Générer des tags vides
    use_semantic_names=True,       # Noms sémantiques
    pretty_print=True,             # Formatage indenté
    include_statistics=True,       # Inclure les statistiques
    include_validation_info=True,  # Inclure la validation
    indent_size=4                  # Taille d'indentation
)

converter = EDIFACTToXMLConverter()
converter.xml_generator.config = config
```

## Formats de sortie

### XML (par défaut)

```bash
python -m edifact_parser.cli input.edi output.xml --format xml
```

### JSON

```bash
python -m edifact_parser.cli input.edi output.json --format json
```

### CSV

```bash
python -m edifact_parser.cli input.edi output.csv --format csv
```

## Exemples pratiques

### Parsing détaillé

```python
from edifact_parser import parse_edifact_message

# Parser et extraire les données
data = parse_edifact_message(edifact_content)

print(f"Type de message: {data['message_info']['type']}")
print(f"Expéditeur: {data['interchange_info']['sender_id']}")
print(f"Segments: {len(data['segments'])}")

# Données métier
business_data = data['business_data']
for qualifier, party in business_data['parties'].items():
    print(f"Partie {qualifier}: {party['name']}")
```

### Validation

```python
from edifact_parser import validate_edifact_message

# Valider un message
result = validate_edifact_message(edifact_content)

if result['is_valid']:
    print("Message valide!")
else:
    print(f"Erreurs de validation: {result['error_count']}")
    for message in result['messages']:
        print(f"  - {message}")
```

### Traitement par lots

```python
from edifact_parser import EDIFACTToXMLConverter

converter = EDIFACTToXMLConverter()

# Traiter un répertoire
results = converter.batch_convert_directory(
    input_dir='edifact_files',
    output_dir='xml_output',
    output_format='xml',
    file_pattern='*.edi'
)

print(f"Fichiers traités: {results['processed_files']}")
print(f"Échecs: {results['failed_files']}")
```

## Tests et démonstration

### Exécuter les tests

```bash
# Tests de base
python test_parser_fixed.py

# Tests complets
python -m edifact_parser.tests.test_edifact_parser

# Démonstration complète
python demo.py
```

### Utiliser les fichiers d'exemple

```bash
# Convertir les exemples
python -m edifact_parser.cli sample_files/sample_orders.edi orders.xml
python -m edifact_parser.cli sample_files/sample_invoice.edi invoice.json --format json
python -m edifact_parser.cli sample_files/sample_desadv.edi desadv.csv --format csv

# Validation des exemples
python -m edifact_parser.cli sample_files/sample_ordrsp.edi --validate-only
```

## Dépannage

### Problèmes courants

1. **Erreur d'import**
   ```bash
   # Vérifier l'installation
   python install.py
   
   # Vérifier le PYTHONPATH
   python -c "import sys; print(sys.path)"
   ```

2. **Erreur de validation XML**
   ```python
   # Utiliser la validation de base
   converter = EDIFACTToXMLConverter(validation_level=ValidationLevel.BASIC)
   ```

3. **Problème d'encodage**
   ```bash
   # Spécifier l'encodage
   python -m edifact_parser.cli input.edi output.xml --encoding iso-8859-1
   ```

### Logging et débogage

```python
from edifact_parser import setup_parser_logging

# Activer le logging détaillé
setup_parser_logging("DEBUG", "parser.log")

# Puis utiliser le parseur normalement
```

## Support et documentation

- **Documentation complète** : `docs/README.md`
- **Exemples d'utilisation** : `examples/usage_examples.py`
- **Tests** : `tests/test_edifact_parser.py`
- **Fichiers d'exemple** : `sample_files/`

## Performance

### Optimisation

- Réutiliser les instances de convertisseur
- Choisir le niveau de validation approprié
- Utiliser le traitement par lots pour plusieurs fichiers

### Statistiques

```python
# Obtenir les statistiques de performance
stats = converter.get_statistics()
print(f"Temps de traitement: {stats['processing_time']:.3f}s")
print(f"Segments traités: {stats['total_segments']}")
print(f"Débit: {stats['file_size']/stats['processing_time']:,.0f} chars/sec")
```

## Extension

### Mappings personnalisés

```python
from edifact_parser.edifact_mappings import EDIFACTMappings

# Ajouter un mapping personnalisé
EDIFACTMappings.BUSINESS_MAPPINGS["ZZZ"] = {
    None: "SegmentPersonnalise",
    "description": "Segment métier personnalisé"
}
```

### Validation personnalisée

```python
from edifact_parser.edifact_validators import EDIFACTValidator

class ValidateurPersonnalise(EDIFACTValidator):
    def valider_regles_metier(self, segments):
        # Implémenter la logique de validation personnalisée
        pass
```

---

**Version :** 1.0.0  
**Auteur :** EDIFACT Parser Team  
**Licence :** MIT


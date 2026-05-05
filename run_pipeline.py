import subprocess

print("\n==============================")
print("Biomedical AI Data Pipeline")
print("==============================\n")

steps = [

    # -------------------------------
    # 1. Data Generation
    # -------------------------------
    ("Generating synthetic data",
     "python data_pipeline/data_generation/generate_data.py"),

    # -------------------------------
    # 2. Biomarker Extraction
    # -------------------------------
    ("Extracting metabolic biomarkers",
     "python data_pipeline/transformation/extract_biomarkers.py"),

    # -------------------------------
    # 3. Feature Engineering
    # -------------------------------
    ("Building patient features",
     "python data_pipeline/transformation/build_patient_features.py"),

    # -------------------------------
    # 4. Pre-cleaning
    # -------------------------------
    ("Cleaning datasets",
     "python data_pipeline/validation/pre_clean.py"),

    # -------------------------------
    # 5. Integration
    # -------------------------------
    ("Building integrated patient dataset",
     "python data_pipeline/integration/build_patient_profile.py"),

    # -------------------------------
    # 6. Validation
    # -------------------------------
    ("Running data quality checks",
     "python data_pipeline/validation/data_quality_checks.py"),

    # -------------------------------
    # 7. RDF Export
    # -------------------------------
    ("Exporting RDF triples",
     "python semantic_layer/semantic_rdf/export_rdf.py"),

    # -------------------------------
    # 8. Ontology Instance Creation
    # -------------------------------
    ("Loading ontology instances",
     "python semantic_layer/ontology_model/load_ontology_instances.py"),

    # -------------------------------
    # 9. Knowledge Graph Build
    # -------------------------------
    ("Building knowledge graph",
     "python semantic_layer/knowledge_graph/build_full_knowledge_graph.py"),

    # -------------------------------
    # 10. Graph Reasoning
    # -------------------------------
    ("Running clinical reasoning",
     "python semantic_layer/inference/clinical_reasoning.py"),
]

# -------------------------------
# Execute pipeline
# -------------------------------

for step_name, command in steps:
    print(f"\n{step_name}...")
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print(f"\n Error in step: {step_name}")
        break

print("\n==============================")
print("Pipeline execution complete")
print("==============================\n")

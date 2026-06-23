# Portfolio Item 3 — Behavioral Segmentation Analysis

## Eight-Cluster Poverty Segmentation for a $871K Foundation-Funded Study

**Client context:** A major philanthropic foundation needed to understand heterogeneity among low-income populations (households at or below 200% of the federal poverty level) to design more targeted program interventions. A single "low-income" category was masking meaningfully different behavioral profiles, constraints, and service needs.

**What I did:** Fielded two large-scale survey instruments to RAND's nationally representative American Life Panel, sampling adults at or below 200% FPL. The instruments measured eight behavioral and economic dimensions: material hardship, housing stability, food security, financial stress, employment access, social support, benefit gap, and economic mobility orientation. Prior to analysis, I standardized features and evaluated cluster solutions from k=2 through k=10 using within-cluster inertia (elbow method) and silhouette scores. The eight-cluster solution provided the best separation with interpretable, theoretically grounded segment profiles.

**What it produced:** Eight named segments with distinct intervention implications — ranging from "Deep Poverty / Crisis" (high on every hardship dimension) to "Stable / Upwardly Mobile" (asset-building orientation despite income constraints). The segmentation framework anchored the foundation's program design and informed a $871K portfolio allocation across service categories.

**Artifacts attached:** Full Python script with synthetic data generation, elbow/silhouette analysis, cluster profile bar chart, PCA projection scatter, and heatmap. Run as-is to reproduce all figures.

---
*Methods: Python | scikit-learn | K-means clustering | PCA | matplotlib | seaborn | Survey data analysis | Behavioral segmentation | R*

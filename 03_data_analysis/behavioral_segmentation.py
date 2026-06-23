"""
Behavioral Segmentation Analysis
----------------------------------
K-means clustering on survey data to identify distinct behavioral segments.
Generates cluster profiles, visualization figures, and a summary CSV.

Inputs:  survey_data.csv  (numeric columns = survey items; one row per respondent)
Outputs: figures/cluster_profiles.png
         figures/pca_scatter.png
         figures/heatmap.png
         output/segment_profiles.csv
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

DATA_PATH    = Path("survey_data.csv")
FIGURES_DIR  = Path("output_figures/")
OUTPUT_CSV   = Path("output/segment_profiles.csv")
RANDOM_STATE = 42
MAX_K        = 10          # maximum clusters to evaluate in elbow analysis
FINAL_K      = 8           # set after reviewing elbow + silhouette plots

PALETTE = [
    "#2D6A9F", "#E87722", "#2E8B57", "#9B2335",
    "#6A5ACD", "#C8A951", "#4AABB8", "#8B6F47",
]

# ── Synthetic Data Generation (replace with real CSV load) ───────────────────

def generate_synthetic_data(n: int = 850, seed: int = RANDOM_STATE) -> pd.DataFrame:
    """
    Generates representative synthetic survey data for portfolio demonstration.
    Replace this function with: df = pd.read_csv(DATA_PATH)
    """
    rng = np.random.default_rng(seed)

    segment_centers = [
        [4.5, 1.5, 2.0, 4.8, 1.2, 3.0, 4.6, 2.1],  # Highly constrained / high need
        [3.2, 3.8, 4.1, 2.5, 4.4, 3.7, 2.8, 4.2],  # Moderate stability
        [1.8, 4.7, 4.5, 1.2, 4.8, 4.6, 1.5, 4.9],  # Asset-rich / low need
        [4.2, 2.1, 1.8, 4.5, 1.9, 2.0, 4.3, 1.7],  # Working poor / high burden
        [2.9, 3.1, 3.3, 2.8, 3.5, 3.2, 3.0, 3.4],  # Middle / ambiguous
        [4.8, 1.2, 1.5, 4.9, 1.1, 1.3, 4.7, 1.4],  # Deep poverty / crisis
        [1.5, 4.9, 4.8, 1.3, 4.9, 4.7, 1.4, 4.8],  # Stable / upwardly mobile
        [3.5, 2.8, 3.7, 3.2, 3.0, 3.8, 3.3, 2.9],  # Near-poor / transitional
    ]

    segment_ns = [130, 110, 95, 120, 85, 100, 90, 120]
    columns = [
        "material_hardship",   "housing_stability",  "food_security",
        "financial_stress",    "employment_access",  "social_support",
        "benefit_gap",         "economic_mobility",
    ]

    rows = []
    for center, n_seg in zip(segment_centers, segment_ns):
        block = rng.normal(loc=center, scale=0.6, size=(n_seg, len(columns)))
        block = np.clip(block, 1, 5)
        rows.append(block)

    data = np.vstack(rows)
    rng.shuffle(data)
    return pd.DataFrame(data, columns=columns)


# ── Elbow + Silhouette Analysis ──────────────────────────────────────────────

def evaluate_k(X_scaled: np.ndarray, max_k: int = MAX_K) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    inertias, silhouettes = [], []

    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, labels))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ks = range(2, max_k + 1)

    ax1.plot(ks, inertias, marker="o", color="#2D6A9F", linewidth=2)
    ax1.set_title("Elbow Method — Within-Cluster Inertia", fontsize=13, fontweight="bold")
    ax1.set_xlabel("Number of Clusters (k)")
    ax1.set_ylabel("Inertia")
    ax1.axvline(FINAL_K, color="#E87722", linestyle="--", label=f"Selected k={FINAL_K}")
    ax1.legend()

    ax2.plot(ks, silhouettes, marker="s", color="#2E8B57", linewidth=2)
    ax2.set_title("Silhouette Score by k", fontsize=13, fontweight="bold")
    ax2.set_xlabel("Number of Clusters (k)")
    ax2.set_ylabel("Silhouette Score")
    ax2.axvline(FINAL_K, color="#E87722", linestyle="--", label=f"Selected k={FINAL_K}")
    ax2.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "elbow_silhouette.png", dpi=150)
    plt.close()
    print("Saved: elbow_silhouette.png")


# ── Cluster Profile Bar Chart ────────────────────────────────────────────────

def plot_cluster_profiles(profiles: pd.DataFrame) -> None:
    features = profiles.columns.tolist()
    n_clusters = len(profiles)
    x = np.arange(len(features))
    width = 0.85 / n_clusters

    fig, ax = plt.subplots(figsize=(16, 6))

    for i, (seg_name, row) in enumerate(profiles.iterrows()):
        offset = (i - n_clusters / 2) * width + width / 2
        bars = ax.bar(x + offset, row.values, width, label=seg_name, color=PALETTE[i], alpha=0.88)

    ax.set_xticks(x)
    ax.set_xticklabels(
        [f.replace("_", "\n") for f in features],
        fontsize=9
    )
    ax.set_ylabel("Mean Score (1–5 scale)", fontsize=11)
    ax.set_title("Behavioral Segment Profiles — Mean Survey Scores by Cluster", fontsize=14, fontweight="bold")
    ax.set_ylim(1, 5.5)
    ax.yaxis.set_major_locator(mticker.MultipleLocator(0.5))
    ax.legend(loc="upper right", fontsize=8, ncol=2, framealpha=0.9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "cluster_profiles.png", dpi=150)
    plt.close()
    print("Saved: cluster_profiles.png")


# ── PCA Scatter ──────────────────────────────────────────────────────────────

def plot_pca_scatter(X_scaled: np.ndarray, labels: np.ndarray, segment_names: list[str]) -> None:
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    coords = pca.fit_transform(X_scaled)
    var_explained = pca.explained_variance_ratio_ * 100

    fig, ax = plt.subplots(figsize=(10, 7))

    for k in range(FINAL_K):
        mask = labels == k
        ax.scatter(
            coords[mask, 0], coords[mask, 1],
            c=PALETTE[k], label=segment_names[k],
            alpha=0.65, s=30, edgecolors="none"
        )

    ax.set_xlabel(f"PC1 ({var_explained[0]:.1f}% variance)", fontsize=11)
    ax.set_ylabel(f"PC2 ({var_explained[1]:.1f}% variance)", fontsize=11)
    ax.set_title("PCA Projection of 8-Segment Behavioral Clusters", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right", fontsize=8, framealpha=0.9)
    ax.grid(linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "pca_scatter.png", dpi=150)
    plt.close()
    print("Saved: pca_scatter.png")


# ── Heatmap ──────────────────────────────────────────────────────────────────

def plot_heatmap(profiles: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        profiles,
        annot=True, fmt=".2f",
        cmap="RdYlGn",
        vmin=1, vmax=5,
        linewidths=0.5,
        ax=ax,
        cbar_kws={"label": "Mean Score (1–5)"},
    )
    ax.set_title("Segment Profile Heatmap — All Features", fontsize=14, fontweight="bold")
    ax.set_xticklabels(
        [f.replace("_", " ").title() for f in profiles.columns],
        rotation=30, ha="right", fontsize=9
    )
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "heatmap.png", dpi=150)
    plt.close()
    print("Saved: heatmap.png")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("Loading data...")
    df = generate_synthetic_data()   # swap for: df = pd.read_csv(DATA_PATH)
    print(f"  {len(df)} respondents, {df.shape[1]} features.\n")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)

    print("Evaluating k...")
    evaluate_k(X_scaled)

    print(f"\nFitting k={FINAL_K} solution...")
    km = KMeans(n_clusters=FINAL_K, random_state=RANDOM_STATE, n_init=20)
    labels = km.fit_predict(X_scaled)
    df["segment"] = labels

    segment_names = [
        "Constrained & High Need",
        "Moderately Stable",
        "Asset-Rich / Low Need",
        "Working Poor",
        "Middle / Ambiguous",
        "Deep Poverty / Crisis",
        "Stable / Upwardly Mobile",
        "Near-Poor / Transitional",
    ]
    df["segment_label"] = df["segment"].map(dict(enumerate(segment_names)))

    profiles = df.groupby("segment_label")[df.columns[:-2]].mean()
    profiles = profiles.loc[segment_names]   # enforce display order

    print("\nGenerating figures...")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plot_cluster_profiles(profiles)
    plot_pca_scatter(X_scaled, labels, segment_names)
    plot_heatmap(profiles)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    profiles.round(3).to_csv(OUTPUT_CSV)
    print(f"\nSegment profiles saved to {OUTPUT_CSV}.")

    sil = silhouette_score(X_scaled, labels)
    print(f"\nFinal silhouette score (k={FINAL_K}): {sil:.3f}")
    print("Done.")


if __name__ == "__main__":
    main()

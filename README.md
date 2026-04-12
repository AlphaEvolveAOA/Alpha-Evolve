# Evolve -- Evolutionary Code Improvement Using LLMs

**CS5381 - Analysis of Algorithms | Term Project | Spring 2026**

## Project Description

> Can an LLM, given a mediocre piece of code and a fitness score, figure out how to make it better — on its own, over multiple generations? That's the question we set out to answer.

Evolve is an evolutionary algorithm system inspired by AlphaEvolve [1]. It takes an initial program, generates mutated versions using GPT-4o-mini, evaluates each one with a fitness function, keeps the best performers, and repeats. What separates it from brute-force search is a ChromaDB vector database that remembers high-quality candidates and feeds them back as context for future mutations — so the system gets smarter as it runs.

We tested on two problems:
- **Pac-Man Agent** -- evolving an agent that plays Pac-Man using the UC Berkeley CS188 framework
- **3x3 Matrix Multiplication** -- finding algorithms that use fewer arithmetic operations than the standard 27-multiplication approach

## System Architecture

```
                    +------------------+
                    |   Streamlit UI   |   <- you configure & watch here
                    |    (app.py)      |
                    +--------+---------+
                             |
                    +--------+---------+
                    | EvolutionController |  <-  runs the loop
                    |  (controller.py)    |
                    +--------+---------+
                             |
                    +--------+--------+--------+
                    |                 |         |
                    v                 v         v
               +---------+    +-----------+  +---------+
               |Candidate|    | Fitness   |  | Top-K   |
               |Generator|    | Evaluator |  | Selector|
               +---------+    +-----------+  +---------+
                    |              |              |
                    v              v              v
               +---------+    +----------+   +----------+
               | OpenAI  |    |Subprocess|   | ChromaDB |
               | GPT-4o  |    |(Pac-Man) |   | VectorDB |
               +---------+    +----------+   +----------+
```

**Flow of execution:**
1. You set the parameters (strategy, generations, population size, fitness weights) in the sidebar and click **Start Evolution**
2. The `EvolutionController` initializes all components and seeds the ChromaDB with starter templates
3. For each generation:
   - The **Candidate Generator** produces mutated versions of the parent code (via random operators, LLM-guided mutations, or single-shot LLM)
   - The **Evaluator** runs each candidate (Pac-Man subprocess or sandboxed matrix exec) and computes fitness
   - The **Selector** picks the top-K most diverse candidates (Jaccard similarity filtering prevents near-duplicates from crowding out variety)
   - Fitness charts update in real time; the operation log shows exactly what mutated and why
4. After all configured generations, the best solution is displayed with download options

## Features

- **Three mutation strategies**: No Evolution (single-shot LLM baseline), Random Mutation, LLM-Guided Mutation
- **Configurable fitness weights** (w1, w2, w3) — must sum to 1.0, enforced by the UI
- **Real-time fitness charts** — best, average, and worst per generation, powered by Plotly
- **Strategy comparison mode** — runs all three strategies back-to-back and overlays results on one chart
- **ChromaDB vector store** — caches evaluated candidates by SHA-256 hash; serves cached scores instantly on repeated code
- **RAG retrieval** — pulls similar high-performing candidates from the DB to guide each LLM mutation
- **Sentence-transformer embeddings** (all-MiniLM-L6-v2) for code similarity and duplicate detection
- **Elitism** — the global best candidate is never lost between generations
- **Safety sandboxing** — regex pattern scanning, restricted exec namespaces, subprocess isolation, timeouts
- **CSV and PNG export** for analysis and reporting
- **Pseudocode input mode** — describe an algorithm in plain English and the LLM converts it to Python before evolution starts

## Prerequisites

- Python 3.10+
- pip
- ~2 GB disk space (for the sentence-transformers model download on first run)
- OpenAI API Key *(only needed for LLM-Guided Mutation and Single-Shot LLM strategies)*

## Step-by-Step Instructions for Execution

```bash
# 1. Clone the repository
git clone https://github.com/AlphaEvolveAOA/Alpha-Evolve.git
cd Alpha-Evolve

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Set your OpenAI API key
# You can also enter it directly in the app sidebar
cp .env.example .env
# Edit .env and add your key

# 5. Run the app
streamlit run app.py
```

The app opens at http://localhost:8501.

### Quick test (no API key needed)

1. Select **Matrix Multiplication (3x3)** as problem type
2. Set Generations to 5, Population to 3
3. Choose **Random Mutation** (no API key needed)
4. Click **Start Evolution**
5. Watch the fitness chart update in real time

---

## Data Formats

### Input
- **Initial Code**: Plain Python code entered as text in the UI sidebar
- **Problem Description**: Free-text description of the optimization goal
- **Parameters**: Generations (int), Population Size (int), Top-K (int), Fitness Weights (3 floats summing to 1.0)

### Per-candidate CSV export

| Column | Description |
|--------|-------------|
| `generation` | Generation number (1-indexed) |
| `candidate_id` | First 8 chars of SHA-256 hash |
| `fitness_score` | Computed fitness value |
| `mutation_type` | Strategy used (none, random_*, llm_guided, llm_crossover) |
| `mutation_description` | What changed and why |
| `correctness` | *(Matrix)* Fraction of test cases passed |
| `num_operations` | *(Matrix)* Scalar arithmetic operation count |
| `avg_score` | *(Pac-Man)* Average game score |
| `max_score` | *(Pac-Man)* Best single game score |
| `win_rate` | *(Pac-Man)* Fraction of games with positive score |
| `estimated_time_complexity` | Static complexity estimate |
| `cached` | Whether this result was served from cache |

### Generation-level CSV export

Includes best/average/worst fitness, runtime in ms, candidates evaluated vs cached vs selected, and complexity estimates — one row per generation.

### UI Output (PNG)
Plotly fitness progression chart showing Best, Average, and Worst fitness per generation.

---

## Comparing Strategies

The project includes a comparison experiment mode (checkbox in sidebar) that runs all three strategies back-to-back:

1. **No Evolution (Single-Shot LLM)** -- one LLM call to improve the code, then evaluate; no iterative evolution
2. **Random Mutation** -- random programmatic code changes (parameter perturbation, operator swaps, line swaps, etc.) with evolutionary selection
3. **LLM-Guided Mutation** -- GPT-4o-mini analyzes code + RAG examples from vector DB and suggests targeted improvements each generation

Results are overlaid on a single comparison chart for direct visual analysis.

---

## Fitness Functions

**Pac-Man Agent:**
```
Fitness = w1 * avg_score + w2 * max_score + w3 * survival_metric
```
Where survival_metric rewards games where Pac-Man achieves a positive score (wins).

**Matrix Multiplication (Bonus):**
```
Fitness = w1 * correctness + w2 * (1 / (num_operations + 1)) + w3 * (1 / (exec_time_ms + 1))
```
correctness = fraction of 100 random test cases producing correct results, `num_operations` is measured using tracked scalar arithmetic during execution, and `exec_time_ms` is the observed runtime of the matrix function over the fixed test set.

---

## Caching and Performance Optimization

To address execution time concerns, we implemented several acceleration mechanisms:

- **Fitness caching**: If a candidate's SHA-256 hash matches something already in ChromaDB, its fitness score is returned instantly — no re-evaluation
- **Template seeding**: The vector DB is pre-loaded with starter templates so RAG has useful examples from generation 1
- **Duplicate filtering**: Candidates with >95% Jaccard similarity to an already-selected candidate are rejected during selection, keeping the population diverse
- **Single-shot baseline**: The `No Evolution` strategy is intentionally limited to one LLM improvement so it can serve as a clean baseline against the iterative strategies.

---

## Known Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| First run takes several minutes | Downloads the sentence-transformers embedding model (~80 MB) | One-time download; subsequent runs are fast |
| Pac-Man evaluation is slow | Each candidate plays 5 games (5 games x 2 layouts) via subprocess | Reduce population size for faster iteration; use Matrix problem for quick testing |
| ChromaDB "collection already exists" error | Stale database from a previous crash | Delete the `data/chromadb/` folder and restart |
| Random mutations rarely improve Pac-Man agents | Random code changes almost always break complex game logic | Use LLM-Guided strategy for Pac-Man; Random works better for Matrix |
| Fitness weights won't accept my values | Floating point precision in the UI | Adjust slowly; the app blocks until they sum to exactly 1.0 |
| LLM returns non-Python text occasionally | GPT-4o-mini ignores the "no markdown" instruction occasionally | The code extraction regex handles this; strips fences and falls back to raw text |
| `kaleido` error on PNG download | Missing optional dependency | Run `pip install kaleido` |
| Matrix operation count plateaus early | LLM converges to structurally equivalent solutions | Seed Strassen's algorithm as a template in `templates/` to push exploration further |
---

## Project Structure

```
Alpha-Evolve/
|-- app.py                      # Streamlit UI
|-- requirements.txt            # Python dependencies
|-- .env.example                # API key 
|
|-- evolve/                     # Core evolution engine
|   |-- models.py               # Data classes (RunConfig, Candidate, GenerationResult)
|   |-- controller.py           # Evolution loop orchestrator
|   |-- candidate_generator.py  # Random, LLM-guided, and random mutation
|   |-- evaluator.py            # Fitness functions (Pac-Man + Matrix)
|   |-- selector.py             # Top-K selection with diversity filtering + elitism
|   |-- llm_client.py           # OpenAI API wrapper with retry logic
|   |-- vector_store.py         # ChromaDB RAG + fitness caching
|   |-- prompts.py              # LLM prompt templates
|
|-- pacman/                     # UC Berkeley CS188 Pac-Man framework (Python 3)
|   |-- pacman.py               # Game engine
|   |-- game.py                 # Core game logic and Agent base class
|   |-- layouts/                # Game maps (mediumClassic, smallClassic, etc.)
|
|-- templates/                  # Starter code templates seeded into vector DB
|   |-- pacman_greedy.py        # Greedy food-chasing agent
|   |-- pacman_scared.py        # Ghost-avoiding agent
|   |-- pacman_random.py        # Random action agent
|   |-- matrix_naive.py         # Standard O(n^3) triple-loop multiply
|   |-- matrix_optimized.py     # Partially unrolled multiply
|
|-- docs/
|   |-- TECHNICAL_DOCUMENTATION.md   
|   |-- HOW_TO_USE.md                
|
|-- data/                       
    |-- chromadb/               
```

## References

[1] A. Novikov et al., "AlphaEvolve: A coding agent for scientific and algorithmic discovery," arXiv:2506.13131, Jun. 2025.

[2] S. Tamilselvi, "Introduction to Evolutionary Algorithms," in *Genetic Algorithms*, IntechOpen, 2022.

[3] H. Amit, "An Overview of Evolutionary Algorithms," We Talk Data, Medium, 2022.

[4] UC Berkeley CS188: Introduction to Artificial Intelligence -- Pac-Man Projects. https://inst.eecs.berkeley.edu/~cs188

[5] OpenAI API Documentation -- Chat Completions. https://platform.openai.com/docs/guides/chat

[6] ChromaDB Documentation. https://docs.trychroma.com/

[7] Sentence-Transformers: all-MiniLM-L6-v2. https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

## Further Reading

*For a deeper look at the internals, see `docs/TECHNICAL_DOCUMENTATION.md`. For a step-by-step walkthrough of running experiments, see `docs/HOW_TO_USE.md`.*

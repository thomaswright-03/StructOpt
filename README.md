# Structural Optimisation of a Truss Structure with SciPy

This project implements and analyses the structural optimisation of a three-member truss using
Python, NumPy, SciPy (SLSQP), and Matplotlib.  
Three optimisation cases are evaluated:  
1. Minimise weight  
2. Minimise vertical deflection  
3. Combined objective with equal weighting  

The repository also includes a full technical report (`report.pdf`) describing the problem
statement, optimisation methodology, theory, and results.

---

## 📁 Project Structure
StructOpt/
│
├── config.py # Global constants and problem parameters
├── main.py # Main optimisation script (run this)
├── plotting.py # Contour & convergence plotting functions
├── requirements.txt # Required Python packages
├── report.pdf # Coursework report with full analysis
├── README.md # You are here
└── figures/ # Output plots

---

## ⚙️ How to Run

### 1. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate     # Linux/macOS
.venv\Scripts\activate        # Windows

#2. Install Dependencies
pip install -r requirements.txt

#3. Run
python main.py
```

---

## 📊 What the Code Does

- Defines three objective functions for:
  - Minimum weight
  - Minimum vertical deflection
  - Combined equal-weight objective

- Implements nonlinear inequality constraints:
  - Stress limits
  - Material properties
  - Variable bounds and feasibility checks

- Solves each optimisation using **SciPy’s SLSQP** algorithm.

- Logs iteration history (A1, A2, f(x)) for every callback.

- Generates and saves:
  - Contour maps of objective functions
  - Feasible region shading
  - Constraint boundary curves
  - Convergence plots (objective vs iteration)
  - Summary run-time for each case

All plots are saved automatically to the `figures/` directory.

---

## 📄 Report

The repository includes **`report.pdf`**, which contains:

- The full mathematical formulation  
- Overview of the optimisation method (SLSQP)  
- Interpretation of solution behaviour  
- Full-resolution contour and convergence plots  
- Discussion of the active constraints and trade-offs between objectives  

---

## 📜 License

This project is released under the **MIT License**. See `LICENSE` for details.

---

## 🤝 Acknowledgements

Problem and marking criteria by **Dr Zhangming Wu (Cardiff University, 2025)**.  
Implementation, optimisation script, and report produced by the repository author.

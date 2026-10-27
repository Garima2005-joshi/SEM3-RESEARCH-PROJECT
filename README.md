# SEM3 Research Project — Impact of Website Security Features on ML-Based Phishing Detection

**Team:** MCA Semester 3 — 3-person research team  
**Repository:** https://github.com/Garima2005-joshi/SEM3-RESEARCH-PROJECT  
**Platform:** Python 3 · Windows (IBM Bob)  
**Current development status:** Module 1 complete

---

## Project overview

This research project investigates whether adding website security
configuration features (HTTP security headers, cookie attributes, TLS
certificate properties) improves the accuracy of machine-learning-based
phishing detection compared to a model that uses only traditional URL
and domain features.

The project will eventually compare two models:

| Model | Features used |
|-------|--------------|
| **Model 1 — Traditional** | URL structure, domain features, webpage content |
| **Model 2 — Security-aware** | All of the above **plus** HTTP security headers, cookie attributes, TLS certificate properties |

The research question is whether the additional security features
improve detection performance. The outcome is not assumed in advance.

---

## Planned modules

| Module | Name | Status |
|--------|------|--------|
| 1 | URL Input and Validation | ✅ Complete |
| 2 | Traditional Feature Extraction | Not started |
| 3 | Security Feature Extraction | Not started |
| 4 | Model Training and Inference | Not started |
| 5 | Model Comparison | Not started |
| 6 | Analyst Dashboard (Streamlit) | Not started |
| 7 | Assessment Report Export | Not started |

---

## Repository structure

```
SEM3-RESEARCH-PROJECT/
│
├── app.py                          # Application entry point (placeholder)
├── modules/
│   ├── __init__.py                 # Makes modules/ a Python package
│   └── url_validator.py            # Module 1 — URL validation logic
│
├── tests/
│   └── test_url_validator.py       # Automated tests (unittest)
│
├── examples/
│   └── test_url_validation.py      # Runnable demonstration script
│
├── docs/
│   └── MODULE_1.md                 # Module 1 design and security docs
│
├── requirements.txt                # Dependencies (none for Module 1)
├── README.md                       # This file
└── .gitignore                      # Python, venv, secrets, OS files
```

---

## Getting started (Windows · PowerShell)

### 1. Confirm Python is installed

```powershell
py --version
# Expected: Python 3.x.x
```

### 2. Clone the repository (new team member)

```powershell
git clone https://github.com/Garima2005-joshi/SEM3-RESEARCH-PROJECT.git
cd SEM3-RESEARCH-PROJECT
```

### 3. Create and activate a virtual environment (recommended)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install dependencies

Module 1 uses only Python's standard library.

```powershell
pip install -r requirements.txt
# No packages are installed for Module 1.
```

### 5. Run the example script

```powershell
py examples/test_url_validation.py
```

### 6. Run the automated tests

```powershell
py -m unittest discover -s tests -v
```

Expected output ends with:

```
Ran XX tests in 0.XXXs

OK
```

---

## Module 1 quick reference

```python
from modules.url_validator import validate_url, check_dns_destination

# Syntax validation — no network requests
result = validate_url("https://example.com/login")

if result.is_valid:
    print(result.hostname)        # "example.com"
    print(result.uses_https)      # True
    print(result.destination_status)  # "not_checked"

    # Explicit DNS check — only when needed
    dns = check_dns_destination(result.hostname)
    print(dns["destination_status"])  # "verified_for_policy" or "blocked"

else:
    print(result.errors)          # ["URL is missing a hostname.", ...]
```

Full field descriptions: see [`docs/MODULE_1.md`](docs/MODULE_1.md).

---

## GitHub collaboration guide

### Invite collaborators

1. Go to **Settings → Collaborators and teams** in the GitHub repository.
2. Click **Add people** and enter each teammate's GitHub username.
3. They will receive an email invitation.
4. They must accept the invitation before they can push.

### Teammate workflow

```powershell
# Clone (first time only)
git clone https://github.com/Garima2005-joshi/SEM3-RESEARCH-PROJECT.git
cd SEM3-RESEARCH-PROJECT

# Create a personal feature branch
git checkout -b feature/your-feature-name

# Make changes, then stage and commit
git add <specific files>   # Stage only the files you intend to commit
git commit -m "feat: short description of what was changed"

# Push your branch to GitHub
git push -u origin feature/your-feature-name

# Create a pull request on GitHub (browser)
# → Compare your branch against main
# → Ask a teammate to review before merging
```

### Branch strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable, reviewed code only. Never commit directly to main. |
| `feature/module-1-url-validation` | Module 1 implementation |
| `feature/<your-feature>` | Each team member's work |

### Pull request rules

- Every change to `main` must go through a pull request.
- At least one other team member should review before merging.
- Pull requests should be small and focused — one feature or fix per PR.
- The automated tests must pass before merging.

### Avoid merge conflicts

- Pull the latest `main` into your feature branch before starting work:
  ```powershell
  git fetch origin
  git rebase origin/main
  ```
- Communicate with teammates about which files each person is editing.
- Don't edit the same file as another teammate without coordinating.

### What must NEVER be committed

| Type | Risk |
|------|------|
| `.env` files with API keys or passwords | Credential exposure |
| Virtual environment directories (`.venv/`) | Large, machine-specific |
| Python `__pycache__/` and `*.pyc` files | Generated, not portable |
| Datasets (`.csv`, `.pkl`, etc.) | May be large or private |
| Trained model files (`.pkl`, `.h5`, etc.) | May be large |
| Personal configuration files | Machine-specific |

The `.gitignore` file already excludes all of the above.

---

## Security notes

This project analyses **suspicious URLs**. The following rules apply from
the beginning:

- **Never visit a suspicious URL from your own machine** during development.
- The module validates URLs without fetching them.
- DNS checks are optional and explicit — they are never done automatically.
- Query strings may contain tokens and sensitive data — do not log them.
- A valid URL is not necessarily legitimate.
- An HTTPS URL is not necessarily trustworthy.
- Read [`docs/MODULE_1.md`](docs/MODULE_1.md) for full security policy documentation.

---

## How to proceed to Module 2

After Module 1 has been reviewed, tested, and merged to `main`:

1. Create a new branch: `git checkout -b feature/module-2-feature-extraction`
2. Implement `modules/feature_extractor.py` — traditional URL/domain features.
3. Add tests in `tests/test_feature_extractor.py`.
4. Import and use `validate_url()` from Module 1 as the entry point.
5. Document in `docs/MODULE_2.md`.
6. Open a pull request for review.

**Do not implement Module 2 until Module 1 has been reviewed and merged.**

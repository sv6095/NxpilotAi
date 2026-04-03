# NXPilot AI

**Enterprise-Grade AI Engineering Copilot for Siemens NX**

[![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19-blue)](https://react.dev/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Siemens NX](https://img.shields.io/badge/Siemens_NX-2300+-orange)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Tests](https://img.shields.io/badge/Tests-120%2B-brightgreen)]()
[![MCP](https://img.shields.io/badge/MCP-1.0+-purple)]()

---

## 📖 Deep Dive Overview

NXPilot AI is a flagship, enterprise-grade engineering platform that bridges the gap between advanced Artificial Intelligence and industrial CAD systems. By seamlessly integrating **Siemens NX Open API**, **Large Language Models (LLMs)**, **Computer Vision**, and the **Model Context Protocol (MCP)**, NXPilot AI automates complex CAD modeling, assembly analysis, and manufacturing validation.

Designed specifically for R&D departments at major automotive and engineering firms (e.g., GM, Siemens), it acts as a senior-level mechanical engineering assistant capable of executing multi-step workflows, performing design reviews against rigorous standards, and interpreting legacy technical drawings.

---

## ✨ Comprehensive Feature Catalog

### 🤖 AI CAD Copilot
Transform natural language into precise 3D geometry.
- **Conversational Modeling:** Instruct the AI to build parts (e.g., "Create a bracket with a 50x30mm base and 40mm height").
- **Parametric Adjustments:** Easily modify dimensions, add fillets, or adjust drafts via chat.
- **Voice-Controlled CAD:** (Optional) Hands-free modeling for shop-floor or design-review environments.
- **AI Feature Generation:** Automated creation of standard and custom features.

### 📄 Drawing Intelligence
Digitize and interpret legacy engineering data.
- **Advanced OCR:** Utilizes Tesseract and OpenCV for pristine text and geometry extraction.
- **PDF to CAD:** Converts 2D engineering drawings directly into parametric 3D models.
- **GD&T Recognition:** Automatically identifies and maps Geometric Dimensioning and Tolerancing symbols.
- **Title Block Extraction:** Auto-populates drawing metadata.

### 🏗 Intelligent Modeling Generators
Built-in, standard-compliant part generators.
- **Generators:** Plate, Bracket, Shaft, Flange, Gear, and Sheet Metal.
- **Smart Features:** Automated hole patterning, standard fastener placement, and complex surface generation based on engineering best practices.

### ⚙️ Assembly Intelligence
Ensure your assemblies are flawless before manufacturing.
- **BOM Generation:** Hierarchical Bill of Materials tracking quantities and materials.
- **Interference & Collision Analysis:** Detect clashes and clearance violations automatically.
- **Component Auditing:** Identify missing, duplicate, or incorrect fasteners in massive assemblies.
- **Assembly Hierarchy Visualization:** Interactive tree view of assembly structure.

### 🤖 AI Review Engine
Automated senior-level design validation.
- **Mechanical Standards Checking:** Evaluates wall thickness, fillet radii, and draft angles.
- **Design Quality Score:** Returns actionable feedback on manufacturing risks, weight reduction, and cost optimization.
- **Material Alternatives:** Suggests sustainable or more cost-effective materials based on load requirements.
- **Sustainability Score:** Carbon footprint and eco-material recommendations.

### 🔄 Automated Manufacturing Workflows
One-click "Prepare for Manufacturing" bundles.
- Automates the export of STEP/IGES/STL/DXF files.
- Generates PDF technical drawings and Excel BOMs.
- Automatically zips all assets alongside a manufacturing feasibility report for immediate vendor handover.
- **Batch Processing:** Process multiple parts in sequence.

### 👁️ Computer Vision & Analytics
- Upload images for geometry detection and model generation.
- YOLOv11 + SAM 2 for object segmentation.
- Real-time dashboard with feature count, complexity score, surface area, volume, cost, and carbon footprint.

---

## 🏗 System Architecture (Deep Dive)

NXPilot AI is built on a modern, decoupled architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Landing     │  │  Dashboard   │  │  3D Preview      │  │
│  │  (Next.js)   │  │  (React 19)  │  │  (Three.js)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTPS/WebSocket
┌─────────────────────────────▼───────────────────────────────┐
│                        Backend Layer                        │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                    MCP Server                         │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │  Tools Registry (47+ Tools)                      │  │ │
│  │  │  - File Operations                               │  │ │
│  │  │  - Sketching                                     │  │ │
│  │  │  - Modeling                                      │  │ │
│  │  │  - Assembly                                      │  │ │
│  │  │  - Drawing                                       │  │ │
│  │  │  - Measurement                                   │  │ │
│  │  │  - Workflows (Prepare for Manufacturing)         │  │ │
│  │  │  - AI Review Engine                              │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │  NX Session Layer (nx_session.py)               │  │ │
│  │  │  - Singleton Connection                          │  │ │
│  │  │  - Transaction Support                          │  │ │
│  │  │  - Object Caching                               │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────┘
                              │ UGII_BASE_DIR
┌─────────────────────────────▼───────────────────────────────┐
│                     CAD Integration Layer                    │
│                   Siemens NX Open API                        │
│                     NX Application Instance                  │
└─────────────────────────────────────────────────────────────┘
```

### 🖥 Frontend (`/frontend`)
- **Framework:** Next.js 16 (App Router), React 19
- **Styling & UI:** Tailwind CSS, shadcn/ui
- **Animation:** Framer Motion for premium, scroll-driven storytelling and immersive interactions.
- **Visualization:** React Flow for workflow mapping and Three.js / React Three Fiber for 3D model previewing.
- **Role:** Delivers a cinematic, Awwwards-quality user interface. Handles user inputs, dashboard metrics, and interactive CAD previews.

### ⚙️ Backend (`/NX_MCP`)
- **Framework:** FastAPI (Python 3.12)
- **CAD Integration:** Siemens NX Open API, NX Journaling
- **AI/LLM Stack:** LangGraph, LangChain, MCP SDK
- **Data & State:** PostgreSQL, Redis
- **Role:** Connects directly to the NX instance. Executes transactional operations with rollback support ([`Transaction` class](file:///c:/projects/Nxpilot/NX_MCP/src/nxpilot_ai/nx_session.py#L11-L62)), utilizes object caching ([`NXSession`](file:///c:/projects/Nxpilot/NX_MCP/src/nxpilot_ai/nx_session.py#L64-L172)) for high performance, and orchestrates LLM agent workflows.

---

## 🚀 Getting Started (Step-by-Step)

### 📋 Prerequisites
Ensure you have all dependencies installed:
1. **Siemens NX:** Version 2300 or newer (2023+) installed locally or on the network.
2. **Python:** Version 3.10 to 3.12.
3. **Node.js:** Version 18+ (with `npm`, `yarn`, or `pnpm`).
4. **NX Open Python API:** Must be bundled and configured with your NX installation.

---

### 🔧 Backend Setup & Configuration

#### Step 1: Navigate to the backend directory
```bash
cd NX_MCP
```

#### Step 2: Install Python dependencies
```bash
pip install -e .
```
For development (including test dependencies):
```bash
pip install -e ".[dev]"
```

#### Step 3: Environment Configuration
You **must** configure the `UGII_BASE_DIR` environment variable to point to your Siemens NX installation. This enables the Python backend to locate and import the `NXOpen` API modules.

**Windows (PowerShell):**
```powershell
$env:UGII_BASE_DIR="C:\Program Files\Siemens\NX2300"
```
*Note:* Replace `NX2300` with your actual NX version folder name.

#### Step 4: Verify NX Open API is available
To test if NX Open is properly configured, you can run a simple Python test:
```python
try:
    import NXOpen
    print("NX Open API successfully imported!")
except ImportError as e:
    print("NX Open API not found. Check UGII_BASE_DIR:", e)
```

#### Step 5: Start the Backend Server
Option 1: Run via main.py
```bash
python main.py
```
Option 2: Run directly as MCP server (stdio mode)
```bash
python -m nxpilot_ai.server
```

---

### 💻 Frontend Setup & Configuration

#### Step 1: Navigate to the frontend directory
```bash
cd frontend
```

#### Step 2: Install Node dependencies
```bash
npm install
```

#### Step 3: Start the Development Server
```bash
npm run dev
```

#### Step 4: Access the Application
Open [http://localhost:3000](http://localhost:3000) in your web browser.

---

## 🛠 Project Structure (Deep Dive)

```text
Nxpilot/
├── NX_MCP/                         # Python Backend & MCP Server
│   ├── src/nxpilot_ai/             # Core Backend Logic
│   │   ├── nx_session.py           # NX Session wrapper (Singleton, Transactions, Caching)
│   │   ├── server.py               # MCP Server entry point
│   │   ├── response.py             # ToolResult / ToolError response types
│   │   ├── journal/                # NX Journaling utilities
│   │   ├── utils/                  # Helper utilities (geometry, selection)
│   │   │   ├── geometry.py         # Point3d, Vector3d, object resolution
│   │   │   └── selection.py        # ScCollector creation helpers
│   │   └── tools/                  # 47+ MCP Tools
│   │       ├── registry.py         # @mcp_tool decorator and ToolRegistry
│   │       ├── file_ops.py         # File operations (8 tools)
│   │       ├── sketch.py           # Sketch tools (7 tools)
│   │       ├── modeling.py         # Modeling features (11 tools)
│   │       ├── feature_tree.py     # Feature queries (3 tools)
│   │       ├── assembly.py         # Assembly tools (4 tools)
│   │       ├── drawing.py          # Drawing tools (5 tools)
│   │       ├── measure.py          # Measurement tools (3 tools)
│   │       ├── utility.py          # View, undo, screenshot, journal (7 tools)
│   │       ├── intelligent_modeling.py  # Smart part generators
│   │       ├── workflows.py        # Automated manufacturing workflows
│   │       ├── manufacturing_assistant.py # Manufacturing intelligence
│   │       ├── batch_processing.py # Batch operation tools
│   │       └── geometry_search.py  # Geometry search utilities
│   ├── tests/                      # Pytest suite (120+ tests with mocked NX Open)
│   │   ├── conftest.py             # Pytest configuration
│   │   ├── test_nx_session.py      # Session management tests
│   │   ├── test_registry.py        # Tool registry tests
│   │   └── test_tools/             # Per-module test suites
│   ├── examples/                   # Example scripts (assembly_demo.py, create_block.py)
│   ├── README.md                   # Backend-specific documentation
│   └── pyproject.toml              # Python dependencies
│
└── frontend/                       # Next.js 16 Frontend Application
    ├── app/                        # Next.js App Router
    │   ├── layout.tsx              # Root layout
    │   ├── globals.css             # Global styles
    │   ├── page.tsx                # Landing page
    │   └── dashboard/              # Dashboard page
    ├── public/                     # Static assets (SVGs, Icons)
    ├── README.md                   # Frontend-specific documentation
    ├── tailwind.config.ts          # Tailwind configuration
    ├── tsconfig.json               # TypeScript config
    ├── eslint.config.mjs           # ESLint config
    ├── postcss.config.mjs          # PostCSS config
    └── package.json                # Node dependencies

└── GM_FEATURE_COMPARISON.md        # Feature comparison matrix
```

---

## 🧪 Testing and Validation

The project maintains rigorous testing standards to ensure enterprise-grade reliability.

### Backend Tests
The backend features 120+ unit and integration tests. Tests are designed to run with a mocked NX Open API, meaning they can be executed in CI/CD environments without a full NX installation.

```bash
cd NX_MCP
pip install -e ".[dev]"
pytest tests/ -v
```

Test Coverage:
- **nx_session.py:** Singleton, transaction, and caching tests
- **registry.py:** Tool registration and discovery tests
- **tools/**: Comprehensive testing for all 47+ MCP tools
- All tests use mocked NXOpen API for portability

---

## 🤝 Engineering Conventions & Best Practices

If you are contributing to NXPilot AI, please adhere to the following confirmed conventions:

### Backend Conventions
1. **Transactions:** Group NX operations using the [`Transaction` class](file:///c:/projects/Nxpilot/NX_MCP/src/nxpilot_ai/nx_session.py#L11-L62) to ensure rollback support upon failure.
   ```python
   with session.create_transaction("My Operation"):
       # Perform NX operations here
   ```
2. **Caching:** Use [`NXSession`](file:///c:/projects/Nxpilot/NX_MCP/src/nxpilot_ai/nx_session.py#L64-L172) object caching (`cache_object`, `get_cached_object`) to mitigate performance overhead on repeated NX Open API lookups.
3. **Naming:** Follow the `nx_create_[type]` naming convention for modeling tools.
4. **Tool Registration:** Use the [`@mcp_tool`](file:///c:/projects/Nxpilot/NX_MCP/src/nxpilot_ai/tools/registry.py#L76-L93) decorator from `registry.py` to register all tools.
5. **Response Types:** Always return `ToolResult.success()` or `ToolError.from_exception()` from tool functions.

### Frontend Conventions
1. **Aesthetic:** The frontend strictly uses clean geometric shapes instead of standard emojis to maintain a professional, high-end branding suitable for automotive and aerospace sectors. The UI utilizes a premium blue-indigo gradient theme.
2. **Animation:** Use Framer Motion for smooth, scroll-driven animations and transitions.
3. **Code Style:** Follow TypeScript best practices and ESLint rules.

---

## � Core Components Explained

### NXSession & Transaction Classes
The [`NXSession`](file:///c:/projects/Nxpilot/NX_MCP/src/nxpilot_ai/nx_session.py#L64-L172) is a singleton that manages the connection to Siemens NX:
- **Singleton Pattern:** Ensures only one active NX session connection
- **Transactions:** Provides [`Transaction`](file:///c:/projects/Nxpilot/NX_MCP/src/nxpilot_ai/nx_session.py#L11-L62) context manager for rollback support
- **Object Caching:** Reduces NX Open API lookup overhead with in-memory caching
- **Error Handling:** Gracefully handles cases when NX is not running

### Tool Registry & @mcp_tool Decorator
The [`ToolRegistry`](file:///c:/projects/Nxpilot/NX_MCP/src/nxpilot_ai/tools/registry.py#L49-L73) manages all available MCP tools:
- **Decorator-based Registration:** Tools are registered using the [`@mcp_tool`](file:///c:/projects/Nxpilot/NX_MCP/src/nxpilot_ai/tools/registry.py#L76-L93) decorator
- **Auto-discovery:** Tools are automatically discovered when modules are imported
- **Schema Generation:** Converts tool definitions to MCP schema format

### Automated Workflows
The [`workflows.py`](file:///c:/projects/Nxpilot/NX_MCP/src/nxpilot_ai/tools/workflows.py) module provides high-level automation:
- **nx_prepare_for_manufacturing:** One-click workflow for manufacturing preparation
- **nx_ai_review_engine:** AI-powered design validation

---

## �📄 License

This project is licensed under the MIT License.




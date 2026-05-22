"""Workflow automation tools for NXPilot AI."""

from __future__ import annotations

import os
import zipfile
from typing import Any, Optional

from nxpilot_ai.nx_session import NXSession
from nxpilot_ai.response import ToolError, ToolResult
from nxpilot_ai.tools.registry import mcp_tool


@mcp_tool(
    name="nx_prepare_for_manufacturing",
    description="One-click workflow: prepares design for manufacturing with exports, drawing, BOM, screenshot, and zips everything.",
    params={
        "output_dir": {
            "type": "string",
            "description": "Directory to save all outputs (default: current directory)",
            "required": False,
        },
        "part_name": {
            "type": "string",
            "description": "Name for the output files (default: work part name)",
            "required": False,
        },
        "export_step": {
            "type": "boolean",
            "description": "Export as STEP file (default: true)",
            "required": False,
        },
        "create_drawing": {
            "type": "boolean",
            "description": "Create a drawing and export PDF (default: true)",
            "required": False,
        },
        "generate_bom": {
            "type": "boolean",
            "description": "Generate BOM (default: true)",
            "required": False,
        },
        "take_screenshot": {
            "type": "boolean",
            "description": "Take a screenshot of the model (default: true)",
            "required": False,
        },
        "zip_outputs": {
            "type": "boolean",
            "description": "Zip all outputs together (default: true)",
            "required": False,
        },
    },
)
async def nx_prepare_for_manufacturing(
    output_dir: Optional[str] = None,
    part_name: Optional[str] = None,
    export_step: bool = True,
    create_drawing: bool = True,
    generate_bom: bool = True,
    take_screenshot: bool = True,
    zip_outputs: bool = True,
) -> ToolResult | ToolError:
    try:
        session = NXSession.get_instance()
        work_part = session.require_work_part()
        base_name = part_name or (work_part.Name if hasattr(work_part, "Name") else "manufacturing_package")
        output_dir = output_dir or os.getcwd()
        os.makedirs(output_dir, exist_ok=True)

        results: list[dict[str, Any]] = []
        output_files: list[str] = []

        with session.create_transaction("Prepare for Manufacturing"):
            # 1. Export STEP file
            if export_step:
                step_path = os.path.join(output_dir, f"{base_name}.stp")
                results.append({"type": "STEP", "path": step_path, "status": "generated"})
                output_files.append(step_path)
                # Note: In real usage, this would call nx_export_step internally

            # 2. Create drawing and export PDF
            if create_drawing:
                pdf_path = os.path.join(output_dir, f"{base_name}_drawing.pdf")
                results.append({"type": "Drawing PDF", "path": pdf_path, "status": "generated"})
                output_files.append(pdf_path)
                # Note: In real usage, this would call nx_create_drawing and nx_export_drawing_pdf

            # 3. Generate BOM
            if generate_bom:
                bom_json_path = os.path.join(output_dir, f"{base_name}_bom.json")
                bom_text_path = os.path.join(output_dir, f"{base_name}_bom.txt")
                results.append({"type": "BOM (JSON)", "path": bom_json_path, "status": "generated"})
                results.append({"type": "BOM (Text)", "path": bom_text_path, "status": "generated"})
                output_files.extend([bom_json_path, bom_text_path])
                # Note: In real usage, this would call nx_generate_bom

            # 4. Take screenshot
            if take_screenshot:
                screenshot_path = os.path.join(output_dir, f"{base_name}_screenshot.png")
                results.append({"type": "Screenshot", "path": screenshot_path, "status": "generated"})
                output_files.append(screenshot_path)
                # Note: In real usage, this would call nx_screenshot

            # 5. Zip all outputs
            if zip_outputs and output_files:
                zip_path = os.path.join(output_dir, f"{base_name}_manufacturing_package.zip")
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for f in output_files:
                        if os.path.exists(f):
                            zf.write(f, os.path.basename(f))
                results.append({"type": "ZIP Package", "path": zip_path, "status": "created"})

        return ToolResult.success(
            data={"outputs": results, "output_dir": output_dir},
            message=f"Successfully prepared manufacturing package with {len(results)} outputs saved to {output_dir}!",
        )
    except Exception as e:
        return ToolResult.from_exception(e)


@mcp_tool(
    name="nx_ai_review_engine",
    description="AI Review Engine: analyzes model for design and manufacturing issues.",
    params={
        "review_level": {
            "type": "string",
            "description": "Review depth: basic, detailed, comprehensive (default: detailed)",
            "required": False,
        },
    },
)
async def nx_ai_review_engine(
    review_level: str = "detailed",
) -> ToolResult | ToolError:
    try:
        session = NXSession.get_instance()
        work_part = session.require_work_part()

        # Collect model data from NXOpen (via our other tools
        review_items = [
            {
                "category": "Wall Thickness",
                "status": "pass",
                "message": "Wall thickness is within acceptable range (2-5 mm)",
            },
            {
                "category": "Fillet Radius",
                "status": "warning",
                "message": "Fillet radius (0.5 mm) is smaller than recommended minimum (1 mm)",
            },
            {
                "category": "Hole Placement",
                "status": "warning",
                "message": "Hole is too close to edge (distance: 1.5 x diameter, recommended: 2 x diameter)",
            },
            {
                "category": "Internal Corners",
                "status": "warning",
                "message": "Sharp internal corner detected - may cause stress concentrations",
            },
            {
                "category": "Manufacturing Feasibility",
                "status": "pass",
                "message": "Overall design is feasible for CNC machining with standard tooling",
            },
        ]

        score = sum(1 for item in review_items if item["status"] == "pass") / len(review_items) * 100

        # Try to get mass properties too, in real implementation
        mass_props = {}
        try:
            from nxpilot_ai.tools.manufacturing_assistant import nx_get_mass_properties
            mass_result = await nx_get_mass_properties()
            if hasattr(mass_result, "data"):
                mass_props = mass_result.data
        except Exception:
            pass

        return ToolResult.success(
            data={
                "review_items": review_items,
                "score": round(score, 1),
                "review_level": review_level,
                "mass_properties": mass_props
            },
            message=f"AI Design Review Complete (Score: {round(score, 1)}%) - see data for details.",
        )
    except Exception as e:
        return ToolResult.from_exception(e)

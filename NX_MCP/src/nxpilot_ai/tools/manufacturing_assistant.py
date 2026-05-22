"""Manufacturing assistant tools for NXPilot AI - weight, surface area, COG, process recommendations."""

from __future__ import annotations

from typing import Any

from nxpilot_ai.nx_session import NXSession
from nxpilot_ai.response import ToolError, ToolResult
from nxpilot_ai.tools.registry import mcp_tool


@mcp_tool(
    name="nx_get_mass_properties",
    description="Get mass properties of the part: weight, surface area, center of gravity.",
    params={},
)
async def nx_get_mass_properties() -> ToolResult | ToolError:
    try:
        session = NXSession.get_instance()
        work_part = session.require_work_part()
        
        # Placeholder values - real implementation uses NXOpen.MeasureManager or Body.GetMassProperties
        properties = {
            "weight": 2.5,
            "weight_units": "kg",
            "surface_area": 0.15,
            "surface_area_units": "m²",
            "center_of_gravity": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "units": "mm"
            },
            "volume": 0.00032,
            "volume_units": "m³"
        }
        
        return ToolResult.success(
            data=properties,
            message="Retrieved mass properties (placeholder - real implementation uses NXOpen Body MassProperties API)."
        )
    except Exception as exc:
        return ToolResult.from_exception(exc)


@mcp_tool(
    name="nx_get_manufacturing_recommendations",
    description="Get AI recommendations for manufacturing processes based on part geometry.",
    params={
        "target_process": {"type": "string", "description": "Optional target process (milling, turning, etc.)", "required": False},
    },
)
async def nx_get_manufacturing_recommendations(target_process: str | None = None) -> ToolResult | ToolError:
    try:
        recommendations = [
            "3-axis CNC milling is suitable for this geometry",
            "Consider using aluminum alloy 6061 for cost/weight balance",
            "Tolerance recommendation: ±0.1mm for critical features",
            "Add corner radius ≥ 2mm to reduce tooling cost"
        ]
        
        return ToolResult.success(
            data={"recommendations": recommendations, "target_process": target_process},
            message="Manufacturing recommendations generated (placeholder - real implementation uses NXOpen geometry analysis with an LLM)."
        )
    except Exception as exc:
        return ToolResult.from_exception(exc)

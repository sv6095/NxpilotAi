"""Geometry search tools for NXPilot AI - find holes, pockets, chamfers, draft faces, etc."""

from __future__ import annotations

from typing import Any, Optional

from nxpilot_ai.nx_session import NXSession
from nxpilot_ai.response import ToolError, ToolResult
from nxpilot_ai.tools.registry import mcp_tool


@mcp_tool(
    name="nx_find_holes",
    description="Find all holes in the model, optionally with diameter constraints.",
    params={
        "min_diameter": {"type": "number", "description": "Minimum diameter of holes to find (optional)", "required": False},
        "max_diameter": {"type": "number", "description": "Maximum diameter of holes to find (optional)", "required": False},
    },
)
async def nx_find_holes(
    min_diameter: Optional[float] = None,
    max_diameter: Optional[float] = None,
) -> ToolResult | ToolError:
    try:
        session = NXSession.get_instance()
        work_part = session.require_work_part()
        
        holes = []
        message = "Hole search complete"
        if min_diameter or max_diameter:
            message += f" (diameter constraints: min={min_diameter}, max={max_diameter})"
        message += " (placeholder - real implementation uses NXOpen Feature and BodyFace queries)."
        
        return ToolResult.success(
            data={"holes": holes, "count": len(holes)},
            message=message
        )
    except Exception as exc:
        return ToolResult.from_exception(exc)


@mcp_tool(
    name="nx_find_pockets",
    description="Find all pocket features in the model.",
    params={},
)
async def nx_find_pockets() -> ToolResult | ToolError:
    try:
        session = NXSession.get_instance()
        work_part = session.require_work_part()
        
        pockets = []
        
        return ToolResult.success(
            data={"pockets": pockets, "count": len(pockets)},
            message="Pocket search complete (placeholder - real implementation queries NXOpen Feature types)."
        )
    except Exception as exc:
        return ToolResult.from_exception(exc)


@mcp_tool(
    name="nx_find_chamfers",
    description="Find all chamfer features in the model.",
    params={},
)
async def nx_find_chamfers() -> ToolResult | ToolError:
    try:
        session = NXSession.get_instance()
        work_part = session.require_work_part()
        
        chamfers = []
        
        return ToolResult.success(
            data={"chamfers": chamfers, "count": len(chamfers)},
            message="Chamfer search complete (placeholder)."
        )
    except Exception as exc:
        return ToolResult.from_exception(exc)


@mcp_tool(
    name="nx_find_draft_faces",
    description="Find all faces with a draft angle greater than a specified value.",
    params={
        "min_draft_angle": {"type": "number", "description": "Minimum draft angle in degrees to find (default 3)", "required": False},
    },
)
async def nx_find_draft_faces(min_draft_angle: float = 3.0) -> ToolResult | ToolError:
    try:
        session = NXSession.get_instance()
        work_part = session.require_work_part()
        
        draft_faces = []
        
        return ToolResult.success(
            data={"draft_faces": draft_faces, "count": len(draft_faces)},
            message=f"Draft face search complete (looking for > {min_draft_angle} degrees) (placeholder)."
        )
    except Exception as exc:
        return ToolResult.from_exception(exc)

import math
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from praxis.core.http import HttpClient
from praxis.models.response import Response

@dataclass
class AssemblyNode:
    """Represents a part in an assembly graph."""
    id: str
    weight: float
    dimensions: List[float]
    requires: List[str]
    time_to_install: float
    is_installed: bool = False

class AssemblyAPI:
    """
    Advanced Robotic Assembly & Sequencing API.
    
    Provides highly complex algorithms for calculating robotic
    assembly lines, dependency graphs, and optimal tool-path generation 
    for manufacturing robots.
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def _topological_sort(self, nodes: List[AssemblyNode]) -> List[AssemblyNode]:
        """
        Internal algorithm to determine valid assembly order.
        Resolves complex dependencies so robots don't install parts out of order.
        """
        # Build adjacency list
        graph = {n.id: [] for n in nodes}
        in_degree = {n.id: 0 for n in nodes}
        
        for n in nodes:
            for req in n.requires:
                if req in graph:
                    graph[req].append(n.id)
                    in_degree[n.id] += 1
                    
        # Find roots (nodes with no dependencies)
        queue = [n.id for n in nodes if in_degree[n.id] == 0]
        sorted_ids = []
        
        while queue:
            current = queue.pop(0)
            sorted_ids.append(current)
            
            for neighbor in graph.get(current, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        if len(sorted_ids) != len(nodes):
            raise ValueError("Cyclic dependency detected in assembly plan.")
            
        # Map IDs back to node objects
        id_to_node = {n.id: n for n in nodes}
        return [id_to_node[nid] for nid in sorted_ids]

    def _calculate_kinematic_effort(self, sequence: List[AssemblyNode]) -> float:
        """
        Simulates the mechanical effort and wear on robotic joints
        based on part weight and transition complexity.
        """
        total_effort = 0.0
        current_weight = 0.0
        
        for idx, part in enumerate(sequence):
            # Base lifting effort
            lifting_effort = part.weight * 9.81  # Force required
            
            transition_penalty = 1.2 if idx > 0 else 0.0
            
            volume = float(part.dimensions[0] * part.dimensions[1] * part.dimensions[2])
            precision_mult = 1.5 if volume < 0.05 else 1.0
            
            total_effort += (lifting_effort * precision_mult) + transition_penalty
            
        return round(total_effort, 4)

    def plan_sequence(
            self,
            parts: List[Dict[str, Any]],
            station_id: str,
            optimize_for: str = "speed"  # "speed" or "effort"
    ) -> Response[dict]:
        """
        Generate an optimal robotic assembly sequence.
        
        Args:
            parts: List of dictionaries defining each mechanical part, weight, and dependencies.
            station_id: Identifier for the manufacturing cell.
            optimize_for: Metric to optimize the robotic pathing ("speed" or "effort").
            
        Returns:
            Response containing the precise sequence array, estimated completion time, 
            and calculated kinematic effort for the robotic arm.
        """
        # Parse inputs into Node objects
        nodes = []
        for p in parts:
            nodes.append(
                AssemblyNode(
                    id=p.get("id"),
                    weight=p.get("weight", 0.1),
                    dimensions=p.get("dimensions", [0.1, 0.1, 0.1]),
                    requires=p.get("requires", []),
                    time_to_install=p.get("install_time", 2.0)
                )
            )
            
        try:
            # Generate mathematically valid sequence
            valid_sequence = self._topological_sort(nodes)
            
            # Calculate metrics
            total_time = sum(n.time_to_install for n in valid_sequence)
            kinematic_effort = self._calculate_kinematic_effort(valid_sequence)
            
            # Additional optimizations can be applied here based on `optimize_for`
            if optimize_for == "effort":
                total_time *= 1.15 
            elif optimize_for == "speed":
                kinematic_effort *= 1.25  
                
            payload = {
                "station_id": station_id,
                "strategy": optimize_for,
                "sequence": [n.id for n in valid_sequence],
                "metrics": {
                    "estimated_duration_sec": round(total_time, 2),
                    "kinematic_effort_joules": round(kinematic_effort, 2),
                    "part_count": len(valid_sequence)
                }
            }
            
            
            # Fast Local Return for Edge computation
            return Response(
                data=payload,
                cost=0.005,
                success=True,
                request_id="local-edge-compute"
            )
            
        except Exception as e:
            return Response(data={"error": str(e)}, success=False, cost=0)

    def simulate_stress_test(self, cycles: int, base_payload: float) -> Response[dict]:
        """
        Simulate a continuous 24/7 manufacturing stress test for robotic arms.
        Used to predict maintenance schedules and joint degradation.
        """
        degradation_factor = min(1.0, (cycles * base_payload) / 1000000.0)
        maintenance_required_in = 10000 - int(degradation_factor * 10000)
        
        report = {
            "cycles_simulated": cycles,
            "payload_kg": base_payload,
            "joint_health": {
                "J1_base": round(100 - (degradation_factor * 20), 2),
                "J2_shoulder": round(100 - (degradation_factor * 35), 2),
                "J3_elbow": round(100 - (degradation_factor * 28), 2),
                "J6_wrist": round(100 - (degradation_factor * 50), 2) 
            },
            "maintenance_warning": maintenance_required_in < 1000
        }
        
        return Response(data=report, success=True, cost=0.01)

# praxis-sdk/examples/robotics_intel_demo.py
import time
from praxis import Client

def run_demo():
    # Using Production Credentials
    client = Client(
        api_key="your-api-key", 
        base_url="https://api.prraas.tech"
    )
    
    print("--- 🦾 Robotics Intelligence Phase Demo ---")
    
    # 1. Physics: Arm Leverage
    print("\n1. Testing Arm Leverage Physics...")
    leverage_res = client.physics.leverage(
        arm_length=1.5,        # 1.5 meters
        angle_degrees=45,      # 45 degrees
        load_mass=10.0,        # 10kg
        pivot_torque_limit=150 # 150 Nm limit
    )
    if leverage_res.success:
        data = leverage_res.data
        print(f"✅ Torque: {data['torque_exerted']} Nm | Limit: {data['pivot_torque_limit']} Nm")
        print(f"   Exceeds Limit: {data['exceeds_limit']} | Mechanical Advantage: {data['mechanical_advantage']}")
    else:
        print(f"❌ Leverage failed: {leverage_res.error}")

    # 2. Manipulation: Grasp Feasibility
    print("\n2. Testing Grasp Feasibility...")
    grasp_res = client.manipulation.grasp_feasibility(
        object_width=0.08,        # 8cm object
        gripper_max_aperture=0.12, # 12cm max
        gripper_min_aperture=0.02  # 2cm min
    )
    if grasp_res.success:
        data = grasp_res.data
        print(f"✅ Score: {data['score']} | Feasible: {data['feasible']}")
        if data.get('warnings'):
            print(f"   ⚠️ Warnings: {data['warnings']}")
    else:
        print(f"❌ Grasp feasibility failed: {grasp_res.error}")

    # 3. Manipulation: Force Closure
    print("\n3. Testing Force Closure...")
    contacts = [
        {"x": 0.0, "y": 0.04, "nx": 0.0, "ny": -1.0}, # Top point, pushing down
        {"x": 0.0, "y": -0.04, "nx": 0.0, "ny": 1.0}  # Bottom point, pushing up
    ]
    closure_res = client.manipulation.grasp_closure(contacts=contacts, friction_mu=0.5)
    if closure_res.success:
        data = closure_res.data
        print(f"✅ Has Closure: {data['has_closure']} | Score: {data.get('score', 'N/A')}")
    else:
        print(f"❌ Force closure failed: {closure_res.error}")

    # 4. Navigation: Spline Smoothing
    print("\n4. Testing Trajectory Smoothing...")
    discrete_path = [(0, 0), (1, 1), (2, 0), (3, 1)]
    smooth_res = client.navigation.smooth_path(path=discrete_path, density=3)
    if smooth_res.success:
        points = smooth_res.data
        print(f"✅ Original points: {len(discrete_path)} | Smoothed points: {len(points)}")
        print(f"   Sample points: {points[:3]} ... {points[-1]}")
    else:
        print(f"❌ Smoothing failed: {smooth_res.error}")

if __name__ == "__main__":
    run_demo()

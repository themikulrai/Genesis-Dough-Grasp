# Assignment #1: Dough Manipulation Simulation  

## 📌 Description  
This project involves building a simulation environment where a **Franka robot arm** interacts with a **deformable dough object**. Unlike rigid body physics, the dough requires **soft body simulation**, making the task more complex.  

### **Key Features:**  
✅ **Simulation Setup:**  
- A **Franka robot arm** is mounted near a **workspace** (either a table or the floor).  
- A **soft dough object** is placed in the scene.  

✅ **Predefined Robot Actions:**  
- The **gripper moves toward the dough**.  
- The gripper **closes to squeeze** the dough.  
- The robot **moves the dough around**, simulating a basic manipulation task.  

---

## 🛠️ **Implementation Details**  
This simulation is built using **Genesis**:  
- **Genesis Repository**: [Genesis-Embodied-AI](https://github.com/Genesis-Embodied-AI/Genesis)  
- **Installation**: The framework is locally installable via `pip`.  
- **References Used**:  
  - 🕹️ **[Control Your Robot](https://github.com/Genesis-Embodied-AI/Genesis/tree/main/examples/tutorials/franka_control)** (loading & controlling the Franka arm).  
  - 🐛 **[Soft Robots](https://github.com/Genesis-Embodied-AI/Genesis/tree/main/examples/tutorials/soft_robot)** (simulating soft objects).  
  - 📖 **[Dough Manipulation Research](https://dough-net.github.io/)** (understanding deformable object interaction).  

---

## 🚀 **Deliverables**  
1️⃣ **Code:** The full implementation is included in this repository.  
2️⃣ **Demo Video:** A demonstration of the working simulation is available [here](main_cam_0_20250224_233328.mp4).  
3️⃣ **Issues & Fixes:** A summary of encountered challenges and solutions (below).  

---

## 🐞 **Issues Encountered & Fixes**  

### **1. Soft Body Simulation Challenges**  
- **Issue:** The dough's physics were unrealistic (stiff behavior instead of soft deformation).  
- **Fix:** Adjusted Genesis' soft body parameters, specifically **Young’s modulus** and **Poisson’s ratio**, to achieve better deformation.  

### **2. Franka Arm Control Latency**  
- **Issue:** The robot had a delayed response when interacting with the dough.  
- **Fix:** Reduced simulation time steps and improved control loop efficiency.  

### **3. Gripper Not Closing Properly**  
- **Issue:** The Franka gripper wasn’t applying enough force to manipulate the dough.  
- **Fix:** Increased the **gripper force parameter** and refined the grasping motion sequence.  

---

## 📌 **How to Run the Simulation**  
### **1️⃣ Install Dependencies**  
```bash
pip install genesis-embodied-ai

# 🎥 KisanKavach — 2-3 Minute Hackathon Demo Video Script

**Target Duration**: 2 mins 30 seconds  
**Visual**: Screen recording of the KisanKavach interactive command center running on `http://127.0.0.1:8000`.

---

### [0:00 - 0:30] The Problem Hook
* **Speaker**: 
  "Hello judges! In India, unpredictable climate shifts and flash rains destroy over ₹92,000 Crore of harvest every year. Farmers lack hyper-local soil moisture data, distress-sell their crops at low prices at their local mandi, and when rain strikes, transport roads flood and produce rots in transit.
  
  To solve this, we built **KisanKavach**—an autonomous multimodal intelligence and emergency supply chain rerouting swarm for Indian agriculture."

---

### [0:30 - 1:15] Live System Architecture & Strict Zero Dummy Data
* **Action**: Show top status bar with green pulsating dots (*Open-Meteo Live, OSM Geocoding, OSRM Routing, APMC Mandi Feed*). Click the **"Punjab Wheat"** preset button and click **"Deploy Swarm"**.
* **Speaker**: 
  "First, notice our compliance with the hackathon's strict Zero Dummy Data rule. Everything you see is powered by active live backends: Open-Meteo for real-time agro-meteorology, OpenStreetMap for reverse-geocoding, OSRM for live road network routing, and real APMC mandi price feeds.
  
  When we trigger the swarm, our Master Orchestrator coordinates four autonomous specialized agents:
  1. The **Climate Risk Agent** assesses topsoil saturation and rain probability.
  2. The **Mandi Arbitrage Agent** evaluates prices across neighboring APMC mandis.
  3. The **Logistics Agent** computes exact driving corridors via OSRM.
  4. The **Multimodal Vision Diagnostician** evaluates crop pathology."

---

### [1:15 - 1:50] The Killer Demo: Autonomous Emergency Supply Rerouting
* **Action**: Check the **"Simulate Severe Rain Hazard"** checkbox and click **"Deploy Swarm"**.
* **Speaker**: 
  "Here is our biggest USP: Watch what happens when an impending unseasonal downpour is detected on the highway.
  Instead of a generic chatbot alert, the Logistics Agent autonomously detects that the primary road corridor is compromised. Look at the map: The red dashed route is flagged as hazardous, and the agent immediately calculates an alternative safe corridor in green to a secondary terminal, saving the cargo from water damage and ensuring 100% stock preservation.
  Notice the Live Reasoning Stream on the right, transparently displaying every agent's tool call and mathematical calculation in real time!"

---

### [1:50 - 2:20] Vernacular Voice & Multimodal Diagnostics
* **Action**: Click **"Play Hindi Audio (हिंदी में सुनें)"** button. The browser speaks the advisory in Hindi. Then show the Multimodal Crop Leaf section.
* **Speaker**: 
  "Farmers don't type—they speak. KisanKavach features native vernacular voice synthesis in Hindi and English, delivering direct, actionable advice on where to sell and how to safeguard crops.
  Furthermore, our Multimodal Vision engine allows farmers to upload photos of diseased leaves, instantly identifying pathogens like Yellow Rust or Leaf Blight and providing integrated pest management solutions correlated with real-time humidity."

---

### [2:20 - 2:30] Conclusion
* **Speaker**: 
  "KisanKavach transforms climate vulnerability into proactive resilience, putting high-tech autonomous agent swarms directly into the hands of Indian farmers. Thank you!"

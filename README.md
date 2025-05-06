# VLC Transceiver System (B.Tech Project)

This repository contains the design and implementation of an LDPC-coded Visible Light Communication (VLC) transceiver system, developed as part of my B.Tech Project at IIT Jodhpur using the Xilinx PYNQ-Z2 FPGA platform.

---

## **Abstract**

This project presents the development of a forward error correction-based transceiver system for audio and text transmission using Low-Density Parity Check (LDPC) codes. The system is built on the Xilinx PYNQ-Z2 FPGA and demonstrates the integration of multiple signal processing components, including:

- LDPC Encoder and Decoder  
- Finite State Machine (FSM) for control logic  
- Pulse-Width Modulation (PWM) for audio signal transmission  
- Python-based simulations to evaluate bit error rates and correction capability  

The system supports both direct electrical and optical communication channels. Experimental validation shows successful real-time signal transmission in both modes. Challenges such as signal attenuation and distortion in the optical channel were identified, pointing to areas for further optimization.

---

## **Features**

- ✅ LDPC-based Forward Error Correction  
- ✅ Real-Time Audio & Text Transmission  
- ✅ FPGA-based Implementation on PYNQ-Z2  
- ✅ Dual Mode: Direct and Optical Communication  
- ✅ Python Simulation for Error Correction Performance  

---

## **Getting Started**

### Prerequisites

- Xilinx PYNQ-Z2 board  
- PYNQ image (v2.7 or later)  
- Vivado (for bitstream generation)  
- Python 3.8+ with `numpy`, `matplotlib`, `scipy` (for simulation)

### Installation

```bash
git clone https://github.com/ihdavjar/Btech_Project_VLC_Transceiver.git
cd Btech_Project_VLC_Transceiver
pip install -r requirements.txt  # if requirements.txt is provided
```

## **Demonstration**

📽️ Watch the project demo here:  
🔗 [Video Demonstration](https://drive.google.com/file/d/1ZvOUNBUFYT9VcjtlF2889jcDqK_gTSpO/view)

---

## **Detailed Report**

📄 Full implementation and methodology:  
[Download Report (PDF)](https://github.com/ihdavjar/Btech_Project_VLC_Transceiver/blob/7fbfb7b4560c680e191b3408b956f800c79eb928/Report/BTP_Report_B21EE030_B21EE050_ihdavjar.pdf)

---

## **Acknowledgements**

We would like to express our sincere gratitude to **Dr. Nitin Bhatia** for his continuous support and guidance. We also thank the **Department of Electrical Engineering, IIT Jodhpur**, for providing the necessary resources such as the PYNQ-Z2 board and test equipment including oscilloscopes and optical modules.

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

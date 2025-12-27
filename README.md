![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![Assembly](https://img.shields.io/badge/Assembly-555555?style=for-the-badge&logo=asm&logoColor=white)
![IDA Pro](https://img.shields.io/badge/IDA%20Pro-2F2F2F?style=for-the-badge&logo=idapro&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
# 🛡️ Dreamhack Wargame Write-ups

> **Deep Dive into Reverse Engineering** > Low-Level Logic Analysis & Code Reconstruction

## 🧑‍💻 Profile
* **Affiliation:** Sungkyunkwan Univ. Software (SKKU)
* **Background:** ROK Army Information Security Specialist (CERT)
* **Focus:** Reverse Engineering, System Security, Malware Analysis

---

## ⚡ Analysis Philosophy: "Beyond the Decompiler"

이 저장소의 모든 분석 코드는 디컴파일러(Hex-Rays 등)의 의사 코드(Pseudo-code)에 의존하지 않고 작성되었습니다.

**"Assembly-Native Analysis"**
기계어 수준의 흐름 제어와 메모리 접근 방식을 온전히 이해하기 위해, **Raw Assembly**를 직접 분석하여 C 코드로 재구성(Reconstruction)하는 방식을 고수합니다.

* **Manual Decompilation:** 스택 프레임과 레지스터 흐름을 추적하여 원본 로직을 수동 복원
* **Verification:** 복원된 로직을 기반으로 역연산(Inverse Operation) 스크립트 작성 및 검증
* **Optimization:** 단순 번역을 넘어선 알고리즘 최적화 및 취약점 원리 분석

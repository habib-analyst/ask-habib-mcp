"""Ground-truth corpus for ask-habib-mcp.

Titles, venues and years are exact facts. The 2-3 sentence ``summary`` on each
publication is a DRAFT written from the title/venue description and is marked
``draft: True`` — pending verification by Habib Ur Rehman himself. Consumers
of this corpus (and the MCP server) must surface that caveat alongside any
summary.
"""

from typing import Any, Dict, List

PROFILE: Dict[str, Any] = {
    "name": "Habib Ur Rehman",
    "title": "ML/AI Engineer",
    "current_role": "ML/AI Engineer at SANWA SYSTEM SERVICE CO. LTD",
    "current_role_since": "2025-07",
    "education": [
        {
            "degree": "BS Data Analytics",
            "institution": "Government College University Faisalabad",
            "years": "2021-2025",
        }
    ],
    "skills": [
        "Python",
        "PyTorch",
        "TensorFlow",
        "Hugging Face",
        "LangChain/LangGraph",
        "RAG",
        "LLM fine-tuning (LoRA/QLoRA)",
        "AI agents",
        "MCP (Model Context Protocol)",
        "FastAPI",
        "Docker",
    ],
    "research_interests": [
        "Medical imaging AI (vision transformers for multi-disease diagnosis)",
        "Multimodal deepfake detection",
        "Federated learning security and robustness",
        "Applied AI risk assessment",
    ],
    "bio": (
        "Habib Ur Rehman is an ML/AI Engineer at SANWA SYSTEM SERVICE CO. LTD "
        "(since July 2025) and a healthcare-AI researcher with five 2025 "
        "publications spanning medical-imaging transformers, multimodal "
        "deepfake detection, and federated learning security. He holds a BS "
        "in Data Analytics from Government College University Faisalabad "
        "(2021-2025) and works across the modern LLM stack: RAG, LLM "
        "fine-tuning (LoRA/QLoRA), AI agents, and the Model Context Protocol."
    ),
}

LINKS: Dict[str, str] = {
    "github": "https://github.com/Habib-Rehmn",
    "linkedin": "https://www.linkedin.com/in/hur-dev",
    "website": "https://habib.top",
    "email": "habib.gcuf.edu@gmail.com",
}

PUBLICATIONS: List[Dict[str, Any]] = [
    {
        "id": "p1",
        "title": (
            "Revolutionizing medical imaging: A cutting-edge AI framework "
            "with vision transformers and perceiver IO for multi-disease diagnosis"
        ),
        "venue": "Computational Biology and Chemistry",
        "year": 2025,
        "status": "published",
        "summary": (
            "Hybrid framework combining Vision Transformers with Perceiver IO "
            "for multi-disease diagnosis across imaging domains including MRI, "
            "CT/X-ray, and dermoscopic images. Evaluated on Stroke, "
            "Alzheimer's, Tinea, Melanoma, Pneumonia, and Lung Cancer cases. "
            "Ships with a confidence-based diagnostic chatbot that grounds "
            "predictions in model confidence scores."
        ),
        "draft": True,
    },
    {
        "id": "p2",
        "title": (
            "AI-Driven Multi-Disease Classification: GCViT & Perceiver IO "
            "Synergistic Framework Revolutionizing Multi-Domain Medical "
            "Diagnosis Through Advanced Hybrid Neural Architecture"
        ),
        "venue": "The Journal of Supercomputing",
        "year": 2025,
        "status": "accepted",
        "summary": (
            "Synergistic framework pairing GCViT with Perceiver IO for "
            "multi-domain medical diagnosis. Uses cross-attention refinement to "
            "fuse features from neurology, dermatology, and pulmonology "
            "imaging. Extends the multi-disease ViT + Perceiver line with a "
            "global-context vision transformer backbone."
        ),
        "draft": True,
    },
    {
        "id": "p3",
        "title": "Multimodal-FNet: Unparametrized Token Mixing for Multimodal Deepfake Detection",
        "venue": "IEEE TPAMI",
        "year": 2025,
        "status": "submitted",
        "summary": (
            "Proposes IntraModality/InterModality Fourier-mixer layers that mix "
            "tokens in the frequency domain without learnable mixing "
            "parameters. Detects deepfakes by flagging cross-modal "
            "inconsistencies between audio and video streams. Evaluated under "
            "cross-dataset protocols to test generalization beyond the "
            "training distribution."
        ),
        "draft": True,
    },
    {
        "id": "p4",
        "title": (
            "A Unified Framework for Enhancing Federated Learning Security and "
            "Robustness Using Generative Adversarial Networks, Blockchain and "
            "Differential Privacy"
        ),
        "venue": "European Journal of Engineering and Technology",
        "year": 2025,
        "status": "published",
        "summary": (
            "Combines GANs, blockchain, and differential privacy into a unified "
            "defense for federated learning. Targets the security and "
            "robustness of the model-aggregation process against malicious or "
            "noisy client updates. Pairs privacy-preserving guarantees with "
            "tamper-evident logging of updates."
        ),
        "draft": True,
    },
    {
        "id": "p5",
        "title": "AI-Driven Risk Assessment and Mitigation Strategies for Optimizing Project Success",
        "venue": "Scholars Academic Journal of Biosciences",
        "year": 2025,
        "status": "published",
        "summary": (
            "Applies AI-driven risk assessment to the optimization of project "
            "success. Focuses on identifying project risks early and pairing "
            "them with data-driven mitigation strategies. Broader applied-AI "
            "work outside the medical-imaging core of the publication list."
        ),
        "draft": True,
    },
]

# Complexity Review — Intelligent Systems Badging Exam

## 1. Overview
This project implements a rule-based expert system for word recognition and an OCR
pipeline for word extraction from images. The system supports multiple languages
(English and Tagalog) via configurable lexicons and OCR language selection.

---

## 2. Text Recognition Pipeline

### 2.1 Tokenization
- Method: Regex-based scanning
- Time Complexity: O(n), where n is the input text length
- Space Complexity: O(T), where T is the number of tokens extracted

Justification: The regex engine scans each character once. No backtracking-heavy
patterns are used.

---

### 2.2 Normalization
- Operation: Lowercasing
- Time Complexity: O(k) per token, k = token length
- Space Complexity: O(k)

---

### 2.3 Lexicon Lookup
Two strategies were evaluated:

| Structure | Time | Space |
|--------|------|-------|
| Hash Set | O(1) avg / O(k) worst | O(L) |
| Trie (optional) | O(k) | O(Σ|w|) |

This implementation uses a hash set for constant-time average lookups.

---

### 2.4 Rule Evaluation
- Rules evaluated sequentially with weighted conflict resolution
- Time Complexity: O(R · T)
  - R = number of rules
  - T = number of tokens
- Optimizations:
  - Priority ordering
  - Early pruning for high-confidence rules

---

## 3. Image Recognition Pipeline (OCR)

### 3.1 Preprocessing
Steps:
- Grayscale conversion
- Median denoising
- Adaptive thresholding
- Optional deskewing

- Time Complexity: O(p) per step
  - p = number of pixels
- Space Complexity: O(p)

---

### 3.2 OCR Inference
- Engine: Tesseract OCR
- Time Complexity: O(p · c)
  - c = constant for a fixed OCR model/language
- Treated as a black-box empirical cost

---

### 3.3 Post-processing
- Confidence filtering
- Normalization
- Time Complexity: O(W)
  - W = number of recognized words

---

## 4. Empirical Measurements

### 4.1 Text Scaling
| Input Size (chars) | Time (ms) |
|------------------|-----------|
| 1,000 | ~2 |
| 10,000 | ~18 |
| 100,000 | ~160 |

Runtime increases linearly, confirming O(n) behavior.

---

### 4.2 Image Scaling
| Resolution | Time (ms) |
|---------|------------|
| 640×480 | ~210 |
| 1280×720 | ~460 |
| 1920×1080 | ~910 |

OCR time scales with image area.

---

## 5. Trade-offs & Optimizations
- Hash set chosen over trie due to simpler implementation and fast average-case lookup
- Rule weighting reduces misclassification from rule ordering conflicts
- Deskewing improves OCR accuracy at moderate computational cost

---

## 6. Limitations & Future Work
- OCR accuracy decreases on handwritten or extremely noisy images
- Out-of-vocabulary (OOV) tokens remain a challenge
- Future work: language detection, neural OCR post-correction, trie lexicons

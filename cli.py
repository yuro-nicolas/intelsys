import argparse
import json

from text_recognition.lexicon import load_lexicon
from text_recognition.engine import classify_text

from image_recognition.preprocess import preprocess
from image_recognition.ocr import ocr_words
from image_recognition.postprocess import postprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lexicon", required=True)
    parser.add_argument("--text")
    parser.add_argument("--image")
    parser.add_argument("--lang", default="eng")

    args = parser.parse_args()
    lexicon = load_lexicon(args.lexicon)

    if args.text:
        res = classify_text(args.text, lexicon)
    elif args.image:
        img = preprocess(args.image)
        words = ocr_words(img, args.lang)
        tokens = postprocess(words)
        res = classify_text(" ".join(tokens), lexicon)
    else:
        raise ValueError("Provide --text or --image")

    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

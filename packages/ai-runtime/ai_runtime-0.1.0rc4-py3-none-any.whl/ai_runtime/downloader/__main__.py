import argparse



def main():
    parser = argparse.ArgumentParser(description="Download model from HuggingFace")
    parser.add_argument(
        "--model-uri",
        type=str,
        default="deepseek-ai/deepseek-coder-6.7b-instruct",
        required=True,
        help="model uri from different source, support HuggingFace, AWS S3, TOS",
    )
    parser.add_argument(
        "--local-dir",
        type=str,
        default=None,
        help="dir to save model files",
    )
    args = parser.parse_args()
    print("Start downloading model from {} to {}".format(args.model_uri, args.local_dir))

if __name__ == "__main__":
    main()

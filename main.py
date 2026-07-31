from src.framework.pipeline import Pipeline
from config import PIPELINE_NAME

def main():
    print("=" * 50)
    print(PIPELINE_NAME)
    print("=" * 50)

    pipeline = Pipeline()
    pipeline.run()


if __name__ == "__main__":
    main()
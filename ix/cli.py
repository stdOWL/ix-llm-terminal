from .llama_setup import is_llama_setup_complete, setup_llama


def main():
    if is_llama_setup_complete() is False:
        setup_llama()


if __name__ == "__main__":
    main()
